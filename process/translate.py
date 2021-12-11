# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: translate.py
@version: 1.0
@time: 2021/04/18 01:39:26
@contact: jinxy@pku.edu.cn

翻译文章
txt -> txt_trans

谷歌翻译那块
应该写一个不受长度限制的 Google Translate (是用chunking等方法)
"""
import logging
import os.path as op
import time
import random
import requests
import json
import pandas as pd
from tqdm import tqdm

from process import File, PolicyText, db, get_md5_str, os
from util import pure_text, MyThread, FileName
from disruptive import app
from config import Config

# use app
app.app_context().push()
trans_lg = logging.getLogger("translate")
trans_lg.setLevel(logging.INFO)

TIME_DECAY = 1  # 每一次成功请求后都延迟 TIME_DECAY 秒
TIME_RETRY = 1  # 每一次重试都等待 TIME_RETRY 秒


def read_split(file_path, para_len=3000):
    """
    读取一个文件，如果太长就拆分为段落列表
    Args:
        para_len (int): max len para
        file_path (str): path
    Returns:
        list of para
    """
    para_list = open(file_path, "r", encoding="utf-8", errors="ignore").readlines()
    to_translate = list()
    translate_para = ""
    for i in range(len(para_list)):
        if len(translate_para) + len(para_list[i]) < para_len:
            if i < len(para_list) - 1:
                translate_para += para_list[i]
                continue
            elif i == len(para_list) - 1:
                translate_para += para_list[i]
                to_translate.append(translate_para)
                break
        else:
            if i < len(para_list) - 1:
                to_translate.append(translate_para)
                translate_para = para_list[i]
                continue
            elif i == len(para_list) - 1:
                to_translate.append(translate_para)
                to_translate.append(para_list[i])
                break
    return to_translate


class FileTask:
    """A Translation Task For a Paragraph"""

    def __init__(self, tid, text):
        self.id = tid
        self.text = text
        self.done = False
        self.trans_text = None
        self.tries = 0  # 失败的词数


class TransFileManager:
    """
    read, split, trans(robust), save
    Task:
        1. Read & Split
        2. Reorganize as tasks
        3. Make into batch
        4. Transfer by multi thread
        5. Check Result & Make next batch
        6. Combine results
    """

    def __init__(self, file_path, save_path, batch_size, para_len=6000):
        self.file_path = file_path
        self.save_path = save_path
        self.batch_size = batch_size
        self.para_len = para_len
        task_text_list = read_split(file_path, self.para_len)
        trans_lg.info(f"Split into {len(task_text_list)}")
        self.task_list = [FileTask(idx, text) for idx, text in enumerate(task_text_list)]

    def gen_remain_tasks(self):
        """generate remained tasks"""
        return list(filter(lambda x: not x.done, self.task_list))

    def gen_batch_tasks(self):
        """generate tasks of batch_size"""
        remain_task = self.gen_remain_tasks()
        return remain_task[:self.batch_size]

    def finish_trans(self):
        """
        finish translation:
            1. combine tasks
            2. write file
        """
        # check done
        assert len(self.gen_remain_tasks()) == 0
        trans_text_list = [i.trans_text for i in self.task_list]
        with open(self.save_path, 'w') as f:
            f.write('\n'.join(trans_text_list))


def translate_file_baidu(file_path, save_path, to_lang='zh'):
    """
    Args:
        file_path (str):
        save_path (str):
        to_lang (str):
    Returns:
        None
    """
    bd_translator = BaiduTranslator(to_lang)
    file_mng = TransFileManager(file_path, save_path, bd_translator.batch_size)
    while file_mng.gen_remain_tasks():
        trans_state_list = bd_translator.multi_thread(file_mng.gen_batch_tasks())
        trans_lg.debug(trans_state_list)
        time.sleep(TIME_DECAY)
    file_mng.finish_trans()


class BaiduTransError(Exception):
    def __init__(self, info):
        self.info = info


class BaiduTranslator:
    f_lang = 'auto'
    t_lang: str
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    def __init__(self, to_lang='zh'):
        conf_f = open('./trans_conf.json')
        self.t_lang = to_lang
        self.config = json.load(conf_f)
        self.batch_size = len(self.config)
        self.c_round = 0
        conf_f.close()

    def get_id_key(self, conf_id=-1):
        c_conf = self.config[self.c_round] if conf_id == -1 else self.config[conf_id]
        trans_lg.debug(f"using {c_conf['name']}")
        self.c_round = (self.c_round + 1) % self.batch_size
        return c_conf

    def translate(self, text, max_try=10):
        """
        text with \n to trans_res_list
        Args:
            text: text split by \n
            max_try: 最多尝试次数
        Returns:
            rest list
        """
        salt = random.randint(32768, 65536)
        conf = self.get_id_key()
        sign = get_md5_str(conf['appid'] + text + str(salt) + conf['appkey'])
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'appid': conf['appid'], 'q': text, 'from': self.f_lang, 'to': self.t_lang, 'salt': salt,
                  'sign': sign}
        # Send request
        r = requests.post(self.url, params=params, headers=headers)
        result = r.json()
        if 'error_code' in result and result['error_code'] in ["52001", "54003"]:
            if max_try > 1:
                trans_lg.debug(f'Retry, {max_try - 1} left')
                time.sleep(TIME_RETRY)
                return self.translate(text, max_try - 1)
            else:
                raise BaiduTransError(
                    f"{json.dumps(result, ensure_ascii=False)} | Conf: {conf['name']} | MaxTry: {max_try}")
        if 'trans_result' not in result:
            raise BaiduTransError(f"{json.dumps(result, ensure_ascii=False)} | Conf: {conf['name']}")
        dst_list = [tr['dst'] for tr in result['trans_result']]
        return dst_list

    def translate_task(self, task: FileTask, conf_id: int) -> int:
        """
        translate file task and save
        Args:
            task (FileTask): file task
            conf_id (int): api config id
        Returns:
            state code (0 for success)
        """
        text = task.text
        trans_lg.debug(f"using conf: {conf_id}, time: {time.time()}")
        salt = random.randint(32768, 65536)
        conf = self.get_id_key(conf_id)
        sign = get_md5_str(conf['appid'] + text + str(salt) + conf['appkey'])
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'appid': conf['appid'], 'q': text, 'from': self.f_lang, 'to': self.t_lang, 'salt': salt, 'sign': sign}
        # Send request
        r = requests.post(self.url, params=params, headers=headers)
        result = r.json()
        if 'trans_result' not in result:
            trans_lg.warning(f"{json.dumps(result, ensure_ascii=False)} | Conf: {conf['name']}")
            task.tries += 1
            return int(result['error_code'])
        else:
            task.trans_text = '\n'.join([tr['dst'] for tr in result['trans_result']])
            # trans_lg.debug(f'Result: {task.trans_text}')
            task.done = True
            return 0

    def multi_thread(self, batch_tasks):
        batch_len = len(batch_tasks)
        assert batch_len <= self.batch_size
        threads = [MyThread(func=self.translate_task, args=(batch_tasks[i], i)) for i in range(batch_len)]
        for t in threads: t.start()  # 启动一个线程
        for t in threads: t.join()  # 等待每个线程执行结束
        return [t.get_result() for t in threads]


def run_translator():
    """
    运行翻译转换任务
    Returns: 成功翻译的数量
    """
    converted_cnt = 0
    # 遍历所有的format文件对象
    policy_list = PolicyText.query.join(File, File.id == PolicyText.format_file).filter(PolicyText.use,
                                                                                        # limit threshold
                                                                                        File.savename != None,
                                                                                        # format file exist
                                                                                        PolicyText.translated_file == None
                                                                                        # no translated file
                                                                                        ).all()
    trans_lg.info(f"task len: {len(policy_list)}")
    # go through all valid policy
    for p in policy_list:  # type: PolicyText
        format_f = File.query.get(p.format_file)  # type: File
        format_f_name = FileName()
        format_f_name.set_by_name(format_f.savename)
        format_path = format_f_name.gen_path(2)
        trans_name = format_f_name.gen_name(3)
        trans_path = format_f_name.gen_path(3)
        assert op.exists(format_path)
        print(trans_path)
        if trans_path in ['/root/repos/disruptive/app/data/trans/trans_1870fb52398f185536b63279d62c96a1.txt']:
            # skip bad file
            print(f"skip | {trans_path}")
            continue
        assert not op.exists(trans_path)

        trans_file = File(filetype=3, name=format_f.name, savename=trans_name, extension='txt')
        try:
            translate_file_baidu(format_path, trans_path)
        except Exception as e:
            trans_lg.error(f'translate file error | policy_id: {p.id} | {str(e)}')
        else:
            converted_cnt += 1
            trans_lg.info(f"Done and saved to {trans_path} | finished {converted_cnt}")

            # 转成功之后添加数据库
            db.session.add(trans_file)
            db.session.commit()
            # policy_text 也要更新一下对应的 id
            p.translated_file = trans_file.id
            db.session.add(p)
            db.session.commit()
            # 记一下成功转换的数量


def run_translator_small_lang():
    """
    小语种翻译（直接把format就地翻译，当然为了保险，使用了一个中间文件夹）
    Returns: 成功翻译的数量
    """
    converted_cnt = 0
    src_dir = os.path.join(Config.BASE_DIR, 'process/data_migaration/fetch')
    dest_dir = os.path.join(Config.BASE_DIR, 'process/data_migaration/trans_res')
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
        print(f'created dir: {dest_dir}')

    for file in os.listdir(src_dir):
        if file in ['format_1870fb52398f185536b63279d62c96a1.txt']:
            trans_lg.info(f'skip | {file}')
            continue
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file)
        if os.path.exists(dest_path):
            trans_lg.info(f'Already Done | {dest_path}')
            continue
        trans_lg.info(f"{src_path} -> {dest_path}")
        # translate_file_baidu(src_path, dest_path, to_lang='en')
        # converted_cnt += 1
        # trans_lg.info(f"Done and saved to {dest_path} | finished {converted_cnt}")
        try:
            translate_file_baidu(src_path, dest_path, to_lang='en')
        except Exception as e:
            trans_lg.error(f'translate file error| {e} | {file}')
        else:
            converted_cnt += 1
            trans_lg.info(f"Done and saved to {dest_path} | finished {converted_cnt}")


def run_title_translator(batch_size=20):
    """
    翻译所有的标题
    todo use multi-thread
    """
    batch_policy = list()
    translator = BaiduTranslator()
    for policy in PolicyText.query.filter(PolicyText.use,
                                          PolicyText.original_title != None,
                                          PolicyText.translated_title == None):  # type: PolicyText
        if len(batch_policy) < batch_size:  # 数量没到而且语言一致
            batch_policy.append(policy)
            continue
        # prepare and trans
        batch_title = '\n'.join([p.original_title.replace('\n', ' ') for p in batch_policy])
        try:
            batch_res_list = translator.translate(batch_title)
        except BaiduTransError as e:
            trans_lg.error(e.info)
        else:
            assert len(batch_res_list) == len(batch_policy)
            trans_lg.info(f"batch len: {len(batch_policy)}")
            for p, res in zip(batch_policy, batch_res_list):
                p.translated_title = res
                trans_lg.info(f"Translate Title {p.id}: {p.translated_title} <- {p.original_title}")
                db.session.add(p)
            db.session.commit()
            batch_policy.clear()
        time.sleep(TIME_DECAY)


def run_abs_translator():
    """
    翻译所有的摘要
    todo use multi-thread
    """
    cnt = 0
    translator = BaiduTranslator()
    for policy in PolicyText.query.filter(PolicyText.use,
                                          PolicyText.abstract != None,
                                          PolicyText.translated_abstract == None):  # type: PolicyText
        # prepare and trans
        abs_content = pure_text(policy.abstract)
        try:
            trans_res_list = translator.translate(abs_content)
        except BaiduTransError as e:
            trans_lg.error(e.info)
        else:
            policy.translated_abstract = ''.join(trans_res_list)
            trans_lg.info(f'abs_trans: {policy.id}, res: {policy.translated_abstract[:100]}')
            db.session.add(policy)
            db.session.commit()
            time.sleep(TIME_DECAY)
        cnt += 1
    return cnt

def run_keywords_translator():
    """
    翻译关键词
    Returns:
    """
    cnt = 0
    translator = BaiduTranslator()
    plist = PolicyText.query.filter(PolicyText.use,
                                    PolicyText.translated_keywords == None,
                                    PolicyText.keywords != None).all()
    # 遍历所有符合条件的政策
    for p in tqdm(plist):  # type: PolicyText
        cont_kw = p.keywords  # continuous keywords with comma
        if not cont_kw:
            trans_lg.warning(f"Blank keyword, id: {p.id}| {p.keywords}")
            continue
        sep_trans_kw = translator.translate(cont_kw.replace(', ', '\n'))  # seperated keywords list
        p.translated_keywords = ', '.join(sep_trans_kw)
        trans_lg.debug(f'{p.id} | {cont_kw} -> {p.translated_keywords}')
        db.session.add(p)
        db.session.commit()
        cnt += 0
    return cnt

def make_institute_dict():
    df = pd.read_csv('./translated_institution.csv', usecols=[0, 3])
    trans_dict = dict()

    def make_dict(x):
        trans_dict[x['institution']] = x['机构名称']

    df.apply(make_dict, axis=1)
    return trans_dict


def trans_institute():
    """使用词表翻译机构名称"""
    # load lookup table
    dictionary = make_institute_dict()
    for p in PolicyText.query.filter(PolicyText.use,
                                     PolicyText.institution != None,
                                     PolicyText.translated_institution == None):  # type: PolicyText
        if p.institution not in dictionary:
            trans_lg.error(f'not in dictionary | {p.institution}')
            continue
        p.translated_institution = dictionary[p.institution]
        trans_lg.debug(f'{p.institution} -> {p.translated_institution}')
        db.session.add(p)
        db.session.commit()


if __name__ == '__main__':
    # run_translator()
    run_keywords_translator()
    # run_title_translator()
    # run_abs_translator()
    # run_translator_small_lang()
    # trans_institute()
