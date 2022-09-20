# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'

import sys
import os
import json
import demjson
import chardet
import xlrd
import hashlib
import socket
import time
from flask import Blueprint, jsonify, request, send_from_directory
import requests
from configparser import ConfigParser
import time
import sqlite3
from flask import Flask, g
import selenium
from flask_cors import *
from flask import current_app, session
from flask import make_response
import redis
import sys
from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
from sqlalchemy import create_engine
from app.db_sqlchemy_sqlite.feishu_db import run_jiekou_message_feishu, message_jiekou, locust_run_job, \
    locust_run_before_data


def donwn_tikuaifen_all_data(func):
    def donwn_tikuaifen_all_data():
        if 'win' in sys.platform:
            fn = getattr(sys.modules['__main__'], '__file__')
            root_path = os.path.abspath(os.path.dirname(fn))
            file_path = os.path.join(root_path, 'kaoshifenxi_tikuai')
        else:
            fn = getattr(sys.modules['__main__'], '__file__')
            root_path = os.path.abspath(os.path.dirname(fn))
            file_path = os.path.join(root_path, 'kaoshifenxi_tikuai')
            x = os.system('zip -r ' + os.path.join(root_path, 'xuanke_downd.zip ') + file_path)
            print('zip -r ' + os.path.join(root_path, 'xuanke_downd.zip') + file_path)
            print(x)
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        response = make_response(
            send_from_directory(root_path, 'xuanke_downd.zip', as_attachment=True))
        return response

    return donwn_tikuaifen_all_data


def xiaofentikui_def(func):
    def xiaofentikui_def():
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        patr_d = r'D:\中源宏一\base_code\test_backstage\HGTP_server_test-all\app\static'
        response = make_response(
            send_from_directory(patr_d, 'tikuaifen.xlsx', as_attachment=True))
        return response

    return xiaofentikui_def


def get_kaoshi_list_def(func):
    def get_kaoshi_list_def():
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if not r.get('return_Data'):
            return jsonify(statu='error', detail='没有数据')
        else:
            this_dict = json.loads(r.get('return_Data'))
            return jsonify(statu='success', detail=list(this_dict.keys()))

    return get_kaoshi_list_def


def get_job_detail_vue_def(func):
    def get_job_detail_vue_def():
        db_jiekou = sqlite3.connect(current_app.config.get('JIE_KOU'))
        db_common = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu_jiekou = db_jiekou.cursor()
        cu_common = db_common.cursor()
        run_id = request.args.get('job_id')
        sql_data= 'select run_time from dingshi_run where id=%s ' % (
                str(run_id))
        print (sql_data)
        dingshi_detail = cu_common.execute(
            'select run_time from dingshi_run where id=%s ' % (
                str(run_id))).fetchall()[0][0]
        if 'everyday'in dingshi_detail:
            run_type="每日"
            run_time = dingshi_detail.strip().split(' ')[-1].split('everyday')[-1]
        else :
            run_type= "今日"
            run_time = dingshi_detail.strip().split(' ')[-1]
        this_job_detail = run_jiekou_message_feishu.query.filter_by(run_id=run_id, ).first().run_beizhu
        return jsonify(statu='success', message_title=this_job_detail,run_time=run_time,run_type=run_type,)

    return get_job_detail_vue_def


def login_new_ivew(func):
    def login_new_ivew():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        all_req_data = json.loads(request.get_data())
        ip = request.headers.get('X-Real-IP')
        name = all_req_data['userName']
        passs = all_req_data['password']
        token = all_req_data['login_token']
        h1 = hashlib.md5()
        h1.update(ip.encode(encoding='utf-8'))
        return_token = h1.hexdigest()
        cu.executemany('update  user  set ip="" where ip  like ?', (ip + '##' + '%'))
        db.commit()
        md5_token = ip + '##' + return_token
        user_check = cu.execute('select * from user where name="%s" and pass="%s" ' % (name, passs)).fetchall()
        if len(user_check) == 0:
            return jsonify(statu='error', detail='用户名或者密码错误')
        if len(user_check) != 0 and token.strip() == '':
            cu.executemany('update  user  set time=? ,ip=? where name=?', [(time.time(), md5_token, name)])
            db.commit()
            response = make_response(jsonify(login="success", token=return_token))
            db.close()
            return response
        elif user_check[0][-1] == None:
            db.commit()
            response = make_response(jsonify(login="success", token=return_token))
            db.close()
            return response
        elif len(user_check) != 0 and token.strip != '':
            if token.strip() == user_check[0][-1].strip():
                response = make_response(jsonify(login="success", token=return_token))
                db.close()
                return response
        else:
            response = make_response(jsonify(login="fail"))
            db.close()
            return response

    return login_new_ivew


def getuser_info(func):
    def getuser_info():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        ip = request.headers.get('X-Real-IP')
        token = request.args.get('token')
        user_check = cu.execute('select * from user where ip like "%s" ' % ('%' + token)).fetchall()
        if len(user_check) != 0:
            data = {
                "status": "success",
                "name": list(user_check[0]),
                "user_id": "1",
                "access": ["super_admin", "admin"],
                "token": token,
                "avatar": "https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png"
            }
        else:
            data = {
                "status": "success",
                "name": '',
                "user_id": "1",
                "access": [],
                "token": '',
                "avatar": "https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png"
            }
        db.close()
        return jsonify(data)

    return getuser_info


def get_banben_detail(func):
    def get_banben_detail():
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        a = [list(i) for i in cu.execute('select * from version_detail ').fetchall()]
        for k, i in enumerate(a):
            z = cu.execute('select bus_name,id from bus_detail where id={}'.format(int(i[2]))).fetchall()[0]
            a[k] += z
            a[k][4] = time.strftime("%Y-%m-%d", time.localtime(int(a[k][4])))
            z = cu.execute('select count(*)  from case_detail where version_id=%s' % (str(i[0]))).fetchall()[0][0]
            a[k].append(z)
            z = cu.execute('select count(*)  from interface_detail where version_id=%s' % (str(i[0]))).fetchall()[0][0]
            a[k].append(z)
        b = [list(i) for i in cu.execute('select * from bus_detail ').fetchall()]
        mulu_all = {}
        all_ca = {}
        if len(a) != 0:
            all_ca = cu.execute('select *  from catalog_detail where version_id=%s' % (str(i[0]))).fetchall()
            for i in all_ca:
                if i[2] not in mulu_all.keys():
                    mulu_all[i[2]] = [[i[0], i[3]]]
                else:
                    mulu_all[i[2]].append([i[0], i[3]])
        db.close()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        super_user = current_app.config.get('DB_JURISDICITION').split(',')
        all_user = [i[0] for i in cu.execute('select name from user').fetchall() if i[0] not in super_user]
        all_user.sort(key=lambda i: len(i), reverse=True)
        db.close()
        return jsonify(mulu_all=mulu_all, all_data=a, bus_data=b, all_user=all_user, all_ca=all_ca)

    return get_banben_detail


def add_dingding_token(func):
    def add_dingding_token():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        all_data = json.loads(request.get_data())
        token_name = all_data['name']
        token_data = all_data['token_dingding']
        user_name = all_data['userName']
        if len(cu.execute('select * from dingding_token where token = "%s"' % (token_data)).fetchall()) > 0:
            return jsonify(statu="fail", detail="token、重复")
        else:
            sql = "insert into dingding_token values(null,'%s','%s','%s','%s')" % (
                token_name, token_data, user_name[0], str(int(time.time())))
            cu.execute(sql)
            db.commit()
        db.close()
        return jsonify(statu="success")

    return add_dingding_token


def tongbushuju_test(func):
    def tongbushuju_test():
        path1 = '/wl/exam-databoard/exam/dashboard/sync/data/syncExamBusinessData'
        # 不区分文理
        path2 = '/wl/exam-databoard/exam/dashboard/sync/data/publishReportWl'
        # 区分文理
        path2 = '/wl/exam-databoard/exam/dashboard/sync/data/publishReport'
        data = {
            "examId": 1901882224386048,
            "syncType": 1
        }
        all_data = request.get_json()['request_json']
        qufenwenli = all_data['qufenwenli']
        if qufenwenli == 'qufen':
            path2 = '/wl/exam-databoard/exam/dashboard/sync/data/publishReport'
        else:
            path2 = '/wl/exam-databoard/exam/dashboard/sync/data/publishReportWl'
        tongbu_type = int(all_data['tongbu_type'])
        type_huanjing = all_data['type_huanjing']
        examid = all_data['examid']
        if type_huanjing == 'test':
            host = 'https://qc-bxlm.zkhyedu.com'
        else:
            host = 'https://wz.zkhyedu.com'
        data = {
            "examId": examid,
            "syncType": tongbu_type
        }
        response = requests.post(host + path1, data=data)
        response_returne_first = json.loads(response.text)
        data = {
            "examId": examid,
            "syncType": tongbu_type,
            'zeroFlag': True
        }
        response = requests.post(host + path2, data=data)
        response_returne_second = json.loads(response.text)
        # response_returne_first={"code":0,"data":False,"message":"success"}
        # response_returne_second={"code":0,"data":False,"message":"success"}
        print(json.dumps(response_returne_first, sort_keys=True, indent=2))
        return jsonify(statu="success",
                       response_returne_first=json.dumps(response_returne_first, sort_keys=True, indent=2),
                       response_returne_second=json.dumps(response_returne_second, sort_keys=True, indent=2))

    return tongbushuju_test
