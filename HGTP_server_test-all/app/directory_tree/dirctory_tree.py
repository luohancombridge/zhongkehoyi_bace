# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
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
directory_tree_new = Blueprint('tree',__name__)
#增加节点
@directory_tree_new.route('/get_tree',methods=['POST','GET'])
@cross_origin()
def get_tree():
    if 'user_name' not in list(session.keys()):
        conn = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cur = conn.cursor()
        user = cur.execute('select name from user where ip="%s"' % (request.headers.get('X-Real-IP'))).fetchall()[0][0]
        conn.close()
        session['user_name']=user
    else:
        user=session['user_name']
    tree_resources = request.form['tree_resources']
    tree_type=request.form['tree_type']
    conn= sqlite3.connect(current_app.config.get('JIE_KOU'))
    cur = conn.cursor()
    create_time=int(time.time())
    tree_name=request.form['tree_name']
    if  len(cur.execute('select * from directory_tree where  classification_name="%s"'  % (tree_name)).fetchall())>0:
        return jsonify(statu='error',detail="节点名重复")
    if tree_type.strip()=='添加顶级节点':
          parent_name = ''
          node_level=0
    elif tree_type.strip()=='编辑节点':
        parent_name,node_id,parent_level=cur.execute('select parent_name,id,Node_level from directory_tree where  classification_name="%s"'  % (tree_resources)).fetchall()[0]
        if tree_type.strip() == '添加同级节点':
            parent_name=parent_name
            node_level=parent_level
        elif tree_type.strip() == '添加子节点':
            parent_name = tree_resources
            node_level=int(parent_level)+1
    if tree_type.strip() != '编辑节点':
        cur.executemany('INSERT INTO directory_tree VALUES (null,?,?,?,?,?,?,?)',
                       [(request.form['tree_name'],parent_name,create_time,create_time,user,user,node_level)])
    else:
        cur.execute('UPDATE directory_tree SET classification_name=?,update_user=?,update_time=? WHERE classification_name=?',
                     (tree_name,session['user_name'],int(time.time()),tree_resources))
        cur.execute(
            'UPDATE directory_tree SET parent_name=?,update_user=?,update_time=? WHERE parent_name=?',
            (tree_name, session['user_name'], int(time.time()), tree_resources))
    conn.commit()
    all_detail=cur.execute('select classification_name,Node_level,parent_name,id from directory_tree ').fetchall()
    all_detail=sorted(all_detail,key=lambda all_detail_value:  all_detail_value[1],reverse=True)
    all_node=[]
    z_node=[]
    for k,i in enumerate(all_detail):
        if i[0] not in all_node:
            if  i[2]=='':
                all_node.append(i[0])
                z_node.append({"text": i[0]})
            elif i[2] not in all_node:
                all_node.append(i[2])
                z_node.append({"text": i[2],"nodes":[{"text": i[0]}]})
            elif i[2]  in all_node:
                this_index= all_node.index(i[2])
                z_node[this_index]['nodes'].append({"text": i[0]})
        else:
            if i[2]!='':
               z_node[all_node.index(i[0])]={"text":i[2],"nodes":[ z_node[all_node.index(i[0])]]}
               all_node[all_node.index(i[0])] = i[2]
    conn.close()
    return jsonify(statu='success',detail="success",z_node=z_node)
#查询节点
@directory_tree_new.route('/query_node',methods=['POST','GET'])
@cross_origin()
def query_node():
    conn= sqlite3.connect(current_app.config.get('JIE_KOU'))
    cur = conn.cursor()
    # all_detail=cur.execute('select classification_name from directory_tree where Node_level=0').fetchall()
    # all_node=[]
    # for k,i in enumerate(all_detail):
    #     all_node.append({"text":i})

    all_detail=cur.execute('select classification_name,Node_level,parent_name,id from directory_tree ').fetchall()
    all_detail=sorted(all_detail,key=lambda all_detail_value:  all_detail_value[1],reverse=True)
    all_node=[]
    z_node=[]
    for k,i in enumerate(all_detail):
        if i[0] not in all_node:
            if  i[2]=='':
                all_node.append(i[0])
                z_node.append({"text": i[0]})
            elif i[2] not in all_node:
                all_node.append(i[2])
                z_node.append({"text": i[2],"nodes":[{"text": i[0]}]})
            elif i[2]  in all_node:
                this_index= all_node.index(i[2])
                z_node[this_index]['nodes'].append({"text": i[0]})
        else:
            if i[2]!='':
               z_node[all_node.index(i[0])]={"text":i[2],"nodes":[ z_node[all_node.index(i[0])]]}
               all_node[all_node.index(i[0])] = i[2]
    return jsonify(all_detail=z_node)







#接口目录信息数据存入表中
@directory_tree_new.route('/query_jiekou',methods=['POST','GET'])
@cross_origin()
def query_jiekou():
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    # all_detail=cur.execute('select classification_name from directory_tree where Node_level=0').fetchall()
    # all_node=[]
    # for k,i in enumerate(all_detail):
    #     all_node.append({"text":i})
    return jsonify(a="success")



@directory_tree_new.route('/save_private_config',methods=['POST','GET'])
@cross_origin()
def save_private_config():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif request.is_json:
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
            jiekou_id_config={}
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            for base_path in private_config:
                for f, v1 in private_config[base_path].items():
                    first_path = f
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
                                    db.commit()
                                    db.close()
                                    return jsonify(statu='fail', detail='{},{},{}不存在'.format(first_path, second_path,third_path))
                                else:
                                    # 先把数据记录在表中
                                    data1 = {'mulu_id': mulu_id[0][0], 'jiekou_id':jiekou_id[0][0],'first_path': first_path, 'second_path': second_path,
                                             'third_path': third_path, 'configparse': configparse, 'json': json_con}
                                    list1.append(data1)
                                    if mulu_jiekou_id.get(mulu_id[0][0])!=None:
                                        jiekou_id_ji=mulu_jiekou_id[mulu_id[0][0]]
                                        jiekou_id_ji.append(jiekou_id[0][0])
                                        mulu_jiekou_id[mulu_id[0][0]]=jiekou_id_ji
                                    else:
                                        jiekou_id_ji=[]
                                        jiekou_id_ji.append(jiekou_id[0][0])
                                        mulu_jiekou_id[mulu_id[0][0]]=jiekou_id_ji
            for k, y in mulu_jiekou_id.items():
                # cu.execute('delete from private_config_detail where catalog_id={} and interface_id not in{} and version_id={}'.format(k,tuple(y),version_id))
                for p in y:
                     cu.execute('delete from private_config_detail where catalog_id={} and interface_id={} and version_id={}'.format(k,p,version_id))
                db.commit()
            for i in list1:
                time_new=time.time()
                cu.executemany('INSERT INTO private_config_detail VALUES (?,?,?,?,?,?,?,?,?,?)', [
                        (None,i['mulu_id'], version_id, i['jiekou_id'], json.dumps(i['configparse']), i['json'], int(time.time()), g.user_name,
                         '','')])
            db.commit()
            db.close()
            return jsonify(statu='success', detail=None)

@directory_tree_new.route('/get_interface_detail',methods=['POST','GET'])
def get_interface_detail():
        if g.user_name in (None,''):
            return jsonify(status='fail', detail="未登录")
        elif request.is_json:
            return jsonify(statu='fail', detail='请求格式错误,不是form_data格式')
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()


@directory_tree_new.route('/case_db_run',methods=['POST','GET'])
@case_db_run
def case_db_run():
        pass



# 版本名查询接口
@directory_tree_new.route('/update_version', methods=['post'])
def update_version():
        version_id = request.form['version_id']
        version_name = request.form['version_name']
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        user = cu.execute('select * from version_detail where version_name="%s"' % (version_name)).fetchall()
        if len(user)>0:
            return jsonify(statu="fail",detail="版本名重复")
        cu.execute(
            'UPDATE version_detail SET version_name=?,update_name=?,update_time=? WHERE id=?',
            (version_name, g.user_name, int(time.time()), version_id))
        db.commit()
        db.close()
        return jsonify(statu="success")
# 版本号删除接口
@directory_tree_new.route('/delete_interface', methods=['post'])
def delete_interface():
        if g.user_name == None:
            return json.dumps({'statu': 'fail', 'detail': '请登录!'}, ensure_ascii=False)
        else:
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cur = db.cursor()
            data=json.loads(request.get_data(as_text=True))
            id_sql = cur.execute('SELECT id FROM version_detail').fetchall()
            id = int(data['id'])
            sql = 'SELECT statu,create_name FROM version_detail WHERE  id="{version_id}"'.format(user_name=g.user_name,version_id=id)
            run_statu,create_user=cur.execute(sql).fetchall()[0]
            super_user=current_app.config.get('DB_JURISDICITION').split(',')
            if g.user_name !=create_user and g.user_name not in super_user:
               cur.close()
               return jsonify(statu="fail",detail="用户无该操作权限")
            elif run_statu in [1,2,3]:
                cur.close()
                return jsonify(statu="fail", detail="有操作正在执行")
            else :
                            cur.execute('DELETE FROM version_detail WHERE id={id}'.format(id=id))
                            cur.execute('DELETE FROM catalog_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM interface_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM private_config_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM publick_detail WHERE version_id={id}'.format(id=id))
                            db.commit()
                            db.close()
                            return json.dumps({'statu': 'success', 'detail': 'None'}, ensure_ascii=False)

# 版本号删除接口
@directory_tree_new.route('/delete_version', methods=['post'])
def DeleteVersion():
        if g.user_name == None:
            return json.dumps({'statu': 'fail', 'detail': '请登录!'}, ensure_ascii=False)
        else:
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cur = db.cursor()
            data=json.loads(request.get_data(as_text=True))
            id_sql = cur.execute('SELECT id FROM version_detail').fetchall()
            id = int(data['id'])
            sql = 'SELECT statu,create_name FROM version_detail WHERE  id="{version_id}"'.format(user_name=g.user_name,version_id=id)
            run_statu,create_user=cur.execute(sql).fetchall()[0]
            super_user=current_app.config.get('DB_JURISDICITION').split(',')
            if g.user_name !=create_user and g.user_name not in super_user:
               cur.close()
               return jsonify(statu="fail",detail="用户无该操作权限")
            elif run_statu in [1,2,3]:
                cur.close()
                return jsonify(statu="fail", detail="有操作正在执行")
            else :
                            cur.execute('DELETE FROM version_detail WHERE id={id}'.format(id=id))
                            cur.execute('DELETE FROM catalog_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM interface_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM private_config_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM publick_detail WHERE version_id={id}'.format(id=id))
                            db.commit()
                            db.close()
                            return json.dumps({'statu': 'success', 'detail': 'None'}, ensure_ascii=False)


# 获取权限
@directory_tree_new.route('/get_quanxian', methods=['post'])
@cross_origin()
def get_quanxian():
        user=g.user_name
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cur = db.cursor()
        version_id=request.form['version_id']
        session['quanxian_version']=request.form['version_id']
        all_quanxian=cur.execute('SELECT user_name,statu FROM user_jurisdiction WHERE  version_id="{version_id}"'.format(version_id=version_id)).fetchall()
        create_user=cur.execute('SELECT create_name FROM version_detail WHERE  id="{version_id}"'.format(version_id=version_id)).fetchall()[0][0]
        mulu_detail=cur.execute('SELECT first_catalog,second_catalog,id  FROM catalog_detail WHERE  version_id="{version_id}"'.format(version_id=version_id)).fetchall()
        all_mulu={}
        if len(mulu_detail)>0:
            for z in mulu_detail:
                if z[0] not in all_mulu.keys():
                    all_mulu[z[0]]=[[z[1],z[2]]]
                else:
                    all_mulu[z[0]].append([z[1],z[2]])
        if g.user_name.strip()==create_user.strip():
            statu_this=3
        elif len(all_quanxian)!=0:
            all_quanxian=dict(all_quanxian)
            if g.user_name in all_quanxian.keys():
                statu_this = all_quanxian[user]
            else:
                statu_this = 0
        else:
            statu_this=0
        super_user = current_app.config.get('DB_JURISDICITION').split(',')
        if g.user_name.strip() in super_user:
                statu_this = 3
        return jsonify(statu_this=statu_this,all_quanxian=all_quanxian,all_mulu=all_mulu)

#根据before_request 获取接口信息
@directory_tree_new.route('/case_name_get_detail',methods=['POST','GET'])
@cross_origin()
def get_interface_id_detail():
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            version_id = request.form.get('version_id')
            befor_request_str=request.form['befor_request_str']
            interface_id=request.form['interface_id']
            catalog_id=cu.execute('select catalog_id from case_detail where id=?' % (int(interface_id))).fetchall()[0][0]
            first_mulu=cu.execute('select first_catalog from catalog_detail where id=?' %(int(catalog_id))).fetchall()[0][0]
            try:
                second_mulu,intferface_name=befor_request_str.split('$')[0].split('/')
                case_id=befor_request_str.split('$')[0][1]
            except:
                return  jsonify(statu='fail', detail='前置接口关键字错误')
            this_catalog_id=cu.execute('select id from catalog_detail where first_catalog=? and second_catalog=?' % (first_mulu,second_mulu)).fetchall()[0][0]
            interface_id==cu.execute('select id from catalog_detail where first_catalog=? and second_catalog=?' % (first_mulu,second_mulu)).fetchall()[0][0]
            try:
                int(version_id)
            except:
                return jsonify(statu='fail', detail='参数类型错误')
            result=get_detail(version_id,interface_id)
            return result



def get_detail(version_id,interface_id):
    # version_id=43
    # interface_id='[26,27,28]'
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    interface_id= interface_id.replace('[', '').replace(']', '').split(',')
    detail={}
    for i in interface_id:
        case_detail = cu.execute(
            'select case_detail from case_detail where version_id=? and  interface_id=?',(version_id,i)).fetchall()
        catalog_id = cu.execute(
            'select catalog_id from case_detail where version_id=? and  interface_id=?',(version_id,i)).fetchall()
        if case_detail==[] or catalog_id==[]:
            return jsonify(statu='fail', detail='该接口id或版本号不存在')
        else:
            detail[i]={}
            list1 = []
            for j in case_detail:
                list1.append(json.loads(j[0]))
            # print(list1)
            detail[i]['case_detail']=list1
            #public_detal中读取config,db
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


#根据before_request 获取接口信息
@directory_tree_new.route('/get_real_time_run',methods=['POST','GET'])
@cross_origin()
def get_real_time_run():
            db = sqlite3.connect(current_app.config.get('CONTIN'))
            cu = db.cursor()
            version_id = request.form.get('version_id')
            user_name=g.user_name
            if request.form['type']=="实时":
                get_real_time_data=cu.execute('select * from real_time_run where version_id=%s and name="%s"' % (version_id,user_name)).fetchall()
                return_data = []
                if len(get_real_time_data)==0:
                    return jsonify(return_data=return_data)
                for k ,i in enumerate(get_real_time_data):
                   all_interface=len(list(i[1]))
                   take_time=''
                   if i[12]==0:
                       run_statu="未运行"
                   elif i[12]==1:
                       run_statu="运行中"
                   elif i[12] == 2:
                       user_time=int(i[11])-int(i[10])
                       take_time=str(user_time)
                       run_statu = "运行完毕"
                   sucdess_cas=cu.execute('select count(*) from db_run_result where run_id=%s and statu=1' %(str(i[0]))).fetchall()[0][0]
                   fail_cas = cu.execute(
                       'select count(*) from db_run_result where run_id=%s and statu=0' % (str(i[0]))).fetchall()[0][0]
                   this_list=[]
                   run_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(i[10])))
                   this_list.append(run_time)
                   this_list.append(str(take_time)+'秒')
                   this_list.append(sucdess_cas)
                   this_list.append(fail_cas)
                   this_list.append(len(json.loads(i[1])))
                   this_list.append(run_statu)
                   this_list.append(i[0])
                   return_data.append(this_list)
                return jsonify(get_real_time_data=return_data)
            else:
                get_job_data = cu.execute('select * from timed_tasks where version_id=%s and id="%s"' % (
                version_id, str(request.form['task_job_id']))).fetchall()
                all_jiekou_num= cu.execute('select count(distinct(interface_id)),time from db_run_result where statu=1 and run_id=%s group by time  order by time desc ' % (request.form['task_job_id'])).fetchall()
                pass_num=cu.execute('select count(distinct(interface_id)),count(*),time from db_run_result where statu=1 and run_id=%s and assert_result=1 group by  time order by time desc' % (request.form['task_job_id'])).fetchall()
                fail_num=cu.execute('select count(distinct(interface_id)),count(*),time from db_run_result where statu=1 and run_id=%s and assert_result=0 group by  time order by time desc' % (request.form['task_job_id'])).fetchall()
                return_data=[]
                for k , i in enumerate(all_jiekou_num):
                    timeArray = time.localtime(int(i[1]))
                    run_time = time.strftime("%Y-%m-%d %H:%M", timeArray)
                    pass_num = cu.execute(
                        'select count(distinct(interface_id)),count(*),time from db_run_result where statu=1 and run_id=%s and assert_result=1  and time=%s group by  time order by time desc' % (
                        request.form['task_job_id'],str(i[1]))).fetchall()
                    fail_num = cu.execute(
                        'select count(distinct(interface_id)),count(*),time from db_run_result where statu=1 and run_id=%s and assert_result=0  and time=%s group by  time order by time desc' % (
                        request.form['task_job_id'],str(i[1]))).fetchall()
                    all_jiekou=i[0]
                    if len(pass_num)!=0:
                        pass_num=int(pass_num[0][1])
                    else:
                        pass_num=0
                    if len(fail_num) != 0:
                        fail_num = int(fail_num[0][1])
                    else:
                        fail_num = 0
                    all_case=pass_num+fail_num
                    tongvuolv=str(int((pass_num/all_case)*100))+'%'
                    return_data.append([run_time,all_jiekou,pass_num,fail_num,tongvuolv,i[1]])
                    return jsonify(get_real_time_data=return_data,json_id=request.form['task_job_id'])
#根据before_request 获取接口信息
@directory_tree_new.route('/db_test_reslut',methods=['POST','GET'])
@cross_origin()
def db_test_reslut():
    if request.method == 'POST':
        session['db_run_type']=request.form['db_run_type']
        session['run_id'] = request.form['run_id']
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        if request.form['db_run_type']!='task_time_run':
            run_statu=cu.execute('select statu from  real_time_run where id=%s' %  (request.form['run_id'])).fetchall()[0][0]
            db.close()
            if int(run_statu)==1:
                return jsonify(statu="fail",detail="运行中")
            else:
                return jsonify(statu="success")
        else:
            session['task_run_time']=request.form['run_time']
            return jsonify(statu="success")
    else:
        ip = request.headers.get('X-Real-IP')
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        if session['db_run_type']=="real_time_run":
            all_resul=cu.execute('select * from  db_run_result where run_id=%s' % (str(session['run_id']))).fetchall()
            all_job=cu.execute('select * from  real_time_run where id=%s' % (str(session['run_id']))).fetchall()[0]
            job_start_time=all_job[10]
            job_done_time=all_job[11]
            take_time=str(int(job_start_time-job_done_time))+'秒'
            timeArray = time.localtime(int(job_start_time))
            job_start_time = time.strftime("%Y-%m-%d %H:%M", timeArray)
        else:
            all_resul=cu.execute('select * from  db_run_result where run_id=%s and time=%s' % (str(session['run_id']),str(session['task_run_time']))).fetchall()
            all_job=cu.execute('select * from  timed_tasks where id=%s' % (str(session['run_id']))).fetchall()[0]
            take_time =  '秒'
            job_start_time=time.strftime("%Y-%m-%d %H:%M", time.localtime(int(session['task_run_time'])))
        all_data={}
        all_pass=0
        all_fail=0
        all_num=0
        statu_this_run=0
        for k,i in enumerate(all_resul):
            interface_name=cu.execute('select interface from interface_detail where id=%s' % str(i[1])).fetchall()[0][0]
            if interface_name not in all_data.keys():
                all_data[interface_name]={"common_detial":{"fail_num":0,"pass_num":0,"num":0},"case_detail":[]}
            if 'statu' not in all_data[interface_name]["common_detial"].keys():
                all_data[interface_name]["common_detial"]["statu"]="passClass"
            if int(i[8])==0:
                run_statu="failCase"
                statu_this_run=1
                all_data[interface_name]["common_detial"]["fail_num"]+=1
                all_fail+=1
                all_data[interface_name]["common_detial"]["statu"]="failClass"
            else:
                run_statu = "passCase"
                all_pass+=1
                all_data[interface_name]["common_detial"]["pass_num"] += 1
            all_num+=1
            all_data[interface_name]["common_detial"]["num"] += 1
            # ["passCase", id, i[4], case_assert, result, req, req_url]
            this_data = [run_statu, int(i[3]), i[4], json.dumps(json.loads(i[9]),indent=4), json.dumps(json.loads(i[7]),indent=4), json.dumps(json.loads(i[6]),indent=4), i[5]]
            all_data[interface_name]["case_detail"].append(this_data)
        new_all_data=[]
        for z in all_data:
            num=all_data[z]['common_detial']['num']
            statu=all_data[z]['common_detial']['statu']
            fail_num=all_data[z]['common_detial']['fail_num']
            pass_num=all_data[z]['common_detial']['pass_num']
            this_data=[z,statu,[num,pass_num,fail_num,num,],all_data[z]['case_detail']]
            new_all_data.append(this_data)
        return render_template('/hualala/jiekou_test/test_result_loca_dbl.html',z=new_all_data,take_time=take_time,job_result='none',success=all_pass,fail=all_fail,job_start_time=job_start_time)





        # all=[]
        # all_success=0
        # all_fail=0s
        # if len(all_resul)!=0:
        #      for i in all_resul:
        #          name=i[0]
        #          detail=[]
        #          statu=0
        #          count=len(json.loads(i[2]))
        #          fail=0
        #          succ=0
        #          for k,z in list(json.loads(i[2]).items()):
        #              #result=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int), indent=4, sort_keys=False,
        #                            #ensure_ascii=False)
        #              result=json.dumps(z['respons'],indent=4,ensure_ascii=False)
        #              id=int(k)
        #              if z['case_assert']!='':
        #                  if z['case_assert']=='':
        #                      assert_data=''
        #                  elif '&&' in z['case_assert']:
        #                      assert_data="调用断言函数：%s" % z['case_assert'].split('&&')[-1]
        #                  else:
        #                      try:
        #                          if type(z['case_assert'])  in ['str','unicode']:
        #                              assert_data=json.loads(z['case_assert'])
        #                          else:
        #                              assert_data=z['case_assert']
        #                      except:
        #                          assert_data={"assert_detail":z['case_assert']}
        #              else:
        #                  assert_data=z['case_assert']
        #              case_assert=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(assert_data))), parse_int=int), indent=4,
        #                             sort_keys=False,
        #                             ensure_ascii=False)
        #              comment=z['case_name']
        #              req_url=z['req_url']
        #              req=z['req']
        #              req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
        #                             sort_keys=False,
        #                             ensure_ascii=False)
        #              if z['assert_result']==False:
        #                  statu=1
        #                  fail+=1
        #                  all_fail+=1
        #                  detail.append(["failCase",id,comment,case_assert,result,req,req_url])
        #              else:
        #                  all_success+=1
        #                  succ+=1
        #                  detail.append(["passCase", id, comment, case_assert,result,req,req_url])
        #          detail=sorted(detail,key=lambda x:x[1])
        #          if statu==1:
        #                  all.append([name,"failClass",[count,succ,fail,count],detail])
        #          elif statu==0:
        #                  all.append([name,"passClass", [count, succ, fail, count], detail])
        # #z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        # db.close()
        # return render_template('/hualala/jiekou_test/test_result_local.html',z=all,time=tim,success=all_success,fail=all_fail)
        return render_template('/hualala/jiekou_test/test_result_local.html')


# 运行结果信息保存接口
@directory_tree_new.route('/save_run_case_detail', methods=['POST', 'GET'])
def save_run_case_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        run_type = request.form.get('run_type')
        result_data = request.form.get('result_data')
        run_job_id = request.form.get('run_job_id')
        interface_id = request.form.get('interface_id')
        if run_type == None or result_data == None or run_job_id == None or interface_id == None:
            return jsonify(statu='fail', detail='请求参数缺失')
        elif run_type == '' or result_data == '' or run_job_id == '' or interface_id == '':
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                run_type = int(run_type)
                # interface_id = int(interface_id)
                pass
            except:
                return jsonify(statu='fail', detail='参数类型错误')
            if run_type not in(0,1):
                return jsonify(statu='fail', detail='请求参数错误')
            else:
                if int(run_type)==0:
                   result=sava_run_data(run_job_id,interface_id,result_data,run_type)
                else:
                    result = sava_run_data(run_job_id, interface_id, result_data, run_type, request.form['running_time'])
                return result
def sava_run_data(run_job_id,interface_id,result_data,run_type,*running_time):
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    #[(1, '["1"]', '40', '127.0.0.1', '', '', '', 1, '', 'zhen', 1596003976, '', 0)]
    if int(run_type)==0:
        real_time_run = cu.execute('select * from real_time_run where id={}'.format(run_job_id)).fetchall()
    else:
        real_time_run = cu.execute('select * from timed_tasks where id=%s' % str(run_job_id)).fetchall()
    if real_time_run == []:
        db.close()
        return jsonify(statu='fail', detail='run_job_id不存在')
    else:
        # if run_type==0 and interface_id not in real_time_run[0][1]:
        #         db.close()
        #         return jsonify(statu='fail', detail='接口id不存在')
        # elif run_type==1 and interface_id not in list(real_time_run[0][5]):
        #         db.close()
        #         return jsonify(statu='fail', detail='接口id不存在')
        # else:
            if int(run_type)==0:
                running_time=int(time.time())
            else:
                running_time=int(running_time[0])
                dictince_data=[i[0] for i in cu.execute('select distinct(time) from db_run_result where run_id=%s and statu=1 order by time asc' % str(run_job_id)).fetchall()]
                while  len(dictince_data)>=5:
                      cu.execute('delete from db_run_result where run_id=%s and time=%s '  % (str(run_job_id),str(dictince_data.pop(0))))
                      db.commit()
            # save_run_result(result_data)
            result_data=json.loads(result_data)
            print(result_data)
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
                       (real_time_run[0][2], run_type)).fetchall()
            if a==[]:
                # insert
                cu.execute('insert into  data_statistics values(Null,?,?,?,?,? ,?,?,?)',
                           (real_time_run[0][2],1,interface_pass,interface_fail,cass_fail,case_pass,int(time.time()),run_type ))
                db.commit()
            else:
                cu.execute('update  data_statistics set interface_pass=?,interface_fail=?,case_fail=?,case_pass=?,time=? where version_id=? and statu=?',
                           (int(a[0][3])+interface_pass,int(a[0][4])+interface_fail,int(a[0][5])+cass_fail,int(a[0][6])+case_pass,int(time.time()),real_time_run[0][2], run_type))
                db.commit()
            for i, j in result_data.items():
                if cu.execute('select * from  db_run_result where interface_id=? and run_id=? and case_id=?',
                              (interface_id, run_job_id, i)).fetchall() == [] or int(run_type)==1:
                    cu.execute('insert into  db_run_result values(Null,?,?,?,?,? ,?,?,?,?,?,?)',
                               (interface_id, run_job_id, i, j['case_name'], j['req_url'],json.dumps(j['req'],ensure_ascii=False),
                                json.dumps(j['respons'], ensure_ascii=False), j['assert_result'], json.dumps(j['case_assert']),
                                running_time, run_type))
                    db.commit()
                else:
                    sql=(
                        'update db_run_result set case_name=?,request_url=?,request_detail=?,result_detail=?,assert_result=?,assert_detail=?,time=?,statu=? where interface_id=? and run_id=? and case_id=?',
                        (j['case_name'], j['req_url'], json.dumps(j['req'], ensure_ascii=False),
                         json.dumps(j['respons'], ensure_ascii=False),
                         j['assert_result'], json.dumps(j['case_assert']), running_time, run_type, interface_id,
                         run_job_id, i))
                    print(sql)
                    cu.execute(
                        'update db_run_result set case_name=?,request_url=?,request_detail=?,result_detail=?,assert_result=?,assert_detail=?,time=?,statu=? where interface_id=? and run_id=? and case_id=?',
                        (j['case_name'], j['req_url'], json.dumps(j['req'],ensure_ascii=False),json.dumps(j['respons'], ensure_ascii=False),
                         j['assert_result'], json.dumps(j['case_assert']), running_time, run_type, interface_id, run_job_id,i))
                    db.commit()
            db.close()
            return jsonify(statu='success', detail=None)


@directory_tree_new.route('/running_save_db_detail',methods=['POST'])
def running_save_db_detail():
    if request.method != "POST":
        return jsonify(statu='fail', detail="请求方式错误")
    else:
        update_type=request.form['statu']
        version_id=request.form.get('version_id')
        interface_id=request.form.get('interface_id')
        db_detail=json.loads(request.form.get('db_detail'))
        if version_id == None or interface_id==None or db_detail==None :
            return jsonify(statu='fail', detail='请求参数缺失')
        elif version_id == '' or interface_id == '' or db_detail == '' :
            return jsonify(statu='fail', detail='请求参数错误')
        else:
            try:
                version_id=int(version_id)
                interface_id=int(interface_id)
            except:
                return jsonify(statu='fail', detail='请求参数类型错误')
            db=sqlite3.connect(current_app.config.get('CONTIN'))
            cu=db.cursor()
            catalog=cu.execute('select catalog_id from interface_detail where id={} and version_id={}'.format(interface_id,version_id)).fetchall()
            if catalog!=[]:
                if int(update_type)==1:
                    old_db=cu.execute('select db from   publick_detail  where version_id=? and catalog_id=?',(version_id,catalog[0][0])).fetchall()[0][0]
                    if old_db!='':
                        old_db=json.loads(old_db)
                    for k,i in db_detail.items():
                        if k not in old_db.keys():
                            old_db[k]=db_detail[k]
                        else:
                            for u,b in db_detail[k].items():
                                try:
                                    old_db[k][u]==b
                                except:
                                    pass
                            cu.execute(
                                'update  publick_detail set db=?,update_time=?,update_name=? where version_id=? and catalog_id=?',
                                (json.dumps(old_db, ensure_ascii=False), int(time.time()), g.user_name, version_id,
                                 catalog[0][0]))

                else:
                    cu.execute('update  publick_detail set db=?,update_time=?,update_name=? where version_id=? and catalog_id=?',(json.dumps(db_detail,ensure_ascii=False),int(time.time()),g.user_name,version_id,catalog[0][0]))
                db.commit()
                db.close()
                return jsonify(statu='sucess', detail=None)
            else:
                return jsonify(statu='fail', detail='版本号或接口id不存在')


@directory_tree_new.route('/get_run_statu_all',methods=['POST'])
def get_run_statu_all():
        version_id=request.form.get('version_id')
        user_name=g.user_name
        db=sqlite3.connect(current_app.config.get('CONTIN'))
        cu=db.cursor()
        shishirun_=cu.execute('select * from real_time_run where name="%s" and version_id=%s and statu=1' % (user_name,str(version_id))).fetchall()
        if len(shishirun_)>0:
            shishi_statu=1
        else:
            shishi_statu=0
        dingshi=cu.execute('select * from timed_tasks where create_name="%s" and version_id=%s' % (user_name,str(version_id))).fetchall()
        all_data={}
        all_data['shishi_statu']=shishi_statu
        if len(dingshi)>0:
             for i in dingshi:
                 all_data[i[0]]=int(i[8])
        return jsonify(statu='success',detail=json.dumps(all_data))




#根据before_request 获取接口信息
@directory_tree_new.route('/db_test_reslut_new/<db_run_type>/<run_id>/<send_statu>/<run_time>',methods=['POST','GET'])
@cross_origin()
def db_test_reslut_new(db_run_type,run_id,send_statu,run_time):
        session['run_id']=run_id
        request_url=request.url
        if 'EMAIL_page'  in request.url:
            request_url=request.url.replace('EMAIL_page','web_page').replace('808','5025')
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        if db_run_type!='task_time_run':
            run_statu=cu.execute('select statu from  real_time_run where id=%s' %  (run_id)).fetchall()[0][0]
            db.close()
            if int(run_statu)==1:
                return jsonify(statu="fail",detail="运行中")
        ip = request.headers.get('X-Real-IP')
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        if db_run_type=="real_time_run":
            all_resul=cu.execute('select * from  db_run_result where run_id=%s' % (str(run_id))).fetchall()
            all_job=cu.execute('select * from  real_time_run where id=%s' % (str(run_id))).fetchall()[0]
            job_start_time=all_job[10]
            job_done_time=all_job[11]
            take_time=str(int(job_start_time-job_done_time))+'秒'
            timeArray = time.localtime(int(job_start_time))
            job_start_time = time.strftime("%Y-%m-%d %H:%M", timeArray)
        else:
            all_resul=cu.execute('select * from  db_run_result where run_id=%s and time=%s' % (str(run_id),str(run_time))).fetchall()
            all_job=cu.execute('select * from  timed_tasks where id=%s' % (str(run_id))).fetchall()[0]
            take_time =  '秒'
            job_start_time=time.strftime("%Y-%m-%d %H:%M", time.localtime(int(run_time)))
        all_data={}
        all_pass=0
        all_fail=0
        all_num=0
        statu_this_run=0
        for k,i in enumerate(all_resul):
            interface_name=cu.execute('select interface from interface_detail where id=%s' % str(i[1])).fetchall()[0][0]
            if interface_name not in all_data.keys():
                all_data[interface_name]={"common_detial":{"fail_num":0,"pass_num":0,"num":0},"case_detail":[]}
            if 'statu' not in all_data[interface_name]["common_detial"].keys():
                all_data[interface_name]["common_detial"]["statu"]="passClass"
            if int(i[8])==0:
                run_statu="failCase"
                statu_this_run=1
                all_data[interface_name]["common_detial"]["fail_num"]+=1
                all_fail+=1
                all_data[interface_name]["common_detial"]["statu"]="failClass"
            else:
                run_statu = "passCase"
                all_pass+=1
                all_data[interface_name]["common_detial"]["pass_num"] += 1
            all_num+=1
            all_data[interface_name]["common_detial"]["num"] += 1
            # ["passCase", id, i[4], case_assert, result, req, req_url]
            this_data = [run_statu, int(i[3]), i[4], json.dumps(json.loads(i[9]),indent=4,ensure_ascii=False), json.dumps(json.loads(i[7]),indent=4,ensure_ascii=False), json.dumps(json.loads(i[6]),indent=4,ensure_ascii=False), i[5]]
            all_data[interface_name]["case_detail"].append(this_data)
        new_all_data=[]
        for z in all_data:
            num=all_data[z]['common_detial']['num']
            statu=all_data[z]['common_detial']['statu']
            fail_num=all_data[z]['common_detial']['fail_num']
            pass_num=all_data[z]['common_detial']['pass_num']
            this_data=[z,statu,[num,pass_num,fail_num,num,],all_data[z]['case_detail']]
            new_all_data.append(this_data)
        return render_template('/hualala/jiekou_test/test_result_loca_dbl.html',send_statu=send_statu,z=new_all_data,take_time=take_time,job_result='none',success=all_pass,fail=all_fail,job_start_time=job_start_time,request_url=request_url)





        # all=[]
        # all_success=0
        # all_fail=0s
        # if len(all_resul)!=0:
        #      for i in all_resul:
        #          name=i[0]
        #          detail=[]
        #          statu=0
        #          count=len(json.loads(i[2]))
        #          fail=0
        #          succ=0
        #          for k,z in list(json.loads(i[2]).items()):
        #              #result=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int), indent=4, sort_keys=False,
        #                            #ensure_ascii=False)
        #              result=json.dumps(z['respons'],indent=4,ensure_ascii=False)
        #              id=int(k)
        #              if z['case_assert']!='':
        #                  if z['case_assert']=='':
        #                      assert_data=''
        #                  elif '&&' in z['case_assert']:
        #                      assert_data="调用断言函数：%s" % z['case_assert'].split('&&')[-1]
        #                  else:
        #                      try:
        #                          if type(z['case_assert'])  in ['str','unicode']:
        #                              assert_data=json.loads(z['case_assert'])
        #                          else:
        #                              assert_data=z['case_assert']
        #                      except:
        #                          assert_data={"assert_detail":z['case_assert']}
        #              else:
        #                  assert_data=z['case_assert']
        #              case_assert=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(assert_data))), parse_int=int), indent=4,
        #                             sort_keys=False,
        #                             ensure_ascii=False)
        #              comment=z['case_name']
        #              req_url=z['req_url']
        #              req=z['req']
        #              req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
        #                             sort_keys=False,
        #                             ensure_ascii=False)
        #              if z['assert_result']==False:
        #                  statu=1
        #                  fail+=1
        #                  all_fail+=1
        #                  detail.append(["failCase",id,comment,case_assert,result,req,req_url])
        #              else:
        #                  all_success+=1
        #                  succ+=1
        #                  detail.append(["passCase", id, comment, case_assert,result,req,req_url])
        #          detail=sorted(detail,key=lambda x:x[1])
        #          if statu==1:
        #                  all.append([name,"failClass",[count,succ,fail,count],detail])
        #          elif statu==0:
        #                  all.append([name,"passClass", [count, succ, fail, count], detail])
        # #z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        # db.close()
        # return render_template('/hualala/jiekou_test/test_result_local.html',z=all,time=tim,success=all_success,fail=all_fail)
        return render_template('/hualala/jiekou_test/test_result_local.html')

#删除运行结果
@directory_tree_new.route('/delete_real_run_result_simple',methods=['POST','GET'])
@cross_origin()
def delete_real_run_result_simple():
        run_id=request.form['run_id']
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        cu.execute('delete from db_run_result where run_id=%s'  % (str(run_id)))
        cu.execute('delete from real_time_run where id=%s' % (str(run_id)))
        db.commit()
        return jsonify(statu="success")



#前端页面查看case详情信息
@directory_tree_new.route('/page_get_jiekou_detail',methods=['POST','GET'])
@cross_origin()
def page_get_jiekou_detail():
        jiekou_id=request.form['jiekou_id']
        version_id=request.form['version_id']
        case_id=''
        if 'case_id'  in request.form.keys():
            case_id=request.form['case_id']
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        mulu_id = \
            cu.execute('select catalog_id from interface_detail  where  id=%s ' % (
                str(jiekou_id))).fetchall()[0][0]
        private_detail = \
            cu.execute('select configparse,json from private_config_detail  where catalog_id=%s  and version_id=%s  and interface_id=%s' % (
                str(mulu_id), str(version_id), str(jiekou_id))).fetchall()[0]

        if case_id=='':
            all_case_detail=[list(i) for i in cu.execute('select * from case_detail  where interface_id=%s  and version_id=%s'  % (str(jiekou_id),str(version_id))).fetchall()]
            for k,i  in enumerate(all_case_detail):
                all_case_detail[k][6]=    json.dumps(json.loads(all_case_detail[k][6]), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
            db.close()
            json_moban=json.dumps(json.loads(private_detail[1]), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
            return jsonify(statu="success", all_case_detail=all_case_detail,config_detail=private_detail[0],json_detail=json_moban)
        else:
            case_detail= cu.execute('select case_detail from case_detail  where interface_id=%s  and version_id=%s and id=%s' % (
            str(jiekou_id), str(version_id),str(case_id))).fetchall()[0][0]
            case_detail=json.dumps(json.loads(case_detail), sort_keys=True, indent=4, separators=(',', ': '),ensure_ascii=False)
            db.close()
            return jsonify(statu="success",case_detail=case_detail)
#页面修改case的json
@directory_tree_new.route('/change_case_save',methods=['POST','GET'])
@cross_origin()
def change_case_save():
        case_id=request.form['case_id']
        case_detail=request.form['case_detail']
        try:
            json.loads(case_detail)
        except:
            return jsonify(statu="fail",detail="json各式错误")
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        db.execute("BEGIN TRANSACTION")
        cu.execute('UPDATE case_detail SET case_detail=? WHERE id=?',
                     (case_detail,case_id))
        db.execute("COMMIT")
        db.close()
        return jsonify(statu="success")


#删除运行结果
@directory_tree_new.route('/get_case_detail',methods=['POST','GET'])
@cross_origin()
def get_case_detail():
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        version_id=request.form['version_id']
        case_req=request.form['case_req']
        this_interface_id=request.form['this_interface_id']
        cata_id=cu.execute('select catalog_id from interface_detail where id=%s'  % str(this_interface_id)).fetchall()[0][0]
        first_catalog=cu.execute('select first_catalog from catalog_detail where id=%s'  % str(cata_id)).fetchall()[0][0]
        second_ca,case_name=case_req.split('$')[0].split('/')
        case_id=case_req.split('$')[1]
        ca_id=cu.execute('select id from catalog_detail where first_catalog="%s" and second_catalog="%s" and version_id=%s' %(first_catalog,second_ca,str(version_id))).fetchall()[0][0]
        publick_config,db_config=cu.execute('select config,db from publick_detail where catalog_id=%s and version_id=%s' % (ca_id,version_id)).fetchall()[0]
        interface_id=cu.execute('select id from interface_detail where catalog_id="%s"  and interface="%s"' % (ca_id,case_name)).fetchall()[0][0]
        return_data=cu.execute('select case_id,case_comment,case_detail from case_detail where catalog_id=%s and version_id=%s and interface_id=%s and case_id=%s' % (ca_id,version_id,interface_id,case_id)).fetchall()[0]
        prinvate_conf,private_json=cu.execute('select configparse,json from private_config_detail where catalog_id=%s and version_id=%s and interface_id=%s ' % (ca_id,version_id,interface_id)).fetchall()[0]
        data={
            "prinvate_conf":prinvate_conf,
            "private_json":private_json,
            "publick_conf":publick_config,
            "db_conf":db_config,
            "case_id":return_data[0],
            "case_comment":return_data[1],
            "case_detail": return_data[2]
        }
        return json.dumps(data)

#删除运行结果
@directory_tree_new.route('/save_page_private_config_change',methods=['POST','GET'])
@cross_origin()
def save_page_private_config_change():
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        version_id=request.form['version_id']
        jiekou_id=request.form['jiekou_id']
        config_data=request.form['config']
        json_tem=request.form['json_tem']
        sing_type=request.form['sing_type']
        all_config={"config":{},"sign":{}}
        for k, i in json.loads(config_data).items():
            all_config['config'][k] = i
        all_config['sign']['sign_type']=sing_type
        all_config=json.dumps(all_config)
        db.execute("BEGIN TRANSACTION")
        cu.execute('UPDATE private_config_detail SET configparse=?,json=?,update_time=?,update_name=? WHERE interface_id=?',
                     (all_config,json_tem,str(time.time()),g.user_name,jiekou_id))
        db.execute("COMMIT")
        return jsonify(statu='success')


#删除运行结果
@directory_tree_new.route('/save_data_careate_str',methods=['POST','GET'])
@cross_origin()
def save_data_careate_str():
        create_bianliang_type = request.form['create_bianliang_type']
        if create_bianliang_type=='保存变量':
            bianling_name = request.form['bianliang_name']
            req_type = request.form['type']
            if req_type == 'result':
                req_type = bianling_name + '=' + '["result"]'
                json_str = json.loads(request.form['json_str'])
                uanjian_str = request.form['uanjian_str']
                return_data = save_datai_out(json_str, uanjian_str)
                return_data = [req_type + i for i in return_data]
                return_data = [i.replace('\\', '') for i in return_data]
            else:
                req_type = bianling_name + '=' + '["request"]'
                return_data=req_type+'["'+ request.form['uanjian_str'] +'"]'
        elif create_bianliang_type=='使用变量':
            data_key=request.form['data_key'].strip()
            data_type=request.form['get_data_type_num'].strip()
            return_data=['[data]['+data_key+']['+data_type+']']
            print (111111111111111111)
            print (return_data)
        return jsonify(statu='success',return_data=return_data)

import copy
def get_save_data(a,z,b):
    if type(a)==dict:
        for k,i in a.items():
            if type(i) in [dict,list]:
                this=copy.deepcopy(b)
                this.append(k)
                this_data=get_save_data(i,z,this)
                if this_data:
                   return this_data
            else:
                if k==z:
                    b.append(k)
                    return b
    elif type(a)==list:
        for s,u in enumerate(a):
            if type(u)  in [dict,list]:
                this = copy.deepcopy(b)
                this.append(s)
                this_data=get_save_data(u, z, this)
                if this_data:
                    return this_data
            else:
                if u==z:
                    b.append(s)
                    return b

def save_datai_out(u,b):
    zz=[]
    while True:
        k=get_save_data(u,b,[])
        z=''
        if k!=None:
            for p,i in enumerate(k):
                if p==len(k)-1:
                    c=eval('u'+z)
                    c.pop(i)
                if type(i) !=int:
                    z+='["'+i+'"]'
                else:
                    z+='['+str(i)+']'
            zz.append(z)
        else:
            break
    return zz

#删除运行结果
@directory_tree_new.route('/get_interface_detail_test',methods=['POST','GET'])
@cross_origin()
def get_interface_detail_test():
        db = sqlite3.connect(current_app.config.get('CONTIN'))
        cu = db.cursor()
        try:
                version_id=request.form['version_id']
        except:
            version_id=88
        all_data=cu.execute('select * from catalog_detail where version_id=%s' % (str(version_id))).fetchall()
        print (all_data)
        return jsonify(statu='success',all_data=all_data)