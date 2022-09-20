# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
import time
from flask_cors import cross_origin
from flask import Blueprint,jsonify,request
import configparser
import requests
import time
import sqlite3
json_tiqu = Blueprint('json_tiqu',__name__)
#第一个为json对象，第二个为要查找的key值，
def get_json_data(json_detail,json_key):
    if json_key=='':
        return jsonify(data=json.dumps(json_detail, sort_keys=True, indent=2,ensure_ascii=False))
    else:
        if type(json_detail) ==dict:
            if list(json_key.keys())[0]  in list(json_detail.keys()):
                json_key[list(json_key.keys())[0]]=json_detail[list(json_key.keys())[0]]
            else:
                for k,i in list(json_detail.items()):
                    if type(i)  not in [str, str]:
                        get_json_data(i,json_key)
        elif type(json_detail)==list:
            for k,i in enumerate(json_detail):
                if type(i) in [list,dict]:
                    get_json_data(i, json_key)
@json_tiqu.route('/json_submit',methods=['POST','GET'])
@cross_origin()
def admin_index():
    try:
        json_detail = json.loads(request.form['json_detail'])
    except:
        return jsonify(data='json字符串格式不对')
    json_key = request.form['json_key']
    if json_key=='':
       return_data=get_json_data(json_detail,json_key)
       return return_data
    else:
        json_key={json_key:''}
        get_json_data(json_detail,json_key)
        try:
            json_key[list(json_key.keys())[0]]=json.loads(list(json_key.values())[0])
        except:
            pass
        if type(json_key[request.form['json_key']]) in [dict,list]:
            json_key=json.dumps(json_key[request.form['json_key']],sort_keys=True,indent=2,ensure_ascii=False)
            return jsonify(data=json_key)
        elif  type(json_key)!=list and json_key[request.form['json_key']]!='':
            json_key=json_key[request.form['json_key']]
            return jsonify(data=json_key)
        else:
            return jsonify(data="未找到key")

def find_json_data(json_detail,find_key,return_list):
        if type(json_detail) ==dict:
            statu=0
            if type(find_key)==list:
                for k,i in enumerate(find_key):
                    if i not in list(json_detail.keys()):
                        statu=1
                        break
                if statu==0:
                    u={}
                    for k, i in enumerate(find_key):
                            u[i]=json_detail[i]
                    return_list.append([u,json.dumps(json_detail, sort_keys=True, indent=2,ensure_ascii=False)])
            elif type(find_key)==dict:
                for k,i in list(find_key.items()):
                    try:
                        i=i.encode('gb2312')
                    except:
                        pass
                    if k not in list(json_detail.keys()) :
                        statu=1
                        break
                    elif json_detail[k]!=i.decode('gb2312')  and i!='':
                        try:
                            i=int(i)
                        except:
                            statu=1
                            break
                        else:
                            if json_detail[k]!=i:
                                statu=1
                                break
                if statu==0:
                    u={}
                    for k,i in list(find_key.items()):
                        u[k]=json_detail[k]
                    return_list.append([u,json.dumps(json_detail, sort_keys=True, indent=2,ensure_ascii=False)])
            for k,i in list(json_detail.items()):
                    if type(i) in [dict,list]:
                        find_json_data(i, find_key,return_list)
        elif type(json_detail)==list:
            for k,i in enumerate(json_detail):
                if type(i) in [list,dict]:
                    find_json_data(i, find_key,return_list)
@json_tiqu.route('/find_submit',methods=['POST','GET'])
@cross_origin()
def find_submit():
    if request.form['json_detail'].strip()=='':
        return jsonify(error="不能为空")
    json_detail=json.loads(request.form['json_detail'])
    find_detail=[ i.split('=') for i in request.form['find_detail'].split(',')]
    for k,i in enumerate(find_detail):
        if len(i)==1:
            find_detail[k].append('')
    find_detail=dict(find_detail)
    z=[]
    if len(find_detail)==0:
       return jsonify(error="未找到key")
    else:
        find_json_data(json_detail,find_detail,z)
        print((111111111111))
        print(z)
        return jsonify(data=z)