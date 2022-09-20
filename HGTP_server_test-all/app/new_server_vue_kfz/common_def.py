from flask import Blueprint, g, jsonify
import flask
import sqlite3
import datetime
import json
from flask import current_app, session
import time
from app.new_server_vue_kfz.haiou.user_control import *
from app.new_server_vue_kfz import *
from app.new_server_vue_kfz.haiou.user_control import *
from app.new_server_vue_kfz.feishu_db.db_message import *
from app.new_server_vue_kfz.haiou.Kaoshifenxi import *
kfz = Blueprint('kfz', __name__)
@kfz.route('/test_kfz', methods=['post'])
def test_kfz():
    return  jsonify(a="afafadfasdf")


@kfz.route('/get_job_detail_vue_def', methods=['post','get'])
@cross_origin()
@get_job_detail_vue_def
def get_job_detail_vue_def():
    pass

@kfz.route('/xiaofentikui_def_statu', methods=['post','get'])
@cross_origin()
def xiaofentikui_def_statu():
    r = redis.Redis(host='127.0.0.1', port=6379)
    x = r.get('kaoshifenxi_down_exe')
    print (x.decode('utf-8'))
    if x.decode('utf-8')=='0':
        return  jsonify(statu="done",detail=x.decode('utf-8'))
    else:
        fn = getattr(sys.modules['__main__'], '__file__')
        root_path = os.path.abspath(os.path.dirname(fn))
        file_path = os.path.join(root_path, 'kaoshifenxi_tikuai')
        file = os.listdir(file_path)
        return_data = {}
        last_excel=''
        last_time=0
        for f in file:
            # 字符串拼接
            real_url = os.path.join(file_path, f)
            if os.path.isdir(real_url):
                return_data[f] = []
            for a in os.listdir(real_url):
                z = os.path.join(file_path, f, a)
                z = os.path.getatime(z)
                if z>last_time:
                    last_excel = '学校：'+f +',         学科：'+ a.split('.')[0]
                    last_time = z
                return_data[f].append(a.split('.')[0])
            # 打印出来
        timeArray = time.localtime(last_time)
        last_time = time.strftime("%H:%M:%S", timeArray)
        return jsonify(last_excel=last_excel,last_time=last_time,return_data=return_data,time_this=time.strftime("%H:%M:%S"),statu="running",detail=x.decode('utf-8'))


@kfz.route('/login', methods=['post','get'])
@cross_origin()
@login_new_ivew
def login_new_ivew():
    pass
@kfz.route('/tongbushuju_test', methods=['post','get'])
@cross_origin()
@tongbushuju_test
def tongbushuju_test():
    pass
@kfz.route('/get_kaoshi_list_def', methods=['post','get'])
@cross_origin()
@get_kaoshi_list_def
def get_kaoshi_list_def():
    pass
@kfz.route('/kaoshifenxi_down_excel_tikui_Def', methods=['post','get'])
@cross_origin()
@kaoshifenxi_down_excel_tikui_Def
def kaoshifenxi_down_excel_tikui_Def():
    pass

@kfz.route('/get_school_redis_def', methods=['post','get'])
@cross_origin()
@get_school_redis_def
def get_school_redis_def():
    pass

@kfz.route('/xiaofentikui_def', methods=['post','get'])
@cross_origin()
@xiaofentikui_def
def xiaofentikui_def():
    pass


@kfz.route('/donwn_tikuaifen_all_data', methods=['post','get'])
@cross_origin()
@donwn_tikuaifen_all_data
def donwn_tikuaifen_all_data():
    pass

@kfz.route('/getuser_info', methods=['post','get'])
@cross_origin()
@getuser_info
def getuser_info():
    pass


@kfz.route('/create_paimai_shanppn', methods=['post','get'])
@cross_origin()
def create_paimai_shanppn():
   return jsonify(a=2)

@kfz.route('/get_banben_detail', methods=['post','get'])
@cross_origin()
@get_banben_detail
def get_banben_detail():
   pass

@kfz.route('/add_dingding_token', methods=['post','get'])
@cross_origin()
@add_dingding_token
def add_dingding_token():
   pass


@kfz.route('/add_jiekou_message', methods=['post','get'])
@cross_origin()
@add_jiekou_message
def add_jiekou_message():
   pass

@kfz.route('/get_jiekou_message', methods=['post','get'])
@cross_origin()
@get_jiekou_message
def get_jiekou_message():
   pass

@kfz.route('/delete_jiekou_message', methods=['post','get'])
@cross_origin()
@delete_jiekou_message
def delete_jiekou_message():
   pass