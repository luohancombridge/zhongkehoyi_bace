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
from flask import make_response
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
from flask import Blueprint,jsonify,request
# from sql_chemy.example_db import *
from app.sql_chemy.example_db import *
tongji_detail = Blueprint('tongji_detial',__name__)
@tongji_detail.route('/get_run_detial_user',methods=['POST','GET'])
def get_run_detial_user():
    # z=tody_tongji('adf','adf','fadfd','afdf','afdaf','afd','afdafd')
    # db_chemy.session.add(z)
    # db_chemy.session.commit()
    # time_tody=time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # s=tody_tongji.query.filter_by(riqi !=time_tody).all()
    # db_chemy.session.delete(s)
    # db.session.commit()
    # admin = tody_tongji.query.filter_by(name="adf",riqi="4444").all()
    # # admin=tody_tongji.query.all()
    all_db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    all_cu = all_db.cursor()
    time_tody = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    all_cu.execute('delete from tody_tongji where riqi !="%s"' % time_tody)
    all_data=all_cu.execute("select * from tody_tongji group by name")
    all_db.commit()
    all_data=all_cu.execute('select user_team,count(jiekou_name),sum(case_num),sum(pass_num),sum(fail_num),sum(jiekou_num),count(name) from tody_tongji group by user_team').fetchall()
    all_team=[ i[0]  for i in  all_cu.execute('select distinct(team) from user_team').fetchall()]
    for k,i in enumerate(all_data):
        all_team.remove(all_data[k][0])
        all_data[k]=list(all_data[k])
        all_num=int(all_data[k][3])+int(all_data[k][4])
        pass_baifenbi=str(int(all_data[k][3])/float(all_num)*100)[:3]+'%'
        all_data[k].append(pass_baifenbi)
    for i in all_team:
        all_data.append([i,0,0,0,0,0,0])
    all_db.close()
    return render_template('/hualala/jiekou_test/tody_tongji.html',all_data=all_data)
#??????????????????
@tongji_detail.route('/return_pic',methods=['POST','GET'])
def return_tongji_pic():
    dir=request.args.get('dir')
    file_name=request.args.get('file')
    response = make_response(
        send_from_directory(dir,file_name, as_attachment=True))
    return response

