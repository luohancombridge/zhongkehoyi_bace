# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import os
import socket
import platform
SECRET_KEY = 'you-will-never-guess'
basedir = os.path.abspath(os.path.dirname(__file__))
print (basedir)
parent_path= os.path.dirname(basedir)
if platform.system()=='Linux':
	db_path = os.path.join(parent_path,'sqlite_db')
	# db_path = r'/root/repo/hgtp_server/sqlite_db'
else :
    db_path= r'D:\中源宏一\base_code\sqlite_db'
# myname = socket.getfqdn(socket.gethostname(  ))
# myaddr = socket.gethostbyname(myname)
SQL_DB_URL= db_path
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_path, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(db_path, 'db_repository')
#脚本存储路径
JIAO_DIZHI=r'C:\s_ben'
#运行模板文件存放路径名为mulu44.py
MOBANDIZHI=r'C:\web flask\mulu44.py'
GENMULU=r'C:\web flask'
SOCKET=8022
#生成结果文件html的地址
JIEGUO=r'C:\web flaskapp\templates\\'
#数据库example地址
DB_DIZHI=os.path.join(db_path,'example.db')
CSRF_ENABLED = True
#生成结果文件存放目录
RESULT=r'C:\web flask\app\templates\result'
PERMANENT_SESSION_LIFETIME=600
LOG=os.path.join(basedir, 'log.txt')
#接口url
JIE_KOU_URL=r'C:\work\lr_test'
LOCUST_FILE=r'C:\all_new\locust_file'
#哗啦啦运行脚本存放地方
ALLRUN_FILE=os.path.join(parent_path,'run_mulu')
#接口运行数据库
JIE_KOU=os.path.join(db_path,'jiekou.db')
#本机ip地址
BENJI_IP=('192.168.18.129',8065)

#本地共享文件存放地址
SERVER_DI=parent_path

#本地server传递过来的zip压缩文件存放目录，要上传到git的文件
GIT_FILE_MULU=os.path.join(parent_path,'GIT_FILE_MULU')

FILE_CASE=os.path.join(basedir,r'app/static/tongji_num')

#要发送的邮件，图片存放地址
RESULT_PICT_SAVE=os.path.join(basedir,r'app/static/result_pic')

#日志存放地址根目录
LOG_FILE=r'/static/log_pic'
#日志存放地址全目录
BASEDIR=os.path.join(basedir,r'app/static/log_pic')
#本地server端口号
LOCAL_SERVER_PORT='5083'
#计数器
NUM_JISHU=0
#挡板数据库example地址
MOKE_DIZHI=os.path.join(db_path,'dangban_server.db')
#挡板 moke url  地址
MOKE_URL='moke_return'
#appium 地址
APPIUM_IP='10.50.180.56:5000'
#jmeter log 数据库
JMETER_LOG=os.path.join(db_path,'jmeter_get.db')
#jmeter log第三方地址
JMETER_IP='192.168.75.35:8889'
#资产数据库
PHONE_DB=os.path.join(db_path,'phone_detail.db')
#资产权限超级用户列表
ZICHAN_QUANXIAN="guochen,chensiyu,yuhao,lihaiyong,zhen"
#资产上传文件保存路径
PHONE_FILE=os.path.join(parent_path,'phone_file')
#资产下载文件路径
PHONE_FILE_DOWNLOAD=os.path.join(parent_path,'phone_file_download')
#持续集成重构加入数据库的db地址
CONTIN=os.path.join(db_path,'Continuous.db')
#数据库接口运行，权限列表
DB_JURISDICITION="sun,wangsiyang,zhen"
#数据库接口运行，权限列表
OWN_URL="127.0.0.1:5025"
#接口请求超时的时间
JIEKU_RESPONSE_TIME = 1
#mysql数据库连接
DIAODU_MYSQLUR={
	"host": '127.0.0.1',
	"user": "root",
	"passwd": "",
	"db": "dispatching_platform",
	"port": 3306,
	"charset": "utf8"
}
#考试分析的测试环境db地址
KAOSHIFENXI_DB= {
'host':'rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
'user':'QA',
'password':'hmk#%^&djofsdh'
}

JISHIBEN=os.path.join(db_path,'phone_detail.db')