# -*- coding: utf-8 -*-
#url自动化测试所调用的二级类
__author__ = 'SUNZHEN519'
#根据列表执行运行文件
com='python D:\efq_ben\mulu.py'
import socket
import time
import os
from subprocess import  *
from flask import render_template, flash, redirect,request,g,session
import random
from app import db
from .shell_name import *
import os
import copy
import sqlite3
from flask import current_app
import time
import datetime
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import os
from functools import wraps
from .zhixing import *
from .yuansudingwei import *
import time
import sqlite3
import threading
from .shell_name import *
# from .form import  *
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   #定义socket类型，网络通信，TCP
k=('127.0.0.1',8023)
s.bind(k)
s.listen(15)         #开始TCP监听
class MyThread(threading.Thread):
    def __init__(self, names,z,db_dizhi,tim):
        self.na=names
        self.z=z
        #数据库example。db 的地址
        self.db_dizhi=db_dizhi
        threading.Thread.__init__(self, name = names)
        self.tim=tim
    def run(self):
        #脚本地址
        if int(self.tim)!=0:
            while True:
                time.sleep(3)
                if int(time.time())>int(self.tim):
                    break
        #self.di=self.z.encode('gb2312')
        self.di=self.z
        self.z='python  '+self.di
        os.system(self.z)
        self.conn=sqlite3.connect(self.db_dizhi)
        cu = self.conn.cursor()
        self.k='update statu set statu=0 where name='+'\''+self.na.strip()+'\''
        cu.execute(self.k)
        self.conn.commit()
        self.conn.close()
        self.conn=sqlite3.connect(self.db_dizhi)
        cu = self.conn.cursor()
        self.k='select statu from statu where name='+'\''+self.na+'\''
        self.k='select statu from statu '
        cu.execute(self.k)
        cu.close()

while 1:
       name=None
       conn,addr=s.accept()   #接受TCP连接，并返回新的套接字与IP地址
       if addr:
           conn.sendall('connect successful')
       print(('Connected by',addr))    #输出客户端的IP地址
       kk=0
       tim=0
       while 1:
                data=conn.recv(1024)   #把接收的数据实例化
                kk+=1
                #新建线程运行脚本
                if 'D:'  in data  and 'example.db' not in data:
                    #保存地址
                    print((333333333333333333333333))
                    print(file)
                    print((type(file)))
                    file=data
                elif 'name is' in data:

                    #保存用户名
                    name=data.split('name is')[1].strip()
                    conn.close()
                    ub=MyThread(name,file,db,tim)
                    ub.start()
                    break
                elif 'time is'  in data:
                    tim=data.split('time is')[1].strip()
                else:
                    db=data