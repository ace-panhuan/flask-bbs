#encoding:utf-8
import os
# os.urandom函数定位  返回一个有n个byte那么长的一个string，很适合用于加密。
SECRET_KEY = os.urandom(24)



#  配置MYSQL连接
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'bbs'
USERNAME = 'root'
PASSWORD = 'panhuan520'

DB_UI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)

# 配置sqlalchemy
SQLALCHEMY_DATABASE_URI = DB_UI
SQLALCHEMY_TRACK_MODIFICATIONS= False

CMS_USER_ID = 'ASDFSADFDSFSDFSDF'


#mail
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = '465'
MAIL_USE_SSL = True #使用SSL，端口号为465或587
MAIL_USERNAME = '15907207005@163.com'
MAIL_PASSWORD = 'panhuan520'   #注意，这里的密码不是邮箱密码，而是授权码
MAIL_DEFAULT_SENDER = '15907207005@163.com'  #默认发送者