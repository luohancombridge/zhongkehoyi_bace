# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket

import os
import json
import urllib2
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
import requests

def jemter_add_linux(func):
    def jemter_add_linux():
        func()
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        if len(cu.execute('select * from linux_detail where ip="%s"' % (request.form['ip'])).fetchall())>0:
            db.close()
            resp = jsonify(statu=u'重复')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            cu.executemany('INSERT INTO  linux_detail values (null,?,?,?,?,?,?,?)', [(request.form['beizhu'],
                                                                             request.form['ip'],
                                                                             request.form['port'],
                                                                             request.form['name'],
                                                                            request.form['password'],'stop','none'
                                                                                )])
            db.commit()
            db.close()
            resp = jsonify(statu="success")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    return jemter_add_linux


def jemter_get_all_linux(func):
    def jemter_get_all_linux():
        func()
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        linux_detail=cu.execute('select * from linux_detail').fetchall()
        db.commit()
        db.close()
        resp = jsonify(linux_detail=linux_detail)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return jemter_get_all_linux

def delete_simple_linux(func):
    def delete_simple_linux():
        func()
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        ip_add=request.form['ip']
        cu.execute('delete  from linux_detail  where ip="%s"' % (ip_add)).fetchall()
        db.commit()
        db.close()
        resp = jsonify(statu="success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return delete_simple_linux

def run_linux(func):
    def run_linux():
        func()
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        request_data={}
        for i in json.loads(request.form['all_ip']):
            cu.executemany('update  linux_detail  set run_statu=?,last_run_start_time=? where ip=?', [('runing',str(time.time()),i)])
            this_detail=cu.execute('select * from linux_detail where ip="%s"' %(i)).fetchall()[0]
            request_data[i] = {"username": this_detail[4], "port": this_detail[3], "password": this_detail[5]}
        db.commit()
        db.close()
        url = 'http://'+current_app.config.get('JMETER_IP')+'/nmon/1001'
        headers = {'content-type': "application/json", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
        response = requests.post(url, data=json.dumps(request_data))
        resp = jsonify(statu=json.loads(response.text)['msg'])
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return run_linux

def bianji_linux(func):
    def bianji_linux():
        func()
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        type_run=request.form['type']
        if type_run=='open':
            ip_add = request.form['ip']
            linux_detail=cu.execute('select * from linux_detail where ip="%s"' % (ip_add)).fetchall()[0]
            db.close()
            resp = jsonify(detail=linux_detail)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return respAX
        elif type_run=='save':
            sql_id=request.form['sql_id']
            linux_name=request.form['linux_name']
            ip_add = request.form['ip_add']
            port = request.form['port']
            server_nam = request.form['server_nam']
            pass_word = request.form['pass_word']
            cu.executemany('update  linux_detail  set beizhu=?,ip=?,port=?,name=?,password=? where id=?', [(linux_name,ip_add,port,server_nam,pass_word,sql_id)])
            db.commit()
            db.close()
            resp = jsonify(statu="success")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    return bianji_linux

def stop_run_linux(func):
    def stop_run_linux():
        func()
        url = 'http://'+current_app.config.get('JMETER_IP')+'/nmon/1002'
        db = sqlite3.connect(current_app.config.get('JMETER_LOG'))
        cu = db.cursor()
        request_data = {}
        for i in json.loads(request.form['ip']):
            cu.executemany('update  linux_detail  set run_statu=? where ip=?', [('stop',i)])
            this_detail = cu.execute('select * from linux_detail where ip="%s"' % (i)).fetchall()[0]
            request_data[i] = {"username": this_detail[4], "port": this_detail[3], "password": this_detail[5]}
        db.commit()
        db.close()
        response = requests.post(url, data=json.dumps(request_data))
        if u'成功'  in response.text:
           resp = jsonify(statu='success')
        print jsonify
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return stop_run_linux