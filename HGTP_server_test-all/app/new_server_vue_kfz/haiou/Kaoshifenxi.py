# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
import os
import json
import demjson
import chardet
import xlrd
import hashlib
import socket
import time
from flask import Blueprint,jsonify,request,send_from_directory
import requests
from  configparser  import ConfigParser
import time
import sqlite3
from flask import Flask, g
import selenium
from flask_cors import *
from flask import current_app,session
from flask import make_response
import redis

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)
def kaoshifenxi_down_excel_tikui_Def(func):
    def kaoshifenxi_down_excel_tikui_Def():
        fn = getattr(sys.modules['__main__'], '__file__')
        root_path = os.path.abspath(os.path.dirname(fn))
        file_path = os.path.join(root_path, 'kaoshifenxi_tikuai')
        this_pat=os.path.join(root_path, 'xuanke_downd.zip')
        print (111111111111111111111111111111111)
        print ('rm -rf file_path')
        print ('rm -rf this_pat')
        os.system('rm -rf /root/repo/hgtp_server/test_backstage/HGTP_server_test-all/kaoshifenxi_tikuai')
        os.system('rm -rf /root/repo/hgtp_server/test_backstage/HGTP_server_test-all/xuanke_downd.zip')
        r = redis.Redis(host='127.0.0.1', port=6379)
        x=r.get('kaoshifenxi_down_exe')
        if x == None:
            r.set('kaoshifenxi_down_exe','1')
        elif x.decode('utf-8')=='1':
            return jsonify(statu="error",detail="已经有任务在运行，限制同时只有一个人任务运行")
        r.set('kaoshifenxi_down_exe', '1')
        all_school_detail =  json.loads(request.get_json()['requet_data'])
        z=executor.submit(all_school_detail_def, all_school_detail)
        return jsonify(statu="success")
    return kaoshifenxi_down_excel_tikui_Def

def get_school_redis_def(func):
    def get_school_redis_def():
        # examid= request.args.get('examid')
        r = redis.Redis(host='127.0.0.1', port=6379)
        r.set('kaoshifenxi_down_exe', '0')
        # if r.get('schoole_all'):
        #     z= json.loads(r.get('schoole_all'))
        #     if str(examid) in z.keys():
        #         return jsonify(statu='success',detail=json.dumps(z[str(examid)]))
        return jsonify(a=2)
    return get_school_redis_def

def all_school_detail_def(all_data):
    examiid = all_data['examiid']
    xuanke_type= all_data['xuanke_type']
    shchool_detail = all_data['shchool_detail']
    num =0
    for k, i in shchool_detail.items():
        try:
            num = num+1
            print ('第几个学校')
            print (num)
            print (k,i)
            schoole_detail_this = {
                'schoole_name': k,
                'schoolCode': i
            }
            urlpath = 'https://wz.zkhyedu.com'
            z = yeujuan_login(urlpath, 13152552926, 'Qq123')
            send_request(urlpath, z['authorization'], z['userid'], examiid,xuanke_type,schoole_detail_this)
        except Exception as e:
            print (e)
    r = redis.Redis(host='127.0.0.1', port=6379)
    r.set('kaoshifenxi_down_exe', '0')
    print (r.get('kaoshifenxi_down_exe'))
def yeujuan_login(url_path,name,password):
    headers = {
    'Content-Type': 'application/json',
    'accessKey': 'test_userCenter',
    'accessSecret': 'test_userCenter',
    'Cache-Control': 'no-cache',
    'Postman-Token': 'aa3760f0-7774-dd9f-515d-7d337337b355',
}
    user_name=name
    password = password
    url = url_path+'/wl/usercenter-serv/uc/userLogin/userCenterLogin'
    z=login(url_path, user_name, password, headers)
    if z['statu']=='success':
         return {'authorization':z['authorization'],"statu":"success","userid":z['userid']}
    else :
        return {"statu": "error"}
def login(base_url,user, passwd,headers):
    data= {"account":user,"password":passwd}
    response = requests.post(base_url+'/wl/union-portal/portal/cas/casLogin',
                             headers=headers, params=data)
    print ( response.status_code)
    if response.status_code != 200:
        return {"statu":"error","detail":"登陆失败"}
    else:
        z = json.loads(response.text)
        authorization = z['result']['token']
        userid = z['result']['userId']
        return {"statu":"success","authorization":authorization, "userid":userid}
def get_school_id(path):
    wb = xlrd.open_workbook(path)  # 打开文件并返回一个工作蒲对象。open_workbook可以点进去看看函数里面的参数的含义之类的，很详细，英语不好的可以百度翻译，翻译出来的结果差不多。
    sheet = wb.sheet_by_index(0)  # 通过索引的方式获取到某一个sheet，现在是获取的第一个sheet页，也可以通过sheet的名称进行获取，sheet_by_name('sheet名称')
    rows = sheet.nrows  # 获取sheet页的行数，一共有几行
    school_id= sheet.col_values(0)[1:]
    school_name=sheet.col_values(1)[1:]
    return dict(zip(school_name,school_id))
#发送下载请求
def send_request(urlpath,authorization,userid, examiid,xuanke_type,schoole_detail):
    schoolCode =schoole_detail['schoole_name']
    schoole_name = schoole_detail['schoolCode']
    this_req=[]
    if xuanke_type == 'all_ kemu_not_wenli':
        all_xueke = {
            "物理": 100003,
            "化学": 100004,
            "生物": 100005,
            "英语": 100016,
            '数学': 100002,
            "语文": 100001,
            "政治": 100007,
            "地理": 100008,
            "历史": 100006
        }
        artsScienceType= ''
        this_req.append([artsScienceType,all_xueke])
    elif  xuanke_type == 'all_kemu_wenli':
        all_xueke = {
            "政治": 100007,
            "地理": 100008,
            "英语": 100016,
            "历史": 100006,
            '数学': 10000201,
            "语文": 100001
        }
        artsScienceType = 1
        this_req.append([artsScienceType, all_xueke])
        all_xueke = {
            "物理": 100003,
            "化学": 100004,
            "生物": 100005,
            "英语": 100016,
            '数学': 10000202,
            "语文": 100001
        }
        artsScienceType= 2
        this_req.append([artsScienceType, all_xueke])
    elif  xuanke_type == 'wenke':
        # 文科 1
        all_xueke = {
            "政治": 100007,
            "地理": 100008,
            "英语": 100016,
            "历史": 100006,
            '数学': 10000201,
            "语文": 100001
        }
        artsScienceType=1
        this_req.append([artsScienceType, all_xueke])
    elif  xuanke_type == 'leke':
        all_xueke = {
            "物理": 100003,
            "化学": 100004,
            "生物": 100005,
            "英语": 100016,
            '数学': 10000202,
            "语文": 100001
        }
        artsScienceType= 2
        this_req.append([artsScienceType, all_xueke])
    path='/wl/exam-databoard/exam/dashboard/report/base/question/student/score/block/detail/download'
    url=urlpath+path
    for k, s in   enumerate(this_req):
        for b,i in s[1].items():
                print (2)
                fn = getattr(sys.modules['__main__'], '__file__')
                root_path = os.path.abspath(os.path.dirname(fn))
                file_path = os.path.join(root_path,'kaoshifenxi_tikuai')
                if not os.path.isdir(file_path):
                    os.mkdir(file_path)
                data={
                "examId": int(examiid),
                "schoolCode": int(schoolCode),
                "subjectCode": i,
                    'artsScienceType':s[0]
            }
                header = {
                    'Content-Type': 'application/json',
                    'accesstoken': 'edu_base_cachezx_user_tokeneyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJucHN4eHM5MCIsImNyZWF0ZWQiOjE2MjkxOTE1MTEzOTcsImV4cCI6MTYyOTE5ODcxMX0.dd_mmdWI_gRvsh7ECOG5AH-dUF1kb3_B0lmkT2sALY4Ops8ALkek8KpOCItUEhIo6QYyBXiRcfCM2GmbYrNSQw',
                    'accessuserid': '1400707743479894016111',
                    "authorization": authorization,
                    "userid": userid
                }
                this_bum_bum=0
                while True:
                    this_bum_bum = this_bum_bum +1
                    response = requests.post(url, data=json.dumps(data), headers=header)
                    if response.status_code==200:
                        break
                    else:
                        print ('第几次重试')
                        print (this_bum_bum)
                        print(response.status_code)
                        if this_bum_bum == 5:
                            break
                        time.sleep(1)
                file_path=os.path.join(file_path,schoole_name)
                if not os.path.isdir(file_path):
                    os.mkdir(file_path)
                if s[0]==1:
                  file_path_this=os.path.join(file_path,b+'文科.xlsx')
                else:
                    file_path_this = os.path.join(file_path, b + '理科.xlsx')
                print (b)
                with open(file_path_this, "wb") as f:
                    f.write(response.content)