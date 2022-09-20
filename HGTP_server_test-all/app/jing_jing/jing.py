# -*- coding: utf-8 -*-
import json
import shutil
import time
from pprint import pprint
from urllib.parse import urljoin

import flask
import os

import math

from demjson import decode

__author__='mojingjing'
#data:2020/7/16
import sqlite3
from flask import current_app, Blueprint, request, g, jsonify, Flask, render_template, make_response, \
    send_from_directory  # 蓝图
from flask_cors import cross_origin

jing_new = Blueprint('jing',__name__)


#增加节点
#业务线管理新增业务接口

@jing_new.route('/add_bus',methods=['POST','GET'])
@cross_origin()
def add_bus():
    if request.method != "POST":
        return jsonify(status='fail', detail="请求方式错误")
    else:
        data = request.get_json()
        if g.user_name in ('', None):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json==False:
            return jsonify(status='fail', detail="请求格式错误，不是json")
        elif data.get('bus_name') ==None:
            return jsonify(status='fail', detail="参数缺失")
        elif data.get('bus_name') == '':
            return jsonify(status='fail', detail="参数错误")
        elif type(data['bus_name']) != str:
            return jsonify(status='fail', detail="参数类型错误")
        else:
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            time_now = time.time()
            # bus_name=request.form['bus_name']
            # bus_name=request.form.get('bus_name')
            # request.get_data()
            # 获取的原始参数，接收的是type为'bytes'的对象
            if cu.execute('select * from bus_detail where bus_name="{}"'.format(
                    data['bus_name'])).fetchall() == []:
                cu.execute('insert into  bus_detail values(Null,?,?,?,?,? )',
                           (data['bus_name'], g.user_name, time_now, None, g.user_name))
                db.commit()
                db.close()
                return jsonify(status='success', detail=None)
            else:
                db.close()
                return jsonify(status='fail', detail="该业务线已存在")

#业务线管理——业务名删除接口
@jing_new.route('/common/delete_bus',methods=['POST','GET'])
@cross_origin()
def delete_bus():
    if request.method!="POST":
        return jsonify(status='fail', detail="请求方式错误")
    else:
        try:
            data=request.get_json()
        except Exception as e:
            return jsonify(status='fail',detail= "请求格式错误")
        if g.user_name  in ('', None):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json==False:
            return jsonify(status='fail', detail="请求格式错误，不是json")
        elif data.get('id') ==None:
            return jsonify(status='fail', detail="参数缺失")
        elif data.get('id') == '':
            return jsonify(status='fail', detail="参数错误")
        else:
            try:
                int(data['id'])
            except:
                return jsonify(status='fail', detail="参数类型错误")
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            if cu.execute('select * from bus_detail where id={}'.format(data['id'])).fetchall()!=[]:
                if g.user_name in (current_app.config.get('DB_JURISDICITION')) or g.user_name==cu.execute('select create_name from bus_detail where id={}'.format(data['id'])).fetchall()[0][0]:

                    if cu.execute('select * from version_detail where bus_id={}'.format(data['id'])).fetchall()==[]:
                        cu.execute('delete from bus_detail where id={}'.format(data['id']))
                        db.commit()
                        db.close()
                        return jsonify(status='success',detail= None)
                    else:
                        db.close()
                        return jsonify(status='fail',detail= "该业务已关联版本不能删除")
                else:
                    return jsonify(status='fail', detail="没有操作权限")

            else:
                db.close()
                return jsonify(status='fail',detail="未找到该id")

#业务线管理——业务名更新接口
@jing_new.route('/common/update_bus',methods=['POST','GET'])
@cross_origin()
def update_bus():
    if request.method!="POST":
        return jsonify(status='fail', detail="请求方式错误")
    else:
        try:
            data = request.get_json()
        except:
            return jsonify(status='fail', detail="请求格式错误，不是json")
        time_now= time.time()
        if g.user_name  in ('', None):
            return jsonify(status='fail', detail="未登录")
        elif data.get('id') == None or data.get('bus_name') == None:
            return jsonify(status='fail', detail="参数缺失")
        elif data.get('id') == '' or data.get('bus_name') == '':
            return jsonify(status='fail', detail="参数错误")
        elif type(data.get('bus_name')) !=str:
            return jsonify(status='fail', detail="参数类型错误")
        else:
            try:
                int(data['id'])
            except:
                return jsonify(status='fail', detail="参数类型错误")
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            id = cu.execute('select * from bus_detail where id={}'.format(data['id'])).fetchall()
            bus_name = cu.execute('select * from bus_detail where bus_name="{}" '.format(data['bus_name'])).fetchall()
            print("id",id,"bus_name",bus_name)
            if id != [] and bus_name == []:
                cu.execute('update bus_detail set bus_name="{}",update_time="{}",update_time="{}" where id={}'.format(data['bus_name'], time_now,g.user_name, data['id']))
                db.commit()
                db.close()
                return jsonify(status='success', detail=None)
            else:
                db.close()
                return jsonify(status='fail', detail="id不存在或bus_name已存在")
#业务线管理——业务名查询接口
@jing_new.route('/common/get_bus',methods=['POST','GET'])
@cross_origin()
def get_bus():
    if request.method != "POST":
        return jsonify(status='fail', detail="请求方式错误")
    else:
        try:
            data = request.get_json()
            print("请求参数", data)
        except:
            return jsonify(status='fail', detail="请求格式错误，不是json")
        if g.user_name  in ('', None):
            return jsonify(status='fail', detail="未登录")
        elif  data.get('type') == None:
            return jsonify(status='fail', detail="参数缺失")
        elif  data.get('type') == '' :
            return jsonify(status='fail', detail="参数错误")
        elif  data.get('type') != 0 and  data.get('bus_id')==None:
            return jsonify(status='fail', detail="参数错误")
        elif data.get('type') != None and data.get("type") not in(0,1):
            return jsonify(status='fail', detail="请输入正确的参数")
        else:
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            try:
                int(data.get('type'))
                # int(data.get('bus_id'))
            except:
                return jsonify(status='fail', detail="参数类型错误")
            if data.get('type')==0:
                #查询所有信息
                result_sql = cu.execute('select * from bus_detail').fetchall()
                db.commit()
                db.close()
                list1 = []
                for re in result_sql:
                    print(re)
                    data2 = {re[0]: re}
                    list1.append(data2)
                data=json.dumps(list1)
                return data
            elif data.get('type')==1 and data.get('bus_id')!=None:
                result_sql = cu.execute('select * from bus_detail where id={}'.format(data['bus_id'])).fetchall()
                db.commit()
                db.close()
                if result_sql!=[]:
                    list1 = []
                    for re in result_sql:
                        print(re)
                        data2 = {re[0]: re}
                        list1.append(data2)
                    data = json.dumps(list1)
                    return data
                else:
                    return jsonify(status='fail', detail="未找到该业务线")
            else:
                db.close()
                return jsonify(status='fail', detail="参数错误")
#公共配置文件存储
@jing_new.route('/save_publick_config',methods=['POST','GET'])
@cross_origin()
def  save_publick_config():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('publick_config_detail') == None or request.form.get('id') == None:
            return jsonify(statu='fail',detail='请求参数缺失')
        elif request.form.get('publick_config_detail') =='' or request.form.get('id') == '':
            return jsonify(statu='fail',detail='请求参数错误')
        else:
            publick_config_detail = request.form.get('publick_config_detail')
            id = request.form.get('id')
            if type(publick_config_detail) !=None:
                try:
                    int(id)
                    pass
                except:
                    return jsonify(statu='fail', detail='参数类型错误')
            else:
                return jsonify(statu='fail', detail='参数类型错误')
            publick_config_detail=json.loads(publick_config_detail)
            list1 = []
            for base_path in publick_config_detail:
                for f, v in publick_config_detail[base_path].items():
                    first_path = f
                    for index in range(len(v)):
                        for s, config_db in v[index].items():
                            second_path = s
                            config = config_db['config']
                            db_file = config_db['db']
                            db = sqlite3.connect(current_app.config.get('CONTIN'))
                            cu = db.cursor()
                            mulu_id = cu.execute(
                                'select id from catalog_detail where first_catalog="{}" and second_catalog="{}"  and version_id ={}'.format(first_path, second_path, id)).fetchall()
                            if mulu_id == []:
                                db.commit()
                                db.close()
                                return jsonify(statu='fail', detail='{},{},不存在'.format(first_path, second_path))
                            else:
                                data1 = {'mulu_id': mulu_id[0][0], 'first_path': first_path, 'second_path': second_path,
                                         'config': config, 'db': db_file}
                                list1.append(data1)
            # print(list1)
            mulu_list = [i['mulu_id'] for i in list1]
            print(mulu_list)
            # interface_jurisdiction = cu.execute('select catalog_list from interface_jurisdiction where user_name ="{}" and version_id={} '.format(g.user_name,id)).fetchall()
            # if len(interface_jurisdiction)!=0:
            #     catalog_list=interface_jurisdiction[0][0].replace('[', '').replace(']', '').replace("'", "").replace(' ', '').replace(
            #         '"', '').split(',')
            #     catalog_list =[int(i) for i in catalog_list]
            #     print(catalog_list)
            #     for m in mulu_list:
            #         if m in catalog_list:
            #             pass
            #         else:
            #             for index,item in enumerate(list1):
            #                 if item['mulu_id']==m:
            #                     del list1[index]
            # else:
            #     return jsonify(statu='fail', detail='没有权限')
            print([i['mulu_id'] for i in list1])

            for i in list1:
                # print(i)
                publick_detial_sql = cu.execute(
                    'select * from publick_detail where catalog_id={}'.
                        format(i['mulu_id'])).fetchall()
                if publick_detial_sql == []:
                    cu.execute('insert into  publick_detail values(Null,?,?,?,?,?,?,Null,Null)',(i['mulu_id'], id, json.dumps(i['config'],ensure_ascii=False), json.dumps(i['db'],ensure_ascii=False ), int(time.time()), g.user_name))
                    db.commit()

                else:
                    cu.execute(
                        'update publick_detail set version_id=?,config=?,db=?,update_time=?,update_name=? where catalog_id=?',
                            (id, json.dumps(i['config'],ensure_ascii=False), json.dumps(i['db'],ensure_ascii=False), int(time.time()), g.user_name,i['mulu_id']))
                    db.commit()
            db.close()
            return jsonify(statu='success', detail=None)

def publick_config_detail(**kwargs):

    list1=[]
    for base_path in publick_config_detail:
        for f,v in publick_config_detail[base_path].items():
            # k=第一层目录
            first_path=f
            for index in range(len(v)):
                for s,config_db in v[index].items():
                    second_path=s
                    config = config_db['config']
                    db = config_db['db']
                    # print(config)
                    # print(db)
                    db = sqlite3.connect(current_app.config.get('CONTIN'))
                    cu = db.cursor()
                    # 判断是否存在，返回目录id
                    mulu_id=cu.execute('select id from catalog_detail where first_ catalog={} and second_ catalog={}  and version_id ={}'.
                               format(first_path,second_path,id)).fetchall()

                    if mulu_id ==None:
                        cu.close()
                        return jsonify(statu='fail', detail='{},{},不存在'.format(first_path,second_path))
                    else:
                        data1={'mulu_id':mulu_id,'first_path':first_path,'second_path':second_path,'config':config,'db':db}
                        list1.append(data1)

    # print(list1)
    for i in list1:

        time_new=time.time()
        # 查询该记录是否在publick_detial表中
        publick_detial_sql=cu.execute(
            'select * from publick_detial where catalog_id={}'.
            format(i['mulu_id'])).fetchall()
        if publick_detial_sql==[]:
            # insert
            cu.execute('insert into  publick_detial values(Null,?,?,?,?,?,?,?,? )',
                       (i['mulu_id'],id,i['config'],i['db'],time_new,g.user_name,None,None))
        else:
            cu.execute(
                'update publick_detial set version_id="{}",config={},db={},update_time="{},update_name" where catalog_id={}'.
                    format(id,i['config'],i['db'],time_new,g.user_name))

    return jsonify(statu='success', detail=None)

# jing_new.run(debug=True,threaded=True)
# 接口配置文件存储
@jing_new.route('/save_private_config',methods=['POST','GET'])
@cross_origin()
def save_private_config():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('private_config') == None or request.form.get('version_id') == None:
            return jsonify(statu='fail',detail='请求参数缺失')
        elif request.form.get('private_config') == '' or request.form.get('version_id') == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            private_config = request.form.get('private_config')
            private_config=json.loads(private_config)
            version_id = request.form.get('version_id')
            if type(private_config) !=None:
                try:
                    int(version_id)
                    pass
                except:
                    return jsonify(statu='fail', detail='参数类型错误')
            else:
                return jsonify(statu='fail', detail='参数类型错误')
            list1 = []
            mulu_jiekou_id={}

            for base_path in private_config:
                for f, v1 in private_config[base_path].items():
                    first_path = f
                    db = sqlite3.connect(current_app.config.get('CONTIN'))
                    cu = db.cursor()
                    for second_path, v2 in v1.items():
                        for third_path, configparse_json in v2.items():
                            configparse = configparse_json['configparse']
                            json_con = configparse_json['json']
                            # 判断是否存在，返回目录id
                            mulu_id = cu.execute(
                                'select id from catalog_detail where first_catalog="{}" and second_catalog="{}"  and version_id ={}'.
                                format(first_path, second_path, version_id)).fetchall()
                            if mulu_id == []:
                                db.commit()
                                db.close()
                                return jsonify(statu='fail', detail='{},{},不存在'.format(first_path, second_path))
                            else:
                                # 根据mulu_id 和版本id去查找interface_detail表中id
                                jiekou_id=cu.execute(
                                    'select id from interface_detail where catalog_id ={} and version_id={} and  interface="{}"'.format(mulu_id[0][0],version_id,third_path)).fetchall()
                                if jiekou_id==[]:
                                    return jsonify(statu='fail', detail='{},{},{}不存在'.format(first_path, second_path,third_path))
                                else:
                                    # 先把数据记录在表中
                                    data1 = {'mulu_id': mulu_id[0][0], 'jiekou_id':jiekou_id[0][0],'first_path': first_path, 'second_path': second_path,
                                             'third_path': third_path, 'configparse': configparse, 'json': decode(json_con)}
                                    list1.append(data1)
                                    # print(data1)
                                    if mulu_jiekou_id.get(mulu_id[0][0])!=None:
                                        jiekou_id_ji=mulu_jiekou_id[mulu_id[0][0]]
                                        jiekou_id_ji.append(jiekou_id[0][0])
                                        mulu_jiekou_id[mulu_id[0][0]]=jiekou_id_ji
                                    else:
                                        jiekou_id_ji=[]
                                        jiekou_id_ji.append(jiekou_id[0][0])
                                        mulu_jiekou_id[mulu_id[0][0]]=jiekou_id_ji
            # print("list1",list1)
            mulu_list = [i['mulu_id'] for i in list1]
            # interface_jurisdiction = cu.execute(
            #     'select catalog_list from interface_jurisdiction where user_name ="{}" and version_id={} '.format(
            #         g.user_name, version_id)).fetchall()
            # if len(interface_jurisdiction) != 0:
            #     catalog_list = interface_jurisdiction[0][0].replace('[', '').replace(']', '').replace("'", "").replace(
            #         ' ', '').replace(
            #         '"', '').split(',')
            #     catalog_list = [int(i) for i in catalog_list]
            #     for m in mulu_list:
            #         if m in catalog_list:
            #             pass
            #         else:
            #             for index, item in enumerate(list1):
            #                 if item['mulu_id'] == m:
            #                     del list1[index]
            # else:
            #     return jsonify(statu='fail', detail='没有权限')
            # print([i['mulu_id'] for i in list1])

            for k, y in mulu_jiekou_id.items():
                db = sqlite3.connect(current_app.config.get('CONTIN'))
                cu = db.cursor()
                if len(y)==1:
                    cu.execute(
                        'delete from private_config_detail where catalog_id={} and interface_id not in({}) and version_id={}'.format(
                            k, y[0], version_id))
                else:
                    cu.execute('delete from private_config_detail where catalog_id={} and interface_id not in{} and version_id={}'.format(k,tuple(y),version_id))
                db.commit()
                db.close()
            for i in list1:
                # 查询该记录是否在private_config_detail表中
                db = sqlite3.connect(current_app.config.get('CONTIN'))
                cu = db.cursor()
                private_config_detail_sql=cu.execute(
                    'select * from private_config_detail where catalog_id={} and version_id={} and interface_id={}'.
                        format(i['mulu_id'],version_id,i['jiekou_id'])).fetchall()
                if private_config_detail_sql==[]:
                    cu.execute('insert into  private_config_detail values (Null,?,?,?,?,?,?,?,Null,Null)',
                               (i['mulu_id'],version_id,i['jiekou_id'],json.dumps(i['configparse'],ensure_ascii=False),
                                       json.dumps(i['json'],ensure_ascii=False),int(time.time()),g.user_name))
                    db.commit()
                else:
                    cu.execute(
                        'update private_config_detail set configparse=?,json=?,update_time=?,update_name=? where catalog_id=? and version_id=? and interface_id=?',
                            (json.dumps(i['configparse'],ensure_ascii=False),json.dumps(i['json'],ensure_ascii=False),int(time.time()),g.user_name,i['mulu_id'],version_id,i['jiekou_id']))
                    db.commit()
                db.close()
            return jsonify(statu='success', detail=None)
# 接口case文件存储
@jing_new.route('/save_case',methods=['POST','GET'])
@cross_origin()
def save_case():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('case_detail') == None or request.form.get('version_id') == None:
            return jsonify(statu='fail',detail='请求参数缺失')
        elif request.form.get('case_detail') == '' or request.form.get('version_id') == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            case_detail = request.form.get('case_detail')
            case_detail = json.loads(case_detail)
            version_id = request.form.get('version_id')
            if type(case_detail) != None:
                try:
                    int(version_id)
                    pass
                except:
                    return jsonify(statu='fail', detail='参数类型错误')
            else:
                return jsonify(statu='fail', detail='参数类型错误')
            get_data(case_detail,version_id)
            return jsonify(statu='success', detail=None)

def get_data(case_detail,version_id):

    list1 = []
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    for base_path in case_detail:
        try:
            for f, v1 in case_detail[base_path].items():
                pass
        except:
            pass
        for f, v1 in case_detail[base_path].items():
            first_path = f
            for second_path, v2 in v1.items():
                for third_path, case_list in v2.items():
                    # 判断是否存在，返回目录id
                    mulu_id = cu.execute(
                        'select id from catalog_detail where first_catalog="{}" and second_catalog="{}"  and version_id ={}'.
                            format(first_path, second_path, version_id)).fetchall()
                    if mulu_id == []:
                        db.commit()
                        db.close()
                        return jsonify(statu='fail', detail='{},{},不存在'.format(first_path, second_path))
                    else:
                        # 根据mulu_id 和版本id去查找interface_detail表中id
                        jiekou_id = cu.execute(
                            'select id from interface_detail where catalog_id ={} and version_id={} and  interface="{}"'.format(
                                mulu_id[0][0], version_id, third_path)).fetchall()
                        # print(jiekou_id)
                        if jiekou_id == []:
                            db.commit()
                            db.close()
                            return jsonify(statu='fail',
                                           detail='{},{},{}不存在'.format(first_path, second_path, third_path))
                        else:
                            # 先把数据记录在表中
                            for case_id ,case_data in case_list.items():

                                data1 = {'mulu_id': mulu_id[0][0], 'jiekou_id': jiekou_id[0][0], 'first_path': first_path,
                                         'second_path': second_path,
                                         'third_path': third_path, 'case_id': case_id, 'case_data': case_data}
                                list1.append(data1)
                                # print(list1)

    mulu_list = [i['mulu_id'] for i in list1]
    print(mulu_list)
    # interface_jurisdiction = cu.execute(
    #     'select catalog_list from interface_jurisdiction where user_name ="{}" and version_id={} '.format(
    #         g.user_name, version_id)).fetchall()
    # if len(interface_jurisdiction) != 0:
    #     catalog_list = interface_jurisdiction[0][0].replace('[', '').replace(']', '').replace("'", "").replace(
    #         ' ', '').replace(
    #         '"', '').split(',')
    #     catalog_list = [int(i) for i in catalog_list]
    #     for m in mulu_list:
    #         if m in catalog_list:
    #             pass
    #         else:
    #             for index, item in enumerate(list1):
    #                 if item['mulu_id'] == m:
    #                     del list1[index]
    # else:
    #     return jsonify(statu='fail', detail='没有权限')
    print([i['mulu_id'] for i in list1])
    for i in list1:
        # case_detail表中陪陪数据删除
        cu.execute(
            'delete from case_detail where catalog_id={} and version_id={} and interface_id={}'.
                format(i['mulu_id'], version_id, i['jiekou_id'])).fetchall()
        db.commit()
    for i in list1:
        # case_detail表中存入数据
        cu.execute(
            'insert into  case_detail values (Null,?,?,?,?,?,?,?,?)',
            (i['mulu_id'], version_id,i['jiekou_id'],i['case_id'],i['case_data']['Comment'], json.dumps(i['case_data'],ensure_ascii=False), int(time.time()),g.user_name))
        db.commit()
    db.close()

# 获取case信息接口
@jing_new.route('/get_interface_id_detail',methods=['POST','GET'])
@cross_origin()
def get_interface_id_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        # if g.user_name in (None,''):
        #     return jsonify(status='fail', detail="未登录")
        if flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('version_id') == None or request.form.get('interface_id') == None:
            return jsonify(statu='fail',detail='请求参数缺失')
        elif request.form.get('version_id') == '' or request.form.get('interface_id') == '':
            return jsonify(statu='fail', detail='请求参数错误')
        elif type(request.form.get('interface_id')) != str:
            return jsonify(statu='fail', detail='请求参数类型错误')
        else:
            version_id = request.form.get('version_id')
            interface_id = request.form.get('interface_id')

            try:
                int(version_id)
                pass
            except:
                return jsonify(statu='fail', detail='参数类型错误')
            result=get_detail(version_id,interface_id)
            return result
def get_detail(version_id,interface_id):
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    interface_id= interface_id.replace('[', '').replace(']', '').replace("'","").replace(' ','').replace('"','').split(',')
    detail={}
    for i in interface_id:
        case_detail = cu.execute(
            'select case_detail from case_detail where version_id=? and  interface_id=?',(version_id,i)).fetchall()
        catalog_id = cu.execute(
            'select distinct(catalog_id) from case_detail where version_id=? and  interface_id=?',(version_id,i)).fetchall()
        if case_detail==[] or catalog_id==[]:
            return jsonify(statu='fail', detail='该接口id或版本号不存在')
        else:
            detail[i]={}
            list1 = []
            for j in case_detail:
                list1.append(json.loads(j[0]))
            detail[i]['case_detail']=list1
            config_db = cu.execute(
                'select config,db from publick_detail where version_id=? and  catalog_id=?', (version_id, catalog_id[0][0])).fetchall()
            if config_db==[]:
                return jsonify(statu='fail', detail='public_detal中缺失config,db数据')
            else:
                publick_config={}
                publick_config['config']=config_db[0][0]
                publick_config['db']=config_db[0][1]
                detail[i]['publick_config']=publick_config
            #private_config_detail中读取configparse,json
            configparse_json = cu.execute(
                'select configparse,json from private_config_detail where version_id=? and  interface_id=?', (version_id,i)).fetchall()
            if configparse_json==[]:
                return jsonify(statu='fail', detail='configparse_json中缺失configparse,json数据')
            else:
                private_config={}
                private_config['configparse']=configparse_json[0][0]
                private_config['json']=configparse_json[0][1]
                detail[i]['private_config']=private_config
                # print(detail)
    return jsonify(statu='success', detail=detail)

#接口数据读取
@jing_new.route('/get_version_case', methods=['POST','GET'])
def get_version_case():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None, ''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('version_id') == None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif request.form.get('version_id') == '':
            return jsonify(statu='fail', detail='请求参数错误')

        else:
            version_id = request.form.get('version_id')
            try:
                int(version_id)
                pass
            except:
                return jsonify(statu='fail', detail='参数类型错误')

            result = read_case_data(version_id)
            return result
def read_case_data(version_id):
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    if cu.execute('select * from version_detail where id={}'.format(version_id)).fetchall()==[]:
        db.close()
        return jsonify(statu='fail', detail='不存在该版本号')
    else:
        detail = {}
        mulu=[list(i) for i in cu.execute('select id,first_catalog,second_catalog from catalog_detail where version_id={}'.format (version_id)).fetchall()]
        # print(mulu)
        for i in mulu:
            # print(i)
            publick=cu.execute('select config, db from publick_detail where version_id={} and catalog_id={}'.format(version_id,i[0])).fetchall()
            interface=cu.execute('select id,interface from interface_detail where version_id={} and catalog_id={}'.format(version_id,i[0])).fetchall()

            if detail.get(i[1]):
                second_path[i[2]] = {}
                detail[i[1]] = second_path
            else:
                detail[i[1]]={}  #{'CRM接口重构': {}}
                second_path={}
                second_path[i[2]]={}
                detail[i[1]]=second_path
            publick_config={}
            publick_config['config']=publick[0][0]
            publick_config['db']=publick[0][1]
            detail[i[1]][i[2]]=publick_config
            for t in interface: ##[(26, '01_我的门店列表接口'), (27, '02_公海门店业态'), (28, '03_公海门店行政区域')]
                private = cu.execute(
                    'select configparse,json from private_config_detail where version_id={} and catalog_id={} and interface_id={}'.format(version_id, i[0],t[0])).fetchall()

                detail[i[1]][i[2]][t[1]]={}
                private_config={}
                private_config['configparse']=private[0][0]
                private_config['json']=private[0][1]
                detail[i[1]][i[2]][t[1]]=private_config
                case_detail = cu.execute(
                    'select case_id,case_detail from case_detail where version_id={} and catalog_id={} and interface_id={}'.format(
                        version_id, i[0], t[0])).fetchall()
                case_list = []
                for k in case_detail:

                    case={}
                    case['case_id']=k[0]
                    case['case_detail']=k[1]
                    case_list.append(case)
                detail[i[1]][i[2]][t[1]][t[1]]=case_list
        print(detail)
        return jsonify(statu='success', detail=detail)

# 运行结果信息保存接口
@jing_new.route('/save_run_case_detail', methods=['POST', 'GET'])
def save_run_case_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        run_type = request.form.get('run_type')
        result_data = request.form.get('result_data')
        run_job_id = request.form.get('run_job_id')
        interface_id = request.form.get('interface_id')
        running_time = request.form.get('running_time')
        if g.user_name in (None, ''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif run_type == None or result_data == None or run_job_id == None or interface_id == None or running_time==None:
            return jsonify(statu='fail', detail='请求参数缺失')
        elif run_type == '' or result_data == '' or run_job_id == '' or interface_id == '' or running_time=='':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                run_type = int(run_type)
                interface_id = int(interface_id)
                running_time = int(running_time)
                pass
            except:
                return jsonify(statu='fail', detail='参数类型错误')
            if run_type not in(0,1):
                return jsonify(statu='fail', detail='请求参数错误')
            else:
                result=sava_run_data(run_job_id,interface_id,result_data,run_type,running_time)
                return result
def sava_run_data(run_job_id,interface_id,result_data,run_type,running_time):
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    real_time_run = cu.execute('select * from real_time_run where id={}'.format(run_job_id)).fetchall()
    # print(real_time_run) #[(9, '["1","2"]', '53', '192.168.0.155', '', '', '', 1, '', '莫晶晶', 1596712108, '', 1)]
    timed_tasks = cu.execute('select * from timed_tasks where id={}'.format(run_job_id)).fetchall()
    # print(timed_tasks)   #[(22, 0, '1', '1', '1', '1', '1', 1, 0, 1596700186, 'mojingjing', None)]

    if run_type==0:
        run_time_data=real_time_run
        if run_time_data == []:
            db.close()
            return jsonify(statu='fail', detail='run_job_id不存在')
        else:
            interface_list=real_time_run[0][1]
            version_id=real_time_run[0][2]
    elif run_type==1:
        run_time_data = timed_tasks
        if run_time_data == []:
            db.close()
            return jsonify(statu='fail', detail='run_job_id不存在')
        else:
            interface_list = timed_tasks[0][5]
            version_id = timed_tasks[0][1]

            num=cu.execute('select distinct(time) from  db_run_result where  statu=1 and run_id= {} order by time desc '.format(run_job_id)).fetchall()
            if len(num)< 5:
                pass
            else:
                cu.execute('delete from db_run_result where run_id={run_id} and statu=1 and time<(select distinct(time) from db_run_result where run_id={run_id} and statu=1 order by time desc limit 3,1)'.format(run_id=run_job_id))
                db.commit()

    else:
        return jsonify(statu='fail', detail='run_type不正确')
    interface_list=[int(i) for i in interface_list.replace('[','').replace(']','').replace('"','').replace("'","").split(',')]
    print(interface_list)
    if interface_id not in interface_list:
        db.close()
        return jsonify(statu='fail', detail='接口id不存在')
    else:

        # save_run_result(result_data)
        result_data=json.loads(result_data)
        cass_fail=0
        case_pass=0
        for i, j in result_data.items():
            if j['assert_result']==False:
                cass_fail+=1
            else:
                case_pass+=1
        if cass_fail==0:
            interface_pass=1
            interface_fail=0
        else:
            interface_pass = 0
            interface_fail = 1
        a=cu.execute('select * from  data_statistics where version_id=? and statu=? ',
                   (version_id, run_type)).fetchall()
        if a==[]:
            # insert
            cu.execute('insert into  data_statistics values(Null,?,?,?,?,? ,?,?,?)',
                       (version_id,1,interface_pass,interface_fail,cass_fail,case_pass,int(time.time()),run_type ))
            db.commit()
        else:
            cu.execute('update  data_statistics set interface_pass=?,interface_fail=?,case_fail=?,case_pass=?,time=? where version_id=? and statu=?',
                       (int(a[0][3])+interface_pass,int(a[0][4])+interface_fail,int(a[0][5])+cass_fail,int(a[0][6])+case_pass,int(time.time()),version_id, run_type))
            db.commit()
        for i, j in result_data.items():
            if run_type==1:
                cu.execute('insert into  db_run_result values(Null,?,?,?,?,? ,?,?,?,?,?,?)',
                           (interface_id, run_job_id, i, j['case_name'], j['req_url'],
                            json.dumps(j['req'], ensure_ascii=False),
                            json.dumps(j['respons'], ensure_ascii=False), j['assert_result'],
                            json.dumps(j['case_assert']),
                            int(running_time), run_type))
                db.commit()
            if run_type==0:
                if cu.execute('select * from  db_run_result where interface_id=? and run_id=? and case_id=?',
                              (interface_id, run_job_id, i)).fetchall() == []:

                    cu.execute('insert into  db_run_result values(Null,?,?,?,?,? ,?,?,?,?,?,?)',
                               (interface_id, run_job_id, i, j['case_name'], j['req_url'],json.dumps(j['req'],ensure_ascii=False),
                                json.dumps(j['respons'], ensure_ascii=False), j['assert_result'], json.dumps(j['case_assert']),
                                int(running_time), run_type))
                    db.commit()
                else:

                    cu.execute(
                        'update db_run_result set case_name=?,request_url=?,request_detail=?,result_detail=?,assert_result=?,assert_detail=?,time=?,statu=? where interface_id=? and run_id=? and case_id=?',
                        (j['case_name'], j['req_url'], json.dumps(j['req'],ensure_ascii=False),json.dumps(j['respons'], ensure_ascii=False),
                         j['assert_result'], json.dumps(j['case_assert']), int(running_time), run_type, interface_id, run_job_id,i))
                    db.commit()
        db.close()
        return jsonify(statu='success', detail=None)
# 读取运行结果
@jing_new.route('/read_run_case_detail', methods=['POST', 'GET'])
def read_run_case_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None, ''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('version_id') == None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif request.form.get('version_id')=='':
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            a=cu.execute('select sum(frequency),sum(interface_pass),sum(interface_fail),sum(case_pass),sum(case_fail) from data_statistics').fetchall()
            detail={
                "frequency":a[0][0],
                "interface_pass":a[0][1],
                "interface_fail":a[0][2],
                "case_pass":a[0][3],
                "case_fail":a[0][4],
                "pass_rate": "{:.0%}".format((math.ceil((a[0][3] / (a[0][3] + a[0][4]))*100))/100)

            }
            return jsonify(status='success', detail=detail)
        else:
            version_id = request.form.get('version_id')
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            try:
                int(version_id)
            except:
                return jsonify(status='fail', detail="参数类型错误")
            # a=cu.execute('select * from data_statistics where version_id={}'.format(version_id)).fetchall()
            a=cu.execute('select sum(frequency),sum(interface_pass),sum(interface_fail),sum(case_pass),sum(case_fail) from data_statistics where version_id={}'.format(version_id)).fetchall()
            detail = {
                "frequency": a[0][0],
                "interface_pass": a[0][1],
                "interface_fail": a[0][2],
                "case_pass": a[0][3],
                "case_fail": a[0][4],
                "pass_rate": "{:.0%}".format((math.ceil((a[0][3] / (a[0][3] + a[0][4]))*100))/100)

            }
            return jsonify(status='success', detail=detail)
#定时任务创建接口
@jing_new.route('/timed_tasks_create', methods=['POST', 'GET'])
def timed_tasks_create():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        version_id=request.form.get('version_id')
        email_sender=request.form.get('email_sender')
        email_receiver=request.form.get('email_receiver')
        email_title=request.form.get('email_title')
        interface_lise=request.form.get('interface_lise')
        run_time=request.form.get('run_time')
        run_interval=request.form.get('run_interval')
        if g.user_name in (None, ''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif version_id == None or email_sender==None or email_receiver==None or email_title==None or interface_lise==None or run_time==None or run_interval==None:
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == ''  or interface_lise == '' or run_time == '' or run_interval == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                # email_sender=int(email_sender)
                run_interval=int(run_interval)
                hour=["{:0>2d}".format(i) for i in range(24)]
                minute=["{:0>2d}".format(i) for i in range(60)]
                if len(run_time) == 5 and run_time[2] == ':' and run_time[0:2] in hour and run_time[3:] in minute:
                    pass
                else:
                    return jsonify(statu='fail', detail='运行时间错误')
            except:
                return jsonify(statu='fail', detail='请求参数类型错误')
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            num=cu.execute('select count(*) from timed_tasks where version_id=? and create_name=?',(version_id,g.user_name)).fetchall()
            print(num[0][0])
            if num[0][0]<5:
                pass
            else:
                cu.execute('delete from timed_tasks where version_id={} and create_name="{}" and statu in(0,2) and id<(select id from timed_tasks where version_id={} and create_name="{}" and statu in(0,2) order by create_time desc limit 3,1)'.format(version_id,g.user_name,version_id,g.user_name))
                db.commit()
            cu.execute('insert into timed_tasks values(Null,?,?,?,?,?,?,?,?,?,?,Null)',
                       (
                       version_id, email_sender, email_receiver, email_title, interface_lise, run_time, run_interval, 0,
                       int(time.time()), g.user_name))
            db.commit()
            db.close()
            return jsonify(statu='success', detail=None)
# 运行中更新db配置文件内容接口
@jing_new.route('/running_save_db_detail',methods=['POST'])
def running_save_db_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        version_id=request.form.get('version_id')
        interface_id=request.form.get('interface_id')
        db_detail=request.form.get('db_detail')
        statu=request.form.get('statu')
        if flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif version_id == None or interface_id==None or db_detail==None or statu==None:
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == '' or interface_id == '' or db_detail == '' or statu=='':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                interface_id=int(interface_id)
                statu=int(statu)
            except:
                return jsonify(statu='fail', detail='请求参数类型错误')
            db=sqlite3.connect(current_app.config.get('CONTIN'))
            cu=db.cursor()
            catalog=cu.execute('select catalog_id from interface_detail where id={} and version_id={}'.format(interface_id,version_id)).fetchall()
            if catalog!=[]:
                if statu==0:
                    cu.execute('update  publick_detail set db=?,update_time=?,update_name=? where version_id=? and catalog_id=?',(json.dumps(db_detail,ensure_ascii=False),int(time.time()),g.user_name,version_id,catalog[0][0]))
                    db.commit()
                    db.close()
                    return jsonify(statu='success', detail=None)
                elif statu==1:
                    db_con=cu.execute('select db from publick_detail  where version_id=? and catalog_id=?',(version_id,catalog[0][0])).fetchall()
                    db_con=json.loads(db_con[0][0])
                    db_detail = json.loads(db_detail)
                    for k,v in db_con.items():
                        for i,j in db_detail.items():
                            if k==i:
                                d={}
                                d.update(v)
                                d.update(j)
                                db_con[k]=d
                    for i, j in db_detail.items():
                        if not db_con.get(i):
                            db_con[i] = j
                    cu.execute('update  publick_detail set db=?,update_time=?,update_name=? where version_id=? and catalog_id=?',(json.dumps(db_con,ensure_ascii=False),int(time.time()),g.user_name,version_id,catalog[0][0]))
                    db.commit()
                    db.close()
                    return jsonify(statu='success', detail=None)
                    pass
                else:
                    return jsonify(statu='fail', detail='statu错误')
            else:
                return jsonify(statu='fail', detail='版本号或接口id不存在')
# 实时运行进度查询
@jing_new.route('/real_time_job_progress',methods=['POST'])
def real_time_job_progress():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        version_id=request.form.get('version_id')
        run_type=request.form.get('run_type')

        if flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif version_id == None or run_type==None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == '' or run_type == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                run_type=int(run_type)
            except:
                return jsonify(statu='fail', detail='请求参数类型错误')
            db=sqlite3.connect(current_app.config.get('CONTIN'))
            cu=db.cursor()
            a=cu.execute('select * from real_time_run where version_id=? and name=? and statu=1',(version_id,g.user_name)).fetchall()
            b=cu.execute('select * from real_time_run where version_id=? and name=? and statu=2 order by create_time desc',
                               (version_id, g.user_name)).fetchone()
            if len(a)>1:
                return jsonify(statu='fail', detail='存在多个运行中任务')
            elif len(a)<1:
                if b not in([],None):
                    print(b)
                    interface_id = cu.execute(
                        'select interface_id,id from real_time_run where version_id=? and name=? and statu=2 order by create_time desc',
                        (version_id, g.user_name)).fetchall()
                else:
                    return jsonify(statu='fail', detail='没有任务')
            else:
                interface_id=cu.execute('select interface_id,id from real_time_run where version_id=? and name=? and statu=1',
                           (version_id, g.user_name)).fetchall()
            print(interface_id)#[('["1"]', 8), ('["1","2"]', 9), ('["1"]', 12)]
            interface_list=interface_id[0][0].replace('"','').replace('[','').replace(']','').split(',')
            detail={}
            # detail['run_detail']=[]
            detail['interface_num']=len(interface_list)
            pass_interface_num=0
            fail_interface_num=0
            list1=[]
            for i in interface_list:
                interface=cu.execute('select interface from interface_detail where version_id=? and id=?',(version_id,int(i))).fetchall()[0][0]
                assert_result=cu.execute('select assert_result from db_run_result where interface_id=? and run_id=?',(int(i),interface_id[0][1])).fetchall()
                success_num = 0
                fail_num = 0
                for k in assert_result:
                    # print(k[0])
                    if k[0]==0:
                        fail_num+=1
                    else:
                        success_num+=1
                if fail_num==0 and success_num==0:
                    pass_interface_num+=1
                    fail_interface_num+=0
                elif fail_num==0 and success_num!=0:
                    pass_interface_num+=1
                else:
                    fail_interface_num+=1
                data1 = {interface:{}}

                data1[interface]['success_num']=success_num
                data1[interface]['fail_num']=fail_num
                # print(data1)
                list1.append(data1)
            detail['run_detail']=list1
            detail['pass_interface_num'] = pass_interface_num
            detail['fail_interface_num'] = fail_interface_num
            # print(detail)
            return jsonify(statu='success', detail=detail)

# 接口删除
@jing_new.route('/del_interface',methods=['POST'])
def del_interface():
    g.user_name='mojingjing'
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        version_id=request.form.get('version_id')
        interface_id=request.form.get('interface_id')
        if g.user_name in (None, ''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif version_id == None or interface_id==None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == '' or interface_id == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                interface_id=int(interface_id)

            except:
                return jsonify(statu='fail', detail='参数类型错误')
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            statu=cu.execute('select statu from user_jurisdiction where user_name=? and version_id=?',(g.user_name,version_id)).fetchall()

            print(statu)
            super_user = current_app.config.get('DB_JURISDICITION').split(',')
            print(super_user)
            if g.user_name in super_user or (statu!=[] and statu[0][0]==2):
                interface_list1 = cu.execute('select interface_id from real_time_run where version_id=? and statu=?',
                                   ( version_id,1)).fetchall()
                interface_list2 = cu.execute('select interface_list from timed_tasks where version_id=? and statu=?',
                                   ( version_id,1)).fetchall()
                if interface_list1==[] and interface_list2==[]:
                    pass
                if interface_list1!=[]:
                    interface_list1 = interface_list1[0][0].replace('"', '').replace('[', '').replace(']', '').split(
                        ',')
                    interface_list1=[int(i) for i in interface_list1]
                    if interface_id in interface_list1:
                        return jsonify(statu='fail', detail='存在运行中的实时任务')
                    else:
                        pass

                if interface_list2!=[]:
                    interface_list2 = interface_list2[0][0].replace('"', '').replace('[', '').replace(']', '').split(
                        ',')
                    interface_list2 = [int(i) for i in interface_list2]
                    if interface_id in interface_list2:
                        return jsonify(statu='fail', detail='存在运行中的定时任务')
                    else:
                        pass
                cu.execute('delete  from interface_detail where version_id={} and id={}'.format(version_id,interface_id))
                cu.execute('delete  from private_config_detail where version_id={} and interface_id={}'.format(version_id,interface_id))
                cu.execute('delete  from case_detail where version_id={} and interface_id={}'.format(version_id,interface_id))
                cu.execute('delete  from db_run_result where interface_id={0} and (run_id in (select id from timed_tasks where version_id={1}) or run_id in (select id from real_time_run where version_id={1}))'.format(interface_id,version_id))
                db.commit()
                db.close()
                return jsonify(statu='success', detail='删除成功')
            else:
                return jsonify(statu='fail', detail='没有权限删除')

# 接口case列表查询
@jing_new.route('/get_case_detail_page',methods=['POST'])
def get_case_detail_page():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        version_id=request.form.get('version_id')
        interface_id=request.form.get('interface_id')

        if flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif version_id == None or interface_id==None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == '' or interface_id == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                interface_id=int(interface_id)

            except:
                return jsonify(statu='fail', detail='参数类型错误')
            result=get_case_detail(version_id,interface_id)
            return result

def get_case_detail(version_id,interface_id):
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    detail={}
    case_detail = cu.execute(
        'select case_detail from case_detail where version_id=? and  interface_id=?', (version_id, interface_id)).fetchall()

    if case_detail == [] :
        return jsonify(statu='fail', detail='该接口id或版本号不存在')
    else:
        detail[interface_id] = {}
        list1 = []
    for j in case_detail:
        list1.append(json.loads(j[0]))
    detail[interface_id]['case_detail'] = list1
    return jsonify(statu='success', detail=detail)
import matplotlib.pyplot as plt
# #通过率图片接口
# @jing_new.route('/pass_rate_image_interface',methods=['POST','GET'])
# def pass_rate_image_interface():
#
#     version_id=request.values.get('version_id')
#     job_id=request.values.get('job_id')
#     run_type=request.values.get('run_type')
#     print(version_id,job_id,run_type)
#     # return jsonify(statu='fail', detail="请求方式错误")
#     if flask.request.is_json:
#         return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
#     elif version_id == None or job_id==None or run_type==None:
#         return jsonify(statu='fail', detail='请求参数缺失')
#     elif version_id == '' or job_id == '' or run_type==None:
#         return jsonify(statu='fail', detail='请求参数错误')
#     else:
#         try:
#             version_id=int(version_id)
#             run_type=int(run_type)
#             job_id=int(job_id)
#
#         except:
#             return jsonify(statu='fail', detail='参数类型错误')
#         db=sqlite3.connect(current_app.config.get('CONTIN'))
#         cu=db.cursor()
#         pass_case = 0
#         fail_case = 0
#         if run_type==1:
#             timed_tasks=cu.execute('select * from timed_tasks where id={} and version_id={}'.format(job_id,version_id)).fetchall()
#             if timed_tasks ==[]:
#                 return jsonify(statu='fail', detail='没有找到')
#             else:
#                 assert_result=[list(i) for i in cu.execute('select assert_result from db_run_result where run_id={} and statu={}'.format(job_id, run_type)).fetchall()]
#                 print(assert_result)
#                 for i in assert_result:
#                     if i[0]==0:
#                         fail_case+=1
#                     else:
#                         pass_case+=1
#         elif run_type==0:
#             real_time_run = cu.execute(
#                 'select * from real_time_run where id={} and version_id={}'.format(job_id, version_id)).fetchall()
#             if real_time_run == []:
#                 return jsonify(statu='fail', detail='没有找到')
#             else:
#                 assert_result = [list(i) for i in cu.execute(
#                     'select assert_result from db_run_result where id={} and statu={}'.format(job_id,
#                                                                                               run_type)).fetchall()]
#                 print(assert_result)
#                 pass_case = 0
#                 fail_case = 0
#                 for i in assert_result:
#                     if i == 0:
#                         fail_case += 1
#                     else:
#                         fail_case += 1
#         else:
#             jsonify(statu='success', detail='run_type错误')
#         pass_rate="{:.0%}".format(math.ceil((pass_case/(pass_case+fail_case))*100)/100)
#         fail_rate="{:.0%}".format(math.ceil((fail_case/(pass_case+fail_case))*100)/100)
#         plt.figure(1, figsize=(9, 4),facecolor='blue')
#
#         plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
#         plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#         # plt.title('接口case通过/失败率')
#         plt.ylabel("case数量")
#         # plt.xlabel("pass/fail状态")
#         x = ['PASS', 'FAIL']
#         y = [pass_case, fail_case]
#         print(max(pass_case,fail_case))
#         plt.xlim(-1, 3)
#         if pass_case<5 and fail_case<5:
#             plt.ylim(0, 5)
#         else:
#             plt.ylim(0, max(pass_case,fail_case)+2)
#         plt.bar(range(len(x)), y,width=0.3, color='gr', tick_label=x,)
#         # 添加数据标签
#         for a, b,c in zip(range(len(x)), y,[pass_rate,fail_rate]):
#             plt.text(a, b + 0.03, "{}".format(c), ha='center', va='bottom', fontsize=7)
#         # plt.legend()
#         # plt.show()
#         basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#         print(basedir)
#         if run_type==1:
#             PATH_PICTURE =os.path.join(basedir,'static','result_pic_job', '{}_{}_task.png'.format(g.user_name,job_id))
#             plt.savefig(os.path.join(basedir,'static','result_pic_job', '{}_{}_task.png'.format(g.user_name,job_id)),
#                         bbox_inches='tight')
#             path_url=request.url_root+'static'+'/result_pic_job'+'/{}_{}_task.png'.format(g.user_name,job_id)
#         if run_type==0:
#             plt.savefig(
#                 os.path.join(basedir, 'static', 'result_pic_job', '{}_{}_real.png'.format(g.user_name, job_id)),
#                 bbox_inches='tight')
#             PATH_PICTURE=os.path.join(basedir, 'static', 'result_pic_job', '{}_{}_real.png'.format(g.user_name, job_id))
#             path_url=request.url_root, 'static', '/result_pic_job', '/{}_{}_real.png'.format(g.user_name, job_id)
#         if request.method=='GET':
#             return jsonify(statu='success', detail=path_url)
#         else:
#             file=open(PATH_PICTURE,'rb')
#             read=file.read()
#             file.close()
#             return jsonify(statu='success', detail=str(read))


# 导入权限接口
@jing_new.route('/Import_permission', methods=['post'])
def import_permission():
    version_id=request.values.get('version_id')
    user=request.values.get('user')
    catalog_list=request.values.get('catalog_list')
    # return jsonify(statu='fail', detail="请求方式错误")
    if flask.request.is_json:
        return jsonify(statu='fail', error_detail='请求格式错误,不是form_data格式')
    elif version_id == None or user==None or catalog_list==None:
        return jsonify(statu='fail', error_detail='请求参数缺失')
    elif version_id == '' or user == '' or catalog_list==None:
        return jsonify(statu='fail', error_detail='请求参数错误')
    else:
        try:
            version_id=int(version_id)
        except:
            return jsonify(statu='fail', error_detail='参数类型错误')
        db=sqlite3.connect(current_app.config.get('CONTIN'))
        cu=db.cursor()
        super_user = current_app.config.get('DB_JURISDICITION').split(',')
        g.user_name='mojingjing'

        s=cu.execute( 'SELECT statu FROM user_jurisdiction WHERE user_name="{}" and version_id={}'.format(g.user_name,version_id)).fetchall()
        if len(s) == 0:
            statu=0
        else:
            statu = s[0][0]
            print(statu)
        create_name=cu.execute( 'SELECT create_name FROM version_detail WHERE create_name="{}" and id={}'.format(g.user_name,version_id)).fetchall()
        print(g.user_name,s,create_name)
        if (g.user_name in super_user) or statu==2 or create_name!=[]:
            db_example = sqlite3.connect(current_app.config.get('DB_DIZHI'))
            cu_example = db_example.cursor()
            name = cu_example.execute('SELECT name FROM user WHERE name="{user}"'.format(user=user)).fetchall()
            print(name)
            db_example.close()
            if len(name) == 0:
                return jsonify(statu='fail', error_detail='用户不存在')
            else:
                statu = cu.execute('SELECT statu FROM user_jurisdiction WHERE user_name="{user_name}"'.format(user_name=user)).fetchall()
                if len(statu)==0:
                    db.close()
                    return jsonify(statu='fail', error_detail='权限表用户不存在')
                else:
                    if statu[0][0] in [1,2]:
                        i=cu.execute('select * from interface_jurisdiction where user_name ="{}" and version_id={} '.format(user,version_id)).fetchall()
                        if len(i)==0:
                            cu.execute(
                                'insert into interface_jurisdiction values(null,?,?,?,?,?) ',(user,version_id,catalog_list,int(time.time()),g.user_name))
                        else:
                            cu.execute(
                                'update interface_jurisdiction set catalog_list="{}",update_time={},update_name="{}" where user_name ="{}" and version_id={}'.format(catalog_list,int(time.time()),g.user_name,user,version_id))
                        db.commit()
                        db.close()
                        return jsonify(statu='success', error_detail=None)
                    else:
                        db.close()
                        return jsonify(statu='fail', error_detail='statu不在12中')
        else:
            db.close()
            return jsonify(statu='fail', error_detail='权限不足')


# 版本删除及case删除
@jing_new.route('/delete_all_data',methods=['POST','GET'])
@cross_origin()
def delete_all_data():
    g.user_name='mojingjing'
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif flask.request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        elif request.form.get('statu') == None or request.form.get('detail') == None:
            return jsonify(statu='fail',detail='请求参数缺失')
        elif request.form.get('statu') == '' or request.form.get('detail') == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            statu = request.form.get('statu')
            detail = request.form.get('detail')
            try:
                statu=int(statu)
                pass
            except:
                return jsonify(statu='fail', detail='参数类型错误')
            a=delete_data(statu,detail)
            return a

            # return jsonify(statu='success', detail=None)



# def delete_data():
def delete_data(statu,detail):

    detail=detail.replace('"','').replace("'","").replace(' ','').replace('[','').replace(']','').split(',')
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    DB_CONFIG_FILE=current_app.config.get('DB_CONFIG_FILE')
    print(DB_CONFIG_FILE)
    if statu==1:
        detail=[int(i) for i in detail]
        if len(detail)>1:
            catalog_version_id=cu.execute('select catalog_id,version_id from case_detail where id in {}'.format(tuple(detail))).fetchall()
        else:
            catalog_version_id = cu.execute(
                'select catalog_id,version_id from case_detail where id = {}'.format(tuple(detail)[0])).fetchall()
        print(catalog_version_id)
        data1={}
        for i,j in enumerate(catalog_version_id):
            if i==0 or j[1] not in data1.keys():
                data1[j[1]]=[]
                list1=[]
                list1.append(j[0])
                data1[j[1]]=list1
            else:
                if j[0] not in data1[j[1]]:
                    data1[j[1]].append(j[0])
        print(data1)
        for k,v in data1.items():

            interface_jurisdiction = cu.execute(
                'select catalog_list from interface_jurisdiction where user_name ="{}" and version_id={} '.format(
                    g.user_name, k)).fetchall()
            if len(interface_jurisdiction) != 0:
                catalog_list = interface_jurisdiction[0][0].replace('[', '').replace(']', '').replace("'", "").replace(
                    ' ', '').replace('"', '').split(',')
                catalog_list = [int(i) for i in catalog_list]
                for c_id in v:
                    if c_id in catalog_list:
                        pass
                    else:
                        db.close()
                        return jsonify(statu='fail', detail='没有权限')

            else:
                db.close()
                return jsonify(statu='fail', detail='没有权限')
        # 查询是否存在运行中的任务
        version_list=[i for i in data1.keys()]
        print(version_list)
        if len(version_list)>1:
            a=cu.execute(
                'select * from real_time_run where  version_id in {} and statu=1'.format(tuple(version_list))).fetchall()
            b=cu.execute(
                'select * from timed_tasks where  version_id in {} and statu=1'.format(tuple(version_list))).fetchall()
        else:
            a = cu.execute(
                'select * from real_time_run where  version_id = {} and statu=1'.format(
                    tuple(version_list)[0])).fetchall()
            b = cu.execute(
                'select * from timed_tasks where  version_id = {} and statu=1'.format(tuple(version_list)[0])).fetchall()

        if len(a)==0 and len(b)==0:
            pass
        else:
            db.close()
            return jsonify(statu='fail', detail='存在运行中的任务，不能删除')
        cu.execute('delete from case_detail where id in {}'.format(tuple(detail)))
        db.commit()
        return jsonify(statu='success', detail=None)
    elif statu==0:
        #是否有权限删除
        for k in detail:
            interface_jurisdiction = cu.execute(
                'select catalog_list from interface_jurisdiction where user_name ="{}" and version_id={} '.format(
                    g.user_name, k)).fetchall()
            print(interface_jurisdiction)
            if len(interface_jurisdiction) != 0:
                pass
            else:
                db.close()
                return jsonify(statu='fail', detail='没有权限')
        # 查询是否存在运行中的任务
        if len(detail)>1:
            a=cu.execute(
                'select * from real_time_run where  version_id in {} and statu=1'.format(tuple(detail))).fetchall()
            b=cu.execute(
                'select * from timed_tasks where  version_id in {} and statu=1'.format(tuple(detail))).fetchall()
        else:
            a = cu.execute(
                'select * from real_time_run where  version_id = {} and statu=1'.format(
                    tuple(detail)[0])).fetchall()
            b = cu.execute(
                'select * from timed_tasks where  version_id = {} and statu=1'.format(tuple(detail)[0])).fetchall()
        if len(a) == 0 and len(b) == 0:
            pass
        else:
            db.close()
            return jsonify(statu='fail', detail='存在运行中的任务，不能删除')
        #进行删除
        a = [i[0] for i in cu.execute(
            'select id from real_time_run where  version_id in {}'.format(tuple(detail))).fetchall()]
        b = [i[0] for i in cu.execute(
            'select id from timed_tasks where  version_id in {} '.format(tuple(detail))).fetchall()]
        a.extend(b)
        print(a)
        cu.execute('delete from case_detail where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from catalog_detail where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from data_statistics where version_id in {}'.format(tuple(detail)))

        cu.execute('delete from db_run_result where run_id in {}'.format(tuple(a)))

        cu.execute('delete from interface_detail where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from interface_jurisdiction where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from private_config_detail where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from publick_detail where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from real_time_run where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from timed_tasks where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from user_jurisdiction where version_id in {}'.format(tuple(detail)))
        cu.execute('delete from version_detail where id in {}'.format(tuple(detail)))
        db.commit()
        db.close()
        for version_id in os.listdir(DB_CONFIG_FILE):
            print(version_id)
            if int(version_id) in detail:
                # os.rmdir(os.path.join(DB_CONFIG_FILE,version_id))
                shutil.rmtree(os.path.join(DB_CONFIG_FILE,version_id))
        print(os.listdir(DB_CONFIG_FILE))
        return jsonify(statu='success', detail=None)



#通过率图片接口
@jing_new.route('/pass_rate_image_interface',methods=['POST','GET'])
def pass_rate_image_interface():
    version_id=request.values.get('version_id')
    job_id=request.values.get('job_id')
    run_type=request.values.get('run_type')
    print (1111111111111111111111111111111111111111)
    print(version_id,job_id,run_type)
    # return jsonify(statu='fail', detail="请求方式错误")
    if flask.request.is_json:
        return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
    elif version_id == None or job_id==None or run_type==None:
        return jsonify(statu='fail', detail='请求参数缺失')
    elif version_id == '' or job_id == '' or run_type==None:
        return jsonify(statu='fail', detail='请求参数错误')
    else:
        try:
            version_id=int(version_id)
            run_type=int(run_type)
            job_id=int(job_id)
        except:
            return jsonify(statu='fail', detail='参数类型错误')
        db=sqlite3.connect(current_app.config.get('CONTIN'))
        cu=db.cursor()
        pass_case = 0
        fail_case = 0
        if run_type==1:
            timed_tasks=cu.execute('select * from timed_tasks where id={} and version_id={}'.format(job_id,version_id)).fetchall()
            if timed_tasks ==[]:
                return jsonify(statu='fail', detail='没有找到')
            else:
                assert_result=[list(i) for i in cu.execute('select interface_id,assert_result from db_run_result where run_id={} and statu={}'.format(job_id, run_type)).fetchall()]
                all_pass=cu.execute('select interface_id,count(*) from db_run_result where run_id={} and statu={} and assert_result=1 group by interface_id'.format(job_id, run_type)).fetchall()
                print(assert_result)
                for k,i in assert_result:
                    if i[0]==0:
                        fail_case+=1
                    else:
                        pass_case+=1
        elif run_type==0:
            real_time_run = cu.execute(
                'select * from real_time_run where id={} and version_id={}'.format(job_id, version_id)).fetchall()
            if real_time_run == []:
                return jsonify(statu='fail', detail='没有找到')
            else:
                assert_result = [list(i) for i in cu.execute(
                    'select assert_result from db_run_result where id={} and statu={}'.format(job_id,
                                                                                              run_type)).fetchall()]
                print(assert_result)
                pass_case = 0
                fail_case = 0
                for i in assert_result:
                    if i == 0:
                        fail_case += 1
                    else:
                        fail_case += 1
        else:
            jsonify(statu='success', detail='run_type错误')
        pass_rate="{:.0%}".format(math.ceil((pass_case/(pass_case+fail_case))*100)/100)
        fail_rate="{:.0%}".format(math.ceil((fail_case/(pass_case+fail_case))*100)/100)
        plt.figure(1, figsize=(9, 4),facecolor='blue')

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # plt.title('接口case通过/失败率')
        plt.ylabel("case数量")
        # plt.xlabel("pass/fail状态")
        x = ['PASS', 'FAIL']
        y = [pass_case, fail_case]
        print(max(pass_case,fail_case))
        plt.xlim(-1, 3)
        if pass_case<5 and fail_case<5:
            plt.ylim(0, 5)
        else:
            plt.ylim(0, max(pass_case,fail_case)+2)
        plt.bar(range(len(x)), y,width=0.3, color='gr', tick_label=x,)
        # 添加数据标签
        for a, b,c in zip(range(len(x)), y,[pass_rate,fail_rate]):
            plt.text(a, b + 0.03, "{}".format(c), ha='center', va='bottom', fontsize=7)
        # plt.legend()
        # plt.show()
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        print(basedir)
        if run_type==1:
            PATH_PICTURE =os.path.join(basedir,'static','result_pic_job', '{}_{}_task.png'.format(g.user_name,job_id))
            plt.savefig(os.path.join(basedir,'static','result_pic_job', '{}_{}_task.png'.format(g.user_name,job_id)),
                        bbox_inches='tight')
            path_url=request.url_root+'static'+'/result_pic_job'+'/{}_{}_task.png'.format(g.user_name,job_id)
        if run_type==0:
            plt.savefig(
                os.path.join(basedir, 'static', 'result_pic_job', '{}_{}_real.png'.format(g.user_name, job_id)),
                bbox_inches='tight')
            PATH_PICTURE=os.path.join(basedir, 'static', 'result_pic_job', '{}_{}_real.png'.format(g.user_name, job_id))
            path_url=request.url_root, 'static', '/result_pic_job', '/{}_{}_real.png'.format(g.user_name, job_id)
        if request.method=='GET':
            return jsonify(statu='success', detail=path_url)
        else:
            file=open(PATH_PICTURE,'rb')
            read=file.read()
            file.close()
            return jsonify(statu='success', detail=str(read))

