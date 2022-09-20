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
def add_email(func):
    func()
    def sz():
        name=request.form['name']
        beizhu=request.form['beizhu']
        email=request.form['email']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if len(cu.execute('select * from email_address where user="%s" and address="%s" ' % (name,email)).fetchall())!=0:
            db.close()
            return jsonify(a='2')
        cu.executemany('INSERT INTO email_address VALUES (?,?,?)',
                       [(name,email,beizhu)])
        db.commit()
        db.close()
        html='<tr   name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email" id="%s">delete</button></div></td></tr>'    %(name+'#'+email,email,beizhu,name+'#'+email)
        return jsonify(a='add-success',html=html)
    return sz

def show_email(func):
    func()
    def aaee():
        user = request.form['name']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        emali_list = cu.execute('select address,beizhu from email_address where user="%s"  ' % (user)).fetchall()
        db.close()
        html=''
        for i  in emali_list:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email" id="%s">delete</button></div></td></tr>'    %(user+'#'+i[0],i[0],i[1],user+'#'+i[0])
        return jsonify(a='add-success',html=html,emali_list = emali_list)
    return aaee
def delete_email(func):
    func()
    def aaeea():
        if 'name'  in request.form.keys():
            user = request.form['name']
            address = request.form['email']
        else:
            user, address = request.form['detail'].split('#')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.execute('delete  from email_address where user="%s" and address="%s" ' % (user,address))
        db.commit()
        db.close()
        return jsonify(a='1')
    return aaeea
import requests
from urllib.parse import urlparse
def change_curl(func):
    func()
    def change_curl():
        curl_data=  json.loads(request.get_data())['curl_data']
        request_data = {
            "command": curl_data,
            'target': 'python'
        }
        url = 'https://tool.lu/curl/ajax.html'
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://tool.lu',
            'referer': 'https://tool.lu/curl',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        z = requests.post(url, data=request_data, headers=header)
        if 'code' in json.loads(z.text).keys():
            all_data = json.loads(z.text)['code'].split('response = requests')
            exec(all_data[0])
            if '.post' in all_data[1]:
                method  = 'post'
                if type(locals()['data'])  in [list,dict] :
                    request_type= 'form_data'
                    request_data = locals()['data']
                else:
                    request_type = 'json'
                    try:
                        request_data= json.loads(locals()['data'].replace('^',''))
                    except:
                        request_data = json.loads(locals()['data'].replace('^', '').replace('\\', '"'))
            elif '.get' in all_data[1]:
                method = 'get'
            header= locals()['headers']
            url = urlparse('http'+ all_data[1].split('(')[-1].split(',')[0].split('http')[1])
            if 'https' in all_data[1].split('(')[-1].split(',')[0]:
                netloc = 'https://' + url.netloc
            else:
                netloc = 'http://' + url.netloc
            path = url.path.replace("'",'')
            return jsonify(statu='success',  return_data={"header": header,'url': url,'path':path,'netloc':netloc,'request_data':request_data})
        else:
            return jsonify(statu='fail',detail='解析失败，请检查curl字符串是否正确')

    return change_curl


import smtplib
from email.mime.text import MIMEText
def send_emali(func):
    func()
    def aaddd():
            db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu = db.cursor()
            name = cu.execute(
                'select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[
                0][0]
            email_address=[i for i in cu.execute(
                'select email from run where name="%s" order  by time desc limit 0,1 ' % name).fetchall()[
                0][0].split('##')  if i.strip()!='']
            if len(email_address)==0:
                return jsonify(a='111')
            # 文件名列表
            db.close()
            file_name = []
            for parent, dirnames, filenames in os.walk(os.path.join(current_app.config.get('RUN_FILE'), name)):
                for i in filenames:
                    file_name.append(i)
            url = os.path.join(current_app.config.get('RUN_FILE'), name, sorted(file_name)[-1]).replace("\\", '/')
            print (url)
            content = open(url, 'r').read()
            sender = 'luohancombridge@163.com'
            receiver = email_address
            subject = 'test result'
            smtpserver = 'smtp.163.com'
            username = 'luohancombridge@163.com'
            password = '6551268sunzhen'
            msg = MIMEText(content, 'html', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = 'luohancombridge@163.com'
            msg['To'] = 'luohancombridge@163.com'
            smtp = smtplib.SMTP()
            smtp.connect('smtp.163.com')
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            return jsonify(a='111')
    return aaddd











#增加发件人
def add_fajianren(func):
    def add_fajianren():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.executemany('INSERT INTO  fajianren values (?,?,?,?,null)', [(request.form['email'],
                                                                         request.form['email_password'],
                                                                         request.form['beizhu'],
                                                                         request.form['name'])])
        db.commit()
        id=cu.execute('select id from fajianren where name="%s" order by id desc limit 0,1' % request.form['name']).fetchall()[0][0]
        db.close()
        html='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email_fa" id="fajianren%s">delete</button></div></td></tr>'    %(request.form['name'],request.form['email'],request.form['beizhu'],id)
        return jsonify(a="add-success",html=html)
    return add_fajianren

#显示发件人
def show_fajianren(func):
    def show_fajianren():
        func()
        name=request.args.get('name')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('select email_user,email_detail,name,id from fajianren where name="%s"'%name).fetchall()
        db.close()
        html=''
        for i  in fajian_detail:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_email_fa" id="fajianren%s">delete</button></div></td></tr>'    %(name,i[0],i[1],i[3])
        return jsonify(a="add-success",html=html,fajian_detail = fajian_detail)
    return show_fajianren




#删除发件人
def delete_fajianren(func):
    def delete_fajianren():
        func()
        id=request.args.get('id').split('fajianren')[-1]
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from fajianren where id=%s'% id)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return delete_fajianren



#增加jekins
def add_jekins(func):
    def add_jekins():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.executemany('INSERT INTO  jekins values (?,?,?,?,null,?,?,?)', [(request.form['jekins_user'],
                                                                         request.form['name'],
                                                                         request.form['token'],
                                                                         request.form['job'],
                                                                        request.form['url'],
                                                                        request.form['beizhu'],
                                                                        request.form['canshu']
                                                                            )])
        db.commit()
        id=cu.execute('select id from jekins where name="%s" order by id desc limit 0,1' % request.form['name']).fetchall()[0][0]
        db.close()
        html='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_jekins" id="fajianren%s">delete</button></div></td></tr>'    %(id,request.form['job'],request.form['beizhu'],id)
        return jsonify(a="add-success",html=html)
    return add_jekins



#jekins 列表
def jekins_list(func):
    def jekins_list():
        func()
        name=request.args.get('name')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('select job_name,beizhu,id from jekins ').fetchall()
        tongyong_detail=cu.execute('select user,token_id,url from jekins ').fetchall()
        if len(tongyong_detail)==0:
            tongyong_detail=['','','']
        else:
            tongyong_detail=tongyong_detail[0]
        db.close()
        html=''
        for i  in fajian_detail:
            html +='<tr name="%s"><td>%s</td><td>%s</td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="delete_jekins" >delete</button></div></td><td><div class="btn-group"><button type="button" class="btn btn-default" name ="wirte_jekins" >编辑</button></div></td></tr>'    %(i[2],i[0],i[1])
        #job 名添加进列表中
        tongyong_detail=list(tongyong_detail)
        tongyong_detail.append(fajian_detail[0][0])
        return jsonify(a="add-success",html=html,tongyong_detail=tongyong_detail)
    return jekins_list


#删除jekins
def jekins_delete(func):
    def jekins_delete():
        func()
        id=request.form['id']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from jekins where id=%s'% id)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return jekins_delete



#删除suite
def suite_delete(func):
    def suite_delete():
        func()
        name=request.form['name']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        fajian_detail=cu.execute('delete  from dingshi_run where name="%s"'% name)
        db.commit()
        db.close()
        html=''
        return jsonify(a="delete-success")
    return suite_delete


#操作数据库
def sqlite_exe(func):
    def sqlite_exe():
        func()
        detail=request.form['detail']
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        if 'select' in detail:
            fanhui=json.dumps(cu.execute(detail).fetchall())
        else:
            fanhui=''
        db.commit()
        db.close()
        return jsonify(a="sqllite-success",data=fanhui)
    return sqlite_exe