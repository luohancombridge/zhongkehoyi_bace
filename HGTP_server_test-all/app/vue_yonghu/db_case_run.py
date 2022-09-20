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


def add_uzhi(func):
    def add_uzhi():
        func()
        request_json=request.get_json()['request_data']
        print (request_json)
        user = zuzhi_jiagou(name=request_json['name'], parent_id=request_json['parent_id'], create_time=str(int(time.time())),
                        create_user=g.user_name)
        db.session.add(user)
        db.session.flush()
        locust_id = user.id
        db.session.commit()
        return jsonify(this_id=locust_id)
    return add_uzhi

def get_zuzhi(func):
    def get_zuzhi():
        x = zuzhi_jiagou.query.filter_by().all()
        return_data=[]
        return_list=sorted([[i.id,i.name,i.parent_id] for i in x],key=lambda x:x[2])
        for i in return_list:
            if i[2] == 0:
                return_data.append({
                    'title':i[1],
                    'id':i[0],
                    'children':[],
                    "expand": True,
                    "nodeKey": 0
                })
            else:
                get_this_data(return_data,i)
        func()
        return jsonify(return_data=return_data)
    return get_zuzhi

def get_this_data(yuanshi_data,this_data):
    for k, z in enumerate(yuanshi_data):
        if z['id'] == this_data[2]:
            if 'children' not in yuanshi_data[k].keys():
                yuanshi_data[k]['children'] = []
            else:
                yuanshi_data[k]['children'].append({
                    'title': this_data[1],
                    'id': this_data[0],
                    'children': [],
                    "expand": True,
                })
            break
        else:
            if 'children'  in yuanshi_data[k].keys():
                   get_this_data(yuanshi_data[k]['children'],this_data)

def delete_zuzhi(func):
    def delete_zuzhi():
        func()
        request_data= request.get_json()['request_data']
        print (request_data)
        parentId= request_data['parentId']
        thisDeleteId = request_data['thisDeleteId']
        x = zuzhi_jiagou.query.filter_by(parent_id = thisDeleteId).all()
        if len(x)>0:
           return jsonify(statu='error',detail='请先删除子部门')
        else:
            db.session.delete(zuzhi_jiagou.query.filter_by(id=int(thisDeleteId)).first())
            for i in user_team_vue.query.filter_by().all():
                if int(thisDeleteId) in json.loads(i.team):
                  if len(json.loads(i.team)) ==1:
                      db.session.delete(user_team_vue.query.filter_by(id=i.id).first())
                  else:
                    this_list= json.loads(i.team)
                    this_list.remove(thisDeleteId)
                    print (this_list)
                    i.team = json.dumps(this_list)
                    db.session.add(i)
            db.session.commit()
            return jsonify(statu='success')
    return delete_zuzhi


def get_all_user(func):
    def get_all_user():
        func()
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        request_type = request.args.get('request_type')
        if request_type == 'all':
            x = zuzhi_jiagou.query.filter_by().all()
            return_data = []
            return_list = sorted([[i.id, i.name, i.parent_id] for i in x], key=lambda x: x[2])
            for i in x:
                if i.parent_id==0:
                    base_uzhi= i.name
                    break
            zuzhi_dict={}
            for i in return_list:
                zuzhi_dict[i[0]] = i[1]
            user_detail = [list(i) for i in cu.execute('select user.name,user.pass,user.time,user.statu,user.ip,user_team.team from user LEFT  OUTER JOIN user_team  on user.name=user_team.user ').fetchall()]
            team_user=[i  for i in cu.execute('select team from team ').fetchall()]
            this_zuzhi={}
            for k ,i in enumerate( cu.execute('select * from user_team_vue').fetchall()):
                this_zuzhi[i[1]]=''
                for u,z in enumerate(json.loads(i[2])):
                    if  this_zuzhi[i[1]] =='':
                        this_zuzhi[i[1]] =  zuzhi_dict[z]
                    else:
                         this_zuzhi[i[1]]= this_zuzhi[i[1]] +','+zuzhi_dict[z]
            print (user_detail)
            for k, i in enumerate(user_detail):
                user_detail[k][2] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( float(user_detail[k][2])))
                if  i[0] in this_zuzhi.keys():
                    user_detail[k].append(this_zuzhi[i[0]])
                else:
                    user_detail[k].append('没有分配部门')
            db.close()
            return jsonify( user_detail= user_detail,team_user=team_user)
        elif request_type =='id_data':
            zuzhi_user= cu.execute('select * from user_team_vue').fetchall()
            zuzhi_dict={}
            for i in zuzhi_user:
                zuzhi_dict[i[1]] = json.loads(i[2])
            wuzuzhi_user= cu.execute('select name from user').fetchall()
            return_data={}
            for i in wuzuzhi_user:
                if i[0] not  in zuzhi_dict.keys():
                    zuzhi_dict[i[0]]=[0]
            return jsonify(return_data= zuzhi_dict)
    return get_all_user



def delete_user(func):
    def delete_user():
        func()
        print (request.get_json())
        name = request.get_json()['request_data']['name']
        bumen = request.get_json()['request_data']['bumen']
        db_sql = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db_sql.cursor()
        cu.execute('delete from user where name = "{}"'.format(name))
        cu.execute('delete from user where name = "{}"'.format(name))
        db_sql.commit()
        db_sql.close()
        user_team_vue.query.filter_by(user=name).delete()
        db.session.commit()
        return jsonify(statuss='success')
    return delete_user

def user_zuzhijiagou_change(func):
    def user_zuzhijiagou_change():
        func()
        name= request.get_json()['name']
        old_data=user_team_vue.query.filter_by(user=name).first()
        x = zuzhi_jiagou.query.filter_by().all()
        db_sql = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db_sql.cursor()
        all_user_name = [i[0] for i in cu.execute('select name from user').fetchall()]
        db_sql.close()
        zuzhi_name=[]
        for i in  user_team_vue.query.filter_by().all():
            zuzhi_name.append(i.user)
        return_data = []
        return_list = sorted([[i.id, i.name, i.parent_id] for i in x], key=lambda x: x[2])
        zuzhi_dict = {}
        for k,i in enumerate(return_list):
            if i[1] == '无归属':
                wuguishu_id = i[0]
            zuzhi_dict[i[0]] ={
                'name':i[1],
                'parent_id':i[2]
            }
        for i in all_user_name:
            if i not in zuzhi_name:
                user = user_team_vue(user=i, team=json.dumps([wuguishu_id]), create_time=str(time.time()),
                                     create_user=g.user_name)
                db.session.add(user)
                db.session.flush()
        user_team = []
        for k,i in enumerate(request.get_json()['team']):
            parent_id = zuzhi_dict[i]['parent_id']
            if  parent_id ==0:
                user_team=[i]
                break
            elif parent_id in request.get_json()['team']:
                if parent_id not in user_team:
                   user_team.append(parent_id)
            elif parent_id not  in request.get_json()['team']:
                user_team.append(i)
        if old_data==None:
              user = user_team_vue(user=name,team=json.dumps(user_team),create_time=str(time.time()),create_user = g.user_name)
              db.session.add(user)
              db.session.flush()
        else :
            old_data.team=json.dumps(user_team)
            old_data.create_time = str(time.time())
            old_data.create_user = g.user_name
            db.session.add(old_data)
        db.session.commit()
        return jsonify(status='success')
    return user_zuzhijiagou_change

def change_password(func):
    def change_password():
        func()
        all_data = request.get_json()['request_data']
        if all_data['new_pass'] != all_data['new_pass_again']:
            return jsonify(status='error',detail='密码不一致')
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        cu.execute('update user  set pass = "{}" where name = "{}" '.format(all_data['new_pass'],all_data['name']))
        db.commit()
        db.close()
        return jsonify(status='success')
    return change_password

def get_vip_user(func):
    def get_vip_user():
        func()
        user_list=current_app.config.get('DB_JURISDICITION').split(',')
        if g.user_name in user_list:
            return jsonify(is_vip=True,name= g.user_name)
        else:
            return jsonify(is_vip=False,name= g.user_name)
    return get_vip_user


def add_gongneng(func):
    def add_gongneng():
        func()
        all_data= request.get_json()['request_data']
        gongnengming=all_data['name']
        beizhu = all_data['beizhu']
        if    gongnengdian.query.filter_by(gongneng_name=gongnengming).first()!=None:
            return jsonify(status="error",detail="功能名重复")
        user = gongnengdian(gongneng_name=gongnengming, beizhu=beizhu, create_time=str(time.time()),
                        create_user=g.user_name)
        db.session.add(user)
        db.session.flush()
        locust_id = user.id
        db.session.commit()
        return  jsonify(status='success')
    return add_gongneng


def get_gongneng_def(func):
    def get_gongneng_def():
        func()
        return_data=[]
        for i in gongnengdian.query.filter_by().all():
            return_data.append({
                'id': i.id,
                'name': i.gongneng_name,
                'beizhu': i.beizhu
            })
        return  jsonify(status='success',detail=return_data)
    return get_gongneng_def


def add_quanxiandian(func):
    def add_quanxiandian():
        func()
        gongnengdian=request.get_json()['request_data']['gongnengdian']
        quanxiandian_list=request.get_json()['request_data']['quanxiandian']
        user_list=request.get_json()['request_data']['user_list']
        beizhu = request.get_json()['request_data']['beizhu']
        tag=request.get_json()['request_data']['tag']
        if quanxiandian.query.filter_by(tag=tag).all()!=[]:
            return jsonify(status='error',detail='tag名重复')
        for   i in  quanxiandian.query.filter_by(gongnengdianid=gongnengdian).all() :
            if i.detail == quanxiandian_list:
                return jsonify(status='error', detail='权限点名名重复')
        create_time = str(time.time())
        create_user = g.user_name
        user = quanxiandian(gongnengdianid=gongnengdian, detail=quanxiandian_list, tag=tag,user_list=json.dumps(user_list),beizhu=beizhu,create_time=create_time,
                        create_user=create_user)
        db.session.add(user)
        db.session.commit()
        return  jsonify(status='success')
    return add_quanxiandian



def get_all_quanxian(func):
    def get_all_quanxian():
        func()
        return_data=[]
        all_gongnengdian={}
        for i in  gongnengdian.query.filter_by().all():
            all_gongnengdian[i.id] = i.gongneng_name
        for i in  quanxiandian.query.filter_by().all():
            ten_timeArray = time.localtime(float(i.create_time))
            ten_otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", ten_timeArray)
            this_data = {
                'id':i.id,
                'gongnengdianid':all_gongnengdian[i.gongnengdianid],
                'detail':i.detail,
                'tag':i.tag,
                'user_list':i.user_list,
                'create_time':ten_otherStyleTime,
                'create_user':i.create_user,
                'beizhu':i.beizhu
            }
            return_data.append(this_data)
        return jsonify(statu='success',detail=return_data)
    return get_all_quanxian

def bianji_quanxian_def(func):
    def bianji_quanxian_def():
        func()
        quanxiandianid = request.get_json()['request_data']['id']
        gongnengdian=request.get_json()['request_data']['gongnengdian']
        quanxiandian_list=request.get_json()['request_data']['quanxiandian']
        user_list=request.get_json()['request_data']['user_list']
        beizhu = request.get_json()['request_data']['beizhu']
        tag=request.get_json()['request_data']['tag']
        for i in quanxiandian.query.filter_by().all():
            if i.id != quanxiandianid:
                if i.detail == gongnengdian:
                    return jsonify(status='error', detail='权限点名名重复')
                elif i.tag == tag:
                    return jsonify(status='error', detail='tag重复')
        user= quanxiandian.query.filter_by(id= quanxiandianid).first()
        user.gongnengdianid = gongnengdian
        user.user_list = json.dumps(user_list)
        user.beizhu =beizhu
        user.tag = tag
        db.session.add(user)
        db.session.commit()
        return  jsonify(status='success')
        return jsonify()
    return bianji_quanxian_def


def delete_quianxian(func):
    def delete_quianxian():
        func()
        quanxian_id =request.args.get('quanxian_id')
        print (quanxian_id)
        db.session.delete(quanxiandian.query.filter_by(id=quanxian_id).first())
        db.session.commit()
        return jsonify(status='success')
    return delete_quianxian

def delete_gongneng(func):
    def delete_gongneng():
        all_data= request.get_json()['request_data']
        gongneng_id = all_data['id']
        user = quanxiandian.query.filter_by(gongnengdianid=gongneng_id).first()
        if user!=None:
            return jsonify(status='error',detail='有关联权限点，请先删除权限点')
        else :
            db.session.delete(gongnengdian.query.filter_by(id=gongneng_id).first())
            db.session.commit()
        return jsonify(status='success')
    return delete_gongneng

def get_quanxian_user(func):
    def get_quanxian_user():
        func()
        quanxian_tag=request.get_json()['tag']
        user = quanxiandian.query.filter_by(tag=quanxian_tag).first().user_list
        user= json.loads(user)
        user_list=current_app.config.get('DB_JURISDICITION').split(',')
        user_list= user+user_list
        return_list=[]
        for k , i in enumerate(user_list):
            if i not in return_list:
                return_list.append(i)
        return jsonify(status='success',all_user=return_list)
    return get_quanxian_user