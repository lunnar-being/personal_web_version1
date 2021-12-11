# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: abstract.py
@version: 1.0
@time: 2021/08/03 18:03:39
@contact: jinxy@pku.edu.cn

抽取关键词
"""
from process import re, File, FileName, db, tqdm, logging
from process import PolicyText as Policy
from disruptive import app
app.app_context().push()

abs_lg = logging.getLogger('abstract')


def get_abstract(filepath):
    text = open(filepath, "r", encoding="utf-8").read()
    text = re.sub(r"\n\s*\n", "\n", text)
    abstract = []
    paralist = text.split("\n")
    i = 0
    while i < len(paralist) - 1:
        if "Abstract" in paralist[i] or "Summary" in paralist[i] or "Overview" in paralist[i] or "Preface" in paralist[i] or "Introduction" in paralist[i]:
            if len(paralist[i].split()) < 7 and paralist[i].count(".") < 2:
                i += 1
                while i < len(paralist) - 1 and len(paralist[i].split()) > 10:
                    abstract.append(paralist[i])
                    i += 1
                if abstract:
                    break
                else:
                    continue
        i += 1
    return "\n".join(abstract)


def run_abs():
    cnt = 0
    p_list = Policy.query.filter(Policy.use,
                                 Policy.abstract == None,
                                 Policy.format_file != None)
    for p in tqdm(p_list):  # type: Policy
        format_file = File.query.get(p.format_file)  # type: File
        name = FileName()
        name.set_by_name(format_file.savename)
        path = name.gen_path(file_type=2)
        abs_res = get_abstract(path)
        abs_lg.debug(abs_res)
        p.abstract = abs_res
        db.session.add(p)
        cnt += 1
    db.session.commit()
    return cnt


if __name__ == '__main__':
    run_abs()
