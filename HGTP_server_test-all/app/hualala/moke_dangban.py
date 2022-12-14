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
def moke_dangban(fun):
    def moke_dangban():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % (
            request.headers.get('X-Real-IP'))).fetchall()[
            0][0]
        db.close()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        xiangmu=cu.execute('select * from xiangmu_data').fetchall()
        yewu=cu.execute('select * from yewu_data').fetchall()
        linux=cu.execute('select id,name from linux_detail').fetchall()
        case_list=cu.execute('select * from case_data').fetchall()
        mulu_url='/'.join(request.url.split('/')[:-1]).replace('8080','5025')
        if len(xiangmu)>0 and len(yewu)>0:
            moke_url=mulu_url+'/'+current_app.config.get('MOKE_URL')+'/'+str(xiangmu[0][0])+'_'+str(yewu[0][0])
        else:
            moke_url='none'
        moke_gen_url=mulu_url+'/'+current_app.config.get('MOKE_URL')+'/'
        db.commit()
        db.close()
        return render_template('/hualala/jiekou_test/dangban_server.html',xiangmu=xiangmu,yewu=yewu,linux=linux,case_list=case_list,moke_url=moke_url,moke_gen_url=moke_gen_url)
    return moke_dangban



def top_add_ceshi(fun):
    def top_add():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % (
            request.headers.get('X-Real-IP'))).fetchall()[
            0][0]
        db.close()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        if  request.form['type']=='top_add':
            if len(cu.execute('select * from xiangmu_data where  name="%s" ' %(request.form['name'])).fetchall())!=0:
                return jsonify(statu='chongfu')
            else:
             cu.executemany('INSERT INTO  xiangmu_data values (null,?,?,?,?)', [(name, request.form['name']
                                                                                ,request.form['request_url'],str(time.time()))])

        elif 'top_bianji'  in request.form['type']:
            id=request.form['type'].split('#')[-1]
            cu.executemany('update  xiangmu_data  set name=?,change_time=? where id=?', [(request.form['name'],str(time.time),id)])

        elif 'second_add'==request.form['type']:
            if len(cu.execute('select * from yewu_data where  name="%s" ' %(request.form['name'])).fetchall())!=0:
                return jsonify(statu='chongfu')
            else:
              cu.executemany('INSERT INTO  yewu_data values (null,?,?,?,?)', [( request.form['name'],name
                                                                                ,request.form['request_url'],str(time.time()))])
        db.commit()
        db.close()
        return jsonify(statu='success')
    return top_add




def delete_moke_xiangmu(fun):
    def delete_moke_xiangmu():
        fun()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        if (request.form['type']=='top_delete'):
            cu.execute('delete from xiangmu_data where id="%s"' % (request.form['id']))
        elif (request.form['type']=='yewu_delete'):
            cu.execute('delete from yewu_data where id="%s"' % (request.form['id']))
        elif (request.form['type']=='case_delete'):
            cu.execute('delete from case_data where id="%s"' % (request.form['id']))
        db.commit()
        db.close()
        return jsonify(statu='success')
    return delete_moke_xiangmu


def yewuadd(func):
    def yewuadd():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        user = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % (
            request.headers.get('X-Real-IP'))).fetchall()[
            0][0]
        db.close()
        name=request.form['name']
        id=request.form['id']
        print((999999999999999999999999999999999))
        print(id)
        request_url = request.form['request_url']
        jiekou_type = request.form['jiekou_type']
        yewu_request_method = request.form['yewu_request_method']
        yewu_send_type = request.form['yewu_send_type']
        header_json=request.form['header_json']
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        before_save=cu.execute('select * from yewu_data where moke_url="%s" and xiangmu_id="%s"' % (request.form['request_url'],str(id))).fetchall()
        if len(before_save)==0:
            cu.executemany('INSERT INTO  yewu_data values (null,?,?,?,?,?,?,?,?,?)', [(name,user,str(time.time()),request_url,jiekou_type,yewu_request_method,yewu_send_type,id,header_json)])
        else:
            return jsonify(statu='url ??????')
        db.commit()
        db.close()
        return jsonify(statu='success')
    return yewuadd

def linux_add(func):
    def linux_add():
        func()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        before_save=cu.execute('select * from linux_detail where ip="%s"' % request.form['linux_url']).fetchall()
        if len(before_save)==0:
            cu.executemany('INSERT INTO  linux_detail values (null,?,?,?,?,?)', [(request.form['linux_name'],request.form['linux_url'],request.form['linux_host'],request.form['linux_user'],request.form['linux_password'])])
        db.commit()
        db.close()
        return jsonify(statu='success')
    return linux_add



def yewu_bianji_show(func):
    def yewu_bianji_show():
        func()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        before_save=cu.execute('select * from yewu_data where id="%s"' % request.form['id']).fetchall()[0]
        return jsonify(name=before_save[1],moke_url=before_save[4],chuancan_type=before_save[5],
           jiekou_type=before_save[6],yewu_request_moetho=before_save[7],yewu_send_type=before_save[8])
    return yewu_bianji_show


def add_case(funct):
    def add_case():
        funct()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        try:
            json.loads(request.form['request_json'])
            json.loads(request.form['xiangmuid'])
        except:
            return jsonify(statu='json error')
        name=request.form['name']
        if len(cu.execute('select * from  case_data where name="%s" and yewu_id="%s"'% (name,request.form['yewuid'])).fetchall())!=0:
            return jsonify(statu='chongfu')
        else:
            cu.executemany('INSERT INTO  case_data values (null,?,?,?,?,?,?)', [(request.form['time_sleep'],request.form['request_json'],request.form['respons_json'],request.form['yewuid'],request.form['xiangmuid'],name)])
        db.commit()
        db.close()
        return jsonify(statu='success')
    return add_case


def   case_read(func):
    def case_read():
        func()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        data=cu.execute('select * from case_data where id="%s"' % (request.form['id'])).fetchall()[0]
        session['case_di']=request.form['id']
        db.commit()
        db.close()
        return jsonify(name=data[6],time_sleep=data[1],request_json=data[2],return_json=data[3])
    return case_read


def  bianji_case(func):
    def bianji_case():
        func()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        try:
            json.loads(request.form['request_json'])
            json.loads(request.form['respons_json'])
        except:
            return jsonify(statu=='json error')
        cu.executemany('update  case_data  set name=?,take_time=?,request_json=?,return_json=? where id=?',
                       [(request.form['name'], request.form['time_sleep'],request.form['request_json'],request.form['respons_json'],  session['case_di'])])

        db.commit()
        db.close()
        return  jsonify(statu='success')
    return bianji_case

def server_use(func):
    def server_use():
        func()
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        linux_detail=cu.execute('select * from linux_detail where name="%s"' %  (request.form['name'])).fetchall()[0]
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('10.104.6.8', username='xiaopeng', password='******')
        return jsonify(statu="success")
    return server_use


def moke_return(func):
    def moke_return(id):
        func(id)
        db = sqlite3.connect(current_app.config.get('MOKE_DIZHI'))
        cu = db.cursor()
        xiangmuid=id.split('_')[0]
        yewuid = id.split('_')[1]
        yewu_detail=cu.execute('select * from yewu_data where id="%s" ' % yewuid  ).fetchall()[0]
        case_detail=cu.execute('select * from case_data where yewu_id="%s"' % yewuid ).fetchall()
        header_json=json.loads(yewu_detail[9].strip())
        if header_json!='':
            for i  in  header_json:
                if i in list(request.headers.keys()) and ']I9 ]'==header_json[i]:
                    pass
                else:
                    return jsonify(statu="header error")
        if yewu_detail[6] == 'get':
               request_json = dict(list(zip(list(request.args.keys()), list(request.args.values()))))
        if yewu_detail[6]=='post' :
            if   yewu_detail[7] == 'json':
               if header_json!='':
                  request_json=json.loads(request.get_data())
            elif   yewu_detail[7] == 'form_data':
                request_json=dict(list(zip(list(request.form.keys()),list(request.form.values()))))
        for i  in case_detail:
            print((i[2]))
            if json.loads(i[2])==request_json:
                return jsonify(i[3])
        return jsonify(statu="not find case")
    return  moke_return