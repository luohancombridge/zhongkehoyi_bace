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
import shutil
import sqlite3
import smtplib
from email.mime.text import MIMEText
import urllib.request, urllib.error, urllib.parse
from tempfile import mktemp
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import unittest
from app.db_sqlchemy_sqlite import *
#import HTMLTestRunner
import functools
from app import db as db_sqlite
from app.db_sqlchemy_sqlite import *
def chixuijicheng_run(fun):
    def chixuijicheng_run():
        fun()
        if 'today_ci_pic' in list(current_app.config.keys()):
            current_app.config.pop('today_ci_pic')
        if 'seven_ci_pic' in list(current_app.config.keys()):
            current_app.config.pop('seven_ci_pic')
        if 'local_seven_pic' in list(current_app.config.keys()):
            current_app.config.pop('local_seven_pic')
        job=request.form['job']
        job=json.dumps({'name':job,'result':''})
        if 'job_id' in list(request.form.keys()):
           job_id=request.form['job']
        else:
            job_id=''
        job = json.dumps({'name': job, 'result': '','job_id':job_id})
        email = json.loads(request.form['email'])
        email_detail=json.dumps({'send':email['sender_user'],'receive':email['receiver_user'],'title':email['title']})
        #获取文件目录列表
        git_path = ''
        git_branch = ''
        for k,i in enumerate(json.loads(request.form['all_path'])):
            git_path =git_path+ '#' + i['git']
            git_branch = git_branch + '#' + i['branch']
        db_sqlite = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db_sqlite.cursor()
        #自动分发
        if request.form['run_server']=='自动分发' or   request.form['run_server']=='Automatic distribution':
          if len(cu.execute('select server from dingshi_run  where statu="1"').fetchall())==0:
              run_server = cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
          else:
            xiancheng_detail= [i[0] for i in cu.execute('select server from dingshi_run  where statu="1"').fetchall()  if i in
                               [z[0] for z in cu.execute('select ip from all_server where statu="1" ').fetchall()]]
            #删除在server中不存在的
            if len(xiancheng_detail)==0:
                run_server=cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
            else:
              all_server = [i[0] for i in cu.execute('select ip from all_server where statu="1" ').fetchall()]
              server_num = {}
              if len(all_server)!=len(list(set(xiancheng_detail))) :
                for i in all_server:
                  if i not in xiancheng_detail   :
                      run_server=i
              else:
                      for k in xiancheng_detail:
                          server_num[k]=xiancheng_detail.count(k)
                      for z in list(server_num.keys()):
                          if server_num[z]==min(server_num.values()):
                              run_server=z
                              break
        else:
            run_server=request.form['run_server']
        #判断web自动化实时运行是否再运行中
        if 'statue' in list(request.form.keys())  and request.form['statue']=='shishi':
            name = cu.execute(
                'select name from user where ip like "%s" order by time desc limit 0,1' % ('%' + request.headers.get('X-Real-IP')+ '%')).fetchall()[
                0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'实时' ) ).fetchall())!=0 and  cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'实时' ) ).fetchall()[0][0]=='1':
                return jsonify(statu='running')
        #判断接口自动化实时运行是否再运行中
        if 'statue' in list(request.form.keys())  and request.form['statue']=='jiekou_shishi':
            name = cu.execute(
                'select name from user where ip like "%s" order by time desc limit 0,1' % ('%' + request.headers.get('X-Real-IP')+ '%')).fetchall()[
                0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'接口实时' ) ).fetchall())!=0 and  cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'接口实时' ) ).fetchall()[0][0]=='1':
                return jsonify(statu='running')
        try:
           name=request.form['name']
        except:
            name = cu.execute(
                'select name from user where ip like "%s" order by time desc limit 0,1' % ('%' + request.headers.get('X-Real-IP')+ '%')).fetchall()[
                0][0]
        #请求时间,如果有传递过来run_time则使用传递过来的，如果没有则用当前时间戳
        if 'time'  in list(request.form.keys()):
            run_time=request.form['time']
        else:
          run_time = str(time.time())
        user_name = [i.strip() for i in request.form['all_name'].split('#') if i.strip() != '']
             #os.popen('git pull http://sunzhen:6551268Sun@' + str(user_name[k]))
        #根据目录copy相应文件到设置的run文件夹下,之前删除以用户名明明的文件夹，
        if 'statu' in request.form and 'dingshi' in request.form['statu']and 'run_statu'  in list(request.form.keys()):
            if 'everyday' not   in request.form['run_statu'].strip():
                 run_time=time.strftime('%Y-%m-%d',time.localtime(time.time())) +'  '+run_time
            if  request.form['statu']=='dingshi':
               all=cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc'  % (name ) ).fetchall()
            elif request.form['statu']=='jiekou_dingshi':
               all=cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc'  % (name ) ).fetchall()
            if len(all)>4:
                for i in all[-4:]:
                         cu.execute('delete from dingshi_run where id=%s '  % (i) )
                         strr='#'+str(all[-1])
                         db_sqlite.commit()
            try:
                 this_time=time.strftime('%Y-%m-%d', time.localtime(time.time()))+'  '+request.form['time']
            except:
                return jsonify(statu='error')
            if request.form['statu'] == 'dingshi':
               cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),request.form['time'],request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
            elif request.form['statu'] == 'jiekou_dingshi':
                if request.form['run_statu'] == 'everyday':
                    this_str = '接口定时设置 ：everyday' + request.form['time']
                else :
                    this_str = '接口定时设置 ：' + this_time
                cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                 this_str,
                                                                                                 git_path, '0',
                                                                                                 email_detail, '', '{}',
                                                                                                git_branch, job,
                                                                                                 run_server)])

            db_sqlite.commit()
            html='  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td> </tr>'
            if request.form['statu'] == 'dingshi':
                dingshi_detail = [[i[1], i[2], i[4],i[-1]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (name)).fetchall()]
            elif request.form['statu'] == 'jiekou_dingshi':
                dingshi_detail = [[i[1], i[2], i[4], i[-1]] for i in cu.execute(
                    'select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name,'接口%')).fetchall()]
                this_job_id = [[i[0]] for i in cu.execute(
                    'select id from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name,'接口%')).fetchall()][0][0]
            db_sqlite.close()
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() in ['0','3'] :
                    i[-2] = 'ready'
                elif i[-2].strip() in ['1','4']:
                    i[-2] = 'running'
                elif i[-2].strip() in ['2','5']:
                    i[-2] = 'over'
            s=''
            for i in dingshi_detail:
                s+=html.replace('{{i[4]}}',str(i[4])).replace('{{i[1]}}',i[1]).replace('{{i[2]}}',i[2]).replace('{{i[3]}}',i[3])
            if 'send_message' in request.form.keys() and request.form['send_message'] != '{}':
                this_message = json.loads(request.form['send_message'])
                add_meesa = run_jiekou_message_feishu(run_id=int(this_job_id), type_message=this_message['type'],
                                                      message_id_list=json.dumps(this_message['seleect_id']),
                                                      run_beizhu=this_message['this_case_beizhu'])
                db.session.add(add_meesa)
                db.session.commit()
                feishu_url_all = []
                for feishu_id in this_message['seleect_id']:
                    result = json.loads(message_jiekou.query.filter_by(id=feishu_id, ).first().message_detail)
                    result['this_case_beizhu'] = this_message['this_case_beizhu']
                    feishu_url_all.append(result)
            return jsonify(statu="success",html=s)
        if  len(cu.execute('select name from run where name="%s"' % name).fetchall())==0:
            cu.executemany('INSERT INTO  run values (?,?,?,?,?,?,?)',[(1, name,request.headers.get('X-Real-IP'),request.form['all_path'],time.time(), run_time,email_detail)])
            db_sqlite.commit()
        else:
            cu.executemany('update  run  set statu=0,ip=?,mulu=?,time=?,time_run=? ,email=? where name=?', [(request.headers.get('X-Real-IP'),request.form['all_path'],time.time(), run_time, email_detail,name)])
            db_sqlite.commit()
        if 'statu' not in list(request.form.keys()):
            if request.form['statue']=='shishi':
                  if   len(cu.execute('select * from dingshi_run where name="%s"   and run_time="%s"' % (name,'实时')).fetchall())==0:
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),'实时',request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
                    db_sqlite.commit()
                  else:
                    cu.executemany('update  dingshi_run  set statu=1,name=?,update_time=?,all_git=?,email=?,git_branch=?,run_result="{}" ,job=?,server=? where name=? and run_time="实时"', [(name,time.time(),request.form['all_path'],email_detail,request.form['all_branch'],job,run_server,name)])
                    db_sqlite.commit()
            elif request.form['statue']=='jiekou_shishi':
                    cu.execute('delete from dingshi_run where run_time="接口实时" and name=? ',(name,))

                    db_sqlite.commit()
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                     '接口实时',
                                                                                                     request.form[
                                                                                                         'all_path'],
                                                                                                     '0', email_detail,
                                                                                                     '', '{}',
                                                                                                     request.form[
                                                                                                         'all_branch'],
                                                                                                     job, run_server)])
                    db_sqlite.commit()

        #拉下来git代码
        #if 'run_time'  in request.form.keys():
           #run_dir=os.path.join(current_app.config.get('ALLRUN_FILE'),name,str(time.time()))
        if 'statue'  not in list(request.form.keys()):
                    run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name, str(time.time()))
                    try:
                        os.chdir(run_dir)
                    except:
                        if not  os.path.isdir(os.path.dirname(run_dir)):
                            os.mkdir(os.path.dirname(run_dir))
                        os.mkdir(run_dir)
                        os.chdir(run_dir)
                    #在每个目录下面增加构造文件
                    if   'statue'  in list(request.form.keys()) and  request.form['statue']!='jiekou_shishi':
                            open(os.path.join(run_dir, '__init__.py'), 'w').close()
                            for fpathe, dirs, fs in os.walk(run_dir):
                                for f in dirs:
                                    if '.git'!=f.strip() and '.idea'!=f.strip():
                                      open(os.path.join(fpathe, f, '__init__.py'), 'w').close()
                    try:
                       os.chdir(r'C:\\')
                    except:
                      pass
        else:
            run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name)
        s={}
        s['name']=name
        b = run_dir.split(os.sep)
        s['run_dir']=run_dir
        if   'statue'  in list(request.form.keys())  and request.form['statue'] != 'jiekou_shishi':
            if  not os.path.isdir(run_dir):
                os.mkdir(run_dir)
            open(os.path.join(run_dir, '__init__.py'), 'w').close()
        if 'statu' in list(request.form.keys()) :
            if  request.form['statu']  in ['dingshi','jiekou_dingshi']:
                 s['id']=request.form['id']
        else:
            if request.form['statue']=='dingshi':
                    id=cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name,'实时')).fetchall()[0][0]
                    s['id']=str(id)
            elif request.form['statue']=='jiekou_shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '接口实时')).fetchall()[0][0]
                s['id'] = str(id)
            elif request.form['statue']=='url_shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '实时')).fetchall()[0][0]
                s['id'] = str(id)
            elif request.form['statue']=='shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '实时')).fetchall()[0][0]
                s['id'] = str(id)
        if run_server.strip()!='':
            port=cu.execute('select duan_kou from all_server where ip="%s"' % (run_server)).fetchall()[0][0]
        db_sqlite.close()
        #发送验证是接口自动化还是url自动化
        if 'statu' in list(request.form.keys()):
             s['statu']=request.form['statu']
        elif 'statue' in list(request.form.keys()):
            s['statu'] = request.form['statue']
        #获取ip地址
        s['server_di'] =current_app.config.get('SERVER_DI')
        s['job_id']=job_id
        #将本地目录转化为网络目录
        #如果不是接口自动化则转为网络目录
        if 'statue'  not  in list(request.form.keys()):
            s['run_dir']=os.path.join(s['server_di'],s['run_dir'].split(os.sep)[-3],s['run_dir'].split(os.sep)[-2],s['run_dir'].split(os.sep)[-1])
        hostname = socket.gethostname()
        # s['server_ip'] = socket.gethostbyname(hostname)
        # s['server_ip']='172.18.29.253'
        s['server_ip']=run_server
        s['git_path']=git_path
        if 'statue'  in list(request.form.keys()) and request.form['statue']=='url_shishi':
            s['statue']=request.form['statue']
        s['git_branch']=git_branch
        s['email_detail']=email_detail
        s['job']=job
        s['OWN_URL']=current_app.config.get('OWN_URL')
        s['pic_mulu']=current_app.config.get('RESULT_PICT_SAVE')
        if 'send_message' in request.form.keys() and request.form['send_message']!='{}':
            this_message= json.loads(request.form['send_message'])
            add_meesa = run_jiekou_message_feishu(run_id=int(s['id']), type_message=this_message['type'],
                                      message_id_list=json.dumps(this_message['seleect_id']),run_beizhu = this_message['this_case_beizhu'])
            db.session.add(add_meesa)
            db.session.commit()
            feishu_url_all =[]
            for feishu_id in this_message['seleect_id']:
                  result = json.loads(message_jiekou.query.filter_by(id=feishu_id,).first().message_detail)
                  result['this_case_beizhu'] = this_message['this_case_beizhu']
                  feishu_url_all.append(result)
            s['feishu_url_all'] = feishu_url_all
        data = json.dumps(s)
        #socket lian jie
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if run_server.strip()=='':
            port = cu.execute('select duan_kou from all_server where ip="%s"' % ('172.16.32.141')).fetchall()[0][0]
            s.connect(("192.168.151.224", port))
        else:
            s.connect((run_server, int(port)))
        #s.connect(("192.168.4.72", 8059))
        # data=data.replace('//','')
        s.send(data.encode())
        s.close()
        return jsonify(statu='scuess')
    return chixuijicheng_run
from app.db_sqlchemy_sqlite.feishu_db import run_jiekou_message_feishu,message_jiekou,locust_run_job,locust_run_before_data
from app import db

def locust_before_data_insert(fun):
    def locust_before_data_insert():
            fun()
            data_json=json.loads(request.get_data())
            print (data_json)
            locust_add_run = locust_run_before_data(run_id=int(data_json['locust_par']['run_id']),locust_id=int(data_json['locust_par']['locust_id']),jiekou_name=data_json['jiekou_name'],run_url=data_json['request_url'],run_header=data_json['request_headers'],run_body=data_json['req'],run_assert=json.dumps(data_json['case_assert']))
            db.session.add(locust_add_run)
            db.session.flush()
            locust_id= locust_add_run.id
            db.session.commit()
            return   jsonify(statu='success')
    return locust_before_data_insert
def run_hualala(fun):
    def zzds():
        fun()
        if 'send_message' in request.form.keys():
            send_message = request.form['send_message']
        if 'today_ci_pic' in list(current_app.config.keys()):
            current_app.config.pop('today_ci_pic')
        if 'seven_ci_pic' in list(current_app.config.keys()):
            current_app.config.pop('seven_ci_pic')
        if 'local_seven_pic' in list(current_app.config.keys()):
            current_app.config.pop('local_seven_pic')
        job=request.form['job'].split('<span class="caret"></span>')[0]
        job=json.dumps({'name':job,'result':''})
        if 'job_id' in list(request.form.keys()):
           job_id=request.form['job_id']
        else:
            job_id=''
        job = json.dumps({'name': job, 'result': '','job_id':job_id})
        email_detail=json.dumps({'send':request.form['send_email_user'],'receive':request.form['email'],'title':request.form['emali_title']})
        #获取文件目录列表
        git_path = [i.strip() for i in request.form['all_path'].split('#') if i.strip() != '']
        git_branch=[i.strip() for i in request.form['all_branch'].split('#') if i.strip() != '']
        db_sqlite = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db_sqlite.cursor()
        #自动分发
        if request.form['run_server']=='自动分发' or   request.form['run_server']=='Automatic distribution':
          if len(cu.execute('select server from dingshi_run  where statu="1"').fetchall())==0:
              run_server = cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
          else:
            xiancheng_detail= [i[0] for i in cu.execute('select server from dingshi_run  where statu="1"').fetchall()  if i in
                               [z[0] for z in cu.execute('select ip from all_server where statu="1" ').fetchall()]]
            #删除在server中不存在的
            if len(xiancheng_detail)==0:
                run_server=cu.execute('select ip from all_server where statu="1" ').fetchall()[0][0]
            else:
              all_server = [i[0] for i in cu.execute('select ip from all_server where statu="1" ').fetchall()]
              server_num = {}
              if len(all_server)!=len(list(set(xiancheng_detail))) :
                for i in all_server:
                  if i not in xiancheng_detail   :
                      run_server=i
              else:
                      for k in xiancheng_detail:
                          server_num[k]=xiancheng_detail.count(k)
                      for z in list(server_num.keys()):
                          if server_num[z]==min(server_num.values()):
                              run_server=z
                              break
        else:
            run_server=request.form['run_server']
        #判断web自动化实时运行是否再运行中
        if 'statue' in list(request.form.keys())  and request.form['statue']=='shishi':
            name = cu.execute(
                'select name from user where ip="%s" order by time desc limit 0,1' % (request.headers.get('X-Real-IP'))).fetchall()[
                0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'实时' ) ).fetchall())!=0 and  cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'实时' ) ).fetchall()[0][0]=='1':
                return jsonify(statu='running')
        #判断接口自动化实时运行是否再运行中
        if 'statue' in list(request.form.keys())  and request.form['statue']=='jiekou_shishi':
            name = cu.execute(
                'select name from user where ip like "%s" order by time desc limit 0,1' % ('%' + request.headers.get('X-Real-IP')+ '%')).fetchall()[
                0][0]
            if len(cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'接口实时' ) ).fetchall())!=0 and  cu.execute('select  statu from dingshi_run where name=? and run_time=?',(name,'接口实时' ) ).fetchall()[0][0]=='1':
                return jsonify(statu='running')
        try:
           name=request.form['name']
        except:
            name = cu.execute(
                'select name from user where ip like "%s" order by time desc limit 0,1' % ('%' + request.headers.get('X-Real-IP')+ '%')).fetchall()[
                0][0]
        #请求时间,如果有传递过来run_time则使用传递过来的，如果没有则用当前时间戳
        if 'run_time'  in list(request.form.keys()):
            run_time=request.form['run_time']
        else:
          run_time = str(time.time())
        user_name = [i.strip() for i in request.form['all_name'].split('#') if i.strip() != '']
             #os.popen('git pull http://sunzhen:6551268Sun@' + str(user_name[k]))
        #根据目录copy相应文件到设置的run文件夹下,之前删除以用户名明明的文件夹，
        if 'statu' in request.form and 'dingshi' in request.form['statu']and 'run_statu'  in list(request.form.keys()):
            if 'everyday' not   in request.form['run_statu'].strip():
                 run_time=time.strftime('%Y-%m-%d',time.localtime(time.time())) +'  '+run_time
            if  request.form['statu']=='dingshi':
               all=cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc'  % (name ) ).fetchall()
            elif request.form['statu']=='jiekou_dingshi':
               all=cu.execute('select id from  dingshi_run where name="%s"  and statu in ("0","1","2")order by update_time asc'  % (name ) ).fetchall()
            if len(all)>4:
                for i in all[-4:]:
                         cu.execute('delete from dingshi_run where id=%s '  % (i) )
                         strr='#'+str(all[-1])
                         db.commit()
            try:
                if 'everyday' in request.form['time']:
                    z=time.strftime('%Y-%m-%d', time.localtime(time.time()))+'  '+request.form['time'].split('everyday')[-1].strip()
                    timeArray = time.strptime(z,"%Y-%m-%d %H:%M")
                else:
                  timeArray = time.strptime(request.form['time'].split('：')[-1].strip(), "%Y-%m-%d %H:%M")
                timestamp = time.mktime(timeArray)
            except:
                return jsonify(statu='error')
            if request.form['statu'] == 'dingshi':
               cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),request.form['time'],request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
            elif request.form['statu'] == 'jiekou_dingshi':

                cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                 request.form['time'],
                                                                                                 request.form[
                                                                                                     'all_path'], '0',
                                                                                                 email_detail, '', '{}',
                                                                                                 request.form[
                                                                                                     'all_branch'], job,
                                                                                                 run_server)])

            db_sqlite.commit()
            html='  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td> </tr>'
            if request.form['statu'] == 'dingshi':
                dingshi_detail = [[i[1], i[2], i[4],i[-1]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (name)).fetchall()]
            elif request.form['statu'] == 'jiekou_dingshi':
                dingshi_detail = [[i[1], i[2], i[4], i[-1]] for i in cu.execute(
                    'select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name,'接口%')).fetchall()]
            db_sqlite.close()
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() in ['0','3'] :
                    i[-2] = 'ready'
                elif i[-2].strip() in ['1','4']:
                    i[-2] = 'running'
                elif i[-2].strip() in ['2','5']:
                    i[-2] = 'over'
            s=''
            for i in dingshi_detail:
                s+=html.replace('{{i[4]}}',str(i[4])).replace('{{i[1]}}',i[1]).replace('{{i[2]}}',i[2]).replace('{{i[3]}}',i[3])
            return jsonify(statu="success",html=s)
        if  len(cu.execute('select name from run where name="%s"' % name).fetchall())==0:
            cu.executemany('INSERT INTO  run values (?,?,?,?,?,?,?)',[(1, name,request.headers.get('X-Real-IP'),request.form['all_path'],time.time(), run_time,email_detail)])
            db_sqlite.commit()
        else:
            cu.executemany('update  run  set statu=0,ip=?,mulu=?,time=?,time_run=? ,email=? where name=?', [(request.headers.get('X-Real-IP'),request.form['all_path'],time.time(), run_time, email_detail,name)])
            db_sqlite.commit()
        if 'statu' not in list(request.form.keys()):
            if request.form['statue']=='shishi':
                  if   len(cu.execute('select * from dingshi_run where name="%s"   and run_time="%s"' % (name,'实时')).fetchall())==0:
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)',[( name,time.time(),'实时',request.form['all_path'],'0',email_detail,'','{}',request.form['all_branch'],job,run_server)])
                    db_sqlite.commit()
                  else:
                    cu.executemany('update  dingshi_run  set statu=1,name=?,update_time=?,all_git=?,email=?,git_branch=?,run_result="{}" ,job=?,server=? where name=? and run_time="实时"', [(name,time.time(),request.form['all_path'],email_detail,request.form['all_branch'],job,run_server,name)])
                    db_sqlite.commit()
            elif request.form['statue']=='jiekou_shishi':
                    cu.execute('delete from dingshi_run where run_time="接口实时" and name=? ',(name,))

                    db_sqlite.commit()
                    cu.executemany('INSERT INTO  dingshi_run values (?,?,?,?,?,?,null,?,?,?,?,?)', [(name, time.time(),
                                                                                                     '接口实时',
                                                                                                     request.form[
                                                                                                         'all_path'],
                                                                                                     '0', email_detail,
                                                                                                     '', '{}',
                                                                                                     request.form[
                                                                                                         'all_branch'],
                                                                                                     job, run_server)])
                    db_sqlite.commit()

        #拉下来git代码
        #if 'run_time'  in request.form.keys():
           #run_dir=os.path.join(current_app.config.get('ALLRUN_FILE'),name,str(time.time()))
        if 'statue'  not in list(request.form.keys()):
                    run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name, str(time.time()))
                    try:
                        os.chdir(run_dir)
                    except:
                        if not  os.path.isdir(os.path.dirname(run_dir)):
                            os.mkdir(os.path.dirname(run_dir))
                        os.mkdir(run_dir)
                        os.chdir(run_dir)
                    #在每个目录下面增加构造文件
                    if   'statue'  in list(request.form.keys()) and  request.form['statue']!='jiekou_shishi':
                            open(os.path.join(run_dir, '__init__.py'), 'w').close()
                            for fpathe, dirs, fs in os.walk(run_dir):
                                for f in dirs:
                                    if '.git'!=f.strip() and '.idea'!=f.strip():
                                      open(os.path.join(fpathe, f, '__init__.py'), 'w').close()
                    try:
                       os.chdir(r'C:\\')
                    except:
                      pass
        else:
            run_dir = os.path.join(current_app.config.get('ALLRUN_FILE'), name)
        s={}
        s['name']=name
        b = run_dir.split(os.sep)
        s['run_dir']=run_dir
        if   'statue'  in list(request.form.keys())  and request.form['statue'] != 'jiekou_shishi':
            if  not os.path.isdir(run_dir):
                os.mkdir(run_dir)
            open(os.path.join(run_dir, '__init__.py'), 'w').close()
        if 'statu' in list(request.form.keys()) :
            if  request.form['statu']  in ['dingshi','jiekou_dingshi']:
                 s['id']=request.form['id']
        else:
            if request.form['statue']=='dingshi':
                    id=cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name,'实时')).fetchall()[0][0]
                    s['id']=str(id)
                    if 'locust_par' in request.form.keys() and json.loads(request.form['locust_par']).last_time!='':
                          locust_par = json.loads(request.form['locust_par'])
                    else :
                        locust_par=''
            elif request.form['statue']=='jiekou_shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '接口实时')).fetchall()[0][0]
                s['id'] = str(id)
            elif request.form['statue']=='url_shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '实时')).fetchall()[0][0]
                s['id'] = str(id)
            elif request.form['statue']=='shishi':
                id = cu.execute(
                    'select id from dingshi_run where name="%s" and run_time="%s" ' % (name, '实时')).fetchall()[0][0]
                s['id'] = str(id)
        if run_server.strip()!='':
            port=cu.execute('select duan_kou from all_server where ip="%s"' % (run_server)).fetchall()[0][0]
        db_sqlite.close()
        #发送验证是接口自动化还是url自动化
        if 'statu' in list(request.form.keys()):
             s['statu']=request.form['statu']
        elif 'statue' in list(request.form.keys()):
            s['statu'] = request.form['statue']
        #获取ip地址
        s['server_di'] =current_app.config.get('SERVER_DI')
        s['job_id']=job_id
        #将本地目录转化为网络目录
        #如果不是接口自动化则转为网络目录
        if 'statue'  not  in list(request.form.keys()):
            s['run_dir']=os.path.join(s['server_di'],s['run_dir'].split(os.sep)[-3],s['run_dir'].split(os.sep)[-2],s['run_dir'].split(os.sep)[-1])
        hostname = socket.gethostname()
        # s['server_ip'] = socket.gethostbyname(hostname)
        # s['server_ip']='172.18.29.253'
        if locust_run_job.query.filter_by(run_statu=1).first() == None and 'locust_par' in request.form.keys() and \
             'last_time' in  json.loads(request.form['locust_par']).keys() and  json.loads(request.form['locust_par'])['last_time'] != '':
            delete_lo = locust_run_job.query.filter_by(user_name=name).first()
            if delete_lo != None:
               db.session.delete(delete_lo)
            locust_add_run = locust_run_job(run_id=int(s['id']), run_canshu=request.form['locust_par'],
                                            user_name=name,
                                            run_statu=0, run_begin_time=int(time.time()), run_stop_time=0)
            db.session.add(locust_add_run)
            db.session.flush()
            locust_id= locust_add_run.id
            db.session.commit()
            s['locust_par'] = json.loads(request.form['locust_par'])
            s['locust_par']['locust_id'] = locust_id
            s['locust_par']['run_id'] = int(s['id'])
        else:
            s['locust_par'] = {
                'biingfa': '',
                'add_per_second': '',
                'last_time': ''
            }
        s['server_ip']=run_server
        s['git_path']=git_path
        if 'statue'  in list(request.form.keys()) and request.form['statue']=='url_shishi':
            s['statue']=request.form['statue']
        s['git_branch']=git_branch
        s['email_detail']=email_detail
        s['job']=job
        s['OWN_URL']=current_app.config.get('OWN_URL')
        s['pic_mulu']=current_app.config.get('RESULT_PICT_SAVE')
        #socket lian jie
        if  'statu' in  request.form.keys() and 'jiekou_dingshi'== request.form['statu']:
            dingshi_job_id = request.form['id']
            feishu_url_all = []
            result = run_jiekou_message_feishu.query.filter_by(run_id=int(dingshi_job_id)).first()
            if result!= None:
                for feishu_id in json.loads(result.message_id_list):
                    result_message = json.loads(message_jiekou.query.filter_by(id=feishu_id, ).first().message_detail)
                    result_message['this_case_beizhu'] = result.run_beizhu
                    feishu_url_all.append(result_message)
                s['feishu_url_all'] = feishu_url_all
        if 'send_message' in request.form.keys() and request.form['send_message']!='{}':
            this_message= json.loads(request.form['send_message'])
            add_meesa = run_jiekou_message_feishu(run_id=int(s['id']), type_message=this_message['type'],
                                      message_id_list=json.dumps(this_message['seleect_id']),run_beizhu = this_message['this_case_beizhu'])
            db.session.add(add_meesa)
            db.session.commit()
            feishu_url_all =[]
            for feishu_id in this_message['seleect_id']:
                  result = json.loads(message_jiekou.query.filter_by(id=feishu_id,).first().message_detail)
                  result['this_case_beizhu'] = this_message['this_case_beizhu']
                  feishu_url_all.append(result)
            s['feishu_url_all'] = feishu_url_all
        data = json.dumps(s)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if run_server.strip()=='':
            port = cu.execute('select duan_kou from all_server where ip="%s"' % ('172.16.32.141')).fetchall()[0][0]
            s.connect(("192.168.151.224", port))
        else:
            s.connect((run_server, int(port)))
        s.send(data.encode())
        s.close()
        return jsonify(statu='scuess')
    return zzds
#根据目录运行脚本病返回结果 html
def run_result(path):
    loader = unittest.TestLoader()
    # case_dir = [r'C:\11\HGTP', r'C:\11\2']
    suite1 = unittest.defaultTestLoader.discover(path, pattern="*.py", top_level_dir=r'E:\run_mulu\lakala')
    # suite2 = unittest.TestSuite(unittest.defaultTestLoader.discover(r'C:\22', pattern="test*.py", top_level_dir=None))
    now = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))  # 输出当前时间
    fp = open(r"D:\python text\11.html", 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='用例执行情况', description='报告:')
    runner.run(suite1)
    fp.close()
#运行状态检查
def run_charge(fun):
    def charge():
        fun()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        try:
          name = cu.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        except:
            return jsonify(statu='0')
        statu = cu.execute('select statu from run where name="%s" ' % name).fetchall()[0][0]
        #判断状态如果状态为0，说明已经运行完毕，则发送邮件
        return jsonify(statu=statu)
    return charge


#增加git库备注详细信息
def add_file_detail(func):
    @functools.wraps(func)
    def aa():
      func()
      if request.method=='POST':
        if  request.form['type']=="jiekou":
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        else:
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.execute('update git_detail set detail="%s" where name="%s"  and  submit="%s" ' %(request.form['detail'],request.form['git'],request.form['name']))
        db.commit()
        db.close()
        return jsonify(a='1')
      if request.method == 'GET':
            if request.args.get('type') == "jiekou":
                db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            else:
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            detail=cu.execute('select detail from  git_detail  where name="%s"  and  submit="%s" ' %(request.args.get('git'),request.args.get('name'))).fetchall()[0][0]
            db.commit()
            db.close()
            return jsonify(a=detail)
    return aa



#查看定时运行的结果文件
def dingshi_result(func):
    def aaaa():
      func()
      if request.method=='POST':
        if request.form['type'] == "jiekou":
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        else:
             db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        db.close()
        id=request.form['update_time']
        url = os.path.join(current_app.config.get('RUN_FILE'), name)
        file_name='#'+str(id)
        session['id']=id
        for parent, dirnames, filenames in os.walk(url):
            for filename in filenames:
                if file_name in filename  :
                    path=os.path.join(parent, filename)
                    print(path)
        db.close()
        session[name]=path
        return jsonify(statu='success')
      else:
          if request.args.get('type') == "jiekou":
              db = sqlite3.connect(current_app.config.get('JIE_KOU'))
          else:
              db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
          cu = db.cursor()
          z = cu.execute('select run_result from dingshi_run where id=?',(session['id'], )).fetchall()[0][0]
          z=json.loads(z)
          db.close()
          print((session[name].replace("\\", '/')))
          return render_template('/hualala/pages/test_result.html',time=str(time.time()),z= z)
    return aaaa



#打开定时运行详细页面
def open_dingshi_detail(func):
    def open_dingshi_det():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        html = '  <tr  class="dingshi_detail"    name="{{i[4]}}"><td   >{{i[1]}}</td><td>  {{i[2]}}</td><td>{{i[3]}}</td><td>erere</td></tr>'
        if 'statu' in list(request.form.keys()) and request.form['statu']=='jiekou_dingshi':
              dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
                  'select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name,'接口%')).fetchall()]
              server_di=[i[0] for i in cu.execute(
                      'select server from dingshi_run where name="%s"    and run_time like "%s"  order by update_time desc ' % (name,'接口%')).fetchall()]
        else:
            dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (
                name)).fetchall()]
            server_di = [i[0] for i in cu.execute(
                'select server from dingshi_run where name="%s"    and statu in ("0","1","2")  order by update_time desc ' % (
                name)).fetchall()]
        db.close()
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
            if i[-2].strip() in ('0','3'):
                i[-2] = 'ready'
            elif i[-2].strip() in ('1','4'):
                i[-2] = 'running'
            elif i[-2].strip() in ('2','5'):
                i[-2] = 'over'
            i.append(server_di[k])
        s = ''
        for i in dingshi_detail:
            s += html.replace('{{i[4]}}', str(i[4])).replace('{{i[1]}}', i[1]).replace('{{i[2]}}', i[2]).replace(
                '{{i[3]}}', i[3]).replace('erere',i[5])
        if 'get_type'  in list(request.form.keys()) and request.form['get_type']=='json_detail':
            resp = jsonify(statu="success", detail=dingshi_detail)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
           return jsonify(statu="success", html=s)
    return open_dingshi_det


#更改运行job的状态
def change_run_statu(func):
    def ceshizhon111ag():
        func()
        if 'run_case_type' not in request.form.keys() or request.form['run_case_type']=="git":
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
                cu = db.cursor()
                data='success'
                if request.form['statu']=='running':
                    if 'run_time_type' in request.form.keys() and request.form['run_time_type']=='real_time':
                       cu.execute('update  real_time_run  set statu=1 where id=%s ' % (int(request.form['data'])))
                    else:
                        cu.execute(
                            'update  dingshi_run  set statu=1 where id=%s ' % (int(request.form['data'])))
                elif request.form['statu']=='over':
                    if 'dingshi' in request.form['data']:
                        cu.execute('update  dingshi_run  set statu=2 where id=%s ' % (int(request.form['data'].split('dingshi')[-1])))
                    else:
                        cu.execute(
                            'update  dingshi_run  set statu=2 where id=%s ' % (int(request.form['data'])))
                elif request.form['statu']=='run':
                    cu.execute('update  run  set statu=0 where name="%s" ' % (request.form['data']))
                elif 'job_result' in request.form['statu']:
                    data=json.loads(request.form['data'])
                    job_detail=json.loads(cu.execute('select job from dingshi_run where id=?',(data['id'],)).fetchall()[0][0])
                    job_detail['result']=data['result']['result']
                    cu.execute('update  dingshi_run  set job=? where id=? ',(json.dumps(job_detail),data['id'],))
                elif request.form['statu']=='jekins':
                    data=json.loads(request.form['data'])
                    id=data['job_id']
                    data=cu.execute('select * from   jekins  where id=?',(id,)).fetchall()[0]
                elif request.form['statu']=='end_time':
                    use_data=json.loads(request.form['data'])
                    id=use_data['id']
                    end_time=use_data['end_time']
                    data=json.loads(cu.execute('select job from dingshi_run where id=?',(id,)).fetchall()[0][0])
                    data['end_time']=end_time
                    cu.execute('update  dingshi_run  set job=? where id=? ',
                               (json.dumps(data),int(id)))
                elif request.form['statu']=='email':
                    data=json.loads(request.form['data'])
                    data = cu.execute('select * from fajianren where name="%s" and email_user="%s"' % (data['name'], data['send_email'])).fetchall()[0]
                db.commit()
                db.close()
                return jsonify(data=data)
        else:
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            if request.form['statu'] == 'running':
                if request.form['run_time_type']=='real_time':
                    cu.execute('update  real_time_run  set statu=1 where id=%s ' % (
                        int(request.form['data'])))
                elif request.form['run_time_type']=='task_time':
                    cu.execute('update  timed_tasks  set statu=1 where id=%s ' % (
                        int(request.form['data'])))
            elif request.form['statu'] == 'over':
                if request.form['run_time_type']=='real_time':
                    cu.execute('update  real_time_run  set statu=2,done_time=%s where id=%s ' % (
                        str(time.time()),int(request.form['data'])))
                elif request.form['run_time_type']=='task_time':
                    cu.execute('update  timed_tasks  set statu=2 where id=%s ' % (
                        int(request.form['data'])))
            db.commit()
            db.close()
            return jsonify(statu="success")
    return ceshizhon111ag


#更改服务器host,post为更新host，get为获取hsot
def update_host(func):
    def ceshizonga():
        if request.method=='post':
            func()
            return jsonify(statu='success')
    return ceshizonga