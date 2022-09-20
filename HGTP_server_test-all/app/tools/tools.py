import sys
import os
import json
import demjson
import chardet
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

tools = Blueprint('tools', __name__)
@tools.route('/clear_all_cats', methods=['post','get'])
def clear_all_cats():
        if 'statu'  in request.form.keys() and request.form['statu']=='1':
                return_data = {"status": "success", "detail": '成功'}
                device_token = '09dc2683c0464dd1962bd09f9656c373'
                db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
                cu = db.cursor()
                all_data=[]
                for i in json.loads(request.form['all_id']):
                        k = cu.execute('select name,password from zhengda_yewu_user where id=%s' % (
                                i)).fetchall()[0]
                        jwt_token=doctor_pig(k[0],k[1])
                        headers={}
                        headers['Authorization'] = jwt_token
                        headers['Device-Token'] = device_token
                        headers['AppidAppid'] = "1"
                        return_data = run_user(headers)
                        if return_data['status']!='success':
                                return_data= {"status":"error","detail":return_data['detail']}
                return jsonify(status=return_data['status'], detail=return_data['detail'])
        else:
                headers = {}
                headers['Authorization'] = request.headers['Authorization']
                headers['Device-Token'] = request.headers['Device-Token']
                headers['AppidAppid'] = request.headers['Appid']
                return_data=run_user(headers)
                return jsonify(status=return_data['status'], detail=return_data['detail'])

def run_user(header_data):
        url = 'https://dev-srv-iorder.cpgroupcloud.com/gateway-mall/cart/cart/list'
        all_card_id = []
        print(requests.get(url, headers=header_data, verify=False).text)
        try:
                for z in json.loads(requests.get(url, headers=header_data, verify=False).text)['data']['cart_list']:
                        for u in z['product']:
                                all_card_id.append(u['cart_id'])
        except:
                return jsonify(status='error', detail="获取购物车接口调用失败")
        # 检查购物车
        url = 'https://dev-srv-iorder.cpgroupcloud.com/gateway-mall/cart/cart/delete'
        try:
                for z in all_card_id:
                        data = {
                                "cart_id": z
                        }
                        print(z)
                        print(requests.get(url, data, headers=header_data, verify=False).text)
        except:
                return_data={"status":"error","detail":'删除购物车接口调用失败'}
        else:
                return_data = {"status": "success", "detail": '成功'}
        return return_data
def doctor_pig(name,password):
    url = 'https://gateway-iorder-dev2.cpgroupcloud.com'+'/api/iorder/v150/auth'
    headers = {
        "appid": "1",
        "device-token": '09dc2683c0464dd1962bd09f9656c373',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={
"username":name,
    "sms_code":password
}
    data1 = requests.post(url, data, headers=headers,verify=False).text
    try:
        jwt_token=json.loads(data1)["data"]["cp_user_info"]["jwt_token"]
    except Exception as e:
        print (url)
        print ("登录接口获取jwt_token失败，请判断登录信息是否正确")
    else:
      return  jwt_token


@tools.route('/add_yewu_user', methods=['post','get'])
@cross_origin()
def add_yewu_user():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        phone_name=request.form['user_name']
        password = request.form['password']
        yanzhengma = request.form['yanzhengma']
        beizhu = request.form['beizhu']
        yewu_name=request.form['yewu_name']
        user_name=g.user_name
        k=cu.execute('select * from zhengda_yewu_user where yewu_name="%s" and name="%s"' % (yewu_name,phone_name)).fetchall()
        if len(k)>0:
                return jsonify(status='fail', detail="用户名重复")
        db.execute("BEGIN TRANSACTION")
        cu.executemany('INSERT INTO zhengda_yewu_user VALUES (null,?,?,?,?,?,?,?)', [
                (phone_name, password, yanzhengma, beizhu,'猪博士', user_name, str(time.time()))])
        db.commit()
        db.close()
        return jsonify(status='success', detail=None)

@tools.route('/get_yewu_user', methods=['post','get'])
@cross_origin()
def get_yewu_user():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        yewu_name=request.form['yewu_name'].strip()
        user_name=g.user_name
        db.execute("BEGIN TRANSACTION")
        all_detail=cu.execute('select id,name,beizhu from zhengda_yewu_user where yewu_name="%s"' %(yewu_name)).fetchall()
        db.close()
        return jsonify(status='success', detail=all_detail)

from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
@tools.route('/clear_car_html', methods=['post','get'])
@cross_origin()
def clear_car_html():
        return render_template('/tools/shuzhen.html')
@tools.route('/delete_yewu_user', methods=['post','get'])
@cross_origin()
def delete_yewu_user():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        all_id=json.loads(request.form['all_id'])
        yewu_name=request.form['yewu_name']
        db.execute("BEGIN TRANSACTION")
        for z in all_id:
               cu.execute('delete from zhengda_yewu_user where id=%s' %(int(z))).fetchall()
        db.commit()
        db.close()
        return jsonify(status='success', detail='null')


@tools.route('/save_param_detail_def', methods=['post','get'])
@cross_origin()
def save_param_detail_def():
        return 'a=2'
