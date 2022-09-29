# -*- coding: utf-8 -*-

from flask import Flask # 引入 flask
from flask import Flask, request, redirect, url_for
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
from sqlalchemy import create_engine
import os
from flask import current_app
import platform
app = Flask(__name__)
# if platform.system()=='Linux':
# 	db_path = r'/root/repo/hgtp_server/sqlite_db'
# else :
#     db_path= r'D:\中源宏一\base_code\sqlite_db'
basedir = os.path.abspath(os.path.dirname(__file__))
parent_path= os.path.dirname(os.path.dirname(basedir))
db_path = os.path.join(parent_path,'sqlite_db')
basedir=os.path.join(db_path,'example.db')
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
db = SQLAlchemy(app)# 实例化一个flask 对象
app.config.from_object('fileconfig')
UPLOAD_FOLDER = r'D:\untitled6\app\Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ basedir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
from app import view
