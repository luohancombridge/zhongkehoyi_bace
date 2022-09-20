# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket

import os
import json
import urllib.request, urllib.error, urllib.parse
import re
import  chardet

import time

import sqlite3

from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import xlrd
import xlwt
def jiekou_fenxi_shouye(func):
    def jiekou_fenxi_shouye():
        func()
        return render_template('/hualala/jiekou_test/jiekou_fenxi.html')
    return jiekou_fenxi_shouye



def inter_face_detail(func):
    def inter_face_detai():
        func()
        if request.method=='POST':
            session['version_id_detail']=request.form['version_id']
            return jsonify(statu="success")
        else:
            if 'version_id_detail' not in session.keys():
                return redirect(url_for('Continuous_integration'))
            version_id=session['version_id_detail']
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            all_data=cu.execute('select catalog_detail.id,catalog_detail.first_catalog,catalog_detail.second_catalog,interface_detail.id, interface_detail.interface from catalog_detail inner join interface_detail on catalog_detail.id=interface_detail.catalog_id where catalog_detail.version_id=%s' % version_id).fetchall()
            #获取定时任务
            all_dingshirenwu=cu.execute('select * from timed_tasks where version_id=%s and create_name="%s"' % (str(version_id),g.user_name)).fetchall()
            all_dingshirenwu=[list(i)  for i in all_dingshirenwu]
            for k,i in enumerate(all_dingshirenwu):
                if str(i[9])!='':
                    timeArray = time.localtime(int(i[9]))
                    otherStyleTime = time.strftime("%Y--%m--%d %H:%M", timeArray)
                    all_dingshirenwu[k][9] =otherStyleTime
                if i[11] != None:
                    timeArray = time.localtime(int(i[11]))
                    otherStyleTime = time.strftime("%Y--%m--%d %H:%M", timeArray)
                    all_dingshirenwu[k][11] = otherStyleTime
                else:
                    all_dingshirenwu[k][11]=''
                if int(i[8])==0:
                    all_dingshirenwu[k][8]="未运行"
                elif int(i[8])==1:
                    all_dingshirenwu[k][8]="运行中"
                elif int(i[8])==2:
                    all_dingshirenwu[k][8]="运行完毕"
                if int(i[7]) == 0:
                    all_dingshirenwu[k][7] = "今日"
                elif int(i[7]) == 1:
                    all_dingshirenwu[k][7] = "每日"
            first_mulu=[]
            second_mulu={}
            for i in all_data:
                if i[1] not in first_mulu:
                         first_mulu.append(i[1])
                if i[2] not in second_mulu.keys():
                    second_mulu[i[2]]=i[1]
            #获取实时运行数据
            all_job=[list(i) for i in cu.execute('select * from real_time_run where name="%s"' % (g.user_name)).fetchall()]
            shishi_time=0
            shishi_type='未运行'
            for k,i in enumerate(all_job):
                if i[10]!='':
                    if int(i[10])>shishi_time:
                        shishi_time=int(i[10])
                    all_job[k][10]=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(all_job[k][10])))
                if int(i[12])==1:
                    shishi_type='运行中'
                elif int(i[12]) == 2:
                    shishi_type = '运行完毕'
            shishi_list=[shishi_type,time.strftime("%H:%M", time.localtime(int(shishi_time)))]
            #获取收发件人
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            all_sender=cu.execute('select id,email_user,email_detail from fajianren where name="%s"' % (g.user_name)).fetchall()
            all_receiver=cu.execute('select beizhu,address from email_address where user="%s"' % (g.user_name)).fetchall()
            cu.close()
            return render_template('/hualala/pages/interface_detail.html',all_dingshirenwu=all_dingshirenwu,all_sender=all_sender,all_receiver=all_receiver,shishi_list=shishi_list,all_job=all_job,all_data=all_data,first_mulu=first_mulu,second_mulu=second_mulu,version_id=session['version_id_detail'])
    return inter_face_detai