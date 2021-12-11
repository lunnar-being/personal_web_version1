# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: main.py
@version: 1.0
@time: 2021/08/18 18:28:31
@contact: jinxy@pku.edu.cn

all the process things
"""


from pdf_parser import run_converter
from html_parser import run_html_parser
from relate_weight import run_weight
from abstract import run_abs
from translate import (run_translator, run_keywords_translator, run_abs_translator, run_title_translator, trans_institute)
from techwords import run_tech_words
# from keywords import
from field import run_filed_cls

def all_process():
    run_converter()
    run_html_parser()
    run_weight()
    run_abs()
    run_translator()
    run_keywords_translator()
    run_abs_translator()
    run_title_translator()
    trans_institute()
    run_tech_words()
    run_filed_cls()


if __name__ == '__main__':
    all_process()
