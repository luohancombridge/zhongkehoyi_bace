# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
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
def chixujicheng_detaiee(func):
    def chixujicheng_detaiee():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        name = cu.execute(
            'select name from user where ip like "%{a}%" order by time desc limit 0,1'.format(a=request.headers.get('X-Real-IP'))).fetchall()
        if len(name) == 0:
            return redirect(url_for('login_new'))
        else:
            name = name[0][0]
        git_detail = [list(i) for i in cu_jiekou.execute('select * from git_detail  ').fetchall()]
        team_detail = [i[0] for i in cu.execute('select team from team').fetchall()]
        team_detail.append('其他')
        for i in git_detail:
            i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
        email_detail = [i for i in
                        cu.execute('select address,beizhu from email_address where user="%s"' % (name)).fetchall()]
        fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
        dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
            'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (
                name)).fetchall()]
        jobs = [[i[4], i[6]] for i in db.execute('select * from jekins ').fetchall()]
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
            if i[-2].strip() == '0':
                i[-2] = 'ready'
            elif i[-2].strip() == '1':
                i[-2] = 'running'
            elif i[-2].strip() == '2':
                i[-2] = 'done'
            if 'everyday'  in i[2]:
                i[2]=i[2].split('everyday')
                i[2][0]="everyday"
            else:
                i[2] = i[2].split(' ')[-1:]
                i[2].insert(0,'only once')
        time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
        server_detail = [i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall()]
        db.close()
        db_jeikou.close()
        return jsonify(git_detail=git_detail, email_detail=email_detail,
                               time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs,
                               server_detail=server_detail, user_name=name, team_detail=team_detail)
    return chixujicheng_detaiee

def chongou_test(func):
    def chongou_test():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu_jiekou = db_jeikou.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
        if len(name) == 0:
            return redirect(url_for('login_new'))
        else:
            name = name[0][0]
        if request.method == 'GET':
            git_detail = [list(i) for i in cu_jiekou.execute('select * from git_detail  ').fetchall()]
            team_detail = [i[0] for i in cu.execute('select team from team').fetchall()]
            team_detail.append('其他')
            for i in git_detail:
                i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
            email_detail = [i for i in
                            cu.execute('select address,beizhu from email_address where user="%s"' % (name)).fetchall()]
            fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
            dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (
                    name)).fetchall()]
            jobs = [[i[4], i[6]] for i in db.execute('select * from jekins ').fetchall()]
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() == '0':
                    i[-2] = 'ready'
                elif i[-2].strip() == '1':
                    i[-2] = 'running'
                elif i[-2].strip() == '2':
                    i[-2] = 'done'
                if 'everyday'  in i[2]:
                    i[2]=i[2].split('everyday')
                    i[2][0]="everyday"
                else:
                    i[2] = i[2].split(' ')[-1:]
                    i[2].insert(0,'only once')
            time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
            server_detail = [i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall()]
            db.close()
            db_jeikou.close()
            return render_template('/hualala/pages/chonggou_second.html', git_detail=git_detail, email_detail=email_detail,
                                   time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs,
                                   server_detail=server_detail, user_name=name, team_detail=team_detail,shishi_id=id)
        else:
            git_url = request.form['git'].strip()
            git_beizhu = request.form['beizu'].strip()
            git_branch = request.form['branch'].strip()
            if git_url.strip() != '' and git_beizhu.strip() != '':
                cu_jiekou.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)',
                                      [(git_url, git_beizhu, name, str(time.time()), '', git_branch)])
            # 向ci同级表中插入数据
            timeStamp = time.time()
            timeArray = time.localtime(timeStamp)
            chushi_date = time.strftime("%Y-%m-%d", timeArray)
            if len(cu.execute('select * from ci_tongji where git_url=? and time=?',
                              (git_url, chushi_date,)).fetchall()) == 0:
                user_number = 0
                cishu = 0
                fail_case_num = json.dumps({name: 0})
                pass_case_num = json.dumps({name: 0})
                cu.executemany('INSERT INTO ci_tongji VALUES (null,?,?,?,?,?,?,?,?)',
                               [(name, git_url, user_number, cishu, fail_case_num, pass_case_num, chushi_date,
                                 git_branch)])
            else:
                cu.execute('UPDATE ci_tongji SET submiter_user=? WHERE git_url=?',
                           (name, git_url))
            db_jeikou.commit()
            db_jeikou.close()
            db.commit()
            db.close()
            return jsonify(a='1')

        # return render_template('/hualala/pages/jiekou_git_chonggou.html')
    return chongou_test


#获取运行状态，返回第一个参数id，第二个参数 ，值
#打开定时运行详细页面
def new_get_run_statu(func):
    def new_get_run_statu():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        sql_ata= 'select name from user where ip  like "%{a}%" order  by time desc limit 0,1 '.format(a=request.headers.get('X-Real-IP'))
        if 'user_name' in request.form.keys():
            name = request.form['user_name']
        else:
            name = cu.execute(sql_ata).fetchall()[0][0]
        if 'statu' in list(request.form.keys()) and request.form['statu']=='jiekou_dingshi':
              dingshi_detail = [[ i[4], i[6]] for i in cu.execute(
                  'select * from dingshi_run where name="%s" and run_time like "%s" order by update_time desc ' % (name,'接口%')).fetchall()]
              server_di=[i[0] for i in cu.execute(
                      'select server from dingshi_run where name="%s"    and run_time like "%s"  order by update_time desc ' % (name,'接口%')).fetchall()]
        else:
            dingshi_detail = [[i[4], i[6]] for i in cu.execute(
                'select * from dingshi_run where name="%s" and statu in ("0","1","2") order by update_time desc ' % (
                name)).fetchall()]
            server_di = [i[0] for i in cu.execute(
                'select server from dingshi_run where name="%s"    and statu in ("0","1","2")  order by update_time desc ' % (
                name)).fetchall()]
        shishi_statu=[[i[4],i[6]] for i in cu.execute(
            'select * from dingshi_run where run_time="%s" and name="%s" ' % (
            '接口实时',name)).fetchall()]
        db.close()
        for k, i in enumerate(dingshi_detail):
            if i[-2].strip() in ('0','3'):
                i[-2] = 'ready'
            elif i[-2].strip() in ('1','4'):
                i[-2] = 'running'
            elif i[-2].strip() in ('2','5'):
                i[-2] = 'done'
        return jsonify(statu="success", all_data=dingshi_detail,shishi_statu=shishi_statu)
    return new_get_run_statu

def git_bianji(func):
    def git_bianji():
        db_comen = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu_cummen = db_comen.cursor()
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        git_name=request.form['git_name']
        git_yewu=request.form['git_yewu']
        git_fenzhi=request.form['git_fenzhi']
        old_git_name=request.form['old_git_name']
        old_git_fenzhi=request.form['old_git_fenzhi']
        name = cu_cummen.execute(
            'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get(
                'X-Real-IP')).fetchall()[0][0]
        db_comen.close()
        cu.execute('UPDATE git_detail SET name=?,beizhu=?,submit=?,time=?,branch=? WHERE name=? and branch=?',(git_name,git_yewu,name,time.time(),git_fenzhi,old_git_name,old_git_fenzhi))
        db.commit()
        db.close()
        return jsonify(statu='success')
    return git_bianji

#获取任务详情
def  get_renwu_detail(func):
    def get_renwu_detail():
        func()
        run_id=request.form['run_id']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        renwu_detail = cu.execute(
            'select * from dingshi_run where id="%s" ' % str(run_id) ).fetchall()[0]
        db.close()
        create_time=time.strftime("%Y--%m--%d", time.localtime(float(renwu_detail[1])))
        send_email = json.loads(renwu_detail[5])['send']
        if '接口实时' not in renwu_detail[2]:
            run_type=renwu_detail[2].split('：')[1]
        else:
            run_type = renwu_detail[2]
        all_git=[i for i in renwu_detail[3].split('#') if i.strip()!='']
        receive_email=[i for i in json.loads(renwu_detail[5])['receive'].split('#') if i.strip()!='']
        if len(receive_email)==0:
            receive_email=['无']
        if '接口实时' not in renwu_detail[2]:
              last_run_time = renwu_detail[7]
        else:
            last_run_time=time.strftime("%Y--%m--%d:%H-%M", time.localtime(float(renwu_detail[1])))
        all_branch =  [i for i in renwu_detail[9].split('#') if i.strip()!='']
        all_git=[ i+'  :  ' + all_branch[k] for k,i in enumerate(all_git) if i.strip()!='']
        resp= jsonify(create_time=create_time,run_type=run_type,all_git=all_git,receive_email=receive_email,
                       last_run_time=last_run_time,send_email=send_email)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return get_renwu_detail
