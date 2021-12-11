# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: pdf.py
@version: 1.0
@time: 2021/04/18 01:38:04
@contact: jinxy@pku.edu.cn

实现PDF转文字
获取任务队列
"""
import re
import os.path as op

import PyPDF2
import pdfplumber
import timeout_decorator
from timeout_decorator.timeout_decorator import TimeoutError
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.psparser import PSEOF

from process import File, PolicyText, BASE_DIR, db, logging
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.exc import InvalidRequestError
from disruptive import app

app.app_context().push()

logging.root.setLevel(logging.WARNING)
pdf_cvt_lg = logging.getLogger("pdf_converter")
pdf_cvt_lg.setLevel(logging.INFO)

puncs = ".,?!;"
TIME_OUT = 60


class PdfTooLongError(Exception):
    def __init__(self, page_num):
        self.page_num = page_num

    def get_page_num(self):
        return self.page_num


class PdfNotReadableError(Exception):
    ...


@timeout_decorator.timeout(TIME_OUT)
def convert_page(page):
    pageContent = page.extract_text()
    if not pageContent: return
    # replace
    pageContent = re.sub("\(cid:\d+\)", "", pageContent)
    lines = pageContent.strip().split("\n")
    if len(lines) > 1:  # go through lines
        paragraphs = lines[0].strip()
        for line in lines[1:]:
            line = line.strip()
            if not line or not paragraphs:
                continue
            if paragraphs[-1] not in puncs and line[0].islower():
                paragraphs += ' ' + line
            else:
                paragraphs += "\n" + line
    else:
        paragraphs = lines[0]
    paragraphs = re.sub("\n\d+$", "", paragraphs)
    paragraphs = re.sub("\n\d+\n", "", paragraphs)
    return paragraphs


def pdf2txt(file_path, save_path, max_page=50):
    """
    Args:
        file_path (str):
        save_path (str):
        max_page (int):
    """
    pdf = pdfplumber.open(file_path)
    content = []
    pdf_pages = pdf.pages
    if len(pdf_pages) > max_page:
        raise PdfTooLongError(len(pdf_pages))

    for page in pdf_pages:
        try:
            paragraphs = convert_page(page)
        except TimeoutError as e:
            pdf_cvt_lg.error(f"Time Out {TIME_OUT}, this page is skipped")
        else:
            if paragraphs:
                content.append(paragraphs)
    pdf.close()

    with open(save_path, "w", encoding="utf-8") as ft:
        ft.write("\n\n".join(content))
        pdf_cvt_lg.info(f'saved to path: {save_path}')


def pdf2text_pypdf(file_path, save_path, max_page=50):
    pdfFile = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)

    text_list = []
    if pdfReader.numPages > max_page:
        raise PdfTooLongError(max_page)
    for p_id in range(pdfReader.numPages):
        page = pdfReader.getPage(p_id)
        page_content = page.extractText()
        paragraph = trim_paragraph(page_content)
        text_list.append(paragraph)

    with open(save_path, 'w') as f:
        f.writelines(text_list)
    pdfFile.close()


class TrimError(Exception):
    def __init__(self, para, line):
        self.para = para
        self.line = line


def trim_paragraph(page_content):
    lines = page_content.split("\n")
    paragraph = str()
    if len(lines) > 1:
        paragraph = lines[0]
        for line in lines[1:]:
            line = line.strip("\n")
            if not line or not paragraph:
                continue
            try:
                # 段末不是标点符号 && 段首是小写
                if (paragraph[-1] not in ".,?!;" or paragraph[-1] == " ") and (line[0].islower() or line[0] == " "):
                    paragraph += line
                else:
                    paragraph += "\n" + line
            except IndexError as e:
                # pdf_cvt_lg.error(f'paragraph {paragraph} | line {line}')
                raise TrimError(paragraph, line)
    return paragraph


def run_converter():
    """
    运行PDF转换任务
    Returns: 成功转换的PDF数量
    """
    converted_cnt = 0
    # query origin file: saved && pdf && format not saved
    file_list = File.query.join(PolicyText,
                                PolicyText.original_file == File.id).filter(File.filetype == 1,
                                                                            File.savename != None,
                                                                            File.extension == 'pdf',
                                                                            # PolicyText.site != 'www.govinfo.gov',
                                                                            PolicyText.spider_condition == 299,
                                                                            PolicyText.format_file == None).all()
    pdf_cvt_lg.info(f"PDF need conversion: {len(file_list)}")
    # 遍历所有的PDF文件对象(origin, not null, pdf)
    for file in file_list:
        # 如果PDF已经下载
        # 预先获取正确的format路径
        format_name = file.savename.replace('origin_', 'format_')
        format_name = re.sub(r'\.(pdf|html)$', '.txt', format_name)
        format_path = op.join(BASE_DIR, 'app/data/format/', format_name)
        # 获取origin文件的路径
        origin_path = op.join(BASE_DIR, 'app/data/origin/', file.savename)

        # 如果format文件不存在就进行转换, 至此快速过滤了需要进行转换的文件, 下面使用 fd_state 缓存
        if op.exists(format_path): continue
        fd_state = file.extra_info['fd_state']
        if 'eof' in fd_state or 'syntax' in fd_state:  # 之前出过问题
            pdf_cvt_lg.warning(f'Problem Before: {fd_state} | {policy}')
            continue

        policy = PolicyText.query.filter_by(original_file=file.id).one()  # 找到相关 policy
        pdf_cvt_lg.info(f"handling new file: {origin_path} | {policy}")
        format_file = File(filetype=2, name=file.name, savename=format_name, extension='txt')  # 指定一些文件的相关参数

        # 尝试转PDF，需要错误处理
        try:
            pdf2txt(origin_path, format_path, max_page=400)
            file.extra_info['fd_state'].append('done')
        except PdfTooLongError as e:  # state 1
            if 'long' not in fd_state:
                file.extra_info['fd_state'].append('long')
            pdf_cvt_lg.warning(f"PDF too long, page: {e.page_num} | origin file id {file.id}")
        # except PdfNotReadableError as e:  # state 2
        #     file.extra_info['fd_state'].append('unreadable')
        #     pdf_cvt_lg.error(f"PDF not readable | origin file id {file.id}")
        # except PDFSyntaxError as e:  # state 4
        #     file.extra_info['fd_state'].append('syntax')
        #     pdf_cvt_lg.warning(f"PDF SyntaxError: origin_path: {origin_path} | origin file id {file.id}")
        except TrimError as e:
            pdf_cvt_lg.error(f'paragraph {e.para} | line {e.line}')
        except PSEOF as e:
            file.extra_info['fd_state'].append('eof')
            pdf_cvt_lg.error(e)
        except PDFSyntaxError as e:
            file.extra_info['fd_state'].append('syntax')
            pdf_cvt_lg.error(e)
        except Exception as e:  # 未知
            file.extra_info['fd_state'].append('unexpected')
            pdf_cvt_lg.error(f"unexpected {type(e).__name__}: {e} | origin file id {file.id}")
        else:  # 转换成功
            # 转成功之后添加数据库
            db.session.add(format_file)
            db.session.commit()

            # policy 也要更新一下对应的 id
            policy.format_file = format_file.id
            db.session.add(policy)
            db.session.commit()
            # 记一下成功转换的数量
            converted_cnt += 1
            pdf_cvt_lg.info(f"PDF Converted: {format_name} | policy_id: {policy.id} | already finished {converted_cnt}")
        finally:
            try:
                flag_modified(file, 'extra_info')
            except InvalidRequestError as e:
                pdf_cvt_lg.error(f"flag error")
            else:
                db.session.add(file)
                db.session.commit()
    return converted_cnt


if __name__ == '__main__':
    cnt = run_converter()
    print(f"[CNT] {cnt}")
    # pdf2txt('/Users/leverest/Downloads/demo.pdf', '/Users/leverest/Downloads/demo_parsed.pdf', max_page=100)
