#!/bin/bash

# 爬虫需要代理
# export https_proxy=http://127.0.0.1:1087 http_proxy=http://127.0.0.1:1087 all_proxy=socks5://127.0.0.1:1080
# 生产环境
export IS_PROD=1
# pythonpath
export PYTHONPATH=/root/repos/disruptive
# 缓存
export PYTHONUNBUFFERED=1

cd /root/repos/disruptive/spider
nohup /root/miniconda3/envs/spider37/bin/python /root/repos/disruptive/spider/download_file.py >> /root/repos/disruptive/log/download_pdf.log 2>&1 &
