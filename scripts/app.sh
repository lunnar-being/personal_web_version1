# kill old
pgrep -f /root/repos/disruptive/disruptive.py | xargs kill -s 9

# 生产环境
export IS_PROD=1
# pythonpath
export PYTHONPATH=/root/repos/disruptive
# 缓存
export PYTHONUNBUFFERED=1

cd /root/repos/disruptive/process
nohup /root/miniconda3/envs/spider37/bin/python /root/repos/disruptive/disruptive.py >> /root/repos/disruptive/log/app.log 2>&1 &