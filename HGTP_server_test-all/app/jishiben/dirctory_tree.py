# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import redis
import sys
import os
import json
import demjson
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from app.directory_tree.db_case_run import *
import chardet
import xlrd
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
import  pymysql
from app.jishiben.db_case_run import *
jishiben = Blueprint('jishiben',__name__)
@jishiben.route('/getall_biaoqian',methods=['POST','GET'])
@cross_origin()
@addbiaoqian
def getall_biaoqian():
    pass

@jishiben.route('/get_all_biaoqian',methods=['POST','GET'])
@cross_origin()
@get_all_biaoqian
def get_all_biaoqian():
    pass


@jishiben.route('/delete_biaoqian',methods=['POST','GET'])
@cross_origin()
@delete_biaoqian
def delete_biaoqian():
    pass


@jishiben.route('/getall_xiangmu',methods=['POST','GET'])
@cross_origin()
@addxiangmu
def addxiangmu():
    pass

@jishiben.route('/get_all_xiangmu',methods=['POST','GET'])
@cross_origin()
@get_all_xiangmu
def get_all_xiangmu():
    pass


@jishiben.route('/delete_xiangmu',methods=['POST','GET'])
@cross_origin()
@delete_xiangmu
def delete_xiangmu():
    pass

@jishiben.route('/message_add',methods=['POST','GET'])
@cross_origin()
@message_add
def message_add():
    pass

@jishiben.route('/message_sousuo',methods=['POST','GET'])
@cross_origin()
@message_sousuo
def message_sousuo():
    pass



@jishiben.route('/message_biaoqianqiehuan',methods=['POST','GET'])
@cross_origin()
@message_biaoqianqiehuan
def message_biaoqianqiehuan():
    pass

@jishiben.route('/message_change_save',methods=['POST','GET'])
@cross_origin()
@message_change_save
def message_change_save():
    pass


@jishiben.route('/delete_message',methods=['POST','GET'])
@cross_origin()
@delete_message
def delete_message():
    pass


@jishiben.route("/message_file_save", methods=["POST"])
@cross_origin()
def message_file_save():
    data = request.files
    file = data['file']
    # 文件写入磁盘
    basedir = os.path.abspath(os.path.dirname(__file__))
    parent_path = os.path.join(basedir,'file_dir',g.user_name)
    if not os.path.isdir(parent_path):
        os.mkdir(parent_path)
    file_name = str(int(time.time())) +'__'+ file.filename
    file.save(os.path.join(parent_path,file_name))
    return jsonify(statu='success',url=os.path.join(parent_path,file_name))


@jishiben.route('/delete_file',methods=['POST','GET'])
@cross_origin()
@delete_file
def delete_file():
    pass


@jishiben.route('/donwnload_file/<string:path>',methods=['POST','GET'])
@cross_origin()
def donwnload_file(path):
    basedir = os.path.abspath(os.path.dirname(__file__))
    all_path = os.path.join(basedir,'file_dir',g.user_name)
    response = make_response(
        send_from_directory(all_path, path.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(path.split('__')[-1].encode().decode('latin-1'))
    return response