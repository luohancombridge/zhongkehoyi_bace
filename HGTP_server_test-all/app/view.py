# -*- coding: utf-8 -*-
from tempfile import mktemp
from flask import send_from_directory, send_file, Response
import socket

# from matplotlib.pyplot import bar_label
from .sql_chemy.example_db import *
from io import BytesIO
# import matplotlib.pyplot as plt
import os
import sys
import platform
from .hualala.jiekou_git_chonggou import *
from .hualala.check_login import *
from .hualala.git_submit import *
import json
import re
import chardet
from .jie_kou import *
from functools import wraps
from .data_verification import *
from .yuansudingwei import *
import time
import sqlite3
from flask import Blueprint, jsonify, request
from .shell_name import *
# from .form import *
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime
import json
from io import BytesIO
from flask import make_response
from .shuzhen_test.change_config import *
from .tongji.locla_tongji import *
from .shuzhen_test.use_question import *
from .json_tiqu.change_config import json_tiqu
from .directory_tree.dirctory_tree import *
from .new_ui.new_ui import *
from app.jing_jing.jing import jing_new
from .hai_ou.haiou import haiou
from app.si_yang.siyang import Siyang
from .hualala.jiekou_fenxi import *
from  app.hai_ou.import_status import *
from app.tools.tools import *
from app.new_server_vue_kfz.common_def import kfz
from app.wuzhou_kaoshi.wuzhou_kaoshi import wuzhou
from app.kaoshifenxi.dirctory_tree import kaoshifenxi
from app.jishiben.dirctory_tree import jishiben
from app.vue_yonghu.dirctory_tree import vueyonghu
app.register_blueprint(vueyonghu, url_prefix='/vueyonghu')
app.register_blueprint(jishiben, url_prefix='/jishiben')
app.register_blueprint(kfz, url_prefix='/kfz')
app.register_blueprint(wuzhou, url_prefix='/wuzhou')
app.register_blueprint(kaoshifenxi, url_prefix='/kaoshifenxi')
app.register_blueprint(tools, url_prefix='/tools')
app.register_blueprint(Siyang, url_prefix='/common')
app.register_blueprint(CONN, url_prefix='/conn')
app.register_blueprint(directory_tree_new, url_prefix='/tree')
app.register_blueprint(new_ui, url_prefix='/new_ui')
app.register_blueprint(new_file, url_prefix='/new')
app.register_blueprint(use_question, url_prefix='/use_question')
# 统计功能
app.register_blueprint(jing_new, url_prefix='/jing')
app.register_blueprint(tongji_detail, url_prefix='/tongji_detial')
# 提取json
# app.register_blueprint(Haiou,url_prefix='/haiou')
app.register_blueprint(json_tiqu, url_prefix='/json_tiqu')
app.register_blueprint(haiou, url_prefix='/haiou')
bootstrap = Bootstrap(app)
UPLOAD_FOLDER = 'static/Uploads'
@app.before_request
def before_request():
    if 'path' in list(request.form.keys()) and request.form['path'] == 'server':
        pass
    elif 'kfz'  in request.url:
        pass
    else:
        statu = 0
        g.db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        g.cu = g.db.cursor()
        login_statu = request.headers.get('X-Real-IP')
        if request.method == 'GET':
            if 'token' in request.args.keys():
                login_statu = '%'+request.args.get('token')
            else:
                login_statu = request.headers.get('X-Real-IP')+'%'
        elif request.method == 'POST':
            try:
                if 'token' in json.loads(request.get_data()).keys() :
                    login_statu = '%'+json.loads(request.get_data())['token']
                else:
                    login_statu = request.headers.get('X-Real-IP') + '%'
            except:
                if 'token' in request.form.keys():
                    login_statu = '%'+request.form['token']
                else:
                    login_statu = request.headers.get('X-Real-IP') + '%'
        name = g.cu.execute(
            'select name from user where ip like "%s" order by time desc limit 0,1' % login_statu).fetchall()
        if request.headers.get('X-Real-IP') != None:
            if len(name) > 0:
                g.user_name = name[0][0]
            else:
                g.user_name = None
        else:
            g.user_name = None
        pubulic_url = ['locust_before_data_insert','/jing/pass_rate_image_interface','/tree/db_test_reslut_new','/tree/save_run_case_detail','/tree/running_save_db_detail','upload_file','/jing/get_interface_id_detail', 'json_take', 'json_submit', 'find_submit', 'submit_question_page',
                       'submit_question_page', '/testtesttest', '/git_bianji', '/get_renwu_detail', '/debugging',
                       '/chongou_test', '/login', '/get_sumint_statu', '/get_file_git', 'piliang_run_git_over',
                       'jiekou_result', 'add_jekins', 'ceshialert', 'change_run_statu', 'login', 'run_hualala',
                       'dingshi_result', 'change_run_statu', 'tongji_mail','/tree/data_config_file']
        for i in pubulic_url:
            if i in pubulic_url:
                statu = 1
        if 'open_window_page_result' in request.url:
            statu = 1
        if statu == 1:
            session['deng_lu'] = True
            g.db.close()
            pass
        elif 'deng_lu' not in session.keys() or session['deng_lu'] != True:
            user = [i[0] for i in g.cu.execute('select ip from user').fetchall()]
            g.db.close()
            if request.headers.get('X-Real-IP') not in user and 'static' not in request.url:
                return redirect(url_for('login_new'))
        else:
            g.db.close()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
@app.after_request
def af1(res):
    hostname = socket.gethostname()
    res.headers["X-Real-IP"] = socket.gethostbyname_ex(hostname)[-1][-1]
    return res

'''
从这里开始是接口路由

 '''

# 接口发送前向linux服务器日志写入起始内容
from .lenove_jie_kou.wirte_logs import *
@app.route('/wirte_logs', methods=['POST', 'GET'])
def wirte_logs():
    pass


# demo测试
@app.route('/post', methods=['POST'])
def demo_post():
    return jsonify(a=request.form)


# demo测试
@app.route('/get', methods=['get'])
def demo_get():
    return jsonify(a=request.argv)


# 读取linux日志信息
@app.route('/read_logs', methods=['POST', 'GET'])
def read_logs():
    ip = '127.0.0.1'
    return jsonify(a=2, b=3)
    if request.method == 'POST':
        linux = g.cu.execute(
            'select linux from jie_kou_test where name="%s" and ip="%s"' % (request.form['name'], ip)).fetchall()[0][0]
        linux = eval(linux)
        hostname = linux['ip']
        username = linux['name']
        password = linux['password']
        if linux['string'].strip() == 'time':
            linux['string'] = datetime.datetime.now().strftime('%Y-%m-%d')
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname, 22, username, password, timeout=5)
        # 获取日志目录信息
        stdin, stdout, stderr = s.exec_command(
            'tail -n  50 ' + linux['mu_lu'])
        # logs='['+time.strftime('%Y-%m-%d',time.localtime(time.time()))+stdout.read().strip().split(time.strftime('%Y-%m-%d',time.localtime(time.time())))[-1]
        k = str(linux['string']) + str(linux['string']).join(
            stdout.read().strip().split(linux['string'])[int('-' + (linux['num'])):])
        g.cu.execute('UPDATE jie_kou_test SET log=?,time=? WHERE num=? and name=? and ip=?',
                     (k.decode('utf-8'), time.time(), 'run', request.form['name'], ip))
        g.db.commit()
        return jsonify(data=k)
    elif request.method == 'GET':
        if request.args.get('shi') == 'yunxing_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="run"' % (
                request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)
        if request.args.get('shi') == 'bug_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="bug"' % (
                request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)
        if request.args.get('shi') == 'tiaoshi_log':
            data = g.cu.execute('select log from jie_kou_test where name="%s" and ip="%s" and num="debug"' % (
                request.args.get('name'), ip)).fetchall()[0]
            return jsonify(data=data)


# 获取传过来的服务器连接信息，并保存到配置缓存中
@app.route('/linux_config', methods=['POST'])
def linux_config():
    if request.method == 'POST':
        linux = request.form['linux']
        config = request.form['config']
        name = request.form['name']
        if g.cu.execute('select * from jie_kou_test where name="%s"' % name).fetchall() == []:
            g.cu.executemany('INSERT INTO jie_kou_test VALUES (?,?,?,?,?,?,?,?)', [
                ('run', name, linux, 'no data', config, str(request.headers.get('X-Real-IP')), 'no data', time.time())])
            g.db.commit()
        else:
            g.cu.execute('UPDATE jie_kou_test SET name=?,linux=?,ifconfig=?,time=? WHERE num=? and name=? and ip=?',
                         (name, linux, config, time.time(), 'run', name, request.headers.get('X-Real-IP')))
            g.db.commit()
        return jsonify(da=1)


# 开发调试接口页面
@app.route('/jie_run', methods=['GET', 'POST'])
def jie_run():
    if request.method == "GET":
        return render_template('/simple_page/yun_jiekou.html', data='11'
                               )
    elif request.method == "POST":
        jie_kou_test = request.form['shi']
        jie_name = request.form['name']
        data = g.cu.execute('select ifconfig from jie_kou_test where name="%s" and ip="%s"' % (
        jie_name, str(request.headers.get('X-Real-IP')))).fetchall()[0][0].split('\n')
        pon = kaifa_run(jie_kou_test, data)
        return jsonify(a=pon.x)


# 开发调试接口页面
@app.route('/no_use', methods=['GET', 'POST'])
def jie_rueen():
    return render_template('/simple_page/yun_jiekou.html')


# 开发调试接口页面tabs 测试
@app.route('/tabs_kaifa', methods=['GET', 'POST'])
def tabs_kaifa():
    if 'barcode' not in list(session.keys()) or session['barcode'].strip() == '':
        session['barcode'] = '201701221000005'
        table = ['no data', 'no data', 'no data']
        data = ['no data', 'no data', 'no data', 'no data', 'no data']
        return render_template('/simple_page/tabs_kaifa.html', b=table, value=data, b1=table, value1=data,
                               b2=table, value2=data)
    else:
        conn_old = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip', db='visAdmin',
                                   cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
        conn_new = MySQLdb.connect(host='10.199.128.61', port=3309, user='vis', passwd='vispvip',
                                   db='vip_vis_stockservice',
                                   cursorclass=MySQLdb.cursors.DictCursor, charset='utf8')
        cur_old = conn_old.cursor()
        cur_new = conn_new.cursor()
        # 读取excel表格
        k = read_excel(r'E:\osp\11.xlsx')
        if 'barcode' in list(session.keys()):
            cur_new.execute('select * from stock_applications where stock_application_no=%s' % session['barcode'])
            new_data0 = cur_new.fetchone()
            cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s' % session['barcode'])
            s = []
            old_data0 = cur_old.fetchone()
            s.append(
                'SELECT nomal_change_id, SUM( CASE WHEN frozen_num < 0 THEN frozen_num ELSE 0 END ) AS minus_done_boxs_total, SUM( CASE WHEN frozen_num > 0 THEN frozen_num ELSE 0 END ) AS plus_done_boxs_total, SUM( CASE WHEN num < 0 THEN num ELSE 0 END ) AS minus_change_boxs_total, SUM( CASE WHEN num > 0 THEN num ELSE 0 END ) AS plus_change_boxs_total, COUNT(DISTINCT item_code) AS change_goods_total FROM normality_sell_stocks_change_detail WHERE nomal_change_id IN (%s) AND is_deleted = 0 GROUP BY nomal_change_id' %
                old_data0['id'])
            cur_old.execute(s[0])
            ji_data0 = cur_old.fetchone()
            if new_data0 == None or old_data0 == None or ji_data0 == None:
                pass
            else:
                for i in k.data0:
                    if i[0].strip() in list(new_data0.keys()):
                        i.insert(1, new_data0[i[0].strip()])
                    if i[2].split('*')[0].strip() in list(old_data0.keys()):
                        i.insert(3, old_data0[i[2].strip()])
                    elif i[2].split('*')[0].strip() in list(ji_data0.keys()):
                        i.insert(3, ji_data0[i[2].split('*')[0].strip()])
                    else:
                        i.insert(3, 'no data')
        else:
            for i in k.data0:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
        if 'barcode' in list(session.keys()):

            cur_new.execute(
                'select * from stock_application_details where stock_application_no=%s' % session['barcode'])
            new_data1 = cur_new.fetchone()
            cur_old.execute(
                'SELECT * FROM normality_sell_stocks_change_detail WHERE item_code="%s" and  nomal_change_id IN (SELECT id FROM normality_sell_stocks_change_log WHERE apply_no=%s ) ORDER BY id DESC' % (
                new_data1['barcode'], session['barcode']))
            old_data1 = cur_old.fetchone()
            old_data1.pop('vendor_name')
            old_data1.pop('vendor_code')
            cur_old.execute('select * from normality_sell_goods where flagship_id=%s and goods_barcodes="%s"' % (
            old_data1['flagship_id'], old_data1['item_code']))
            ji_data1 = cur_old.fetchone()
            ji_data1.pop('vendor_name')
            ji_data1.pop('vendor_code')
            cur_old.execute('select * from normality_sell_stocks_change_log where apply_no=%s' % session['barcode'])
            s = cur_old.fetchone()
            ji1_data1 = {}
            ji1_data1['vendor_name'] = s['vendor_name']
            ji1_data1['vendor_code'] = s['vendor_code']
            ji1_data1['apply_no'] = s['apply_no']
            cur_old.execute('select * from vendor_shop_schedule where shop_code=%s AND warehouse="%s"' % (
            old_data1['flagship_id'], old_data1['sell_area']))
            s = cur_old.fetchone()
            ji1_data1['schedule_id'] = s['schedule_id']
            cur_old.execute('SELECT * FROM purchase_agreement_goods  WHERE barcode="%s" limit 1' % new_data1['barcode'])
            s = cur_old.fetchone()
            ji1_data1['v_sku_id'] = s['v_sku_id']
            if new_data1 == None or old_data1 == None or ji_data1 == None:
                pass
            else:
                for i in k.data1:
                    if i[0].strip() in list(new_data1.keys()):
                        i.insert(1, new_data1[i[0].strip()])
                    if i[2].split('*')[0].strip() in list(old_data1.keys()):
                        i.insert(3, old_data1[i[2].strip()])
                    elif i[2].strip() in list(ji_data1.keys()):
                        i.insert(3, ji_data1[i[2].strip()])
                    elif i[2].strip() in list(ji1_data1.keys()):
                        i.insert(3, ji1_data1[i[2].strip()])
                    else:
                        i.insert(3, 'no data')
        else:
            for i in k.data1:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
        if 'barcode' in list(session.keys()):
            cur_new.execute('select * from stock_product_status where stock_application_no=%s' % session['barcode'])
            new_data2 = cur_new.fetchone()
            cur_old.execute(
                'SELECT * FROM visAdmin.normality_sell_goods WHERE goods_barcodes="%s" and nomal_change_id IN (SELECT id FROM visAdmin.normality_sell_stocks_change_log WHERE apply_no=%s) ORDER BY id DESC' % (
                new_data2['barcode'], session['barcode']))
            old_data2 = cur_old.fetchone()
            if new_data2 == None or old_data2 == None:
                pass
            else:
                for i in k.data2:
                    if i[0].strip() in list(new_data2.keys()):
                        i.insert(1, new_data2[i[0].strip()])
                    if i[2].split('*')[0].strip() in list(old_data2.keys()):
                        i.insert(3, old_data2[i[2].strip()])
                    else:
                        i.insert(3, 'no data')
        else:
            for i in k.data2:
                i.insert(1, 'no data')
                i.insert(3, 'no data')
        return render_template('/simple_page/tabs_kaifa.html', b=k.table0, value=k.data0, b1=k.table1, value1=k.data1,
                               b2=k.table2, value2=k.data2)


@app.route('/yansql', methods=['GET', 'POST'])
def yan_sql():
    session['barcode'] = request.form['barcode']
    return jsonify(a='1')


# 测试返回测试前段接口信息(不是自动打开的页面，是手动打开的页面)
from .lenove_jie_kou.ceshi_no import *


@app.route('/signal_run', methods=['POST', 'GET'])
@ceshi_no
def signal_run():
    pass


# 本地server调用，更新批量接口运行状态,post为本地发过来的结束运行的更新请求，post请求为前端发过来的运行状态查询请求
@app.route('/piliang_run_over', methods=['POST', 'GET'])
@cross_origin()
def piliang_run_over():
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    if request.method == 'POST':
        if 'ip' not in request.form.keys():
            cu.execute('update jiekou_mulu set run_statu="2" where ip=? and statu=?',
                       (request.headers.get('X-Real-IP'), '批量'))
        else:
            cu.execute('update jiekou_mulu set run_statu="2" where ip=? and statu=?',
                   (request.form['ip'], '批量'))
        db.commit()
        db.close()
        return jsonify(statu="update_success")
    elif request.method == 'GET':
        run_statu = cu.execute('select run_statu from  jiekou_mulu  where ip=? and statu=?',
                               (request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = cu.execute('select update_time from  jiekou_mulu  where ip=? and statu=?',
                              (request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = time.strftime('%Y-%m-%d:  %H:%M:%S ', time.localtime(float(run_time)))
        return jsonify(run_statu=run_statu, run_time=run_time)


# 本地server调用，更新批量接口运行状态,post为本地发过来的结束运行的更新请求，post请求为前端发过来的运行状态查询请求
@app.route('/piliang_run_git_over', methods=['POST', 'GET'])
@cross_origin()
def piliang_run_git_over():
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.method == 'POST':
        cu.execute('update dingshi_run set statu="3" where id=? ',
                   (request.form['id'],))
        db.commit()
        db.close()
        return jsonify(statu="update_success")
    elif request.method == 'GET':
        run_statu = cu.execute('select run_statu from  jiekou_mulu  where ip=? and statu=?',
                               (request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = cu.execute('select update_time from  jiekou_mulu  where ip=? and statu=?',
                              (request.headers.get('X-Real-IP'), '批量')).fetchall()[0][0]
        run_time = time.strftime('%Y-%m-%d:  %H:%M:%S ', time.localtime(float(run_time)))
        return jsonify(run_statu=run_statu, run_time=run_time)


# 前端页面输入接口list的目录
@app.route('/uplate_jiekou_list', methods=['GET', 'POST'])
@cross_origin()
def uplate_jiekou_list():
    # hostname = socket.gethostname()
    # webserver_ip = socket.gethostbyname(hostname)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    webserver_ip = s.getsockname()[0]
    if request.method == "GET":
        # 判断异地目录ip是否和请求ip地址一致，若为周一致则允许跳转调试，否则，置灰
        if 'yidi_mulu_ip' not in list(session.keys()):
            session['yidi_mulu_ip'] = '127.0.0.1'
        if session['yidi_mulu_ip'] == request.headers.get('X-Real-IP'):
            yizhi = 1
        else:
            yizhi = 0
        yizhi = 1
        if 'mulu_detail' in session:
            res = session['mulu_detail']
            return render_template('/hualala/pages/jiekou_list.html', yewu_name=res['yewu_name'],
                                   ip_server=session['yidi_mulu_ip'],
                                   select_huanjing=res['select_huanjing'], huanjing=res['huanjing'],
                                   all_mulu=res['gen_mulu'], yizhi=yizhi,
                                   local_port=current_app.config.get('LOCAL_SERVER_PORT'))
        else:
            return render_template('/hualala/pages/jiekou_list.html', yewu_name='',
                                   select_huanjing='', huanjing='',
                                   all_mulu='', yizhi=yizhi, local_port=current_app.config.get('LOCAL_SERVER_PORT'))
    else:
        pass
    # 判断是否本地调试，还是异地调试,包含ip_dizhi为异地调试
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    if 'ip_dizhi' in list(request.form.keys()):
        session['yidi_mulu_ip'] = request.form['ip_dizhi']
        ip_dizhi = request.form['ip_dizhi']
        # if ip_dizhi==webserver_ip:
        #     ip_dizhi='127.0.0.1'
        mulu = request.form['mulu']
        mulu = cu.execute('select  mulu from jiekou_mulu where ip=? and statu=?', (ip_dizhi, '批量')).fetchall()
        url = 'http://' + ip_dizhi.strip() + ':' + current_app.config.get('LOCAL_SERVER_PORT') + '/mulu_detail'
        if len(mulu) == 0:
            return render_template('/hualala/pages/jiekou_list.html', yewu_name='',
                                   select_huanjing='', huanjing='',
                                   all_mulu='', local_port=current_app.config.get('LOCAL_SERVER_PORT'))
        else:
            mulu = mulu[0][0]
    else:
        # session['yidi_mulu_ip'] = request.headers.get('X-Real-IP')
        session['yidi_mulu_ip'] = '127.0.0.1'
        mulu = request.form['mulu']
        ip = request.headers.get('X-Real-IP')
        if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?',
                          (request.headers.get('X-Real-IP'), '批量')).fetchall()) > 0:
            cu.execute('update jiekou_mulu set mulu=?,update_time=?,run_statu="0" where ip=? and statu=?',
                       (request.form['mulu'], str(time.time()), request.headers.get('X-Real-IP'), '批量'))
        else:
            cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?,?)',
                           [('批量', request.form['mulu'], request.headers.get('X-Real-IP'), str(time.time()), '0')])
        # 发送本地服务气请求获取接口目录信息
        url = 'http://' + request.headers.get('X-Real-IP') + ':' + current_app.config.get(
            'LOCAL_SERVER_PORT') + '/mulu_detail'
    db.commit()
    db.close()
    mulu = mulu.encode('utf-8')
    if 'huanjing' in list(request.form.keys()):
        session['huanjing'] = request.form['huanjing']
    else:
        if 'huanjing' not in list(session.keys()):
            session['huanjing'] = ''
    test_data = {'mulu': mulu, 'huanjing': session['huanjing'].encode('utf-8')}
    test_data_urlencode = urllib.parse.urlencode(test_data)
    if 'all_data' not in list(request.form.keys()):
        req = urllib.request.Request(url=url, data=test_data_urlencode)
        try:
            res_data = json.loads(urllib.request.urlopen(req).read())
        except:
            return '找不到相应服务或目录'
    else:
        res_data = json.loads(request.form['all_data'])
    if 'error_detail' in list(res_data.keys()):
        return res_data['error_detail']
    if 'statu' in list(res_data.keys()) and res_data['statu'] == 'no dir':
        return '目录不存在'
    res = json.loads(res_data['data'])
    if session['huanjing'].strip() != '':
        res['select_huanjing'] = session['huanjing']
    res['gen_mulu'] = mulu.decode('utf-8')
    session['mulu_detail'] = res
    if session['yidi_mulu_ip'] == request.headers.get('X-Real-IP'):
        yizhi = 1
    else:
        yizhi = 0
    resp = make_response(render_template('/hualala/pages/jiekou_list.html', ip_server=session['yidi_mulu_ip'],
                                         yewu_name=res['yewu_name'], select_huanjing=res['select_huanjing'],
                                         huanjing=res['huanjing'], all_mulu=res['gen_mulu'], yizhi=yizhi,
                                         local_port=current_app.config.get('LOCAL_SERVER_PORT'))
                         )
    return resp


# 接收接口测试返回过来的批量接口数据，并存入数据库中
from .lenove_jie_kou.run_jiekou import *


@app.route('/jie_kou_result', methods=['POST', 'GET'])
@jiekou_result
def jiek_result():
    pass


# 所有接口信息列表展示
from .lenove_jie_kou.jiekou_list import jiekou_list_show


@app.route('/jiekou_list', methods=['POST', 'GET'])
@jiekou_list_show
def jiekou_list_show():
    pass


# 根据运行按钮批量运行脚本并弹出结果页面
from .lenove_jie_kou.jiekou_list import jiekou_result_run


@app.route('/simple_jie_kou_run', methods=['POST', 'GET'])
@jiekou_result_run
def jiekou_list_showeeaa():
    pass


# get请求为打开修改配置文件弹出框，获取第一个选中元素的class值，返回对应配置目录下的配置文件值
# post请求为获取要更新的配置，在相应目录下更新。
from .lenove_jie_kou.change_config import change_config


@app.route('/read_configparse', methods=['POST', 'GET'])
@change_config
def jiekou_list_showeeaa():
    pass


from .lenove_jie_kou.jiekou_list import *


@app.route('/jiaobenshuru', methods=['POST'])
@jiaobenshuru
def jiaoben_shuru():
    pass


# 跳转到试试调试页面
@app.route('/shishitiaoshi', methods=['GET', 'POST'])
@cross_origin()
@shishitiaoshi
def shishitiaoshi():
    pass


# 调试url入库
@app.route('/jiekou_mulu', methods=['GET', 'POST'])
@cross_origin()
@url_insert
def jiekou_mulu():
    pass


# 调试url入库
@app.route('/get_mulu', methods=['GET', 'POST'])
@get_mulua
def get_mulua():
    pass


# 批量运行接口
@app.route('/piliang_run', methods=['GET', 'POST'])
@cross_origin()
@piliang_run
def piliang_run():
    pass


# 获取后端发过来的本地批量运行的结果并存入数据库中
@app.route('/piliang_run_result', methods=['GET', 'POST'])
@cross_origin()
@piliang_run_resulttt
def piliang_run_result():
    pass


# 获取git页面接口批量运行结果并存入数据库中
@app.route('/piliang_git_result', methods=['GET', 'POST'])
@piliang_git_result
def piliang_git_result():
    pass


# 获取接口运行结果
@app.route('/jie_kou_result', methods=['GET', 'POST'])
def jie_kou_result():
    return jsonify(a="1")


# 从数据库中拉取数据，返回批量测试结果
from .lenove_jie_kou.run_jiekou import *


@app.route('/jie_kou', methods=['POST', 'GET'])
@cross_origin()
@piliangjiekou_result
def run_jiekou():
    pass



@app.route('/jie_kou_vue', methods=['POST', 'GET'])
@cross_origin()
@jie_kou_vue
def jie_kou_vue():
    pass



# 接口git 页面返回
@app.route('/jiekou_page', methods=['GET', 'POST'])
@jiekou_piliang
def jiekou_page():
    pass


# moke挡板
from .hualala.moke_dangban import moke_dangban


@app.route('/moke_dangban', methods=['GET', 'POST'])
@moke_dangban
def moke_dangban():
    pass


# 增加case
from .hualala.moke_dangban import add_case


@app.route('/add_case', methods=['GET', 'POST'])
@add_case
def add_case():
    pass


# 读取case
from .hualala.moke_dangban import case_read


@app.route('/case_read', methods=['GET', 'POST'])
@case_read
def case_read():
    pass


# 修改case
from .hualala.moke_dangban import bianji_case


@app.route('/bianji_case', methods=['GET', 'POST'])
@bianji_case
def bianji_case():
    pass


# 返回挡板业务信息
from .hualala.moke_dangban import yewu_bianji_show


@app.route('/yewu_bianji_show', methods=['GET', 'POST'])
@yewu_bianji_show
def yewu_bianji_show():
    pass


# moke挡板添加linux信息
from .hualala.moke_dangban import linux_add


@app.route('/linux_add', methods=['GET', 'POST'])
@linux_add
def linux_add():
    pass


# moke挡板增加项目
from .hualala.moke_dangban import top_add_ceshi


@app.route('/top_add', methods=['GET', 'POST'])
@top_add_ceshi
def top_add_ceshi():
    pass


# moke挡板fanhui
from .hualala.moke_dangban import moke_return


@app.route('/moke_return/<id>', methods=['GET', 'POST'])
@moke_return
def moke_return(id):
    pass


# moke挡板增加业务
from .hualala.moke_dangban import yewuadd


@app.route('/yewu_add', methods=['GET', 'POST'])
@yewuadd
def yewuadd():
    pass


# moke应用linux，修改host
from .hualala.moke_dangban import server_use


@app.route('/server_use', methods=['GET', 'POST'])
@server_use
def server_use():
    pass


# 删除项目
from .hualala.moke_dangban import delete_moke_xiangmu


@app.route('/delete_moke_xiangmu', methods=['GET', 'POST'])
@delete_moke_xiangmu
def top_add_ceshi():
    pass


@app.route('/<name>', methods=['GET', 'POST'])
def top_add_ceshi(name):
    return jsonify(statu=name)


'''
接口路由结束
 '''


# 项目首页，如果是post请求则是输入进来git，自动从相关目录下获取git文件地址
@app.route('/first_page', methods=['GET', 'POST'])
def first_page_exe():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute(
        'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get(
            'X-Real-IP')).fetchall()
    if len(name) == 0:
        return redirect(url_for('login_new'))
    else:
        name = name[0][0]
    if request.method == 'GET':
        git_detail = [list(i) for i in cu.execute('select * from git_detail  ').fetchall()]
        for i in git_detail:
            i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
        email_detail = [i[0] for i in
                        cu.execute('select address from email_address where user="%s"' % (name)).fetchall()]
        fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
        dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
            'select * from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
        jobs = [i[0] for i in db.execute('select job_name from jekins where name="%s"' % name).fetchall()]
        for k, i in enumerate(dingshi_detail):
            i.insert(0, i[0])
            i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
            if i[-2].strip() == '0':
                i[-2] = 'ready'
            elif i[-2].strip() == '1':
                i[-2] = 'running'
            elif i[-2].strip() == '2':
                i[-2] = 'over'
        time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
        server_detail = [i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall()]
        db.close()
        return render_template('/hualala/pages/index.html', git_detail=git_detail, email_detail=email_detail,
                               time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs,
                               server_detail=server_detail)
    else:
        git_url = request.form['git'].strip()
        git_beizhu = request.form['beizu'].strip()
        git_branch = request.form['branch'].strip()
        if git_url.strip() != '' and git_beizhu.strip() != '':
            cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)',
                           [(git_url, git_beizhu, name, str(time.time()), '', git_branch)])
            db.commit()
            db.close()
        return jsonify(a='1')


# 登陆页面
@app.route('/login', methods=['GET', 'POST'])
def login_new():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.method == 'GET':
        db.close()
        return render_template('/hualala/login.html')
    else:
        ip = request.headers.get('X-Real-IP')
        name = request.form['name']
        passs = request.form['password']
        user_check = cu.execute('select * from user where name="%s" and pass="%s" ' % (name, passs)).fetchall()
        if len(user_check) != 0:
            # cu.executemany('UPDATE user SET ip="null" WHERE ip=?', [(ip)])
            cu.execute('update  user  set ip="" where ip=?', [ip])
            db.commit()
            cu.executemany('update  user  set time=? ,ip=? where name=?', [(time.time(), ip, name)])
            db.commit()
            response = make_response(redirect(url_for('chongou_test')))
            response.set_cookie('flask_login', "a")
            db.close()
            return response
        else:
            db.close()
            return render_template('/hualala/login.html')


# 用户管里页面
from .hualala.user import *


@app.route('/user_manage', methods=['GET', 'POST'])
@cross_origin()
@user
def user_manage():
    pass


# server管里页面
@app.route('/server_manage/<server_type>', methods=['GET', 'POST'])
@cross_origin()
@server
def server_manage(server_type):
    pass


# server启动停止
@app.route('/change_server', methods=['GET', 'POST'])
@cross_origin()
def change_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['statu'] == 'true':
        statu = '0'
    else:
        statu = '1'
    cu.executemany('update   all_server set statu=? where id=?', [(statu, int(request.form['change_id']))])
    db.commit()
    db.close()
    return jsonify(a=1)


# server增加
@app.route('/add_server', methods=['GET', 'POST'])
@cross_origin()
def add_server():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    if request.form['ip'].strip() == '' or request.form['duankou'].strip() == '':
        return jsonify(a="输入不能为空")
    elif len(cu.execute('select * from all_server where ip="%s"' % (request.form['ip'])).fetchall()) > 0:
        return jsonify(a="server ip 已经存在")
    cu.executemany('INSERT INTO  all_server values (null,?,?,?,?)',
                   [(request.form['ip'], request.form['duankou'], '0', '0')])
    db.commit()
    db.close()
    return jsonify(a=1)


# 脚本运行
from .hualala.run import *
from app.db_sqlchemy_sqlite import *

@app.route('/run_hualala', methods=['GET', 'POST'])
@cross_origin()
@run_hualala
def run_hual():
    pass
@app.route('/locust_before_data_insert', methods=['GET', 'POST'])
@cross_origin()
@locust_before_data_insert
def locust_before_data_insert():
    pass


@app.route('/chiujicheng_run', methods=['GET', 'POST'])
@cross_origin()
@chixuijicheng_run
def chixuijicheng_run():
    pass

# 运行检查
from .hualala.run import *


@app.route('/run_charge', methods=['GET', 'POST'])
@cross_origin()
@run_charge
def run_hual():
    pass


@app.route('/delete_ben', methods=['GET', 'POST'])
@cross_origin()
def delete_ben():
    tongji_db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    tongji_cu = tongji_db.cursor()
    if request.form['statu'] == 'url':
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
    else:
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
    ip = request.headers.get('X-Real-IP')
    name = request.form['name'].strip()
    branch = request.form['branch'].strip()
    git = request.form['git'].strip()
    cu.execute('delete from git_detail  where  name="%s"  and submit= "%s"  and  branch= "%s"  ' % (
    git, name, branch)).fetchall()
    db.commit()
    tongji_cu.execute('delete from ci_tongji  where  git_url="%s"  and branch= "%s"' % (git, branch)).fetchall()
    tongji_db.commit()
    db.commit()
    tongji_db.close()
    db.close()
    return jsonify(statu='success')


from .hualala.add_email import *


@app.route('/add_email', methods=['GET', 'POST'])
@cross_origin()
@add_email
def add_email():
    pass


@app.route('/emali_list_all', methods=['GET', 'POST'])
@cross_origin()
@show_email
def emali_list():
    pass


@app.route('/delete_email', methods=['GET', 'POST'])
@cross_origin()
@delete_email
def emali_list():
    pass


@app.route('/change_curl', methods=['GET', 'POST'])
@cross_origin()
@change_curl
def change_curl():
    pass


@app.route('/send_emali', methods=['GET', 'POST'])
@cross_origin()
@send_emali
def send_emali():
    pass


@app.route('/add_file_detail', methods=['GET', 'POST'])
@cross_origin()
@add_file_detail
def add_file_detail():
    pass


@app.route('/dingshi_result/<id>', methods=['GET', 'POST'])
def dingshi_result(id):
    # 查看定时运行的结果文件
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    url_detail = 'http://' + socket.gethostbyname(socket.gethostname()) + ':5021' + url_for('dingshi_result', id=id)
    if str(id).strip() == 'shishi':
        # name = cu.execute('select name from user where ip="%s" order  by time desc limit 0,1 ' % request.headers.get('X-Real-IP')).fetchall()[0][0]
        z = cu.execute('select run_result from dingshi_run where id=?', (id).fetchall()[0][0])
        timee = cu.execute('select update_time,last_run_time from dingshi_run where id=?',
                           (id)).fetchall()[0]
    else:
        z = cu.execute('select run_result from dingshi_run where id=?', (id,)).fetchall()[0][0]
        timee = cu.execute('select update_time,last_run_time from dingshi_run where  id=?', (id,)).fetchall()[0]
        z = json.loads(z)
    job = json.loads(cu.execute('select job from dingshi_run where id=?', (id,)).fetchall()[0][0])
    if 'name' in list(job.keys()) and 'no select' != job['name'].strip():
        job_r = job['name'] + ':' + job['result']
    else:
        job_r = 'null'
    run_taken = float(job['end_time'])
    if run_taken > 60:
        run_time_detail = str(int(run_taken) / 60) + '分' + str(int(run_taken) % 60) + '秒'
    else:
        run_time_detail = str(int(run_taken)) + '秒'
    total = [0, 0, 0, 0]
    timeArray = time.localtime(float(timee[0]))
    otherStyleTime = time.strftime("%H:%M:%S", timeArray)
    timee = list(timee)
    if timee[1].strip() == '':
        timee[1] = time.strftime('%Y:%m:%d', timeArray)
    timee = timee[1] + '   ' + otherStyleTime
    for k in z:
        total[0] += z[k]['count']
        total[1] += z[k]['Pass']
        total[2] += z[k]['fail']
        total[3] += z[k]['error']

    db.close()
    return render_template('/hualala/pages/test_result.html', time=str(time.time()), z=z, total=total, timee=timee,
                           job=job_r, taken=run_time_detail, url_detail=url_detail)


from .hualala.yunxing_tongji import pic_yewu_email
@app.route('/jiekou_result_vue/<id>', methods=['GET', 'POST'])
@cross_origin()
def jiekou_result_vue(id):
    ursr_idid = id
    # 查看定时运行的结果文件
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    url_detail = 'http://' + request.remote_addr + ':5025' + url_for('jiekou_result', id=id)
    if request.method == "GET" or request.method == "POST":
        s_assert = assert_run()
        # 根据ip地址读取测试数据
        data = cu.execute('select * from  dingshi_run where id=?', (id,)).fetchall()
        if len(data)>0:
            data= data[0]
        else:
            return jsonify(statu='error',detail='数据已被清空，请重新运行')
        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[1])))
        all = []
        top_all = {}
        taken_time = int(json.loads(data[10])['end_time'])
        job_result = json.loads(data[10])["result"]
        if job_result.strip() == '':
            job_result = 'NULL'
        if taken_time >= 60:
            fen = int(taken_time / 60)
            miao = taken_time % 60
            taken_time = "%s分   %s秒" % (fen, miao)
        else:
            taken_time = "%s秒" % (taken_time)
        taken_time = taken_time
        all_result = json.loads(data[8])
        qll_fail = 0
        all_succ = 0
        chaoshi_time_all = 0
        yewuxian_detail = {}
        chaoshi_time=  current_app.config.get('JIEKU_RESPONSE_TIME') if current_app.config.get('JIEKU_RESPONSE_TIME')>0 else 0
        if len(all_result) != 0:
            for i in all_result:
                git_beizhu =json.loads(i)['git_beizhu']
                name = json.loads(i)['all_name'][-1]
                detail = []
                statu = 0
                fail = 0
                succ = 0
                xingneng_fail= 0
                count = len(json.loads(all_result[i]))
                for k, z in list(json.loads(all_result[i]).items()):
                    result = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int),
                                        indent=4,
                                        sort_keys=False,
                                        ensure_ascii=False)
                    id = int(k)
                    run_take_time = round(z['run_take_time'], 2)
                    req_url = z['req_url']
                    if type(z['case_assert']) in ['str', 'unicode'] and z['case_assert'].strip() != '':
                        assert_data = json.loads(z['case_assert'])
                    elif type(z['case_assert']) in [dict, list]:
                        assert_data = z['case_assert']
                    else:
                        assert_data = ''
                    case_assert = json.dumps(
                        json.loads(json.dumps(demjson.decode(json.dumps(assert_data))), parse_int=int), indent=4,
                        sort_keys=False,
                        ensure_ascii=False)
                    if chaoshi_time<run_take_time:
                        xingneng_fail = xingneng_fail+1
                        chaoshi_time_all= chaoshi_time_all+1
                    xingneng_assert= True if run_take_time < chaoshi_time else False
                    comment = z['case_name']
                    req = z['req']
                    # respons_headers = z['respons_headers']
                    req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
                                     sort_keys=False,
                                     ensure_ascii=False)
                    # respons_headers = json.dumps(
                    #     json.loads(json.dumps(demjson.decode(json.dumps(respons_headers))), parse_int=int), indent=4,
                    #     sort_keys=False,
                    #     ensure_ascii=False)
                    respons_headers=json.dumps({})
                    if z['assert_result'] == False:
                        statu = 1
                        fail += 1
                        qll_fail += 1
                        detail.append(["failCase", id, comment, case_assert, result, req, req_url,respons_headers,run_take_time])
                    elif z['assert_result'] != False and xingneng_assert==False:
                        statu = 1
                        detail.append(["failCase", id, comment, case_assert, result, req, req_url, respons_headers,run_take_time])
                    else:
                        succ += 1
                        all_succ += 1
                        detail.append(["passCase", id, comment, case_assert, result, req, req_url,respons_headers,run_take_time])
                detail = sorted(detail, key=lambda x: x[1])
                if git_beizhu not in list(yewuxian_detail.keys()):
                    yewuxian_detail[git_beizhu] = {'success': 0, 'fail': 0, 'count': 0, 'all': 0}
                # result_detail=git_beizhu+','+name.split(':')[0]+','+name.split(':')[0]
                result_detail=json.loads(i)['git_beizhu']+':'+json.loads(i)['all_name'][0]+':'+json.loads(i)['all_name'][1]
                if result_detail not in list(top_all.keys()):
                    top_all[result_detail] = {'success': 0, 'fail': 0, 'count': 0, 'all': [],'all_name':json.loads(i)}
                if statu == 1:
                    top_all[result_detail]['all'].append([name, "failClass", [count, succ, fail, count], detail])
                    top_all[result_detail]['success'] = top_all[result_detail]['success'] + int(succ)
                    top_all[result_detail]['fail'] = top_all[result_detail]['fail'] + int(fail)
                    top_all[result_detail]['count'] = top_all[result_detail]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1
                elif statu == 0:
                    top_all[result_detail]['all'].append([name, "passClass", [count, succ, fail, count], detail])
                    top_all[result_detail]['success'] = top_all[result_detail]['success'] + int(succ)
                    top_all[result_detail]['fail'] = top_all[result_detail]['fail'] + int(fail)
                    top_all[result_detail]['count'] = top_all[result_detail]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1
        # z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        try:
            top_all[result_detail]['all'] = sorted(top_all[result_detail]['all'], key=lambda zzz: zzz[0])
        except:
            pass
        db.close()
        hostname = socket.gethostname()
        pic_url = os.path.join('http://' + request.remote_addr + ':5025/static/result_pic', str(ursr_idid) + '.png')
        session['take_result'] = yewuxian_detail
        if len(all_result) != 0:
            ##定时任务发送图片
            if platform.system() == 'Linux':
                pass
            else:
              # pic_yewu_email(ursr_idid)
              pass
        # return jsonify(fail=qll_fail, success=all_succ,chaoshi_time_all=chaoshi_time_all,xingnengbiaozhun =  current_app.config.get('JIEKU_RESPONSE_TIME'))
        return jsonify( z=top_all, time=tim, result_url=url_detail,
                                   taken_time=taken_time, fail=qll_fail, success=all_succ, job_result=job_result,
                                   pic_url=pic_url, request_statu=request.args.get('statu'))


@app.route('/jiekou_result/<id>', methods=['GET', 'POST'])
def jiekou_result(id):
    ursr_idid = id
    # 查看定时运行的结果文件
    ip = request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    url_detail = 'http://' + request.remote_addr + ':5025' + url_for('jiekou_result', id=id)
    if request.method == "GET" or request.method == "POST":
        s_assert = assert_run()
        # 根据ip地址读取测试数据
        data = cu.execute('select * from  dingshi_run where id=?', (id,)).fetchall()
        if len(data)>0:
            data= data[0]
        else:
            return jsonify(statu='error',detail='数据已被清空，请重新运行')
        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(data[1])))
        all = []
        top_all = {}
        taken_time = int(json.loads(data[10])['end_time'])
        job_result = json.loads(data[10])["result"]
        if job_result.strip() == '':
            job_result = 'NULL'
        if taken_time >= 60:
            fen = int(taken_time / 60)
            miao = taken_time % 60
            taken_time = "%s分   %s秒" % (fen, miao)
        else:
            taken_time = "%s秒" % (taken_time)
        taken_time = taken_time
        all_result = json.loads(data[8])
        qll_fail = 0
        all_succ = 0
        chaoshi_time_all = 0
        yewuxian_detail = {}
        chaoshi_time=  current_app.config.get('JIEKU_RESPONSE_TIME') if current_app.config.get('JIEKU_RESPONSE_TIME')>0 else 0
        if len(all_result) != 0:
            for i in all_result:
                git_beizhu =json.loads(i)['git_beizhu']
                name = json.loads(i)['all_name'][-1]
                detail = []
                statu = 0
                fail = 0
                succ = 0
                xingneng_fail= 0
                count = len(json.loads(all_result[i]))
                for k, z in list(json.loads(all_result[i]).items()):
                    result = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int),
                                        indent=4,
                                        sort_keys=False,
                                        ensure_ascii=False)
                    id = int(k)
                    run_take_time = round(z['run_take_time'], 2)
                    req_url = z['req_url']
                    if type(z['case_assert']) in ['str', 'unicode'] and z['case_assert'].strip() != '':
                        assert_data = json.loads(z['case_assert'])
                    elif type(z['case_assert']) in [dict, list]:
                        assert_data = z['case_assert']
                    else:
                        assert_data = ''
                    case_assert = json.dumps(
                        json.loads(json.dumps(demjson.decode(json.dumps(assert_data))), parse_int=int), indent=4,
                        sort_keys=False,
                        ensure_ascii=False)
                    if chaoshi_time<run_take_time:
                        xingneng_fail = xingneng_fail+1
                        chaoshi_time_all= chaoshi_time_all+1
                    xingneng_assert= True if run_take_time < chaoshi_time else False
                    comment = z['case_name']
                    req = z['req']
                    # respons_headers = z['respons_headers']
                    req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
                                     sort_keys=False,
                                     ensure_ascii=False)
                    # respons_headers = json.dumps(
                    #     json.loads(json.dumps(demjson.decode(json.dumps(respons_headers))), parse_int=int), indent=4,
                    #     sort_keys=False,
                    #     ensure_ascii=False)
                    respons_headers=json.dumps({})
                    if z['assert_result'] == False:
                        statu = 1
                        fail += 1
                        qll_fail += 1
                        detail.append(["failCase", id, comment, case_assert, result, req, req_url,respons_headers,run_take_time])
                    elif z['assert_result'] != False and xingneng_assert==False:
                        statu = 1
                        detail.append(["failCase", id, comment, case_assert, result, req, req_url, respons_headers,run_take_time])
                    else:
                        succ += 1
                        all_succ += 1
                        detail.append(["passCase", id, comment, case_assert, result, req, req_url,respons_headers,run_take_time])
                detail = sorted(detail, key=lambda x: x[1])
                if git_beizhu not in list(yewuxian_detail.keys()):
                    yewuxian_detail[git_beizhu] = {'success': 0, 'fail': 0, 'count': 0, 'all': 0}
                # result_detail=git_beizhu+','+name.split(':')[0]+','+name.split(':')[0]
                result_detail=json.loads(i)['git_beizhu']+':'+json.loads(i)['all_name'][0]+':'+json.loads(i)['all_name'][1]
                if result_detail not in list(top_all.keys()):
                    top_all[result_detail] = {'success': 0, 'fail': 0, 'count': 0, 'all': [],'all_name':json.loads(i)}
                if statu == 1:
                    top_all[result_detail]['all'].append([name, "failClass", [count, succ, fail, count], detail])
                    top_all[result_detail]['success'] = top_all[result_detail]['success'] + int(succ)
                    top_all[result_detail]['fail'] = top_all[result_detail]['fail'] + int(fail)
                    top_all[result_detail]['count'] = top_all[result_detail]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1
                elif statu == 0:
                    top_all[result_detail]['all'].append([name, "passClass", [count, succ, fail, count], detail])
                    top_all[result_detail]['success'] = top_all[result_detail]['success'] + int(succ)
                    top_all[result_detail]['fail'] = top_all[result_detail]['fail'] + int(fail)
                    top_all[result_detail]['count'] = top_all[result_detail]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['success'] = yewuxian_detail[git_beizhu]['success'] + int(succ)
                    yewuxian_detail[git_beizhu]['fail'] = yewuxian_detail[git_beizhu]['fail'] + int(fail)
                    yewuxian_detail[git_beizhu]['count'] = yewuxian_detail[git_beizhu]['count'] + int(count)
                    yewuxian_detail[git_beizhu]['all'] = yewuxian_detail[git_beizhu]['all'] + 1
        # z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        try:
            top_all[result_detail]['all'] = sorted(top_all[result_detail]['all'], key=lambda zzz: zzz[0])
        except:
            pass
        db.close()
        hostname = socket.gethostname()
        pic_url = os.path.join('http://' + request.remote_addr + ':5025/static/result_pic', str(ursr_idid) + '.png')
        session['take_result'] = yewuxian_detail
        if len(all_result) != 0:
            ##定时任务发送图片
            if platform.system() == 'Linux':
                pass
            else:
              # pic_yewu_email(ursr_idid)
              pass
        if request.method == 'POST':
            return jsonify(fail=qll_fail, success=all_succ,chaoshi_time_all=chaoshi_time_all,xingnengbiaozhun =  current_app.config.get('JIEKU_RESPONSE_TIME'))
        else:
            return render_template('/hualala/jiekou_test/test_result.html', z=top_all, time=tim, result_url=url_detail,
                                   taken_time=taken_time, fail=qll_fail, success=all_succ, job_result=job_result,
                                   pic_url=pic_url, request_statu=request.args.get('statu'))


@app.route('/open_dingshi_detail', methods=['GET', 'POST'])
@open_dingshi_detail
def open_dingshi_detail():
    pass


# 设置发件人
@app.route('/add_fajianren', methods=['GET', 'POST'])
@cross_origin()
@add_fajianren
def add_fajianren():
    pass


# 显示 发件人
@app.route('/show_fajianren', methods=['GET'])
@cross_origin()
@show_fajianren
def show_fajianren():
    pass


# 删除发件人
@app.route('/delete_fajianren', methods=['GET'])
@cross_origin()
@delete_fajianren
def delete_fajianren():
    pass


# 设置jekins
@app.route('/add_jekins', methods=['GET', 'POST'])
@add_jekins
def add_fajianren():
    pass


# jekins_list 列表
@app.route('/jekins_list', methods=['GET', 'POST'])
@jekins_list
def jekins_list():
    pass


# jekins_list删除
@app.route('/jekins_delete', methods=['GET', 'POST'])
@jekins_delete
def jekins_delete():
    pass


# suite_list删除
@app.route('/suite_delete', methods=['GET', 'POST'])
@cross_origin()
@suite_delete
def suite_delete():
    pass


# suite_list删除
@app.route('/xiaomin', methods=['GET', 'POST'])
def xiaomin():
    a = 222
    return jsonify(statu='success')


# 打开second 页面
@app.route('/second_page', methods=['GET', 'POST'])
def second():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute(
        'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get(
            'X-Real-IP')).fetchall()
    if len(name) == 0:
        return redirect(url_for('login_new'))
    else:
        name = name[0][0]
    data = cu.execute('select * from locust_file order by id desc').fetchall()
    db.close()
    return render_template('/hualala/pages/second_page.html', data=data)


# 打开教程页面
@app.route('/teach', methods=['GET', 'POST'])
def teach():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    db.close()
    return render_template('/hualala/pages/texch.html')


# 上传脚本文件
from .hualala.locust_fiel import upload_fil


@app.route('/upload_file', methods=['GET', 'POST'])
@upload_fil
def upload_file():
    pass


# 上传脚本文件同时更新文件表格信息
from .hualala.locust_fiel import upload_fil_beizu


@app.route('/upload_fil_beizu', methods=['GET', 'POST'])
@upload_fil_beizu
def upload_file():
    pass


# 接口自动化平台首页
from .lenove_jie_kou.run_jiekou import jiekou_gitce


@app.route('/jiekou_yun', methods=['GET', 'POST'])
@cross_origin()
@jiekou_gitce
def jiekou_git():
    pass


# 关联ipi地址，方便开发查看调试结果
from .lenove_jie_kou.run_jiekou import guanlian_ip_dizhi


@app.route('/guanlian_ip', methods=['GET', 'POST'])
@guanlian_ip_dizhi
def guanlian_ip():
    pass


# 根据关联地址，返回他人调试页面
from .lenove_jie_kou.run_jiekou import debugging


@app.route('/debugging', methods=['GET', 'POST'])
@debugging
def run_dubbing():
    pass


# jekins job 编辑框弹出
from .lenove_jie_kou.jekins import signal_job_detail


@app.route('/signal_job_detail', methods=['GET', 'POST'])
@signal_job_detail
def signal_job_detail():
    pass


# 更新jekins job信息
from .lenove_jie_kou.jekins import job_gengxin


@app.route('/job_gengxin', methods=['GET', 'POST'])
@job_gengxin
def job_gengxin():
    pass


# 删除server

from .lenove_jie_kou.jekins import delete_server


@app.route('/delete_server', methods=['GET', 'POST'])
@cross_origin()
@delete_server
def delete_server():
    pass


# 更改相应job的运行状态
from .hualala.run import change_run_statu
@app.route('/change_run_statu', methods=['POST'])
@change_run_statu
def change_run_statu():
    pass


# 更新服务器host
from .hualala.run import update_host


@app.route('/updata_html', methods=['POST'])
@update_host
def update_host22():
    pass


# 获取local_server传过来的接口文件信息
from .hualala.submit_git import submit_git


@app.route('/get_file_git', methods=['POST'])
@submit_git
def get_file_git():
    pass


# 验证是否别人在提交中
from .hualala.submit_git import get_sumint_statu


@app.route('/get_sumint_statu', methods=['POST'])
@get_sumint_statu
def get_sumint_statu():
    pass


# 获取local_server传过来的接口文件信息
from .hualala.yunxing_tongji import yunxing_tongji


@app.route('/yunxing_tongji', methods=['POST'])
@yunxing_tongji
def yunxing_tongji():
    pass


from .hualala.yunxing_tongji import test_image


@app.route('/test_image/<id>', methods=['POST', 'GET'])
@test_image
def test_image(id):
    pass


from .hualala.yunxing_tongji import pic_yewu_today


@app.route('/pic_yewu_oday/<testid>', methods=['POST', 'GET'])
@pic_yewu_today
def pic_yewu_today(testid):
    pass


# 返回统计图片，ci丹田
from .hualala.yunxing_tongji import pic_yewu_today_email


@app.route('/pic_yewu_today_email', methods=['POST', 'GET'])
@pic_yewu_today_email
def pic_yewu_today_email():
    pass


# from hualala.yunxing_tongji import pic_local_today_email
# @app.route('/pic_local_today_email',methods=['POST','GET'])
# @pic_local_today_email
# def pic_local_today_email():
#     pass


from .hualala.yunxing_tongji import tongji_mail


@app.route('/tongji_mail', methods=['POST', 'GET'])
@tongji_mail
def tongji_mail():
    pass


# from hualala.yunxing_tongji import pic_yewu_email
# @app.route('/pic_yewu_email/<testid>',methods=['POST','GET'])
# @pic_yewu_email
# def pic_yewu_email(testid):
#     pass


from .hualala.user import add_user_team


@app.route('/add_user_team', methods=['POST', 'GET'])
@add_user_team
def add_user_team():
    pass


from .hualala.user import gengxin_team


@app.route('/gengxin_team', methods=['POST', 'GET'])
@gengxin_team
def gengxin_team():
    pass


# 本地运行统计七天
from .hualala.yunxing_tongji import local_tongji_seven


@app.route('/local_seven_today', methods=['POST', 'GET'])
@local_tongji_seven
def local_tongji_seven():
    pass


from .hualala.yunxing_tongji import local_seven_pic


@app.route('/local_seven_pic/<testid>', methods=['POST', 'GET'])
@local_seven_pic
def local_seven_pic(testid):
    pass


# 本地运行统计七天
from .hualala.yunxing_tongji import local_tongji_today


@app.route('/local_today_today', methods=['POST', 'GET'])
@local_tongji_today
def local_tongji_today():
    pass


from .hualala.yunxing_tongji import local_today_pic


@app.route('/local_today_pic/<testid>', methods=['POST', 'GET'])
@local_today_pic
def local_today_pic(testid):
    pass


from .hualala.save_log_jiequ import save_log_jiequ


@app.route('/save_log_jiequ', methods=['POST', 'GET'])
@save_log_jiequ
def save_log_jiequ():
    pass


@app.route('/plot.png')
def plot():
    from io import BytesIO
    import base64
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(1, 1))
    sio = BytesIO()
    fig.savefig(sio, format='png', bbox_inches='tight', pad_inches=0.0)
    data = base64.encodebytes(sio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)


# appium  ui首页
from .hualala.appium_server import appium_server


@app.route('/appium_server', methods=['GET', 'POST'])
@appium_server
def appium_server():
    pass


# 本地ui 脚本测试
@app.route('/local_ui_test', methods=['GET', 'POST'])
def local_ui_test():
    return render_template('/hualala/pages/local_ui_test.html', port=current_app.config.get('LOCAL_SERVER_PORT'))


# 返回结果页面
@app.route('/open_window_page_result', methods=['GET', 'POST'])
def open_window_page_result():
    return render_template('/hualala/pages/local_ui_result.html', port=current_app.config.get('LOCAL_SERVER_PORT'))


# jmeter 添加lniux信息
from .jmeter_log.jmeter_log import jemter_add_linux


@app.route('/jemter_add_linux', methods=['GET', 'POST'])
@jemter_add_linux
def jemter_add_linux():
    pass


# 获取所有linux信息
from .jmeter_log.jmeter_log import jemter_get_all_linux


@app.route('/jemter_get_all_linux', methods=['GET', 'POST'])
@jemter_get_all_linux
def jemter_get_all_linux():
    pass


# 删除单个linux
from .jmeter_log.jmeter_log import delete_simple_linux


@app.route('/delete_simple_linux', methods=['GET', 'POST'])
@delete_simple_linux
def delete_simple_linux():
    pass


# 运行jmeter_log
from .jmeter_log.jmeter_log import run_linux


@app.route('/run_linux', methods=['GET', 'POST'])
@run_linux
def run_linux():
    pass


# 编辑linux
from .jmeter_log.jmeter_log import bianji_linux


@app.route('/bianji_linux', methods=['GET', 'POST'])
@bianji_linux
def bianji_linux():
    pass


# linux运行停止
from .jmeter_log.jmeter_log import stop_run_linux


@app.route('/stop_run_linux', methods=['GET', 'POST'])
@stop_run_linux
def stop_run_linux():
    pass


# nomon 首页
@app.route('/nmon_log', methods=['GET', 'POST'])
def nmon_log():
    return render_template('/nmon_jmeter/base.html')


# nomon 首页,启动
@app.route('/run_jiankong', methods=['GET', 'POST'])
def run_jiankong():
    json_data = json.loads(request.get_data())
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for i in json_data:
        ip = i
        name = json_data[i]['name']
        password = json_data[i]['password']
        port = int(json_data[i]['port'])
        ssh.connect(ip, port, name, password)
        stdin, stdout, stderr = ssh.exec_command('我的命令')
        ssh.close()
    return jsonify(statu="run_success")


# 资产处常量增加
from .hualala.phone import phone_changliang_add


@app.route('/phone_changliang_add', methods=['GET', 'POST'])
@phone_changliang_add
def phone_changliang_add():
    pass


# 资产增加
from .hualala.phone import add_phone_modal


@app.route('/add_phone_modal', methods=['GET', 'POST'])
@add_phone_modal
def add_phone_modal():
    pass


# 资产编辑
from .hualala.phone import bianji_phone_modal


@app.route('/bianji_phone_modal', methods=['GET', 'POST'])
@bianji_phone_modal
def bianji_phone_modal():
    pass


# 资产管理首页
from .hualala.phone import shouye


@app.route('/zichan_shouye', methods=['GET', 'POST'])
@shouye
def shouye():
    pass


# 删除iphon资源
from .hualala.phone import phone_changliang_delete


@app.route('/phone_changliang_delete', methods=['GET', 'POST'])
@phone_changliang_delete
def phone_changliang_delete():
    pass


# 单独操作
from .hualala.phone import phone_simple_caozuo


@app.route('/phone_simple_caozuo/<name>', methods=['GET', 'POST'])
@phone_simple_caozuo
def phone_simple_caozuo(name):
    pass


# 上传表格
from .hualala.phone import phone_submit


@app.route('/phone_submit', methods=['GET', 'POST'])
@phone_submit
def phone_submit():
    pass


# 导出
from .hualala.phone import excel_daochu


@app.route("/daochu_phone_list", methods=['GET'])
@excel_daochu
def excel_daochu():
    pass


# 删除全部信息
from .hualala.phone import all_phone_delete


@app.route("/all_phone_delete", methods=['POST'])
@all_phone_delete
def all_phone_delete():
    pass


# 获取邮件收发件人性情信息
@app.route('/get_email_detail', methods=['POST', 'GET'])
def get_email_detail():
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    name = cu.execute(
        'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get(
            'X-Real-IP')).fetchall()
    if len(name) == 0:
        return jsonify(error_detail="未登陆，获取不到用户名")
    else:
        name = name[0][0]
    email_detail = [i[0] for i in
                    cu.execute('select address from email_address where user="%s"' % ('weixidong')).fetchall()]
    fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % 'weixidong').fetchall()]
    db.close()
    resp = jsonify(user_name='weixidong', shoujianren=email_detail, fajianren=fajianren)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 接口结果分析首页



@app.route("/jiekou_fenxi", methods=['GET'])
@jiekou_fenxi_shouye
def jiekou_fenxi_shouye():
    pass

@app.route("/chongou_test", methods=['GET'])
@chongou_test
def chongou_test():
    pass
@app.route("/get_git_list", methods=['GET'])
@cross_origin()
@chixujicheng_detaiee
def chixujicheng_detaiee():
    pass

@app.route("/git_bianji", methods=['POST'])
@git_bianji
def git_bianji():
    pass


# 接口持续集成获取运行状态
from .hualala.jiekou_git_chonggou import new_get_run_statu


@app.route("/new_get_run_statu", methods=['POST'])
@cross_origin()
@new_get_run_statu
def new_get_run_statu():
    pass


@app.route("/git_hengfeng_detail", methods=['POST', 'GET'])
def git_hengfeng_detail():
    data = {}
    import requests
    from datetime import datetime
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    data["serviceName"] = "PERSONAL_REGISTER_EXPAND"
    data["platformNo"] = "5000001104"
    data["keySerial"] = "1"
    ss = {
        "redirectUrl": "http://192.168.33.216:5025/23adadff232323",
        "platformUserNo": "HFJYJFCR190509000065999",
        "realName": "苏秦",
        "checkType": "LIMIT",
        "idCardType": "PRC_ID",
        "userRole": "INVESTOR",
        "idCardNo": "513436200005099634",
        "mobile": "19992131029",
        "bankcardNo": "6222600260001072445",
        "bankcode": "COMM",
        "accessType": "FULL_CHECKED",
        "auditStatus": "PASSED",
        "groupAccountNO": "",
        "timestamp": time_now,
        "requestNo": "19050914021912868874",
        "code": "0",
        "status": "SUCCESS"
    }
    # ss = {"redirectUrl": "http://192.168.33.216:5025/git_hengfeng_detail", "checkType": "LIMIT", "timestamp": time_now,
    #       "platformUserNo": "HFJYJFCR190507000000162", "realName": "sunzhen", "idCardType": "PRC_ID",
    #       "userRole": "INVESTOR", "idCardNo": "372928198510260038", "mobile": "19992131026",
    #       "bankcardNo": "6222600260001072444", "bankcode": "COMM", "accessType": "FULL_CHECKED",
    #       "auditStatus": "PASSED", "groupAccountNO": "", "requestNo": "19050713405053234122", "code": "0",
    #       "status": "SUCCESS"}
    data["reqData"] = json.dumps(ss)
    print((data["reqData"]))
    # url="http://115.182.212.71:8783/core-web-pub/hfFundDeposit/bindCard/confirm"
    url_sing = 'http://xq-app-server.jc1.jieyue.com/xqAppServer/api/APPBizRest/sign/v1/'
    headers = {"Content-Type": "application/json"}
    headers_sing = {"Content-Type": "application/json"}
    headers_sing['reqJSON'] = data["reqData"]
    k = requests.post(url_sing, data=data["reqData"], headers=headers_sing)
    print((8888888888888888888888888))
    print((k.text))
    k = json.loads(k.text)['responseBody']['sign']
    print(k)
    data["sign"] = k
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    dd = 'http://47.95.110.16:8096/bha-neo-app/lanmaotech/gateway'
    s = requests.post(dd, data=data, headers=headers)
    # print data["respData"]
    # print type(data["respData"])
    print((11111111111111111111111111111111))
    print(data)
    requestkey = s.text.split("requestKey: '")[-1].split("',")[0]
    print(requestkey)
    print((222222222222222))
    # url_msg='http://47.95.110.16:8096/bha-neo-app/gateway/bankcard/bin'
    # data={
    #     'bankcardNo': 6222600260001072445,
    #     'requestKey': requestkey,
    #         'serviceType': 'BANKCARD_AUTH'
    # }
    url_msg = "http://47.95.110.16:8096/bha-neo-app/gateway/sms/smsForEnterprise"
    data = {
        'requestKey': requestkey,
        'bizType': 'REGISTER',
        'mobile': '19992131029'
    }
    s = requests.post(url_msg, data=data, headers=headers)
    url3 = 'http://47.95.110.16:8096/bha-neo-app/gateway/mobile/personalRegisterExpand/register'
    data = {
        'serviceType': 'BANKCARD_AUTH',
        'realName': '苏秦',
        'credType': 'PRC_ID',
        'idCardNo': '513436200005099634',
        'maskedCredNum': '51343 ** ** ** ** ** 634',
        'bankcardNo': '6222600260001072445',
        'mobile': '19992131029',
        'smsCode': '456543',
        'smsCount': '32',
        'password': '655126',
        'confirmPassword': '655126',
        'protocolCheckBox': 'false',
        'requestKey': requestkey
    }
    s = requests.post(url3, data=data, headers=headers)
    return s.text


@app.route("/23adadff232323", methods=['POST', 'GET'])
def adfaffedfdfe():
    return jsonify(statu=2)


@app.route("/test_hengfeng_aa", methods=['POST', 'GET'])
def test_hengfeng_aa():
    return render_template('/1.html')


# 接口持续集成获取运行状态
from .hualala.jiekou_git_chonggou import get_renwu_detail


@app.route("/get_renwu_detail", methods=['POST', 'GET'])
@get_renwu_detail
def get_renwu_detail():
    pass


# from hualala.xiangqian_jiami import  AESCipher
# @app.route("/testtesttest", methods=['POST','GET'])
# def testtesttest():
#     import requests
#     url = 'http://xq-h5-app.jc4.jieyue.com/xqAppServer/depository/bindDepositoryCard/M/'
#     data = {"mobile":"15689783832","custCode":"CR19051600000009"}
#     e = AESCipher('Jy_ApP_0!9i+90&#')
#     headers = {'Content-Type': 'application/json'}
#     enc_str = e.encrypt(json.dumps(data))
#     print 2222222222222222
#     print enc_str
#     data={
# 'aesRequest': enc_str
#
# }
#     # s = requests.post(url, data=json.dumps(data), headers=headers)
#     headers['Cookie']='JSESSIONID=79568F5BA24E1C8AA751DAFC05B9766A'
#     url2='http://115.182.212.71:8783/core-web-pub/hfFundDeposit/bindCard/forward'
#     data2={"ccy":"","bankAcctNo":"","bindflag":"","jyAcctId":"92000000000000000001854151","acctProv":"","dpChannel":"02","instrCd":"DP0102","changeFlag":"1","callPageUrl":"http://api.stg.xiangqianjinfu.com:82/xqAppServer/depository/resultDepositoryCommon/M/?mobile=15689783832&depositoryAccountStatus=0&type=1&appType=null&activityFlag=0","isLoanFlg":"2","acctCity":"","digest":"","busiCode":"20055","dpAcctId":"","acctBrchName":"","hyType":"","transDate":"","busiType":"","acctCardType":"1","oldBankCard":"","sBankCode":"","transTime":"","cardChage":"","role":"","coreTransNo":"","acctCardId":"513436200005168011","openDate":None,"checkType":"","isAppFlg":"1","custType":"0","reqId":"19051614385740313918","validateDate":None,"bankAcctName":"孙振","bankAcctType":"","interfaceNo":"20055","reqBusiParam":"","bankCd":"","bankMobile":"","bankName":"","userRole":"","cardType":"","checker":"","pass":"","dpStatus":"","bankCode":"","bankId":"","callBackUrl":"http://xq-account.jc4.jieyue.com/account/AC005/v2","message":"","bankFlg":"","cvn2":"","custCode":"CR19051600000009","bankAcctSt":"","applicant":"","busiNo":"","sysSource":"5","subSysSource":"","subsidiaryCode":"JYJF"}
#     s = requests.post(url2, data=json.dumps(data2), headers=headers)
#     return s.text
#     return e.decrypt(json.loads(s.text)['aesResponse'])
#
#
# @app.route("/adadfdaf", methods=['POST','GET'])
# def adadfdaf():
#     import requests
#     url1='http://47.95.110.16:8096/bha-neo-app/gateway/desktop/recharge/rechargeSwift.do'
#     data={
#         'needSecurityCode': True,
#         'pageBank': 'CMBC',
#         'maskedBankcardNo': '0818',
#             'maskedMobile': '152 ** ** 4142',
#     'projectName':'',
#     'smsCode': 'qwerew',
#     'smsCount': 6,
#     'password': 655126,
#     'encryptPassword':'',
#     'maskPassword':'',
#     'randomNum':'',
#     'requestKey': '9ed1a028-caaa-4140-b08d-f16e27119b00'
#     }
#     header={'Content-Type': 'application/x-www-form-urlencoded'}
#     return requests.post(url1,data=data,headers=header).text
#
#
#
# @app.route("/jfiejfeie", methods=['POST','GET'])
# def jfiejfeie():
#     import requests
#     url1='http://47.95.110.16:8096/bha-neo-app/gateway/desktop/checkPassword/checkPassword'
#
#
#     data={
# 	"password": "655126",
# 	"encryptPassword": "",
# 	"maskPassword": "",
# 	"randomNum": "",
# 	"requestKey": "7a76d2cd-84c0-43bd-a9fd-e87c516551bb"
# }
#     header={'Content-Type': 'application/x-www-form-urlencoded'}
#     return requests.post(url1,data=data,headers=header).text
#
#
# @app.route("/adfadfasdfadf", methods=['POST','GET'])
# def adfadfasdfadf():
#     import requests
#     s= {
#     "result": "\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\n<!DOCTYPE html>\n<html>\n<head>\n\n\n    <meta charset=\"utf-8\">\n    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge,chrome=1\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n    <meta http-equiv=\"pragma \" content=\"no-cache \">\n    <meta http-equiv=\"cache-control \" content=\"no-cache \">\n    <meta http-equiv=\"expires \" content=\"0 \">\n    <meta content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0\" name=\"viewport\">\n    <title>返回通知</title>\n    \n\n\n<script src=\"/bha-neo-app/resource/jquery/jquery.min.js\"></script>\n<script type=\"text/javascript\" src=\"/bha-neo-app/resource/validform/Validform_v16.js\"></script>\n\n  \r\n    \r\n    <script type=\"text/javascript\">\r\n        function redirectUrl() {\r\n            document.form0.submit();\r\n        }\r\n        $(document).ready(function () {\r\n            redirectUrl();\r\n        });\r\n    </script>\r\n\n\n    <link rel=\"icon\" href=\"/bha-neo-app/resource/images/favicon-LM.ico\"\n          mce_href=\"/resource/custom/favicon-LM.ico\" type=\"image/x-icon\">\n    <link rel=\"shortcut icon\" href=\"/bha-neo-app/resource/images/favicon-LM.ico\"\n          mce_href=\"/resource/custom/favicon-LM.ico\" type=\"image/x-icon\">\n    <link type=\"text/css\" href=\"/bha-neo-app/resource/css/jquery.areaopt.css\" rel=\"stylesheet\"/>\n    <link type=\"text/css\" href=\"/bha-neo-app/resource/css/style_v16.css\" rel=\"stylesheet\"/>\n\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/jquery.areaopt.js\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/cfca-LM/CFCASIPInput.min.js\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/bha_v15.js\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/requestKey.js?v=2.0\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/areaopt.data.js\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/clipboard.min.js\"></script>\n    <script type=\"text/javascript\" src=\"/bha-neo-app/resource/js/crypto-js.js\"></script>\n    \n</head>\n<body>\n\n\n    \n        <div class=\"header\">\n            <div class=\"div-m\">\n                    \n                <h1 class=\"logo\">\n                   \n                       \n                       \n                           \n                               \n                               \n                                   <a href=\"#\" class=\"logoImg\">\n                                       <img src=\"/bha-neo-app/resource/images/logo-LM.png\">\n                                   </a>\n                               \n                           \n                       \n                   \n                </h1>\n            </div>\n        </div>\n    \n\n\n\n  \r\n<form name=\"form0\" action='http://115.182.212.71:8783/core-web-pub/hfFundDeposit/checkPwd/confirm' method=\"post\">\r\n    <input type=\"hidden\" name=\"serviceName\" value='CHECK_PASSWORD'/>\r\n    <input type=\"hidden\" name=\"platformNo\" value=\"5000001104\"/>\r\n    <input type=\"hidden\" name=\"responseType\" value=\"CALLBACK\"/>\r\n    <input type=\"hidden\" name=\"keySerial\" value=\"1\"/>\r\n    <input type=\"hidden\" name=\"respData\" value=\"{&#034;platformUserNo&#034;:&#034;HFJYJFCR190527000000372&#034;,&#034;bizTypeDescription&#034;:&#034;存管用户银行卡交易密码验证&#034;,&#034;requestNo&#034;:&#034;19052815450694794379&#034;,&#034;code&#034;:&#034;0&#034;,&#034;status&#034;:&#034;SUCCESS&#034;}\"/>\r\n    <input type=\"hidden\" name=\"userDevice\" value=\"PC\"/>\r\n    <input type=\"hidden\" name=\"sign\" value=\"eiPqP2W9VZ7nOLj4zqYmMpR6pUHhdehhVBEpuGPYCiTRs4avWnwQqkQEyWrB73bDRniA+KrVCVue4WAcFNpGhxtDhbnOYTMGtuuXC91TZav5c9Ns4PYU1sCnbBb71gn/hNavt18gl5IXRG5DXE8GpG7svFwjcr0/Jcn3bOMgh5BeMcxyleuSx1pGwdR1TK8Ly6DgtxDL50+X4aSidojNKAV0YgCMC4yXidvePJEhTjaSnL76vfaLvHL4kaE34Q+Qb0Rlga5SdBvhQFHqD+86JTobhEg9sRHHOlSpv/vHBZXso86zT5m4JWUWWDPwaPnFdLih/1yBfEgs8fjs5RZEQg==\"/>\r\n    <input type=\"hidden\" name=\"showBankInfoError\" value=\"true\"/>\r\n</form>\r\n\r\n    <!--主体开始-->\r\n    <div class=\"container\">\r\n        <div class=\"infoBar\">\r\n            <div class=\"div-m\">\r\n                <span class=\"subtitle\">跳转中</span>\r\n            </div>\r\n        </div>\r\n        <div class=\"div-m\">\r\n            <div class=\"formBlock\">\r\n                <div class=\"processingCon tc\">\r\n                    \r\n                        <img src=\"/bha-neo-app/resource/images/loading-LM.gif\">\r\n                    \r\n                    即将前往 <span class=\"blue\">平台页面</span>，请耐心等待...\r\n                </div>\r\n            </div>\r\n        </div>\r\n        <div class=\"clear\"></div>\r\n        \r\n            \r\n            <div class=\"tips\" style=\"color:#AAAAAA\">温馨提示：恒丰银行不承担网贷平台的投融资标的物及投融资人的审核责任，不对网贷平台业务提供明示或默示的担保或连带责任，网贷平台的交易风险由投融资人自行承担，与恒丰银行无关。</div>\r\n        \r\n        \r\n    </div>\r\n    <!--主体结束-->\r\n\r\n\r\n\n\n\n<div id=\"__env__\" style=\"visibility: collapse;\">\n    <input type=\"hidden\" id=\"contextPath\" name=\"contextPath\" value='/bha-neo-app'/>\n    <input name='requestKey' id='requestKey' type='hidden' value='b4d42474-0c5a-43f5-8328-2810d9c982ec'/>\n</div>\n\n<div class=\"footer\">\n    <p class=\"tc\">\n        \n    </p>\n</div>\n<div id=\"mask\" style=\"display: none;\"></div>\n<div id=\"alertLayer-2\" style=\"display: none; width: 400px; height: 210px;\">\n    <div class=\"layerTit\">提 示</div>\n    <div class=\"layerCtr\">\n        <div class=\"layerCon tc\"></div>\n        <a href=\"javascript:void(0);\" class=\"submitBtn submitBtn-2\">我知道了</a>\n    </div>\n</div>\n<script src=\"/bha-neo-app/resource/js/my2.js\" type=\"text/javascript\"></script>\n<script src=\"/bha-neo-app/resource/js/cfca-LM/cfcaEncrypt.js\" type=\"text/javascript\"></script>\n\n\n</body>\n</html>"
# }
#     respdata=json.loads(s['result'].split('name="respData" value="')[-1].split('"')[0].replace('&#034;','"'))
#     sign=s['result'].split('name="sign" value="')[-1].split('"')[0].replace('&#034;','"')
#     url1='http://115.182.212.71:8783/core-web-pub/hfFundDeposit/checkPwd/confirm'
#     parm=  {
#        'serviceName': 'CHECK_PASSWORD',
#         'platformNo': '5000001104',
#         'responseType': 'CALLBACK',
#         'keySerial': '1',
#         'respData':respdata,
#         "userDevice": "PC",
#         "sign":sign
#     }
#     header={'Content-Type': 'text/html;charset=UTF-8'}
#     s=requests.post(url1,data=parm,headers=header).text
#     print 1111111111111111111111111
#     print  s
#     return s
#


# 读取linux_log.txt文件
@app.route('/insert_xingneng_jiekou', methods=['GET', 'POST'])
@cross_origin()
def insert_xingneng_jiekou():
    jiekou_name = request.form['jiekou_name']
    new_url = request.form['new_url']
    new_header = request.form['new_header']
    new_body = request.form['new_body']
    old_url = request.form['old_url']
    old_header = request.form['old_header']
    old_body = request.form['old_body']
    # 查看定时运行的结果文件
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    cu.executemany('INSERT INTO xingneng_jiekou VALUES (?,?,?,?,?,?,?,?)', [
        ('', jiekou_name, new_url, new_header, new_body, old_url, old_header, old_body)])
    db.commit()
    return jsonify(statu="success")


@app.route("/submit_question_page", methods=['GET'])
def submit_question_page():
    return render_template('/hualala/pages/question_tijiao.html')


@app.route("/json_take", methods=['GET'])
def json_ti_qu():
    return render_template('/mafengwo/json_get_new.html')


@app.route("/json_ti_qu_if", methods=['GET'])
def json_ti_qu_if():
    return render_template('/hualala/pages/iframe_page.html')


@app.route("/Continuous_integration", methods=['GET'])
def Continuous_integration():
    db = sqlite3.connect(current_app.config.get('CONTIN'))
    cu = db.cursor()
    a = [list(i) for i in cu.execute('select * from version_detail ').fetchall()]
    for k, i in enumerate(a):
        z = cu.execute('select bus_name,id from bus_detail where id={}'.format(int(i[2]))).fetchall()[0]
        a[k] += z
        a[k][4] = time.strftime("%Y-%m-%d", time.localtime(int(a[k][4])))
        z = cu.execute('select count(*)  from case_detail where version_id=%s' % (str(i[0]))).fetchall()[0][0]
        a[k].append(z)
        z = cu.execute('select count(*)  from interface_detail where version_id=%s' % (str(i[0]))).fetchall()[0][0]
        a[k].append(z)
    b= [list(i) for i in cu.execute('select * from bus_detail ').fetchall()]
    mulu_all = {}
    all_ca={}
    if len(a)!=0:
        all_ca=cu.execute('select *  from catalog_detail where version_id=%s' % (str(i[0]))).fetchall()
        for i  in all_ca:
            if i[2]  not in mulu_all.keys():
                mulu_all[i[2]]=[[i[0],i[3]]]
            else:
                mulu_all[i[2]].append([i[0],i[3]])
    db.close()
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    super_user=current_app.config.get('DB_JURISDICITION').split(',')
    all_user=[i[0]  for i in cu.execute('select name from user').fetchall() if i[0] not in super_user]
    all_user.sort(key=lambda i:len(i),reverse=True)
    print  (url_for('chongou_test'))
    db.close()
    return render_template('/hualala/pages/chixujicheng_chonggou.html',mulu_all=mulu_all,all_data=a,bus_data=b,all_user=all_user,all_ca=all_ca)


@app.route("/inter_face_detail", methods=['POST','GET'])
@inter_face_detail
def inter_face_detail():
    pass


@app.route("/get_file", methods=['POST','GET'])
def get_file():
    params_file=request.files['file']
    for k,i in request.files.items():
        print (k)
    print (params_file.name)
    dst = os.path.join(r'C:\Users\Administrator\Desktop\新建文件夹 (3)', params_file.name)
    params_file.save(dst)
    return jsonify(statu="success")
    pass


@app.route("/testtest_file", methods=['POST','GET'])
def testtest_file():
    return render_template('/tools/test_index.html')


@app.route("/test_vuee", methods=['POST','GET'])
@cross_origin()
def test_vuee():
    return json.dumps(current_app.config.get('test_all_data'))
from app.jisuan_kaohao.change_config import *
import redis
@app.route("/get_yuanshifen_qujian", methods=['POST','GET'])
@cross_origin()
def get_yuanshifen_qujian():
    try:
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                                    user='QA', password='hmk#%^&djofsdh', database='exam_databoard', charset='utf8')
    except:
        return  jsonify(status='fail',detail='连不上数据库')
    else:
        sql_data='SELECT exam_registration_no,student_name,subject_code,score,school_code,grade_code,class_code,class_name FROM exam_score_transfer_for_bi WHERE exam_id= {}'.format(str(request.args.get('kaohao')))
        cursor = conn.cursor()
        cursor.execute(sql_data)
        this_all_data = cursor.fetchall()
        if len(this_all_data)<=0:
            return jsonify(status='fail', detail='该考试数据在bi表中查不到')
        conn.close()
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    except:
        return jsonify(status='fail', detail='连不上redis')
    kaohao = int(request.args.get('kaohao'))
    if not r.get('return_Data'):
        r.set('return_Data', json.dumps({int(kaohao):''}))
    elif str(kaohao) not in json.loads(r.get('return_Data')).keys():
        this_dict=  json.loads(r.get('return_Data'))
        this_dict[int(kaohao)] = {}
        r.set('return_Data',json.dumps(this_dict))
    executor.submit(long_task, kaohao)
    # print ( r.get('return_Data'))
    print("保存成功")
    return jsonify(result=r.get('nameeee'),status='success')

@app.route("/kaoshifenxi_firdst_run_statu", methods=['POST','GET'])
@cross_origin()
def kaoshifenxi_firdst_run_statu():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    if not r.get('return_Data'):
        r.set('return_Data', {})
    # u = r.get('return_Data')
    # print (u)
    kaohao = request.args.get('kaohao')
    results= executor.submit(long_task, kaohao)
    for result in results:
        print(result)
    return jsonify(result=r.get('nameeee'))

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)
def long_task(kaohao):
    return_data = get_all_fufen(kaohao).get_fufen()
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    this_dict=json.loads(r.get('return_Data'))
    this_dict[str(kaohao)]=return_data
    r.set('return_Data', json.dumps(this_dict))

@app.route("/get_score_stuecnt_axios", methods=['POST','GET'])
@cross_origin()
def get_score_stuecnt_axios():
    request_data= json.loads(request.get_data())
    kaoshihao= request_data['kaoshihao']
    kaohao=request_data['kaohao']
    zuhe_list= request_data['zuhe_list']
    fufen_or_yuanshifen = request_data['fufen_or_yuanshifen']
    all_studend_all_score= request_data['all_studend_all_score']
    all_score_list = request_data['all_score_list']
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[kaoshihao]
    return_data = get_zuhe_paiming(kaohao, zuhe_list, all_studend_all_score, all_score_list, fufen_or_yuanshifen)
    try:
        return_data=get_zuhe_paiming(kaohao,zuhe_list,all_studend_all_score,all_score_list,fufen_or_yuanshifen)
    except:
        return jsonify(statu='error',detail='学号不存在')
    print (return_data)
    return jsonify(dict_data=return_data)

@app.route("/get_score_banji_axios", methods=['POST','GET'])
@cross_origin()
def get_score_banji_axios():
    request_data= json.loads(request.get_data())
    kaoshihao= request_data['banji_detail']['kaoshihao']
    banji_id=request_data['banji_detail']['banji_id']
    zuhe_list= request_data['banji_detail']['xueke']
    fufen_or_yuanshifen = request_data['banji_detail']['banji_type']
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list= json.loads(r.get('return_Data'))[str(kaoshihao)]
    try:
        return_data=get_zuhe_paiming_banji(kaoshihao,banji_id,zuhe_list,all_studend_all_score,all_score_list,fufen_or_yuanshifen)
    except:
        return jsonify(statu='error',detail='老师名不存在')
    print (return_data)
    return jsonify(dict_data=return_data)


import traceback
@app.route("/get_xiaozhang_score_fenbu", methods=['POST','GET'])
@cross_origin()
def get_xiaozhang_score_fenbu():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    jiange = int(request_data['jiange'])
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！')
    try:
        all_score, xuexiao_score_all, banji_score_all, banji_info = get_danke_score(all_studend_all_score, class_type, xuexiao_id, zongfen_type=1)
        all_total_score_list = all_score.get("总分")
        xuexiao_total_score_list = xuexiao_score_all.get("总分", [])
        if not xuexiao_total_score_list:
            return jsonify(statu='error',detail='考试数据中没有这个学校的数据，请检查学校id是否正确！')
        return_data={
            "联考成绩分布": jisuan_score_fnbu(all_total_score_list, jiange),
            "本校成绩分布": jisuan_score_fnbu(xuexiao_total_score_list, jiange),
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='校长报告-联考成绩分布 计算异常', error_log=error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)

def jisuan_score_fnbu(score_list, jiange = 20):  # 计算成绩区间的人数，包左不包右
    max_score = max(score_list)
    max_fenbuzu = int(max_score/jiange) + 1
    fenbu_renshu = [ 0 for n in range(max_fenbuzu) ]
    for score in score_list:
        fenbu_renshu[int(float(score)/jiange)] += 1
    fenbu_renshu_result = [["%s-%s"%(i[0]*jiange, (i[0]+1)*jiange), i[1]] for i in list(enumerate(fenbu_renshu)) ]
    return fenbu_renshu_result


@app.route("/get_jianzisheng_xuekepipei", methods=['POST','GET'])
@cross_origin()
def get_jianzisheng_xuekepipei():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    renshu = int(request_data['jianzishengrenshu'])
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！')
    try:
        jianzisheng_list = jisuan_jianzisheng_renshu(all_studend_all_score, xuexiao_id, renshu, class_type)
        if not jianzisheng_list:
            return jsonify(statu='error',detail='尖子生数据获取异常，请检查请求参数是否正确！')
        all_score_list=[]
        for k,i in all_studend_all_score.items():
            all_score_list.append([k,i])
        import copy
        jianzisheng_xuekepippei = copy.deepcopy(jianzisheng_list)
        for n in range(len(jianzisheng_list)):
            jianzisheng = jianzisheng_xuekepippei[n]
            xuesheng_id = jianzisheng[0]
            kaoshixueke = list(jianzisheng[-1].keys())
            paiming = get_zuhe_paiming(xuesheng_id, kaoshixueke, all_studend_all_score, all_score_list,"原始分")   # 计算总分的排名
            jianzisheng.insert(-1, paiming['联盟名次'])
            jianzisheng.insert(-1, paiming['班级名次'])
            if class_type == 1:
                xuekepaiming = get_zuhe_paiming(xuesheng_id, ["政治", "历史", "地理"], all_studend_all_score, all_score_list,"原始分")
                jianzisheng[-1]["文综"] = xuekepaiming['学校名次']
            elif class_type == 2:
                xuekepaiming = get_zuhe_paiming(xuesheng_id, ["物理", "化学", "生物"], all_studend_all_score, all_score_list,"原始分")
                jianzisheng[-1]["理综"] = xuekepaiming['学校名次']
            for xueke in kaoshixueke:
                xuekepaiming = get_zuhe_paiming(xuesheng_id, [xueke], all_studend_all_score, all_score_list,"原始分")
                jianzisheng[-1][xueke] = xuekepaiming['学校名次']
        return_data={
            "尖子生学科匹配": jianzisheng_xuekepippei
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error', detail='校长报告-尖子生学科匹配 计算异常', error_log=error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)

def jisuan_jianzisheng_renshu(all_studend_all_score, xuexiao_id, renshu, class_type):
    benxiao_total_score_list = []  # 数据结构为[[学生id，姓名，班级名称，总分, {各科成绩}], [学生id，姓名，班级名称，总分, {各科成绩}], ...]
    for xuesheng_id in list(all_studend_all_score.keys()):
        xuesheng = all_studend_all_score[xuesheng_id]
        if class_type in [1,2] and class_type != int(xuesheng["班级信息"]["class_type"]):
            all_studend_all_score.pop(xuesheng_id)
            continue
        if int(xuesheng["班级信息"]["school_code"]) == int(xuexiao_id):
            benxiao_total_score_list.append([xuesheng_id, xuesheng["班级信息"]["student_name"], xuesheng["班级信息"]["class_name"], sum(list(xuesheng["原始分"].values())), xuesheng["原始分"]])
    get_jianzisheng_list(benxiao_total_score_list, class_type)
    return benxiao_total_score_list[0: renshu]

def get_jianzisheng_list(score_list, class_type):
    if class_type == 1:
        wen_or_li = ["政治", "历史", "地理"]
    elif class_type == 2:
        wen_or_li = ["物理", "化学", "生物"]
    else:
        wen_or_li = ["政治", "历史", "地理","物理", "化学", "生物"]
    if wen_or_li:
        score_list.sort(key=lambda i: (i[3], i[4]["语文"]+i[4]["数学"]+i[4]["英语"], i[4]["语文"]+i[4]["数学"], i[4]["语文"], i[4][wen_or_li[0]], i[4][wen_or_li[1]], i[4][wen_or_li[2]] ), reverse=True)
    else:
        score_list.sort(key=lambda i:i[3], reverse=True) 


@app.route("/get_jianzisheng_tiduichaju", methods=['POST','GET'])
@cross_origin()
def get_jianzisheng_tiduichaju():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    diyititui_renshu = int(request_data['diyitituirenshu'])
    diertidui_renshu = int(request_data['diertiduirenshu'])
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！')
    try:
        jianzisheng_list = jisuan_jianzisheng_renshu(all_studend_all_score, xuexiao_id, diyititui_renshu + diertidui_renshu, class_type)
        if not jianzisheng_list:
            return jsonify(statu='error',detail='尖子生数据获取异常，请检查请求参数是否正确！')
        all_score = {"总分": []}    # {"总分": [], "物理": [], .....}
        for jianzisheng in jianzisheng_list:
            all_score["总分"].append(jianzisheng[3])
            for xueke in jianzisheng[-1]:
                if xueke not in all_score:
                    all_score[xueke] = []
                all_score[xueke].append(jianzisheng[-1][xueke])
            if class_type == 1:
                all_score.setdefault("文综", [])
                all_score["文综"].append(jianzisheng[-1]["政治"] + jianzisheng[-1]["历史"] + jianzisheng[-1]["地理"])
            elif class_type == 2:
                all_score.setdefault("理综", [])
                all_score["理综"].append(jianzisheng[-1]["物理"] + jianzisheng[-1]["化学"] + jianzisheng[-1]["生物"])
        tiduichaju = {}
        for n in all_score:
            diyitidui_avg = mean(all_score[n][0:diyititui_renshu])
            diertidui_avg = mean(all_score[n][diyititui_renshu:])
            tiduichaju[n] = {
                "第一梯队平均分": '%.2f' %diyitidui_avg,
                "第二梯队平均分": '%.2f' %diertidui_avg,
                "梯队差值": '%.2f' %(diyitidui_avg - diertidui_avg),
            }
        return_data={
            "尖子生梯队差距": tiduichaju
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='校长报告-尖子生学科匹配 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)


@app.route("/get_jianzisheng_chengjiqushi", methods=['POST','GET'])
@cross_origin()
def get_jianzisheng_chengjiqushi():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    xuesheng_id = request_data['xuesheng_id']   
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！')
    try:
        jianzisheng = all_studend_all_score.get(str(xuesheng_id),None)
        if not jianzisheng or int(jianzisheng["班级信息"].get("class_type", None)) != class_type:
            return jsonify(statu='error',detail='学生ID不存在或者class_type参数错误，请先检查参数！')
        xuesheng_score_all = jianzisheng["原始分"].copy()
        xuesheng_score_all["总分"] = sum(list(xuesheng_score_all.values()))       
        all_score, xuexiao_score_all, banji_score_all, banji_info = get_danke_score(all_studend_all_score, class_type, xuexiao_id, zongfen_type=1, wenlizong_type=0)
        jianzisheng_qushi = {}
        for xueke in xuesheng_score_all:
            jianzisheng_qushi[xueke] = jisuan_biaozhunfen(xuesheng_score_all[xueke], xuexiao_score_all[xueke])
        return_data={
            "尖子生成绩趋势": jianzisheng_qushi
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='校长报告-尖子生成绩趋势 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)

import numpy
def jisuan_biaozhunfen(xuesheng_score, score_list):
    if len(score_list) == 1 and xuesheng_score == score_list[0]:
        biaozhunfen = 0
    else:
        baiozhuncha = numpy.std(score_list, ddof=1)
        biaozhunfen = (xuesheng_score - mean(score_list))/baiozhuncha
    biaozhunfen_meihua = 500 + 100 * biaozhunfen
    return '%.2f' %biaozhunfen,'%.2f' %biaozhunfen_meihua


@app.route("/get_zhuren_zongtifenxi", methods=['POST','GET'])
@cross_origin()
def get_zhuren_zongtifenxi():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！')
    try:
        all_score, xuexiao_score_all, banji_score_all, banji_info = get_danke_score(all_studend_all_score, class_type, xuexiao_id, zongfen_type=1)
        zongtifenxi_result = {}
        for xueke in all_score:
            zhibiao = {}
            all_xueke_score = all_score[xueke]
            all_xueke_score.sort(reverse=True)
            xuexiao_xueke_score = xuexiao_score_all[xueke]   
            if not xuexiao_xueke_score:
                return jsonify(statu='error',detail='获取的学校数据异常，请检查学校id是否正确！')
            xuexiao_xueke_score.sort(reverse=True)
            all_avg = mean(all_xueke_score)
            xuexiao_avg = mean(xuexiao_xueke_score)
            zhibiao.update({"平均分":{
                "本校": '%.2f' %xuexiao_avg,
                "联盟": '%.2f' %all_avg,
                "两者差值": '%.2f' %(xuexiao_avg - all_avg)
            }})
            xuexiao_zhongweishu = jisuan_zhongweizhu(xuexiao_xueke_score)
            all_zhongweishu = jisuan_zhongweizhu(all_xueke_score)
            zhibiao.update({"中位数":{
                "本校": '%.2f' %xuexiao_zhongweishu,
                "联盟": '%.2f' %all_zhongweishu,
                "两者差值": '%.2f' %(xuexiao_zhongweishu - all_zhongweishu)    
            }})
            xuexiao_zhongshu = jisuan_zhongshu(xuexiao_xueke_score)
            all_zhongshu = jisuan_zhongshu(all_xueke_score)
            zhibiao.update({"众数":{
                "本校": xuexiao_zhongshu,
                "联盟": all_zhongshu  
            }})
            xuexiao_min = min(xuexiao_xueke_score)
            all_min = min(all_xueke_score)
            xuexiao_max = max(xuexiao_xueke_score)
            all_max = max(all_xueke_score)
            zhibiao.update({"最低分":{
                "本校": xuexiao_min,
                "联盟": all_min,  
                "两者差值": xuexiao_min - all_min
                },
                "最高分":{
                "本校": xuexiao_max,
                "联盟": all_max,  
                "两者差值": xuexiao_max - all_max
                },
                "计分人数":{
                "本校": len(xuexiao_xueke_score),
                "联盟": len(all_xueke_score) 
                }
            })
            zongtifenxi_result[xueke] = zhibiao
        return_data={
            "考试总体分析": zongtifenxi_result
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年纪主任报告-考试总体分析 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)    

def jisuan_zhongweizhu(score_list):
    geshu = len(score_list)
    if geshu % 2 == 0:
        return (score_list[geshu//2] + score_list[geshu//2-1])/2
    else:
        return score_list[geshu//2]

from collections import Counter
def jisuan_zhongshu(score_list):
    result = []
    tongjishuliang = Counter(score_list)
    tongjishuliang_list = list(tongjishuliang.items())
    tongjishuliang_list.sort(key=lambda i:i[1], reverse=True)
    stop_tag = tongjishuliang_list[0][1]
    for s, n in tongjishuliang_list:
        if n != stop_tag:
            break
        result.append(str(s))
    return ",".join(result)


@app.route("/get_zhuren_chengjiqushi", methods=['POST','GET'])
@cross_origin()
def get_zhuren_chengjiqushi():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id'] 
    banji_id_list = request_data['banji_id_list'] 
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！') 
    try:
        all_score, xuexiao_score_all, banji_score_all, banji_info = get_danke_score(all_studend_all_score, class_type, xuexiao_id)
        # 计算各种各科的平均分
        xuexiao_avg_score_all, banji_avg_score, banji_chengjiqushi = {}, {}, {}
        for banji_id in banji_id_list:
            banji_avg_score.setdefault(banji_id,{})
            banji_chengjiqushi.setdefault(banji_id,{'班级名称': banji_info.get(banji_id, ""), '各科成绩趋势': {}})
        for class_code in banji_score_all:
            banji_score = banji_score_all[class_code]
            for xueke in banji_score:
                xueke_score_avg = mean(banji_score[xueke])
                xuexiao_avg_score_all.setdefault(xueke,[])
                xuexiao_avg_score_all[xueke].append(xueke_score_avg)
                if class_code in banji_id_list:
                    banji_avg_score[class_code][xueke] = xueke_score_avg
        for banji_id in banji_avg_score:
            banji_score = banji_avg_score[banji_id]
            for xueke in banji_score:
                banji_avg = banji_score[xueke]
                avg_score_list = xuexiao_avg_score_all[xueke]
                biaozhunfen = jisuan_biaozhunfen(banji_avg, avg_score_list)
                banji_chengjiqushi[banji_id]["各科成绩趋势"][xueke] = biaozhunfen
        return_data={
            "班级成绩趋势": banji_chengjiqushi
        }
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年级主任报告-班级成绩趋势 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)


@app.route("/get_zhuren_boruixueke", methods=['POST','GET'])
@cross_origin()
def get_zhuren_boruixueke():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id']
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！') 
    try:
        all_score, xuexiao_score_all, banji_score_all, banji_info = get_danke_score(all_studend_all_score, class_type, xuexiao_id)
        boruoxueke = {}
        for xueke in all_score:
            danke_boruo = {}
            danke_boruo["联盟均分"] = '%.2f' %mean(all_score[xueke])
            danke_boruo["年级均分"] = '%.2f' %mean(xuexiao_score_all[xueke])
            for banji_id in banji_score_all:
                danke_boruo["%s班均分"%banji_info[banji_id]] = '%.2f' %mean(banji_score_all[banji_id].get(xueke, 0))
            boruoxueke[xueke] = danke_boruo
        return_data={
            "薄弱学科": boruoxueke
        }  
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年级主任报告-薄弱学科分析 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)

def get_danke_score(all_studend_all_score, class_type, xuexiao_id, wenlizong_type=1, zongfen_type=0):
    # zongfen_type 是否需要总分，1返回总分，0不返回，默认为0
    # wenlizong_type 是否计算文综理综，1返回文综理综，0不返回，默认为1
    all_score, xuexiao_score_all, banji_score_all, banji_info = {}, {}, {}, {}
    for uid in all_studend_all_score:
        if class_type in [1,2] and class_type != int(all_studend_all_score[uid]["班级信息"]["class_type"]):
            continue
        scores =   all_studend_all_score[uid]["原始分"].copy()
        class_code = int(all_studend_all_score[uid]["班级信息"]["class_code"])
        class_name = all_studend_all_score[uid]["班级信息"]["class_name"]   
        if zongfen_type == 1:
            total_score = sum(list(scores.values()))
            if total_score == 0:
                continue
            all_score.setdefault("总分", [])
            all_score["总分"].append(total_score)
            if int(all_studend_all_score[uid]["班级信息"]["school_code"]) == int(xuexiao_id):
                xuexiao_score_all.setdefault("总分", [])
                xuexiao_score_all["总分"].append(total_score)
                banji_score_all.setdefault(class_code, {})
                banji_score_all[class_code].setdefault("总分", [])
                banji_score_all[class_code]["总分"].append(total_score)
        if wenlizong_type ==1 and class_type == 1:
            scores["文综"] = scores["政治"] + scores["历史"] + scores["地理"]
        elif wenlizong_type ==1 and class_type == 2:
            scores["理综"] = scores["物理"] + scores["化学"] + scores["生物"]   
        for xueke in scores:
            if scores[xueke] == 0:
                continue
            all_score.setdefault(xueke, [])
            all_score[xueke].append(scores[xueke])
            if int(all_studend_all_score[uid]["班级信息"]["school_code"]) == int(xuexiao_id):
                xuexiao_score_all.setdefault(xueke, [])
                xuexiao_score_all[xueke].append(scores[xueke])
                banji_info.setdefault(class_code, class_name)
                banji_score_all.setdefault(class_code, {})
                banji_score_all[class_code].setdefault(xueke, [])
                banji_score_all[class_code][xueke].append(scores[xueke])
    return all_score, xuexiao_score_all, banji_score_all, banji_info


@app.route("/get_zhuren_linjieshengfenxi", methods=['POST','GET'])
@cross_origin()
def get_zhuren_linjieshengfenxi():
    request_data = json.loads(request.get_data())
    benci_kaoshihao = request_data['benci_kaoshihao']
    shangci_kaoshihao = request_data.get('shangci_kaoshihao', None)
    xuexiao_id = request_data['xuexiao_id']
    qingbei_line = request_data['qingbei_line']
    qingbei_min = request_data['qingbei_min']
    yiben_line = request_data['yiben_line']
    yiben_min = request_data['yiben_min']
    benke_line = request_data['benke_line']
    benke_min = request_data['benke_min']
    jiange = request_data['jiange']
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score_benci, all_score_list_benci = json.loads(r.get('return_Data'))[str(benci_kaoshihao)]
    if not all_studend_all_score_benci:
        return jsonify(statu='error',detail='redis中没有本次考试id的数据，请检查参数或者先加载考试数据！') 
    try:
        benci_xuexiao_score = get_xuexiao_zongfen(all_studend_all_score_benci, xuexiao_id, class_type)
        if not benci_xuexiao_score:
            return jsonify(statu='error',detail='redis中没有该学校id的考试数据，请检查参数！') 
        benci_qingbei_linjiesheng_list, benci_qingbei_linjiesheng_score_list = jisuan_linjiesheng(benci_xuexiao_score, float(qingbei_line), float(qingbei_min))
        benci_yiben_linjiesheng_list, benci_yibei_linjiesheng_score_list = jisuan_linjiesheng(benci_xuexiao_score, float(yiben_line), float(yiben_min))
        benci_benke_linjiesheng_list, benci_beike_linjiesheng_score_list = jisuan_linjiesheng(benci_xuexiao_score, float(benke_line), float(benke_min))
        benci_xuexiao_cankao_renshu = len(benci_xuexiao_score)
        linjiesheng_fenxi = {"本次考试": {
            "清北临界生人数": len(benci_qingbei_linjiesheng_list),
            "清北临界生比率": '%.2f%%' %(len(benci_qingbei_linjiesheng_list)/benci_xuexiao_cankao_renshu*100),
            "一本临界生人数": len(benci_yiben_linjiesheng_list),
            "一本临界生比率": '%.2f%%' %(len(benci_yiben_linjiesheng_list)/benci_xuexiao_cankao_renshu*100),
            "本科临界生人数": len(benci_benke_linjiesheng_list),
            "本科临界生比率": '%.2f%%' %(len(benci_benke_linjiesheng_list)/benci_xuexiao_cankao_renshu*100),
            }}
        if shangci_kaoshihao:
            all_studend_all_score_shangci, all_score_list_shangci = json.loads(r.get('return_Data'))[str(shangci_kaoshihao)]
            if not all_studend_all_score_shangci:
                return jsonify(statu='error',detail='redis中没有上次考试id的数据，请检查参数或者先加载考试数据！') 
            shangci_xuexiao_score = get_xuexiao_zongfen(all_studend_all_score_shangci, xuexiao_id, class_type)
            if not shangci_xuexiao_score:
                return jsonify(statu='error',detail='redis中没有该学校id的考试数据，请检查参数！')  
            shangci_qingbei_linjiesheng_list, shangci_qingbei_linjiesheng_score_list = jisuan_linjiesheng(shangci_xuexiao_score, float(qingbei_line), float(qingbei_min))
            shangci_yiben_linjiesheng_list, shangci_yibei_linjiesheng_score_list = jisuan_linjiesheng(shangci_xuexiao_score, float(yiben_line), float(yiben_min))
            shangci_benke_linjiesheng_list, shangci_beike_linjiesheng_score_list = jisuan_linjiesheng(shangci_xuexiao_score, float(benke_line), float(benke_min))
            shangci_xuexiao_cankao_renshu = len(shangci_xuexiao_score)
            linjiesheng_fenxi.update({"上次考试": {
                "清北临界生人数": len(shangci_qingbei_linjiesheng_list),
                "清北临界生比率": '%.2f%%' %(len(shangci_qingbei_linjiesheng_list)/shangci_xuexiao_cankao_renshu*100),
                "一本临界生人数": len(shangci_yiben_linjiesheng_list),
                "一本临界生比率": '%.2f%%' %(len(shangci_yiben_linjiesheng_list)/shangci_xuexiao_cankao_renshu*100),
                "本科临界生人数": len(shangci_benke_linjiesheng_list),
                "本科临界生比率": '%.2f%%' %(len(shangci_benke_linjiesheng_list)/shangci_xuexiao_cankao_renshu*100),
                }})
            qingbei_zhuanduansheng_list = jisuan_zhuanduansheng(shangci_qingbei_linjiesheng_list, benci_xuexiao_score, qingbei_line)
            yiben_zhuanduansheng_list = jisuan_zhuanduansheng(shangci_yiben_linjiesheng_list, benci_xuexiao_score, yiben_line)
            benke_zhuanduansheng_list = jisuan_zhuanduansheng(shangci_benke_linjiesheng_list, benci_xuexiao_score, benke_line)
            linjiesheng_fenxi["本次考试"].update({
                "清北转段人数": len(qingbei_zhuanduansheng_list),
                "清北转段比率": '%.2f%%' %(len(qingbei_zhuanduansheng_list)/len(shangci_qingbei_linjiesheng_list)*100),
                "一本转段人数": len(yiben_zhuanduansheng_list),
                "一本转段比率": '%.2f%%' %(len(yiben_zhuanduansheng_list)/len(shangci_yiben_linjiesheng_list)*100),
                "本科转段人数": len(benke_zhuanduansheng_list),
                "本科转段比率": '%.2f%%' %(len(benke_zhuanduansheng_list)/len(shangci_benke_linjiesheng_list)*100),
            })
        return_data={
            "临界生历次考试分析": linjiesheng_fenxi
        }  
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年级主任报告-临界生历次考试分析 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)

def get_xuexiao_zongfen(all_studend_all_score, xuexiao_id, class_type):
    total_score_dict = {}
    for xuesheng_id in all_studend_all_score:
        if class_type in [1,2] and class_type != int(all_studend_all_score[xuesheng_id]["班级信息"]["class_type"]):
            continue
        r = all_studend_all_score[xuesheng_id]
        if int(r["班级信息"]["school_code"]) == int(xuexiao_id):
            total_score = sum(list(r["原始分"].values()))
            if total_score == 0:
                continue
            total_score_dict[xuesheng_id] = sum(list(r["原始分"].values())) 
    return total_score_dict     
            
def jisuan_linjiesheng(score_all, max, min):
    # 含左不含右，包含min，不包括max
    linjiesheng, linjiesheng_score = [], []
    for xuesheng_id in score_all:
        score = score_all[xuesheng_id]
        if max > score and score >= min:
            linjiesheng.append(xuesheng_id)
            linjiesheng_score.append(score)
    return linjiesheng, linjiesheng_score

def jisuan_zhuanduansheng(shangci_linjiesheng_list, benci_xuexiao_score, score_line):
    # 上次考试的临界生，本次考试达到分数线的即为转段生
    zhuanduansheng = []
    for xuesheng_id in shangci_linjiesheng_list:
        benci_score = benci_xuexiao_score.get(xuesheng_id, 0)
        if benci_score >= score_line:
            zhuanduansheng.append(xuesheng_id)
    return zhuanduansheng


@app.route("/get_zhuren_xuekegongxian", methods=['POST','GET'])
@cross_origin()
def get_zhuren_xuekegongxian():
    request_data = json.loads(request.get_data())
    kaoshihao = request_data['kaoshihao']
    xuexiao_id = request_data['xuexiao_id'] 
    qingbei_line = request_data['qingbei_line']
    yiben_line = request_data['yiben_line']
    benke_line = request_data['benke_line']
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有这个考试id的数据，请先加载考试数据！') 
    try:
        lianmeng_total_score, xuexiao_total_score, lianmeng_score, xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, 0) # 分数线为0，获取所有学生
        lianmeng_total_score_avg = mean(lianmeng_total_score)
        xuexiao_total_score_avg = mean(xuexiao_total_score)
        benke_lianmeng_total_score, benke_xuexiao_total_score, benke_lianmeng_score, benke_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, benke_line, yiben_line)
        benke_lianmeng_total_score_avg = mean(benke_lianmeng_total_score) if benke_lianmeng_total_score else 0
        benke_xuexiao_total_score_avg = mean(benke_xuexiao_total_score) if benke_xuexiao_total_score else 0
        benke_lianmeng_total_chazhi = benke_lianmeng_total_score_avg - lianmeng_total_score_avg
        benke_xuexiao_total_chazhi = benke_xuexiao_total_score_avg - xuexiao_total_score_avg
        yiben_lianmeng_total_score, yiben_xuexiao_total_score, yiben_lianmeng_score, yiben_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, yiben_line, qingbei_line)
        yiben_lianmeng_total_score_avg = mean(yiben_lianmeng_total_score) if yiben_lianmeng_total_score else 0
        yiben_xuexiao_total_score_avg = mean(yiben_xuexiao_total_score) if yiben_xuexiao_total_score else 0
        yiben_lianmeng_total_chazhi = yiben_lianmeng_total_score_avg - lianmeng_total_score_avg
        yiben_xuexiao_total_chazhi = yiben_xuexiao_total_score_avg - xuexiao_total_score_avg
        qingbei_lianmeng_total_score, qingbei_xuexiao_total_score, qingbei_lianmeng_score, qingbei_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, qingbei_line)
        qingbei_lianmeng_total_score_avg = mean(qingbei_lianmeng_total_score) if qingbei_lianmeng_total_score else 0
        qingbei_xuexiao_total_score_avg = mean(qingbei_xuexiao_total_score) if qingbei_xuexiao_total_score else 0
        qingbei_lianmeng_total_chazhi = qingbei_lianmeng_total_score_avg - lianmeng_total_score_avg
        qingbei_xuexiao_total_chazhi = qingbei_xuexiao_total_score_avg - xuexiao_total_score_avg
        xuekegongxiang = {"本科": {
            "联考学科贡献": {"全科":{
                "联考达线生均分": "%.2f"%benke_lianmeng_total_score_avg,
                "联考均分": "%.2f"%lianmeng_total_score_avg,
                "均分差": "%.2f"%benke_lianmeng_total_chazhi
            }},
            "本校学科贡献": {"全科": {
                "本校达线生均分": "%.2f"%benke_xuexiao_total_score_avg,
                "本校均分": "%.2f"%xuexiao_total_score_avg,
                "均分差": "%.2f"%benke_xuexiao_total_chazhi  
            }}
        },"一本": {
            "联考学科贡献": {"全科":{
                "联考达线生均分": "%.2f"%yiben_lianmeng_total_score_avg,
                "联考均分": "%.2f"%lianmeng_total_score_avg,
                "均分差": "%.2f"%yiben_lianmeng_total_chazhi
            }},
            "本校学科贡献": {"全科": {
                "本校达线生均分": "%.2f"%yiben_xuexiao_total_score_avg,
                "本校均分": "%.2f"%xuexiao_total_score_avg,
                "均分差": "%.2f"%yiben_xuexiao_total_chazhi    
            }}
        },"清北": {
            "联考学科贡献": {"全科":{
                "联考达线生均分": "%.2f"%qingbei_lianmeng_total_score_avg,
                "联考均分": "%.2f"%lianmeng_total_score_avg,
                "均分差": "%.2f"%qingbei_lianmeng_total_chazhi
            }},
            "本校学科贡献": {"全科": {
                "本校达线生均分": "%.2f"%qingbei_xuexiao_total_score_avg,
                "本校均分": "%.2f"%xuexiao_total_score_avg,
                "均分差": "%.2f"%qingbei_xuexiao_total_chazhi   
            }}
        }}
        all_score = {
            "本科": [benke_lianmeng_score, benke_xuexiao_score, benke_lianmeng_total_chazhi, benke_xuexiao_total_chazhi],
            "一本": [yiben_lianmeng_score, yiben_xuexiao_score, yiben_lianmeng_total_chazhi, yiben_xuexiao_total_chazhi],
            "清北": [qingbei_lianmeng_score, qingbei_xuexiao_score, qingbei_lianmeng_total_chazhi, qingbei_xuexiao_total_chazhi]
        }
        for xueke in lianmeng_score:
            danke_lianmeng_score_avg = mean(lianmeng_score[xueke])
            danke_xuexiao_score_avg = mean(xuexiao_score[xueke])
            for name in all_score:
                lianmeng_score_avg = mean(all_score[name][0].get(xueke, 0))
                lianmeng_chazhi = lianmeng_score_avg - danke_lianmeng_score_avg
                xuekegongxiang[name]["联考学科贡献"].update({
                    xueke:{
                        "联考达线生均分": "%.2f"%lianmeng_score_avg,
                        "联考均分": "%.2f"%danke_lianmeng_score_avg,
                        "均分差": "%.2f"%lianmeng_chazhi,
                        "联考贡献占比": "%.2f%%"%(lianmeng_chazhi/all_score[name][2]*100)
                    }
                })
                xuexiao_score_avg = mean(all_score[name][1].get(xueke, 0))
                xuexiao_chazhi = xuexiao_score_avg - danke_xuexiao_score_avg
                xuekegongxiang[name]["本校学科贡献"].update({
                    xueke: {
                        "本校达线生均分": "%.2f"%xuexiao_score_avg,
                        "本校均分": "%.2f"%danke_xuexiao_score_avg,
                        "均分差": "%.2f"%xuexiao_chazhi,
                        "联考贡献占比": "%.2f%%"%(xuexiao_chazhi/all_score[name][3]*100)
                    }
                })
        return_data={
            "学科贡献占比": xuekegongxiang
        }  
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年级主任报告-学科贡献占比 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)


def get_daxian_list(all_studend_all_score, xuexiao_id, class_type, score_min, score_max = 20000):
    lianmeng_total, xiao_total, lianmeng_score, xiao_score = [], [], {}, {}
    for uid in all_studend_all_score:
        if class_type in [1,2] and class_type != int(all_studend_all_score[uid]["班级信息"]["class_type"]):
            continue
        scores = all_studend_all_score[uid]["原始分"]
        total_score = sum(list(scores.values()))
        if total_score == 0:
            continue
        if score_max > total_score and total_score >= score_min:
            lianmeng_total.append(total_score)
            if int(all_studend_all_score[uid]["班级信息"]["school_code"]) == int(xuexiao_id):
                xiao_total.append(total_score)
            for xueke in scores:
                if xueke not in lianmeng_score:
                    lianmeng_score[xueke] = []
                    xiao_score[xueke] = []
                if scores[xueke] == 0:
                    continue
                lianmeng_score[xueke].append(scores[xueke])
                if int(all_studend_all_score[uid]["班级信息"]["school_code"]) == int(xuexiao_id):
                    xiao_score[xueke].append(scores[xueke])
    return lianmeng_total, xiao_total, lianmeng_score, xiao_score


@app.route("/get_zhuren_licifenxi", methods=['POST','GET'])
@cross_origin()
def get_zhuren_licifenxi():
    request_data = json.loads(request.get_data())
    benci_kaoshihao = request_data['benci_kaoshihao']
    shangci_kaoshihao = request_data.get('shangci_kaoshihao', None)
    xuexiao_id = request_data['xuexiao_id'] 
    qingbei_line = request_data['qingbei_line']
    yiben_line = request_data['yiben_line']
    benke_line = request_data['benke_line']
    try:
        class_type = int(request_data['class_type'])
    except:
        class_type = 0
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    all_studend_all_score,all_score_list = json.loads(r.get('return_Data'))[str(benci_kaoshihao)]
    if not all_studend_all_score:
        return jsonify(statu='error',detail='redis中没有本次考试id的数据，请先加载考试数据！') 
    try:
        lianmeng_total_score, xuexiao_total_score, lianmeng_score, xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, 0) # 分数线为0，获取所有学生
        benke_lianmeng_total_score, benke_xuexiao_total_score, benke_lianmeng_score, benke_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, benke_line, yiben_line)
        yiben_lianmeng_total_score, yiben_xuexiao_total_score, yiben_lianmeng_score, yiben_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, yiben_line, qingbei_line)
        qingbei_lianmeng_total_score, qingbei_xuexiao_total_score, qingbei_lianmeng_score, qingbei_xuexiao_score = get_daxian_list(all_studend_all_score, xuexiao_id, class_type, qingbei_line)
        benci_xuexiao_cankao_renshu = len(xuexiao_total_score) 
        licikaoshifenxi = {"本次考试": {
            "本科达线情况":{
                "人数": len(benke_xuexiao_total_score),
                "比率": "%.2f%%"%(len(benke_xuexiao_total_score)/benci_xuexiao_cankao_renshu*100)
            },
            "一本达线情况":{
                "人数": len(yiben_xuexiao_total_score),
                "比率": "%.2f%%"%(len(yiben_xuexiao_total_score)/benci_xuexiao_cankao_renshu*100)
            },
            "清北达线情况":{
                "人数": len(qingbei_xuexiao_total_score),
                "比率": "%.2f%%"%(len(qingbei_xuexiao_total_score)/benci_xuexiao_cankao_renshu*100)
            }
        }}
        if shangci_kaoshihao:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            all_studend_all_score_shangci,all_score_list = json.loads(r.get('return_Data'))[str(shangci_kaoshihao)]
            if not all_studend_all_score_shangci:
                return jsonify(statu='error',detail='redis中没有上次考试id的数据，请先加载考试数据！') 
            lianmeng_total_score, shangci_xuexiao_total_score, lianmeng_score, xuexiao_score = get_daxian_list(all_studend_all_score_shangci, xuexiao_id, class_type, 0) # 分数线为0，获取所有学生
            benke_lianmeng_total_score, shangci_benke_xuexiao_total_score, benke_lianmeng_score, benke_xuexiao_score = get_daxian_list(all_studend_all_score_shangci, xuexiao_id, class_type, benke_line, yiben_line)
            yiben_lianmeng_total_score, shangci_yiben_xuexiao_total_score, yiben_lianmeng_score, yiben_xuexiao_score = get_daxian_list(all_studend_all_score_shangci, xuexiao_id, class_type, yiben_line, qingbei_line)
            qingbei_lianmeng_total_score, shangci_qingbei_xuexiao_total_score, qingbei_lianmeng_score, qingbei_xuexiao_score = get_daxian_list(all_studend_all_score_shangci, xuexiao_id, class_type, qingbei_line)
            shangci_xuexiao_cankao_renshu = len(shangci_xuexiao_total_score)
            licikaoshifenxi.update({"上次考试": {
                "本科达线情况":{
                    "人数": len(shangci_benke_xuexiao_total_score),
                    "比率": "%.2f%%"%(len(shangci_benke_xuexiao_total_score)/shangci_xuexiao_cankao_renshu*100)
                },
                "一本达线情况":{
                    "人数": len(shangci_yiben_xuexiao_total_score),
                    "比率": "%.2f%%"%(len(shangci_yiben_xuexiao_total_score)/shangci_xuexiao_cankao_renshu*100)
                },
                "清北达线情况":{
                    "人数": len(shangci_qingbei_xuexiao_total_score),
                    "比率": "%.2f%%"%(len(shangci_qingbei_xuexiao_total_score)/shangci_xuexiao_cankao_renshu*100)
                }
            }, "两次考试差值": {
                "本科达线情况":{
                    "人数": len(benke_xuexiao_total_score) - len(shangci_benke_xuexiao_total_score),
                    "比率": "%.2f%%"%((len(benke_xuexiao_total_score)/benci_xuexiao_cankao_renshu - len(shangci_benke_xuexiao_total_score)/shangci_xuexiao_cankao_renshu)*100)
                },
                "一本达线情况":{
                    "人数": len(yiben_xuexiao_total_score) - len(shangci_yiben_xuexiao_total_score),
                    "比率": "%.2f%%"%((len(yiben_xuexiao_total_score)/benci_xuexiao_cankao_renshu - len(shangci_yiben_xuexiao_total_score)/shangci_xuexiao_cankao_renshu)*100)
                },
                "清北达线情况":{
                    "人数": len(qingbei_xuexiao_total_score) - len(shangci_qingbei_xuexiao_total_score),
                    "比率": "%.2f%%"%((len(qingbei_xuexiao_total_score)/benci_xuexiao_cankao_renshu - len(shangci_qingbei_xuexiao_total_score)/shangci_xuexiao_cankao_renshu)*100)
                }
            }})
        return_data={
            "历次考试成绩分布": licikaoshifenxi
        }  
    except:
        error_log = traceback.format_exc()
        print(error_log)
        return jsonify(statu='error',detail='年级主任报告-学科贡献占比 计算异常', error_log = error_log)
    print ("成功")
    # print (return_data)
    return jsonify(dict_data=return_data)






@app.route("/get_xuanke_student", methods=['POST','GET'])
@cross_origin()
@get_xuanke_student
def get_xuanke_student():
        pass

@app.route("/chushihua_xuanke_def", methods=['POST','GET'])
@cross_origin()
@chushihua_xuanke_def
def chushihua_xuanke_def():
        pass

@app.route("/fenshuduantongji_get_def_d", methods=['POST','GET'])
@cross_origin()
@fenshuduantongji_get_def_d
def fenshuduantongji_get_def_d():
        pass

@app.route("/banjixuankezuhe_def", methods=['POST','GET'])
@cross_origin()
@banjixuankezuhe_def
def banjixuankezuhe_def():
        pass

@app.route("/fenshuduantongji_get", methods=['POST','GET'])
@cross_origin()
@fenshuduantongji_get
def fenshuduantongji_get():
        pass


@app.route("/fenxi_daoru_statu", methods=['POST','GET'])
@cross_origin()
def fenxi_daoru_statu():
        request_data = json.loads(request.get_data())
        kaoshihao = request_data['kaoshihao']
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if r.get('return_Data'):
            this_dict = json.loads(r.get('return_Data'))
            if kaoshihao in this_dict.keys() and this_dict[kaoshihao] != {}:
                return jsonify(statu=True)
        return jsonify(statu=False)

@app.route("/get_yuxuankemku_def", methods=['POST','GET'])
@cross_origin()
def get_yuxuankemku_def():
    request_data= json.loads(request.get_data())
    student_id= request_data['student_id']
    conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                                user='QA', password='hmk#%^&djofsdh', database='exam_business', charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    sql='SELECT id FROM student_todo  WHERE  student_id= %s' % (str(student_id))
    cursor.execute(sql)
    get_data = cursor.fetchall()
    if len(get_data) ==0 :
        conn.close()
        return jsonify(error="查不到选课任务")
    else:
        todu_id = get_data[0][0]
        sql='SELECT choose_type,two_choose_one_subject_name,four_choose_two_subject_one_name,four_choose_two_subject_tow_name FROM student_choose_subject_volunteer  WHERE  student_todo_id=%s' % (str(todu_id))
        cursor.execute(sql)
        get_data = cursor.fetchall()
        if len(get_data) ==0:
            conn.close()
            return jsonify(error='有选课任务，但是没选课信息')
        else:
            return_data={}
            for i in get_data:
                return_data[i[0]]=i[1:]
            conn.close()
            return jsonify(data=return_data)


from .nan3_JiaShiCang.NanSan import *
app.config['JSON_AS_ASCII'] = False
app.register_blueprint(NanSan, url_prefix='/NanSan')