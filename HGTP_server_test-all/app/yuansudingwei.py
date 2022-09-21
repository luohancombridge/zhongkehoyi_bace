# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#根据列表执行运行文件
com='python D:\efq_ben\mulu.py'
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import os
from .zhixing import *
import time
import sqlite3
from .shell_name import *
# from .form import  *
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import xlrd
import random
import xlwt
UPLOAD_FOLDER = 'static/Uploads'
class openn(object):
  #返回定位元素页面
  def open(self,method,sessionn):
    if method=='POST'or method=='GET' :
        b=deng()
        if b.denglu():
            pass
        else:
           return  redirect(url_for('qiangj'))
        s=[session['user']]
        a=[]
        for parent,dirnames,filenames in os.walk(current_app.config.get('JIAO_DIZHI')):
            for i in dirnames:
                if 'mulu44'  in i :
                    continue
                else:
                  a.append(i.decode('gb2312'))
        self.conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        self.cu=self.conn.cursor()
        self.no='select num,url,name,method,canshu from yuansu where mokuai='+"'"+sessionn+"'"+'order by num asc'
        self.cu.execute(self.no)
        self.s=[self.cu.fetchall()]
        self.s.append(a)
        #返回元素编码的最大值加1
        self.no='select num from yuansu where mokuai='+"'"+sessionn+"'"
        self.cu.execute(self.no)
        self.ss=[int(i[0]) for i in self.cu.fetchall()]
        if len(self.ss)!=0:
          for i in range (0,max(self.ss)+2):
            if i not in self.ss:
                self.s.append(i)
                break
        else:
            self.s.append(0)
        print((self.s))
        #c.execute("create table yuansu(url nvarchar(50),name nvarchar(300),method nvarchar(300),canshu nvarchar(300)),mokuai nvarchar(300),num nvarchar(300)")
        return  self.s
  #第一个参数为传过来的表单，第二个参数为业务名
  def yuansuadd(self,form,sessionn):
      if '' in list(form.values()):
          return False
      else:
        self.conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        self.cu=self.conn.cursor()
        self.s='select * from yuansu where num='+"'"+form['id']+"'"
        self.s=self.cu.execute(self.s).fetchall()
        if len(self.s)==0:
         self.cu.executemany('INSERT INTO yuansu VALUES (?,?,?,?,?,?)', [(form['url'],form['yuansuming'],form['dingweifangshi'],form['dingweicanshu'],sessionn,form['id'])])
         self.conn.commit()
        else:
            self.cu.execute('UPDATE yuansu SET url=?,name=?,method=?,canshu=? WHERE num=? and mokuai=? ',(form['url'],form['yuansuming'],form['dingweifangshi'],form['dingweicanshu'],form['id'],sessionn))
            self.conn.commit()
        return True
  def yuansudele(self,form,session):
        self.conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        self.cu=self.conn.cursor()
        self.cu.execute('delete from yuansu where  num=? and mokuai=?',(form['num'],session))
        self.conn.commit()
        return True
  #生成excel表格
  def excel(self,session,user):
        self.conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        self.cu=self.conn.cursor()
        self.no='select num,url,name,method,canshu from yuansu where mokuai='+"'"+session+"'"+'order by num asc'
        self.cu.execute(self.no)
        self.s=self.cu.fetchall()
        self.filename=xlwt.Workbook()
        self.sheet=self.filename.add_sheet(session)
        for k,i in enumerate(['元素编号','元素所在页面','元素名','定位方式','定位参数']):
            self.sheet.write(0,k,i)
        for k,i in enumerate(self.s):
            [self.sheet.write(k+1,z,b) for z,b in enumerate(i)]
        self.filename.save(current_app.config.get('JIAO_DIZHI')+'/'+session+'.xls')
        return current_app.config.get('JIAO_DIZHI')+'\\'+session+'.xls'