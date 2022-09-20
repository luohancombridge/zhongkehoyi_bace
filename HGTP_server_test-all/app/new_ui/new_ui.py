# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
import time
from flask import Blueprint,jsonify,request
import requests
import time
import sqlite3
from flask import Flask, g
from flask_cors import *
from flask import current_app,session
new_ui = Blueprint('new_ui',__name__)
#增加节点
@new_ui.route('/ui_reslut_insert',methods=['POST','GET'])
@cross_origin()
def get_tree():
    db_mulu=current_app.config.get('DB_DIZHI')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = g.db.cursor()

    cu.execute('insert into run_detail values (?,?,?,?,?,?,?,?,?,null)',
                   (request.form['job_id'], str(time.time()), str(time.time()), request.form['def_name'], request.form['class_name'], 'success', request.form['output'],
                    request.form['class_doc'], request.form['def_doc']))
    cu.commit()

    cu.commit()
    cu.close()
    return jsonify(statu='success')
#查询节点
