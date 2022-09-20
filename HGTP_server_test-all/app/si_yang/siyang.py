# -*- coding: utf-8 -*-
__author__ = 'wangsiyang'

from flask import Blueprint, jsonify  # 蓝图
import flask

import json
import sqlite3
from fileconfig import CONTIN, DB_DIZHI, DB_JURISDICITION
from flask import g
import time
from flask import current_app, session
from flask_cors import cross_origin

Siyang = Blueprint('common', __name__)


# 新增版本接口
@Siyang.route('/new_version', methods=['post'])
@cross_origin()
def NewVersion():
    if flask.request.is_json:
        if g.user_name == None:
            return json.dumps({'statu': 'fail', 'detail': '请登录!'}, ensure_ascii=False)
        else:
            db = sqlite3.connect(CONTIN)
            cur = db.cursor()
            version_name_sql = cur.execute('SELECT version_name FROM version_detail').fetchall()
            bus_id_sql = cur.execute('SELECT bus_id FROM version_detail').fetchall()
            version_name = flask.request.json.get('version_name')
            bus_id = flask.request.json.get('bus_id')
            for ver in version_name_sql:
                if version_name in list(ver):
                    return
            user_name = g.user_name
            t = int(time.time())
            cur.execute('INSERT INTO version_detail VALUES(NULL,?,?,?,?,?,?,?)',
                        [version_name, bus_id, user_name, t, t, user_name, 0])
            db.commit()
            cur.close()
            db.close()
            return json.dumps({'statu': 'success', 'detail': 'None'}, ensure_ascii=False)
    else:
        return json.dumps({'statu': 'fail', 'detail': '入参请传入json'}, ensure_ascii=False)


# 版本号删除接口
@Siyang.route('/delete_version', methods=['post'])
def DeleteVersion():
    if flask.request.is_json:

        if g.user_name == None:
            return json.dumps({'statu': 'fail', 'detail': '请登录!'}, ensure_ascii=False)
        else:

            db = sqlite3.connect(CONTIN)
            cur = db.cursor()
            id_sql = cur.execute('SELECT id FROM version_detail').fetchall()
            id = int(flask.request.json.get('id'))

            sql = 'SELECT statu FROM user_jurisdiction WHERE user_name="{user_name}"AND version_id="{version_id}"'.format(
                user_name=g.user_name, version_id=id)
            s = cur.execute(sql).fetchall()
            if len(s) == 0:
                pass
            else:
                status = s[0][0]
            if (g.user_name in DB_JURISDICITION.split(',')) or status == 3:
                for i in id_sql:
                    if id in list(i):
                        statu = cur.execute('SELECT statu FROM version_detail WHERE id={id}'.format(id=id)).fetchall()
                        if list(statu[0])[0] == 0:
                            cur.execute('DELETE FROM version_detail WHERE id={id}'.format(id=id))
                            cur.execute('DELETE FROM catalog_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM interface_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM private_config_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM publick_detail WHERE version_id={id}'.format(id=id))
                            cur.execute('DELETE FROM case_detail WHERE version_id={id}'.format(id=id))
                            db.commit()
                            cur.close()
                            db.close()
                            return json.dumps({'statu': 'success', 'detail': 'None'}, ensure_ascii=False)
                        else:
                            return json.dumps({'statu': 'fail', 'detail': 'statu不为0'}, ensure_ascii=False)
                else:
                    return json.dumps({'statu': 'fail', 'detail': '没有找到该版本号'}, ensure_ascii=False)
            else:
                return json.dumps({'statu': 'fail', 'detail': '没有权限'}, ensure_ascii=False)
    else:
        return json.dumps({'statu': 'fail', 'detail': '入参请传入json'}, ensure_ascii=False)


# 版本名查询接口
@Siyang.route('/get_version', methods=['post'])
def GetVersion():
    if flask.request.is_json:
        # if g.user_name == None:
        #     return json.dumps({'statu': 'fail', 'detail': '请登录!'}, ensure_ascii=False)
        # else:
        bus_id = flask.request.json.get('bus_id')
        db = sqlite3.connect(CONTIN)
        cur = db.cursor()

        sql = 'SELECT id,version_name,bus_id FROM version_detail WHERE bus_id={busid}'.format(busid=bus_id)
        id_sql = cur.execute(sql).fetchall()
        print(id_sql)
        if len(id_sql[0]) != 0:
            cur.close()
            db.close()
            res = {
                "id": list(id_sql[0])[0],
                "version_name": list(id_sql[0])[1],
                "bus_id": list(id_sql[0])[2]
            }
            return json.dumps({'statu': 'success', 'detail': res}, ensure_ascii=False)
        else:
            return json.dumps({'statu': 'fail', 'detail': '没有找到版本名'}, ensure_ascii=False)

    else:
        return json.dumps({'statu': 'fail', 'detail': '入参请传入json'}, ensure_ascii=False)


# 接口列表信息存储
@Siyang.route('/save_interface', methods=['post'])
def saveinterface():
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    t = int(time.time())
    id = flask.request.values.get('id')
    interface_detail = flask.request.values.get('interface_detail')
    interface_detail_dic = json.loads(interface_detail)
    # interface_detail = {"inerface_list": "{\".DS_Store\": \".DS_Store\", \"CRM接口重构\": {\".DS_Store\": \".DS_Store\", \"公海门店\": {\"config.txt\": \"config.txt\", \"db.txt\": \"db.txt\", \"01_我的门店列表接口\": {\"01_我的门店列表接口.xls\": \"01_我的门店列表接口.xls\", \"json.txt\": \"json.txt\", \"configparse.txt\": \"configparse.txt\"}}}}", "error_detail": null, "statu": "success"}
    # res = {"CRM接口重构": {"公海门店": {"01_我的门店列表接口": {"01_我的门店列表接口.xls": "01_我的门店列表接口.xls", "json.txt": "json.txt",
    #                                             "configparse.txt": "configparse.txt"}, "db.txt": "db.txt",
    #                             "config.txt": "config.txt"}, ".DS_Store": ".DS_Store"}, ".DS_Store": ".DS_Store"}
    res = interface_detail_dic

    for k1 in res.keys():
        if list(k1)[0] == '.':
            pass
        else:
            for k2 in res[k1].keys():
                if list(k2)[0] == '.':
                    pass
                else:
                    print(k2)
                    # print(res[k1][k2])
                    # print(res[k1][k2].keys())
                    for k in res[k1][k2].keys():
                        if k == 'db.txt' or k == 'config.txt':
                            pass
                        else:
                            jiekou = k
                            sql = 'SELECT id FROM catalog_detail WHERE version_id={id} AND first_catalog="{k1}" AND second_catalog="{k2}"'.format(
                                id=id, k1=k1, k2=k2)
                            catalog = cur.execute(sql).fetchall()
                            try:
                               catalog_id = list(catalog[0])[0]
                            except:
                                pass
                            if len(catalog) == 0 or catalog_id == None:
                                cur.close()
                                db.close()
                                return json.dumps({'statu': 'fail', 'detail': 'catalog_id不存在'}, ensure_ascii=False)
                            else:
                                sql = 'SELECT id FROM interface_detail WHERE catalog_id={catalog_id} AND interface="{interface}" AND version_id="{version_id}"'.format(
                                    version_id=id, catalog_id=catalog_id, interface=jiekou)
                                return_data = cur.execute(sql).fetchall()
                                user_name = g.user_name
                                if len(return_data) > 0:
                                    sql = "update interface_detail set interface='{}',update_time='{}',update_name='{}' where version_id='{}' and catalog_id='{}' and interface='{}'".format(
                                        jiekou, time.time(), user_name, id, catalog_id, jiekou)
                                    cur.execute(sql)
                                    db.commit()
                                else:
                                    cur.execute('INSERT INTO interface_detail VALUES (NULL,?,?,?,?,?,?,?)',
                                                [catalog_id, jiekou, id, t, user_name, '', ''])
                                    db.commit()
    db.close()
    return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)


# 操作权限接口
@Siyang.route('/user_jurisdiction', methods=['post'])
@cross_origin()
def userjurisdiction():
    db_example = sqlite3.connect(DB_DIZHI)
    cur_db_example = db_example.cursor()
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    user_name = g.user_name
    # user_name = 'wangsiyang'
    if 'quanxian_version' not in session.keys():
        return jsonify(statu="fail", detail="缓存中找不到修改权限的version_id")
    else:
        version_id = session['quanxian_version']
    user = flask.request.values.get('user')
    statuss = flask.request.values.get('statu')
    db_jurisdicition_list = DB_JURISDICITION.split(',')
    t = int(time.time())
    sql = 'SELECT statu FROM user_jurisdiction WHERE user_name="{user_name}"'.format(user_name=user_name)
    s = cur.execute(sql).fetchall()
    if len(s) == 0:
        pass
    else:
        status = s[0][0]
    create_user='SELECT create_name FROM version_detail WHERE id="{version_id}"'.format(version_id=version_id)
    create_user=cur.execute(create_user).fetchall()[0][0]
    if g.user_name.strip()==create_user.strip():
        status=3
    if (user_name in db_jurisdicition_list) or status in [3, 2]:
        n = cur_db_example.execute('SELECT name FROM user WHERE name="{user}"'.format(user=user)).fetchall()
        if len(n) == 0:
            return json.dumps({'statu': 'fail', 'detail': '用户不存在'}, ensure_ascii=False)
        else:
            statu = cur.execute(
                'SELECT statu FROM user_jurisdiction WHERE version_id={version_id} AND user_name="{user}"'.format(
                    version_id=version_id, user=user)).fetchall()
            if len(statu) != 0:
                sql = 'UPDATE user_jurisdiction SET statu={} WHERE user_name="{}"'.format(statuss, user)
                cur.execute(sql).fetchall()

            else:
                cur.execute('INSERT INTO user_jurisdiction VALUES (NULL ,?,?,?,?,?)',
                            [user, version_id, statuss, t, user_name])
            db.commit()
            db.close()
            return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)

    else:
        return json.dumps({'statu': 'fail', 'detail': '权限不足'}, ensure_ascii=False)


# 根据interface_id获取接口信息
@Siyang.route('/get_interface_detail_run', methods=['post'])
@cross_origin()
def getinterfacedetail():
    status = flask.request.values.get('statu')
    id = flask.request.values.get('id')  # interface_id
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    detail = {}
    sql = "select catalog_id,interface,version_id from interface_detail WHERE id={id}".format(id=id)
    res_interface = cur.execute(sql).fetchall()
    if len(res_interface) == 0:
        db.commit()
        db.close()
        return json.dumps({'statu': 'fail', 'detail': 'interface_id不存在'}, ensure_ascii=False)
    else:
        interface_detail = {
            "catalog_id": res_interface[0][0],
            "interface": res_interface[0][1],
            "version_id": res_interface[0][2]
        }
        detail['interface_detail'] = interface_detail

    catalog_id = res_interface[0][0]
    sql = "select config,db from publick_detail WHERE catalog_id={catalog_id}".format(catalog_id=catalog_id)
    res_public = cur.execute(sql).fetchall()
    if len(res_public) == 0:
        db.commit()
        db.close()
        return json.dumps({'statu': 'fail', 'detail': 'public_config为空'}, ensure_ascii=False)
    else:
        public_config = {
            "config": json.loads(res_public[0][0]),
            "db": json.loads(res_public[0][1])
        }
        detail['public_config'] = public_config

    sql = "select configparse,json from private_config_detail WHERE interface_id={id}".format(id=id)
    res_private = cur.execute(sql).fetchall()
    if len(res_private) == 0:
        db.commit()
        db.close()
        return json.dumps({'statu': 'fail', 'detail': 'private_config为空'}, ensure_ascii=False)
    else:
        private_config = {
            "configparse": json.loads(res_private[0][0]),
            "json": json.loads(res_private[0][1])
        }
        detail['private_config'] = private_config

    sql = "select id,case_detail from case_detail where interface_id={id}".format(id=id)
    res_case = cur.execute(sql).fetchall()
    if len(res_case) == 0:
        return json.dumps({'statu': 'fail', 'detail': 'case_detail为空'}, ensure_ascii=False)
    else:
        case_detail = {}
        for i in range(len(res_case)):
            case_detail[res_case[i][0]] = res_case[i][1]

        detail['case_detail'] = case_detail
    db.commit()
    db.close()
    return json.dumps({'statu': 'success', 'detail': detail}, ensure_ascii=False)


# 配置文件修改
@Siyang.route('/running_save_config', methods=['post'])
@cross_origin()
def runningsaveconfig():
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    status = int(flask.request.values.get('status'))
    config_type = flask.request.values.get('config_type')
    detail = flask.request.values.get('detail')
    interface_id = flask.request.values.get('interface_id')
    version_id = flask.request.values.get('version_id')
    sql = 'select catalog_id from interface_detail WHERE id={interface_id}'.format(interface_id=interface_id)
    res = cur.execute(sql).fetchall()
    if len(res) == 0:
        return json.dumps({'statu': 'fail', 'detail': 'interface_id不存在'}, ensure_ascii=False)
    else:
        catalog_id = res[0][0]
        if status == 1:
            if config_type == 'config':
                cur.execute(
                    'update publick_detail SET config="{detail}" WHERE version_id={version_id} and catalog_id={catalog_id}'.format(
                        detail=detail, version_id=version_id, catalog_id=catalog_id)).fetchall()
                db.commit()
                db.close()
                return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)
            elif config_type == 'db':
                cur.execute(
                    'update publick_detail SET db="{detail}" WHERE version_id={version_id} and catalog_id={catalog_id}'.format(
                        detail=detail, version_id=version_id, catalog_id=catalog_id)).fetchall()
                db.commit()
                db.close()
                return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)
            else:
                return json.dumps({'statu': 'fail', 'detail': '公共配置文件类型错误'}, ensure_ascii=False)

        elif status == 2:
            if config_type == 'configparse':
                cur.execute(
                    'UPDATE private_config_detail SET configparse="{configparse}" WHERE version_id={version_id} and interface_id={interface_id}'.format(
                        configparse=detail, version_id=version_id, interface_id=interface_id))
                db.commit()
                db.close()
                return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)
            elif config_type == 'json':
                cur.execute(
                    'UPDATE private_config_detail SET json="{detail}" WHERE version_id={version_id} and interface_id={interface_id}'.format(
                        detail=detail, version_id=version_id, interface_id=interface_id))
                db.commit()
                db.close()
                return json.dumps({'statu': 'success', 'detail': None}, ensure_ascii=False)

            else:
                return json.dumps({'statu': 'fail', 'detail': '私有配置文件类型错误'}, ensure_ascii=False)

        else:
            return json.dumps({'statu': 'fail', 'detail': 'status错误'}, ensure_ascii=False)


# 接口运行排序接口
@Siyang.route('/run_sort', methods=['post'])
@cross_origin()
def runsort():
    interface_list = flask.request.values.get('interface_list').split(',')
    run_sort = []
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    for interface_id in interface_list:

        result = find(int(interface_id), run_sort)
        if result == True:
            pass
        else:

            sql = 'select catalog_id from interface_detail WHERE id={id}'.format(id=interface_id)
            catalog_res = cur.execute(sql).fetchall()
            if catalog_res == []:
                return json.dumps({'statu': 'fail', 'detail': '没有目录ID'}, ensure_ascii=False)
            else:
                catalog_id = catalog_res[0][0]
                sql = 'select first_catalog from catalog_detail WHERE id={catalog}'.format(catalog=catalog_id)
                res = cur.execute(sql).fetchall()
                if res == []:
                    return json.dumps({'statu': 'fail', 'detail': '目录错误'}, ensure_ascii=False)
                else:
                    first_catalog = res[0][0]

                    sql = 'select case_id from case_detail WHERE interface_id={interface_id}'.format(
                        interface_id=interface_id)
                    case_id_res = cur.execute(sql).fetchall()

                    if case_id_res == []:
                        return json.dumps({'statu': 'fail', 'detail': '没有要执行的case'}, ensure_ascii=False)
                    else:
                        for caseid in case_id_res:
                            case_id = caseid[0]
                            sort_list = []
                            sort_list.append(interface_id)
                            case_detail_res = cur.execute(
                                'SELECT case_detail,version_id FROM case_detail WHERE case_id={id} and interface_id={interfaceid}'.format(
                                    id=case_id, interfaceid=interface_id)).fetchall()
                            if len(case_detail_res) == 0:
                                return json.dumps({'statu': 'fail', 'detail': 'interface_list错误'}, ensure_ascii=False)
                            else:
                                case_detail = json.loads(case_detail_res[0][0])
                                sort(case_detail, sort_list, first_catalog)
                                run_sort.append(sort_list)
    return json.dumps({'statu': 'success', 'detail': run_sort}, ensure_ascii=False)


def sort(case_detail, sort_list, first_catalog):
    db = sqlite3.connect(CONTIN)
    cur = db.cursor()
    before_list = []

    for k in case_detail.keys():
        if k == 'before_request':
            before_list.append(case_detail[k])
    if len(before_list) == 1:  # 有before_request
        for before_request in before_list:
            mulu = before_request.split('/')[0]
            sql = 'select version_id from catalog_detail WHERE first_catalog="{firstmulu}" and second_catalog="{mulu}"'.format(
                firstmulu=first_catalog, mulu=mulu)
            sql_res = cur.execute(sql).fetchall()
            if sql_res == []:
                return json.dumps({'statu': 'fail', 'detail': '二级目录没有找到version_id'}, ensure_ascii=False)
            else:
                ver = sql_res[0][0]
                interface_name = before_request.split('/')[1].split('$')[0]
                case_id = before_request.split('/')[1].split('$')[1]
                sql = 'select id from interface_detail WHERE interface="{interfacename}"'.format(
                    interfacename=interface_name)
                sql_res = cur.execute(sql).fetchall()
                intfaceid = sql_res[0][0]

                if sql_res == []:
                    return json.dumps({'statu': 'fail', 'detail': '没有该接口'}, ensure_ascii=False)
                else:
                    sql = 'select case_detail from case_detail WHERE interface_id={interfaceid} and version_id={version_id} and case_id={case_id}'.format(
                        interfaceid=intfaceid, version_id=ver, case_id=case_id)
                    res = cur.execute(sql).fetchall()
                    if res == []:
                        return json.dumps({'statu': 'fail', 'detail': 'beforereques没有找到对应case_detail'},
                                          ensure_ascii=False)
                    else:
                        before_request_detail = res[0][0]
                        sort_list.append(intfaceid)
                        case_detail = json.loads(before_request_detail)
                        sort(case_detail, sort_list, first_catalog)
                        return sort_list
    else:
        return sort_list


def find(target, array):
    i = 0
    if len(array) == 0:
        pass
    else:
        j = len(array[0]) - 1
        while i < len(array) and j >= 0:
            base = array[i][j]
            if target == base:
                return True
            elif target > base:
                i += 1
            else:
                j -= 1
        return False
