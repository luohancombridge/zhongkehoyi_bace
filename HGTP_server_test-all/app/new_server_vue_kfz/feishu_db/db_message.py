# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
import xlrd
import hashlib
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
from flask import make_response
from sqlalchemy import or_,and_
from app.db_sqlchemy_sqlite.feishu_db        import *
def add_jiekou_message(func):
    def add_jiekou_message():
        func()
        mesasge_detail={
            "url":request.form['url'],
            'beizhu':request.form['beizhu']
        }
        add_mees = message_jiekou(name=request.form['name'], type_message=request.form['type_message'],message_detail=json.dumps(mesasge_detail))
        db.session.add(add_mees)
        db.session.commit()
        return jsonify(statu='success')
    return add_jiekou_message

def get_jiekou_message(func):
    def get_jiekou_message():
        func()
        # result= message_jiekou.query.filter_by(message_jiekou.name == request.args.get['name'],message_jiekou.type_message==request.args.get['type_message']).first()
        result= message_jiekou.query.filter_by(type_message=request.args.get('type_message'),name= request.args.get('name')).all()
        return_data = []
        for i in result:
            this_data = {}
            this_data['name']= i.name
            this_data['id']= i.id
            if request.args.get('type_message') == 'feishu':
                   this_data['url']=json.loads(i.message_detail)['url']
                   this_data['beizhu'] = json.loads(i.message_detail)['beizhu']
            return_data.append(this_data)
        return jsonify(statu='success',return_data=return_data)
    return get_jiekou_message

def delete_jiekou_message(func):
    def delete_jiekou_message():
        func()
        result= message_jiekou.query.filter_by(type_message=request.args.get('type_message'),id= request.args.get('id')).first()
        db.session.delete(result)
        db.session.commit()
        return jsonify(statu='success')
    return delete_jiekou_message