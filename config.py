import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
    if os.environ.get('IS_PROD'):
        print("[ENV] PROD ENV")
        # todo 密码放在明文代码，很危险，之后记得改密码然后放到环境变量里面
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://disruptive:jxy@dis@152.136.104.78:3306/disruptive?charset=utf8mb4'
    else:
        print("[ENV] DEV ENV")
        SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://dev:dev@dis_dev@152.136.104.78:3306/disruptive_dev?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_PROJECT_ID = 'decent-habitat-311302'
    BAIDU_ID = os.environ.get('BAIDU_ID')
    BAIDU_KEY = os.environ.get('BAIDU_KEY')
    RANK_TH = 6.7
