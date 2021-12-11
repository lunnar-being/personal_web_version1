# 生产环境
export IS_PROD=1
# pythonpath
export PYTHONPATH=/root/repos/disruptive
# 缓存
export PYTHONUNBUFFERED=1

cd /root/repos/disruptive/process
nohup /root/miniconda3/envs/spider37/bin/python /root/repos/disruptive/process/translate.py >> /root/repos/disruptive/log/trans.log 2>&1 &