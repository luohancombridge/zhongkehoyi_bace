from flask import Blueprint, g, jsonify
import flask
import sqlite3
import datetime
import json
from flask import current_app, session

__author__ = 'haiou'
haiou = Blueprint('haiou', __name__)


@haiou.route('/save_catalog', methods=['post'])
def save_catalog():
    conn = sqlite3.connect(current_app.config.get('CONTIN'))
    cur = conn.cursor()
    now = datetime.datetime.today()
    version_id = flask.request.values.get('id')
    return_info = flask.request.values.get('catalog_detail')
    res = option_database(version_id, cur)  # 判断versionId是否在表里
    detail = json.loads(return_info)['detail']
    if res:  # 库里存在，进行更新
        # 从库里取出该版本下的功能
        sql = "select first_catalog,second_catalog from catalog_detail where version_id = {}".format(version_id)
        cur.execute(sql)
        result = cur.fetchall()
        gong_DB = []
        yewu_DB = []
        for r in result:
            yewu_DB.append(r[0])
            gong_DB.append(r[1])

        for de in detail:
            base_path = de
            status = []  # 记录是否存在的状态  存在True
            for yewu in detail[base_path]:
                gongneng = detail[base_path][yewu]  # 实际传进来的 功能
                if yewu not in yewu_DB:  # 业务不再，进行插入
                    status.append('fail')
                    for gong in gongneng:
                        sql = "insert into catalog_detail values(null,{}, '{}', '{}', '{}', '{}', '{}', '{}')".format(
                            version_id, yewu, gong, now, g.user_name, None, None)
                        cur.execute(sql)
                        conn.commit()
                else:  # 业务在,继续判断
                    for gong in gongneng:
                        r = (yewu, gong)
                        if r in result:  # 功能和业务都没变的情况
                            status.append('sccess')
                            sql = "update catalog_detail set update_time='{}',update_name='{}' where version_id='{}' and first_catalog='{}' and second_catalog='{}'".format(
                                now, g.user_name, version_id, yewu, gong)
                            cur.execute(sql)
                            conn.commit()
                        else:
                            status.append('fail')
                            if gong not in gong_DB:  # 如果这个功能不再数据库里，则进行插入
                                sql = "insert into catalog_detail values(null,{}, '{}', '{}', '{}', '{}', '{}', '{}')".format(
                                    version_id, yewu, gong, now, g.user_name, now, g.user_name)
                                cur.execute(sql)
                                conn.commit()
            if 'fail' not in status:
                print('数据源没变，无需更新')
                return jsonify(status='success', detail=None)
            return jsonify(status='success', detail=None)
    else:  # 返回False，库里不存在 进行插入
        for de in detail:
            base_path = de
            for yewu in detail[base_path]:

                print('detail', detail)
                print('detail[base_path]', detail[base_path])
                print('detail[base_path][yewu]', detail[base_path][yewu])
                gongneng = detail[base_path][yewu]
                for gong in gongneng:
                    sql = "insert into catalog_detail values(null,{}, '{}', '{}', '{}', '{}', '{}', '{}')".format(
                        version_id, yewu, gong, now, g.user_name, None, None)
                    cur.execute(sql)
                    conn.commit()
        return jsonify(status='success', detail=None)


def conn_database(cur):
    try:
        sql = "create table if not exists catalog_detail(" \
              "id INTEGER PRIMARY KEY AUTOINCREMENT," \
              "version_id int," \
              "first_catalog varchar(50)," \
              "second_catalog varchar(50)," \
              "create_time date," \
              "create_name varchar(20)," \
              "update_time date," \
              "update_name varchar(20))"
        cur.execute(sql)
    except Exception as e:
        print('数据库连接信息错误')


def option_database(version_id, cur):
    sql = 'select * from catalog_detail where version_id={}'.format(version_id)
    cur.execute(sql)
    if cur.fetchall():  # 如果查询有结果，证明库里存在
        return True
    else:
        return False
