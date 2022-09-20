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
new_file = Blueprint('new',__name__)
@new_file.route('/run_jiekou_shuzhen',methods=['POST','GET'])
@cross_origin()
def admin_index():
    conn = sqlite3.connect(r'C:\jieyuelianhe\old_all_server\HGTP_server整体\example_test.db')
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Cookie': 'changeSkin=undefined; defSkin=2; cusSkin=2; lan=zh_CN; access_token=undefined; JSESSIONID=7023E229340CC1BFF9CFD049D3256D69; token=1f792659244898d6eec3462093420d720d44c8f4537444cbb5bd1e4386ed29ab',
        'exchange-token': '1f792659244898d6eec3462093420d720d44c8f4537444cbb5bd1e4386ed29ab',
    }
    c = conn.cursor()
    c.execute('delete from shuzhen_test')
    conn.commit()
    for i in range(5):
        # oldtime = time.time()
        # timeArray = time.localtime(oldtime)
        # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data = {"uaTime": ''}
        # url = 'https://www.wbfex.com/fe-ex-api/message/v4/get_no_read_message_count'
        # s = requests.post(url, data=json.dumps(data), headers=headers)
        # old_time=time.time()-oldtime
        k=run_jiekou('/fe-ex-api/message/v4/get_no_read_message_count',
                     headers,data)
        print(k)
        c.executemany('INSERT INTO shuzhen_test VALUES (?,?,?,?,?,?)', [
            ('',k['url'],k['old_time'],k['new_time'],str(time.time()),k['status_code'])])
        data = {"side": "", "pageSize": 10, "page": 1, "symbol": "wtusdt", "uaTime": "2019-09-19 14:58:35"}
        k=run_jiekou('/fe-ex-api/order/list/new',
                     headers,data)
        print(k)
        c.executemany('INSERT INTO shuzhen_test VALUES (?,?,?,?,?,?)', [
            ('',k['url'],k['old_time'],k['new_time'],str(time.time()),k['status_code'])])
    conn.commit()
    conn.close()
    return jsonify(statu='success')
def run_jiekou(url,header,data):
    all_url='https://www.wbfex.com'+url
    oldtime = time.time()
    timeArray = time.localtime(oldtime)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    data['uaTime']=otherStyleTime
    s = requests.post(all_url, data=json.dumps(data), headers=header)
    old_time=str(time.time()-oldtime)
    all_url='https://www.wbfex.com'+url
    newtime = time.time()
    timeArray = time.localtime(newtime)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    data['uaTime']=otherStyleTime
    s = requests.post(all_url, data=json.dumps(data), headers=header)
    new_time=str(time.time()-newtime)
    return {'url':url,'old_time':old_time,'status_code':s.status_code,'new_time':new_time}

#查询接口
@new_file.route('/get_detail_shuzhen',methods=['POST','GET'])
@cross_origin()
def get_detail():
    conn = sqlite3.connect(r'C:\jieyuelianhe\old_all_server\HGTP_server整体\example_test.db')
    c = conn.cursor()
    k=c.execute('select  *  from shuzhen_test  order by  run_time desc').fetchall()
    z={}
    u={}
    for i in k:
        if i[1] not in list(z.keys()):
            z[i[1]]={}
            z[i[1]]['old_time']=float(i[2])+1
            z[i[1]]['new_time'] = float(i[3])
            u[i[1]]=[]
            u[i[1]].append(float(str(float(i[2])+1-float(i[3]))[:4]))
        else:
            z[i[1]]['new_time'] = z[i[1]]['new_time'] + float(i[3])
            z[i[1]]['old_time']= z[i[1]]['old_time']+float(i[2])
            u[i[1]].append(float(str(float(i[2]) + 1 - float(i[3]))[:4]))

    for i in z:
        z[i]['old_time']=z[i]['old_time']/5
        z[i]['new_time']=z[i]['new_time']/5
        z[i]['cha_zhi']=z[i]['old_time']- z[i]['new_time']
        z[i]['old_time']=float(str( z[i]['old_time'])[:4])
        z[i]['new_time'] = float(str(z[i]['new_time'])[:4])
        if  z[i]['cha_zhi']>0:
           z[i]['cha_zhi'] =float(str(z[i]['cha_zhi'])[:4])
    print((11111111111111111111111111111))
    all_time=[0,0,0,0,0]
    for m,n in list(u.items()):
        for k,i in enumerate(all_time):
            all_time[k]=all_time[k]+n[k]
    all_time=[float(str(i/len(u))[:4]) for i in all_time]
    print(all_time)
    conn.close()
    return jsonify(statu=z,all_time=all_time)