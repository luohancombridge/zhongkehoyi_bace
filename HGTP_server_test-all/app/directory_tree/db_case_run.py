# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
import xlrd
import socket
import time
from flask import Blueprint,jsonify,request
import requests
from  configparser  import ConfigParser
import time
import sqlite3
from flask import Flask, g
import selenium
from flask_cors import *
from flask import current_app,session
def case_db_run(func):
    def case_db_run():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        name=g.user_name
        server_ip,server_port=get_run_server(request.form['run_server'],cu)
        db.close()
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        if int(request.form['statue'])==1:
                tongji_shuju=cu.execute('select id, frequency from data_statistics where version_id=%s' % (str(request.form['version_id'])) ).fetchall()
                if len(tongji_shuju)==0:
                    cu.executemany('INSERT INTO data_statistics VALUES (null,?,?,?,?,?,?,?,?)', [
                        (request.form['version_id'], 0,0,0,0,0, time.time(),0)])
                else:
                    tongji_shuju=int(tongji_shuju[0][1])+1
                    cu.execute(
                        'UPDATE data_statistics SET frequency=%s WHERE version_id=%s' %
                        (tongji_shuju,request.form['version_id']))
                db.commit()
                if len(cu.execute('select id from real_time_run where name="{}" and statu=1'.format(name)).fetchall())>0:
                    return jsonify(statu="fail",detail="该用户下有正在运行的case")
                else:
                      all_data=cu.execute('select id from real_time_run where name="{}" order by create_time desc'.format(name)).fetchall()
                      if len(all_data)>=5:
                          cu.execute(
                              'delete from real_time_run where id="{}" '.format(all_data[0]))
                          db.commit()
                      all_job=cu.execute("select id from real_time_run  where name='%s' and version_id='%s' order by create_time " % (g.user_name,request.form['version_id'])).fetchall()
                      if len(all_job)==5:
                          cu.execute('delete from real_time_run where id=%s' % (str(all_job[0][0])))
                      db.commit()
                      cu.executemany('INSERT INTO real_time_run VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?)', [
                          (request.form['interface_id'],request.form['version_id'],server_ip,
                           request.form['email_receiver'],request.form['email_sender'],request.form['emali_title'],
                           request.form['statue'],request.form['jenkins_job'],g.user_name,int(time.time()),'',0)])
                      db.commit()
                      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                      try:
                        s.connect((server_ip, int(server_port)))
                      except:
                          return jsonify(statu="fail",detail="agent连接不上地址："+server_ip)
                      hostname = socket.gethostname()
                      this_run_id=cu.execute('select id from real_time_run where name="{}" and statu=0 order by create_time desc limit 1'.format(name)).fetchall()[0][0]
                      email_detail = json.dumps({'send': request.form['email_sender'], 'receive': request.form['email_receiver'],
                                                 'title': request.form['emali_title']})
                      db.close()
                      email_detail = json.dumps(
                          {'send': '', 'receive': '',
                           "email_pass": '',
                           'title': ''})
                      data={
                          "email_detail":email_detail,
                          "this_run_id":this_run_id,
                          "server_ip":get_host_ip(),
                          "name":name,
                          "interface_id":request.form['interface_id'],
                          "version_id":request.form['version_id'],
                          "run_case_type":"db_case",
                          "run_time":"real_time"
                      }
                      s.send(json.dumps(data).encode())
                      s.close()
                      return jsonify(statu="success",detail='')
        elif int(request.form['statue'])==2:
            tongji_shuju = cu.execute('select id, frequency from data_statistics where version_id=%s' % (
                str(request.form['version_id']))).fetchall()
            if len(tongji_shuju) == 0:
                cu.executemany('INSERT INTO data_statistics VALUES (null,?,?,?,?,?,?,?,?)', [
                    (request.form['version_id'], 0, 0, 0, 0, 0, time.time(), 0)])
            else:
                tongji_shuju = int(tongji_shuju[0][1]) + 1
                cu.execute(
                    'UPDATE data_statistics SET frequency=%s WHERE version_id=%s' %
                    (tongji_shuju, request.form['version_id']))
                db.commit()
            all_data = cu.execute(
                'select * from timed_tasks where id=%s'  % str(request.form['run_id'])).fetchall()[0]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((server_ip, int(server_port)))
            except:
                return jsonify(statu="fail", detail="agent连接不上地址：" + server_ip)
            hostname = socket.gethostname()
            db.close()
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            email_pass=cu.execute('select email_password from fajianren where name="%s" and email_user="%s" ' % (g.user_name,all_data[2])).fetchall()[0][0]
            email_detail = json.dumps(
                {'send': all_data[2], 'receive': all_data[3],
                 "email_pass":email_pass,
                 'title': all_data[4]})
            data = {
                "email_detail":email_detail,
                "this_run_id": int(all_data[0]),
                "server_ip": get_host_ip(),
                "name": name,
                "interface_id":  all_data[5],
                "version_id":  all_data[1],
                "run_case_type": "db_case",
                "run_time": "task_time"
            }
            s.send(json.dumps(data).encode())
            s.close()
            return jsonify(statu="success", detail='')
        db.close()
    return case_db_run
#获取server的ip和端口号
def get_run_server(type_run,cu):
    # 自动分发
    if type_run in ['自动分发',''] :
                run_server = cu.execute('select * from all_server where statu="1" order by num limit 1 ').fetchall()
                return [run_server[0][1],run_server[0][2]]

def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    if ip=='192.168.0.155':
        ip='127.0.0.1'
    ip=request.url.split('http://')[-1].split(':')[0]
    print (22222222222222222222222222222)
    print (ip)
    return ip



