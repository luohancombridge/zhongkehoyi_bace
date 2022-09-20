# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
from flask import make_response
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
from app.sql_chemy.example_db import *
from app.db_sqlchemy_sqlite.feishu_db import *
from app import db
def addbiaoqian(func):
    def addbiassoqsdian():
        func()
        name_biaoqian= request.form['biaoqian_name']
        biaoqian_type = request.form['biaoqian_type']
        message_type_get = request.form['message_type_get']
        if  textList.query.filter_by(name=name_biaoqian).first() != None:
            return jsonify(statu='error',detail='标签名重复')
        else :
            create_time = str(time.time())
            if message_type_get =='message_priv':
               create_user=g.user_name
            else:
                create_user = message_type_get
            user = textList(name=name_biaoqian,biaoqian_type=biaoqian_type,create_time=create_time,create_user=create_user)
            db.session.add(user)
            db.session.flush()
            locust_id = user.id
            db.session.commit()
            return jsonify(a=2)
    return addbiassoqsdian


def get_all_biaoqian(func):
    def get_all_biaoqian():
        func()
        message_type_get = request.args.get('message_type_get')
        all_data=textList.query.all()
        return_data=[]
        for  i in all_data:
            if message_type_get != 'message_priv':
                user_name = message_type_get
            else:
                user_name = g.user_name
            if    i.create_user ==user_name:
                this_data={
                    'biaoqian_type':i.biaoqian_type,
                    "name": i.name,
                    "id": i.id
                }
                return_data.append(this_data)
        return jsonify(statu='success',return_data=return_data)
    return get_all_biaoqian

def delete_biaoqian(func):
    def delete_biaoqian():
        func()
        all_data=request.get_json()['all_id']
        for i in all_data:
            db.session.delete(textList.query.filter_by(id=int(i)).first())
        db.session.commit()
        return jsonify(statu='success')
    return delete_biaoqian


def addxiangmu(func):
    def addxiangmu():
        func()
        name_biaoqian= request.form['biaoqian_name']
        message_type_get =  request.form['message_type_get']
        if  xiangmulist.query.filter_by(name=name_biaoqian).first() != None:
            return jsonify(statu='error',detail='标签名重复')
        else :
            create_time = str(time.time())
            if message_type_get =='message_priv':
               create_user=g.user_name
            else:
                create_user = message_type_get
            user = xiangmulist(name=name_biaoqian,create_time=create_time,create_user=create_user)
            db.session.add(user)
            db.session.flush()
            locust_id = user.id
            db.session.commit()
            return jsonify(a=2)
    return addxiangmu


def get_all_xiangmu(func):
    def get_all_xiangmu():
        func()
        all_data=xiangmulist.query.all()
        if request.args.get('message_type_get')== 'message_priv':
            user_name = g.user_name
        else:
            user_name = request.args.get('message_type_get')
        return_data=[]
        for  i in all_data:
            if i.create_user == user_name:
                this_data={
                    "name": i.name,
                    "id": i.id
                }
                return_data.append(this_data)
        return jsonify(statu='success',return_data=return_data)
    return get_all_xiangmu

def delete_xiangmu(func):
    def delete_xiangmu():
        func()
        all_data=request.get_json()['all_id']
        for i in all_data:
            db.session.delete(xiangmulist.query.filter_by(id=int(i)).first())
        db.session.commit()
        return jsonify(statu='success')
    return delete_xiangmu


def message_add(func):
    def message_add():
        func()
        message_detail = request.get_json()['message_detail']
        message_type_get=  request.get_json()['message_type_get']
        create_time = str(time.time())
        if message_type_get == 'message_priv':
            create_user = g.user_name
        else:
            create_user = message_type_get
        biaoqian_all=json.dumps(message_detail['biaoqian'])
        user = mesage_detail(message=message_detail['detail'], biaoqian_id=biaoqian_all,title=message_detail['title'], xiangmu_id=message_detail['xiangmu'],create_time=create_time, create_user=create_user,
                             file_url = json.dumps(message_detail['file_url']))
        db.session.add(user)
        db.session.flush()
        locust_id = user.id
        db.session.commit()
        return jsonify(statu='success')
    return message_add

def message_sousuo(func):
    def message_sousuo():
        func()
        name_detail=request.get_json()['sousuo_detail']['detail']
        get_alldetail = request.get_json()['sousuo_detail']['message_type_get']
        if get_alldetail == 'message_priv':
            create_user = g.user_name
        else:
            create_user =get_alldetail
        xiangmu_id = int(request.get_json()['sousuo_detail']['xiangmu'])
        all_biaoqian={}
        for i in textList.query.filter_by(create_user=create_user).all():
            all_biaoqian[i.id] = i.name
        this_biaoqian={}
        if name_detail.strip()=='':
            x=mesage_detail.query.filter_by(xiangmu_id=xiangmu_id,create_user=create_user).all()
            all_data={}
            for i in x:
                if i.create_user == create_user:
                        try:
                          json.loads( i.biaoqian_id)
                        except:
                            pass
                        else:
                            for k,z in enumerate( json.loads( i.biaoqian_id)):
                                if z not in this_biaoqian.keys():
                                    this_biaoqian[z] = all_biaoqian[z]
                            this_data={
                                "biaoqian":json.loads(i.biaoqian_id),
                                'message': i.message,
                                'title':i.title,
                                'id':i.id
                            }
                            if i.file_url!=None:
                                this_data['file_url'] = json.loads(i.file_url)
                            else:
                                this_data['file_url'] = []
                            file_name_list={}
                            for k,x in enumerate(this_data['file_url']):
                                if '/' in x :
                                    file_name= x.split('/')[-1]
                                elif '\\' in x:
                                    file_name = x.split('\\')[-1]
                                file_name_list[file_name] = x
                            this_data['file_name_list'] = file_name_list
                            for z in json.loads(i.biaoqian_id):
                                if z not in all_data.keys():
                                    all_data[z]=[]
                                all_data[z].append(this_data)
            print (all_data)
        return jsonify(statu='success',all_biaoqian=all_biaoqian,all_data=all_data)
    return message_sousuo


def message_biaoqianqiehuan(func):
    def message_biaoqianqiehuan():
        func()
        name_detail=request.get_json()['sousuo_detail']
        xiangmu_id = int(request.get_json()['sousuo_detail']['xiangmu'])
        create_user= g.user_name
        x=mesage_detail.query.filter_by(xiangmu_id=xiangmu_id).all()
        all_data={}
        for i in x:
                this_data={
                    "biaoqian":json.loads(i.biaoqian_id),
                    'message': i.message,
                    'title':i.title,
                    'id':i.id
                }
                for z in json.loads(i.biaoqian_id):
                    if z not in all_data.keys():
                        all_data[z]=[]
                    all_data[z].append(this_data)
        return jsonify(statu='success')
        return 2
    return message_biaoqianqiehuan


def message_change_save(func):
    def message_change_save():
        func()
        message_detail = request.get_json()['message_detail']
        create_time = str(time.time())
        create_user = g.user_name
        x=mesage_detail.query.filter_by(id=int(message_detail['id'])).first()
        x.message=message_detail['detail']
        x.biaoqian_id=json.dumps(message_detail['biaoqian'])
        x. title=message_detail['title']
        db.session.commit()
        return jsonify(statu='success')
    return message_change_save

def delete_message(func):
    def delete_message():
        func()
        id=request.get_json()['message_id']
        x = mesage_detail.query.filter_by(id=int(id)).first()
        if x.file_url !=None:
            for k,i in enumerate(json.loads(x.file_url)):
                if os.path.isfile(i):
                    os.remove(i)
        try:
                  db.session.delete(x)
                  db.session.commit()
        except:
            return jsonify(statu='error')
        else:
            return jsonify(statu='success')
    return delete_message


def delete_file(func):
    def delete_file():
        func()
        file_name= request.get_json()['file_name']
        if type(file_name)!=list:
            file_name = json.loads(file_name)
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # parent_path = os.path.join(basedir, 'file_dir', g.user_name)
        # file_path=os.path.join(parent_path, file_name)
        for k,i in enumerate(file_name):
            if os.path.isfile(i):
             os.remove(i)
        return jsonify(statu="success")
    return delete_file


