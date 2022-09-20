# -*- coding: utf-8 -*-
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
from .shell_name import *
from .form import  *
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import logging
#记录日志模块
class log(object):
    def __init__(self):
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(current_app.config.get('LOG'))
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def wri(self,data):
        self.logger.info(data)
#删除脚本,及编辑脚本
class delete(object):
    def __init__(self):
        self.conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        self.cu=self.conn.cursor()
    #删除脚本
    def delete(self,k):
        if type(k)!=list:
            k=[k]
        for i in k:
            if  i.strip()=='':
                continue
            os.remove(session['url']+'/'+str(i.strip()))
            self.cu.execute('delete from userss where benname=? and mulu=? ',(i,session['url'],))
            self.conn.commit()
        self.conn.close()
    #删除目录下文件

#确定单用户登录类 session['time']是执行登录的时候写进去的时间戳
class deng(object):
    #每次执行各种操作需要验证登录状态
    def denglu(self):
        print((55555555555555555))
        print((session['user']))
        try :
            session['user']
        except:
            return False
        #根据user查找time值
        self.cu =g.db.cursor()
        self.cu.execute('select time from user where name=?',[(session['user'])])
        self.time=self.cu.fetchall()[0][0]
        if session['time'] in self.time:
            print((4444444444444444444444))
            print((self.time))
            return True
        else:
            return False
    #登录时插入的time值
    def insert(self,tim):
        self.cu =g.db.cursor()
        self.cu.executemany('update  user  set time=? where name=?', [(tim,session['user'])])
        g.db.commit()
class zhixing(object):


    #当有定时计划运行时，将计划信息填写进入runing表中，并修改statu标志位为3

    def dingshi(self,user,tim):
        #获取当前时间到天
        tim=datetime.datetime.now().strftime("%Y-%m-%d")+' '+tim
        tim = time.strptime(tim, "%Y-%m-%d %H:%M")
        #转换为时间戳
        tim = int(time.mktime(tim))
        cu =g.db.cursor()
        cu.execute('select * from runing  where user='+'\''+user.strip()+'\'')
        if len(cu.fetchall())!=0:
            cu.execute('delete from runing  where user='+'\''+user.strip()+'\'')
            g.db.commit()
        cu.executemany('INSERT INTO runing VALUES (?,?,?,?)', [(user,tim,'2','2')])
        g.db.commit()
        #修改statu表中标志位为3意思是有计划执行的脚本
        cu.execute('update statu set statu=3 where name='+'\''+user.strip()+'\'')
        g.db.commit()
    #将新增脚本信息添加进配置log众
    #插入数据并验证脚本名是否重复若是重复则只是修改类名，并验证类名是否重复，若重复则修改类名name为列表类型第一个为脚本名第二个为类名
    def add_data(self,name):
         name[0]=name[0].strip()
         name[1]=name[1].strip()
         self.s=name[1]
         cu =g.db.cursor()
         self.no='select benname from userss where  mulu='+"'"+session['url']+"'"
         cu.execute(self.no)
         self.benname=[i[0] for i in cu.fetchall()]
         #self.benname=cu.fetchall()
         self.no='select leiname from userss where  mulu='+"'"+session['url']+"'"+ ' and '+'benlei='+"'"+session['benlei']+"'"
         cu.execute(self.no)
         self.leiname=[i[0] for i in cu.fetchall()]
         if name[0].strip() in self.benname:
                 cu.execute('UPDATE userss SET leiname=?,benlei=?,detal=? WHERE benname=? and mulu=?',(name[1].encode('utf-8'),session['benlei'],name[2],name[0].encode('utf-8'),session['url']))
         if name[0].strip() not in self.benname:
             if name[1].strip() not in self.leiname:
                 cu.executemany('INSERT INTO userss VALUES (?,?,?,?,?,?,?)', [(name[0],name[1],session['url'],name[2],session['benlei'],session['add_biao_data'],'0')])
                 self.s=name[1]
             else:
                 self.s=chr(random.randint(97, 122))+chr(random.randint(97, 122))+name[1]
                 cu.executemany('INSERT INTO userss VALUES (?,?,?,?,?,?)', [(name[0],self.s,session['url'],name[2],session['benlei'],session['add_biao_data'],'0')])
             #cu.execute('insert into User(id,benname,leiname) values(%d,%s,%s)'% (self.no,name[0],self.s))
         g.db.commit()
         if self.s==name[1]:
             return None
         else:
             return self.s
    #返回列表结果，参数为列表
    def find_data(self,*k):
         conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
         cu=conn.cursor()
         self.s=[]
         if len(k)!=0:

          if type(k[0])!=list:
             k=[k[0]]
          for i in k[0]:
             print(i)
             url=session['url'].replace('/','//')
             #u='select * from userss where benname='+'\''+i+'\''+'and'+'mulu=' +"'"+session['url']+"'"
             if session['benlei']=='1':
                if 'fen_ye' in session and session['fen_ye']!='全部':
                      cu.execute('select * from userss where benname=? and mulu=? and benlei=? and biao_qian=? ',
                               (i, session['url'], session['benlei'],session['fen_ye']))
                else:
                   cu.execute('select * from userss where benname=? and mulu=? ',(i,session['url']))
             else:
                 if 'fen_ye' in session and session['fen_ye'] != '全部':
                    cu.execute('select * from userss where benname=? and mulu=?  and benlei-? and biao_qian=?',(i,session['url'],session['benlei'],session['fen_ye']))
                 else:
                     cu.execute('select * from userss where benname=? and mulu=?  and benlei-? ',
                                (i, session['url'], session['benlei']))

             for b in cu.fetchall():
                 self.s.append(b)
             #cu.execute(u)
         else:
             if session['benlei']=='1':
                 #print session['fenye']
                 if 'fen_ye' in session  and session['fen_ye']!='全部':
                     cu.execute('select * from userss where mulu=? and benlei=? and biao_qian=?', (session['url'], session['benlei'],session['fen_ye']))
                 else:
                     cu.execute('select * from userss where mulu=? and benlei=?',(session['url'],session['benlei']))
             else:
                 if 'fen_ye' in session and session['fen_ye'] != '全部':
                   cu.execute('select * from userss where mulu=? and biao_qian=?',(session['url'],session['fen_ye']))
                 else:
                     cu.execute('select * from userss where mulu=? ',
                                (session['url'], ))

             for b in cu.fetchall():
                 self.s.append(b)
         conn.close()
         return self.s
    #将文件名合类名存入userss表中，并修改脚本中重复的表名
    def add_ben(self,name):
        #获取文件地址
        self.lei=[session['url']+'\\'+str(i) for i in name]
        #打开文件获取类名
        self.lei1=[]
        for ui,ii in enumerate(self.lei):
            self.s=open(ii,'r')
            self.ss=self.s.readlines()
            #获取所有类名
            if session['benlei']=='1':
               for enu,k in enumerate(self.ss):
                    if 'class ' in k and '(unittest.TestCase):' in k:
                       self.kkk=k.split('class')[1].split('(')[0].strip()
                       self.detal=self.ss[enu-1].split('#')[-1].decode('utf-8')
                       self.s.close()
                       self.change_lei=self.add_data([name[ui],self.kkk,self.detal])
                       #去除重复类名
                       if self.change_lei !=None:
                          self.ss[enu]=self.ss[enu].replace(self.kkk,self.change_lei)
                          self.s=open(ii,'w')
                          self.s.writelines(self.ss)
                          self.s.close()
            else:
              if '.py'  in ii :
                for enu,k in enumerate(self.ss):
                     if 'class ' in k and '(' in k and ':' in k and ')' in k:
                       self.kkk=k.split('class')[1].split('(')[0].strip()
                       self.detal='（非脚本）   '+self.ss[enu-1].split('#')[-1].decode('utf-8')
                       self.s.close()
                       self.change_lei=self.add_data([name[ui],self.kkk,self.detal])
                       #去除重复类名
                       if self.change_lei !=None:
                          self.ss[enu]=self.ss[enu].replace(self.kkk,self.change_lei)
                          self.s=open(ii,'w')
                          self.s.writelines(self.ss)
                          self.s.close()
              elif '.txt' in ii  or '.jmx' in ii:
                       self.kkk='txt 配置文件'

                       self.detal='(第一行内容)   '+self.ss[0].decode('gb2312')
                       self.s.close()
                       self.change_lei=self.add_data([name[ui],self.kkk,self.detal])





    def run_ben(self,name):
        cu = g.db.cursor()
        s='select statu from statu where name='+'\''+session['user']+'\''
        cu.execute(s)
        s=cu.fetchall()[0][0].strip()
        if   s=='3':
            s='select time from runing where USER ='+'\''+session['user']+'\''
            cu.execute(s)
            self.time=int(cu.fetchall()[0][0].strip())
        else:
            self.time=0
        s='update statu set statu=1 where name='+'\''+session['user']+'\''
        cu.execute(s)
        g.db.commit()
        g.statu=1
        self.s=self.find_data(name)
        #脚本名导入
        self.name=[str('from '+i[0].split('.py')[0]+' import '+i[1]+'\n') for i in self.s]
        #类名
        self.lei=[str('unittest.TestLoader().loadTestsFromTestCase('+i[1]+')') for i in self.s]
        self.s=open(current_app.config.get('MOBANDIZHI'),'r')
        self.u=self.s.readlines()
        self.s.close()
        self.s=open(session['url']+'\\'+session['user']+'.py','w')
        self.s.writelines(self.u)
        self.s.close()
        self.b=self.u
        #s删除以前的导入脚本类from
        for k,i in enumerate(self.b):
            if 'import unittest' in i:
                self.k11=k
            if 'import HTMLTestRunner' in i:
                self.k22=k
        self.b=self.b[:self.k11+1]+self.b[self.k22:]
        for i in self.name:
            self.b.insert(self.k11+1,str(i))
        #更新运行语句
        self.s=''
        for i in self.lei:
            self.s=self.s+i+','
        self.s='['+self.s+']'
        self.s=self.s.replace(',]',']')
        for k,i in enumerate(self.b):
            if 'suite = unittest.TestSuite(' in i :
                self.b[k]= 'suite = unittest.TestSuite('+str(self.s)+')'+'\n'
        #将结果文件名该文user文件名
            if 'filename=' in i:
                self.b[k]=i.replace('dizhi',current_app.config.get('RESULT')+'\\'+session['user']+'.html')
            #选择执行文件结果html放置的目路径
        self.s=open(session['url']+'\\'+session['user']+'.py','w')
        self.s.writelines(self.b)
        self.s.close()
        #打开socket
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        u=self.s.connect(('127.0.0.1',current_app.config.get('SOCKET')))
        self.url=(session['url']+'\\'+session['user']+'.py').encode('gb2312')
        print((1111111111111111111111111))
        print((self.url))
        print((session['user']))
        print(name)
        #self.s.sendall(session['url']+'\\'+session['user']+'.py')
        self.s.sendall(self.url)
        time.sleep(1)
        self.s.sendall(current_app.config.get('DB_DIZHI'))
        time.sleep(1)
        self.s.sendall('time is '+str(self.time))
        time.sleep(1)
        self.s.sendall('name is '+session['user'])
        time.sleep(1)
        #验证脚本是否跑完

        self.result='select statu from statu where name='+'\''+session['user'].strip()+'\''


#将传入的脚本内容前面添加入 行号，
class bianji(object):
    def __init__(self,b):
        self.b=b
    #添加行号返回数据
    def add(self):
        for k,i in enumerate(self.b):
            self.p=k+1
            if self.p<10:
                self.b[k]=str(self.p)+'        '+i
            else:
                self.b[k]=str(self.p)+'       '+i
        return self.b
    #将行号删除返回正确脚本数据
    def dele(self):
        for k,i in enumerate(self.b):
            self.p=k+1
            if len(i)>3 and i[:2]=='  ' :
                if k<=10:
                        self.b[k]=i.split('       ')
                        if len(self.b[k])>2:
                            self.count='       '*self.b[k].count('')
                            self.b[k]=self.count+''.join(self.b[k][1:])
                        else:
                           self.b[k]=self.b[k][-1]

                else:
                        self.b[k]=i.split('        ')
                        if len(self.b[k])>2:
                           self.count='        '*self.b[k].count('')
                           self.b[k]=self.count+''.join(self.b[k][1:])
                        else:
                            self.b[k]=self.b[k][-1]
                        self.b[k]='       '.join(self.b[k].split('       ')[1:])
                self.b[k]=self.b[k][2:]
            elif len(i)>3 and i[1]==' ' and i[0]!=' ' :
                self.b[k]=i.split('        ')
                if len(self.b[k])>2:
                    self.count='        '*self.b[k].count('')
                    self.b[k]=self.count+''.join(self.b[k][1:])
                else:
                    self.b[k]=self.b[k][-1]
            else:
                self.b[k]=i.split('       ')
                if len(self.b[k])>2:
                    self.count='       '*self.b[k].count('')
                    self.b[k]=self.count+''.join(self.b[k][1:])
                else:
                    self.b[k]=self.b[k][-1]
        return self.b


if __name__=='__main__':
    s=zhixing(['we','qa'])
