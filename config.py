import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #设置密匙
    SECRET_KEY = 'xcw123456'
    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xcw123456@localhost:3306/homework_submit?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

