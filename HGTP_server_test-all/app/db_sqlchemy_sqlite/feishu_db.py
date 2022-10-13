from flask import Blueprint, g, jsonify
import flask
import sqlite3
import datetime
import json
from flask import current_app, session
from flask import Flask # 引入 flask
from flask import Flask, request, redirect, url_for
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
# from celery import Celery
from sqlalchemy import create_engine
import os
from flask import current_app
from app import db
class message_jiekou(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    type_message = db.Column(db.String(50))
    message_detail = db.Column(db.String(200))
    def __repr__(self):
        return '<User %r>' % self.name

class run_jiekou_message_feishu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.INT)
    type_message = db.Column(db.String(50))
    message_id_list = db.Column(db.String(200))
    run_beizhu = db.Column(db.String(200))
    def __repr__(self):
        return '<User %r>' % str(self.run_id)
class locust_run_job(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    run_id = db.Column(db.INT)  #run_job 的id
    run_canshu = db.Column(db.String(100))  #参数json， 如并发量，加压时间，每秒加压数量
    user_name = db.Column(db.String(200))  #用户名
    run_statu = db.Column(db.String(200))  #0为创建成功未运行，1为运行中，2为运行结束
    run_begin_time =  db.Column(db.INT)  #开始运行时间
    run_stop_time = db.Column(db.INT)  # 结束运行时间
    def __repr__(self):
        return '<User %r>' % str(self.run_id)

class locust_run_before_data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    locust_id = db.Column(db.INT)
    run_id = db.Column(db.INT)
    jiekou_name = db.Column(db.String(100))
    run_url = db.Column(db.String(200))
    run_header = db.Column(db.String(500))
    run_body = db.Column(db.String(500))
    run_assert = db.Column(db.String(500))
    def __repr__(self):
        return '<User %r>' % str(self.run_id)


class textList(db.Model):
    __tablename__ = 'textList'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120), unique=True)
    biaoqian_type = db.Column(db.String(120), unique=True)
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, name=None,biaoqian_type=None,create_time=None,create_user=None):
        self.name = name
        self.biaoqian_type= biaoqian_type
        self.create_time = create_time
        self.create_user=create_user
    def __repr__(self):
        return '<User %r>' % str(self.name)

class xiangmulist(db.Model):
    __tablename__ = 'xiangmulist'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120), unique=True)
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, name=None,create_time=None,create_user=None):
        self.name = name
        self.create_time = create_time
        self.create_user=create_user
    def __repr__(self):
        return '<User %r>' % str(self.name)


class mesage_detail(db.Model):
    __tablename__ = 'mesage_detail'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    message = db.Column(db.String(1200))
    biaoqian_id=db.Column(db.String(120))
    title = db.Column(db.String(120))
    xiangmu_id=db.Column(db.INT)
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    file_url = db.Column(db.String(400))
    def __init__(self, message=None,biaoqian_id=None,title=None,xiangmu_id=None,create_time=None,create_user=None,file_url = None):
        self.message = message
        self.title = title
        self.biaoqian_id = biaoqian_id
        self.xiangmu_id = xiangmu_id
        self.create_time = create_time
        self.create_user=create_user
        self.file_url = file_url

class zuzhi_jiagou(db.Model):
    __tablename__ = 'zuzhi_jiagou'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(1200))
    parent_id=db.Column(db.INT)
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, name=None,parent_id=None,create_time=None,create_user=None,file_url = None):
        self.name = name
        self.parent_id = parent_id
        self.create_time = create_time
        self.create_user=create_user



class user_team_vue(db.Model):
    __tablename__ = 'user_team_vue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100))
    team = db.Column(db.String(100))
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, id= None,user=None,team=None,create_time=None,create_user=None,):
        self.user = user
        self.team = team
        self.create_time = create_time
        self.create_user = create_user



# class quanxiandian(db.Model):
#     __tablename__ = 'quanxiandian'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     gongneng_name = db.Column(db.String(100))
#     quanxian_name = db.Column(db.String(100))
#     user_list = db.Column(db.String(1000))
#     quanxian_tag = db.Column(db.String(100))
#     beizhu = db.Column(db.String(100))
#     create_time = db.Column(db.String(120))
#     create_user = db.Column(db.String(120))
#     def __init__(self, beizhu = None,gongneng_name= None,quanxian_name=None,user_list=None,quanxian_tag=None,create_time=None,create_user=None):
#         self.gongneng_name = gongneng_name
#         self.beizhu = beizhu
#         self.quanxian_name = quanxian_name
#         self.user_list = user_list
#         self.quanxian_tag = quanxian_tag
#         self.create_time = create_time
#         self.create_user = create_user


class gongnengdian(db.Model):
    __tablename__ = 'gongnengdian'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gongneng_name = db.Column(db.String(100))
    beizhu = db.Column(db.String(100))
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, beizhu = None,gongneng_name= None,create_time=None,create_user=None):
        self.gongneng_name = gongneng_name
        self.beizhu = beizhu
        self.create_time = create_time
        self.create_user = create_user

class quanxiandian(db.Model):
    __tablename__ = 'quanxiandian'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gongnengdianid = db.Column(db.INT)
    detail = db.Column(db.String(100))
    tag = db.Column(db.String(100))
    user_list = db.Column(db.String(100))
    beizhu = db.Column(db.String(200))
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, gongnengdianid = None,detail= None,tag=None,user_list=None,beizhu=None, create_time=None,create_user=None):
        self.beizhu = beizhu
        self.gongnengdianid = gongnengdianid
        self.detail = detail
        self.tag = tag
        self.user_list = user_list
        self.create_time = create_time
        self.create_user = create_user


class xiangmu_xiangmu_list(db.Model):
    __tablename__ = 'xiangmu_xiangmu_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    create_time = db.Column(db.String(120))
    create_user = db.Column(db.String(120))
    def __init__(self, name= None,create_time=None,create_user=None):
        self.name = name
        self.create_time = create_time
        self.create_user = create_user


