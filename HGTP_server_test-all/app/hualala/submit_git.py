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
#import HTMLTestRunner
import zipfile
import functools
import chardet
import  subprocess
from concurrent.futures import ThreadPoolExecutor
def  submit_git(func):
    def submit_git1():
        current_app.config['submit_git']=1
        print((1111111111111111111111111111111111111111))
        file = request.files['image1']
        save_mulu=os.path.join(current_app.config.get('GIT_FILE_MULU'),str(time.time()).replace('.',''))
        if not os.path.exists(save_mulu):
            os.makedirs(save_mulu)
        #下载git库
        os.chdir(save_mulu)
        print((9999999999999999999999999999999999999))
        print((request.headers))
        print((request.headers.get('git_address')))
        if 'http' not in request.headers.get('git_address'):
            git_address='http://'+ request.headers.get('git_address').strip()
        else:
            git_address =  request.headers.get('git_address').strip()
        os.popen('git init')
        os.popen('git clone '+git_address)
        #删除git库文件
        path=os.path.join(save_mulu,[i for i in os.listdir(save_mulu) if i!='.git'][0])
        print((9999999999999999999999999999999999999))
        print(path)
        s=[i for i in os.listdir(path) if i!='.git']
        # if len(s)!=0:
        #   path=os.path.join(path,s[0])
        #path=os.path.join(path,[i for i in os.listdir(path) if i!='.git'][0])
        # os.popen('rmdir /s/q' + ' '+path)
        #删除出git外所有文件和目录
        for parent, dirnames, filenamex in os.walk(path):
            # Case1: traversal the directories
            for filename in filenamex:
                if '.git' not in os.path.join(parent, filename):
                    try:
                        os.remove(os.path.join(parent, filename))
                    except:
                        pass
        for parent, dirnames, filenamex in os.walk(path):
            for dirname in dirnames:
                if '.git' not in os.path.join(parent, dirname):
                    try:
                        os.removedirs(os.path.join(parent, dirname))
                    except:
                        pass
        # os.mkdir(path)
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(path, filename))
        except:
            pass
        # executor = ThreadPoolExecutor(1)
        # executor.submit(submit_git_def,os.path.join(path, filename),save_mulu)
        filename=os.path.join(path,filename)
        filedir = path
        executor = ThreadPoolExecutor(1)
        r = zipfile.is_zipfile(filename)
        zip_file = zipfile.ZipFile(filename)
        print((2222222222222222222222222222222))
        print((time.time()))
        for file in zip_file.namelist():
            zip_file.extract(file, os.path.dirname(filename))
        print((time.time()))
        zip_file.close()
        os.remove(os.path.join(path,filename))
        #git 上传
        git_submit_path=os.path.join(save_mulu, [i for i in os.listdir(save_mulu) if i != '.git'][0])
        os.chdir(git_submit_path)
        os.popen('git add .')
        os.popen('git commit -m  server_submit')
        # os.popen('git push -u origin master -f')
        # p = subprocess.Popen('git push -u origin master -f', shell=True, stdout=subprocess.PIPE)

        proc = subprocess.Popen('git push -u origin master -f', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        num=0
        print((777777777777777777777777))
        # for line in iter(proc.stdout.readline, b''):
        #     print line,
        # proc.stdout.close()
        # proc.wait()
        ouput_detail=proc.stdout.read()
        print(ouput_detail)
        print((888888888888888888888))
        os.popen('rmdir /s/q' + ' ' + save_mulu)
        try:
          [shutil.rmtree(os.path.join(current_app.config.get('GIT_FILE_MULU'),i))  for i in os.listdir(current_app.config.get('GIT_FILE_MULU'))]
        except:
            pass
        current_app.config['submit_git'] = 0
        if 'fail' not in ouput_detail and  'Fail' not in ouput_detail:
           return jsonify(statu='success')
        else:
            return jsonify(statu="fail",ouput_detail=ouput_detail)
    return submit_git1


def get_sumint_statu(func):
    def get_sumint_statu():
        func()
        print((888888888888888888888888888888888888888888))
        if 'submit_git'  in list(current_app.config.keys())  and current_app.config['submit_git']==1:
            return jsonify(statu="fail")
        return jsonify(statu="success")
    return get_sumint_statu


def submit_git_def(zip_file,save_mulu):
    r = zipfile.is_zipfile(zip_file)
    zip_file = zipfile.ZipFile(zip_file)
    for file in zip_file.namelist():
        zip_file.extract(file, os.path.dirname(zip_file))
    print((time.time()))
    zip_file.close()
    os.remove(os.path.join(path, zip_file))
    # git 上传
    git_submit_path = os.path.join(save_mulu, [i for i in os.listdir(save_mulu) if i != '.git'][0])
    os.chdir(git_submit_path)
    os.popen('git add .')
    os.popen('git commit -m  server_submit')
    # os.popen('git push -u origin master -f')
    p = subprocess.Popen('git push -u origin master -f', shell=True, stdout=subprocess.PIPE)
    print((666666666666666666666666666666666))
    print((p.stdout.read()))
    out, err = p.communicate()
    print((77777777777777777777777777777777777777777777))
    print(out)
    print((3333333333333333333333333333))
    print(err)
    os.popen('rmdir /s/q' + ' ' + save_mulu)
    try:
        [shutil.rmtree(os.path.join(current_app.config.get('GIT_FILE_MULU'), i)) for i in
         os.listdir(current_app.config.get('GIT_FILE_MULU'))]
    except:
        pass

def do_update():
    time.sleep(3)
    print('start update')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['txt','zip','rar', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

