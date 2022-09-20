# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import redis
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
import  pymysql
kaoshifenxi = Blueprint('kaoshifenxi',__name__)
#增加节点
all_xueke = {
    "物理": 100003,
    "化学": 100004,
    "政治": 100007,
    "生物": 100005,
    "地理": 100008,
    '数学': 100002,
    "语文": 100001,
    "英语": 100016,
    "历史": 100006
}
@kaoshifenxi.route('/xueshengtikuaimingxi_get',methods=['POST','GET'])
@cross_origin()
def banjitikuaimingxi_get():
    db_cofig= current_app.config.get('KAOSHIFENXI_DB')
    conn = pymysql.connect(host=db_cofig['host'],
                                user=db_cofig['user'], password=db_cofig['password'], database='exam_business2', charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    all_data = json.loads(request.get_data())
    request_data= all_data['request_data']
    kaoshihao = all_data['kaoshihao']
    xuexiaoid = all_data['xuexiaoid']
    sql_data='SELECT block_id,question_score,question_id FROM `reading_task_result` WHERE student_code= {} AND subject_code = {} AND  exam_id = {} '.format(
    str(request_data['xuehao']),str(  all_xueke[request_data['kemu']]),str(kaoshihao)
    )
    print (sql_data)
    cursor.execute(sql_data)
    score_data= cursor.fetchall()
    if len(score_data) ==0 :
        return {
            'statu':'error',
            'detail':'查不到数据'
        }
    return_data= []
    zhuguanti_score=0
    keguanti_score=0
    zongfen= 0
    for i in list(score_data):
        sql_dataa='SELECT default_question_block_name,question_ascription FROM question_block_base_info  WHERE exam_id ={} AND subject_code = {}  and business_id = {}'.format(
            str(kaoshihao),str(  all_xueke[request_data['kemu']]),str(i[0])
        )
        cursor.execute(sql_dataa)
        this_data = cursor.fetchall()
        if len(this_data)!=0:
            this_name = '主观题 | {}'.format(str(this_data[0][0]))
            zhuguanti_score = zhuguanti_score +float(i[1])
            zongfen = zongfen + float(i[1])
            this_redd={
                'block_id':i[0],
                'score': i[1],
                'name':this_name,
                "tikuai_name":this_data[0][0]
            }
            return_data.append(this_redd)
        else:
            sql_data = 'SELECT question_num,ascription FROM `question_base` WHERE business_id = {}'.format(str(i[2]))
            cursor.execute(sql_data)
            this_data = cursor.fetchall()
            if len(this_data)>0:
                this_name = '客观题 | {}'.format(str(this_data[0][0]))
                keguanti_score = keguanti_score + float(i[1])
                zongfen= zongfen + float(i[1])
                this_redd = {
                    'block_id': i[2],
                    'score': i[1],
                    'name': this_name,
                    "tikuai_name": this_data[0][0]
                }
                return_data.append(this_redd)
    all_score_list = sorted(return_data, key=lambda x:int(str( x["tikuai_name"]).split('.')[0]), reverse=False)
    conn.close()
    return jsonify(statu='success',return_data=all_score_list,keguanti_score=keguanti_score,zhuguangti_score=zhuguanti_score)
    # return {
    #     'statu':'success',
    #     "return_data":all_score_list,
    #     "keguanti_score":keguanti_score,
    #     "zhuguangti_score":zhuguanti_score
    # }

@kaoshifenxi.route('/banjitikuaimingxi_get',methods=['POST','GET'])
@cross_origin()
def get_tree():
    db_cofig= current_app.config.get('KAOSHIFENXI_DB')
    conn = pymysql.connect(host=db_cofig['host'],
                                user=db_cofig['user'], password=db_cofig['password'], database='exam_business2', charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    all_data = json.loads(request.get_data())
    request_data= all_data['request_data']
    banji=request_data['banji']
    kemu = request_data['kemu']
    timu_type = request_data['timu_type']
    timuming =  request_data['timuming']
    kaoshihao = all_data['kaoshihao']
    xuexiaoid = all_data['xuexiaoid']
    conn1 = pymysql.connect(host=db_cofig['host'],
                                user=db_cofig['user'], password=db_cofig['password'], database='exam_databoard', charset='utf8')
    cursor1 = conn1.cursor()
    # 得到一个可以执行SQL语句的光标对象
    sql = 'SELECT distinct(student_code) FROM exam_score_transfer_for_bi WHERE exam_id= %s  and school_code= %s and class_name="%s"' % \
          (str(kaoshihao), str(xuexiaoid), banji)
    print (sql)
    cursor1.execute(sql)
    conn1.close()
    all_student_list = [i[0] for i in cursor1.fetchall()]
    #获取所有学生考好
    slq_data='SELECT exam_code FROM  `exam_student` WHERE exam_base_id={}  AND user_code in {}'.format(
        str(kaoshihao),str(tuple(all_student_list))
    )
    print (1111111111111111111111111111111111111111111)
    print (slq_data)
    cursor.execute(slq_data)
    all_student_list=[i[0] for i in cursor.fetchall()]
    all_student_num=len(all_student_list)
    #获取客观题题目id
    sql_data = 'SELECT business_id,question_num,score FROM `question_base` WHERE  subject_code={}  and exam_id={} '.format(
        str(  all_xueke[request_data['kemu']]),str(kaoshihao))
    all_keguan_score=0
    cursor.execute(sql_data)
    keguanti_all_detail={}
    for i in cursor.fetchall():
        keguanti_all_detail[i[0]]={
            'name':i[1],
            'score':i[2]
        }
    sql_ata='SELECT  sum(question_score),question_id FROM `reading_task_result` WHERE question_id in {} AND subject_code = {} and student_code in {}  group by question_id'.format(
           str(tuple(keguanti_all_detail.keys())), str(all_xueke[request_data['kemu']]),str(tuple(all_student_list))
        )
    cursor.execute(sql_ata)
    all_score = list(cursor.fetchall())
    keguantidefenlv={}
    keguanti_all_score=0
    all_keguan_get_score=0
    for i in all_score:
        name= '客观题|'+str(keguanti_all_detail[i[1]]['name'])
        zongfen=float(keguanti_all_detail[i[1]]['score'])*all_student_num
        defenlv=float(i[0])/zongfen
        all_keguan_get_score = all_keguan_get_score + float(i[0])
        keguanti_all_score = keguanti_all_score+zongfen
        keguantidefenlv[name] = round(defenlv*100,2)
    #获取主观题题目id
    sql_data = 'SELECT business_id,score,display_question_block_name FROM `question_block_base_info` WHERE  subject_code={}  and exam_id={} '.format(
        str(  all_xueke[request_data['kemu']]),str(kaoshihao))
    cursor.execute(sql_data)
    this_all_dd= cursor.fetchall()
    timu_id={}
    zhuguanti_all_score=0
    for i in  this_all_dd:
        zhuguanti_all_score = zhuguanti_all_score+float(i[1])
        timu_id[i[0]] = {
            'name': i[2],
            'score': i[1]
        }
    all_score=[]
    if len(timu_id) != 0:
        sql_ata='SELECT  sum(question_score),block_id FROM `reading_task_result` WHERE block_id  in {} AND subject_code = {} and student_code in {} group by block_id'.format(
           str(tuple(timu_id.keys())), str(all_xueke[request_data['kemu']]),str(tuple(all_student_list))
        )
        cursor.execute(sql_ata)
        all_score = cursor.fetchall()
    zhuguantidefenlv={}
    all_zhuguan_get_score=0
    zhuguanti_all_score=0
    for i in all_score:
        name= '主观题|'+str(timu_id[i[1]]['name'])
        zongfen=float(timu_id[i[1]]['score'])*all_student_num
        defenlv=float(i[0])/zongfen
        zhuguanti_all_score=zhuguanti_all_score+zongfen
        all_zhuguan_get_score=all_zhuguan_get_score+float(i[0])
        zhuguantidefenlv[name] = round(defenlv*100,2)
    conn.close()
    all_fen=0
    for k,i in zhuguantidefenlv.items():
        all_fen=all_fen+i
    for k,i in keguantidefenlv.items():
        all_fen=all_fen+i
    all_fen= round((all_keguan_get_score+all_zhuguan_get_score)*100/(keguanti_all_score+zhuguanti_all_score),2)
    all_keguang_ge=round(all_keguan_get_score*100/keguanti_all_score,2)
    all_zhuguan_ge=round(all_zhuguan_get_score*100/zhuguanti_all_score,2)
    return jsonify(statu='success',zhuguan=zhuguantidefenlv,keguan=keguantidefenlv,all_fen=all_fen,all_keguang_ge=all_keguang_ge,all_zhuguan_ge=all_zhuguan_ge)
    # return {
    #     "statu":'success',
    #     "zhuguan":zhuguantidefenlv,
    #     "keguan":keguantidefenlv,
    #     "all_fen":all_fen,
    #     'all_keguang_ge':all_keguang_ge,
    #     'all_zhuguan_ge':all_zhuguan_ge
    # }


@kaoshifenxi.route('/get_banji_junfen_def',methods=['POST','GET'])
@cross_origin()
def get_banji_junfen_def():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    request_ata=json.loads(request.get_data())
    kaoshihao= str(request_ata['kaoshihao'])
    banji_name=request_ata['request_data']['banji_name']
    xuexiao_id = request_ata['request_data']['xuexiao_id']
    x = json.loads(r.get('return_Data'))[kaoshihao][0]
    if kaoshihao not in  json.loads(r.get('return_Data')).keys() or len(json.loads(r.get('return_Data'))[kaoshihao])==0 :
        return {
        "statu":"error",
        "detail":"redis查不到该考试下信息，请先操作考试下分数预计算"
    }
    banji_pingjunfen={
            "总分":0,
            "物理": 0,
            "化学": 0,
            "政治": 0,
            "生物": 0,
            "地理": 0,
            '数学': 0,
            "语文": 0,
            "英语": 0,
            "历史": 0,
            "total":0
        }

    xuexiao_pingjunfen={
        "总分": 0,
            "物理": 0,
            "化学": 0,
            "政治": 0,
            "生物": 0,
            "地理": 0,
            '数学': 0,
            "语文": 0,
            "英语": 0,
            "历史": 0,
            "total":0
        }
    lianmeng_pingjunfen={
        "总分": 0,
            "物理": 0,
            "化学": 0,
            "政治": 0,
            "生物": 0,
            "地理": 0,
            '数学': 0,
            "语文": 0,
            "英语": 0,
            "历史": 0,
            "total":0
        }
    for k,i in x.items():
        if i['班级信息']['school_code']==str(xuexiao_id):
            xuexiao_pingjunfen['total'] =  xuexiao_pingjunfen['total'] +1
            for z in i['原始分']:
                 xuexiao_pingjunfen[z]= xuexiao_pingjunfen[z] + i['原始分'][z]
                 xuexiao_pingjunfen['总分'] =  xuexiao_pingjunfen['总分'] + i['原始分'][z]
        if i['班级信息']['school_code']==str(xuexiao_id) and i['班级信息']['class_name']==str(banji_name).strip():
            banji_pingjunfen['total'] = banji_pingjunfen['total'] + 1
            for z in i['原始分']:
               banji_pingjunfen[z] = banji_pingjunfen[z] + i['原始分'][z]
               banji_pingjunfen['总分'] = banji_pingjunfen['总分'] + i['原始分'][z]
        lianmeng_pingjunfen['total'] = lianmeng_pingjunfen['total'] + 1
        for z in i['原始分']:
            lianmeng_pingjunfen[z] = lianmeng_pingjunfen[z] + i['原始分'][z]
            lianmeng_pingjunfen['总分'] = lianmeng_pingjunfen['总分'] + i['原始分'][z]

    banji_pingjunfen_return ={}
    for k,i in banji_pingjunfen.items():
        if k!='total':
            banji_pingjunfen_return[k]=round(i/banji_pingjunfen['total'],2)
    xuexiao_pingjunfen_return ={}
    for k,i in xuexiao_pingjunfen.items():
        if k!='total':
            xuexiao_pingjunfen_return[k]=round(i/xuexiao_pingjunfen['total'],2)
    lianmeng_pingjunfen_return ={}
    for k,i in lianmeng_pingjunfen.items():
        if k!='total':
            lianmeng_pingjunfen_return[k]=round(i/lianmeng_pingjunfen['total'],2)
    return jsonify(banji_pingjunfen_return=banji_pingjunfen_return,xuexiao_pingjunfen_return=xuexiao_pingjunfen_return,
                   lianmeng_pingjunfen_return=lianmeng_pingjunfen_return,statu="success"
    )
    # return {
    #     "banji_pingjunfen_return":banji_pingjunfen_return,
    #     "xuexiao_pingjunfen_return":xuexiao_pingjunfen_return,
    #     "lianmeng_pingjunfen_return":lianmeng_pingjunfen_return,
    #     "statu":"success"
    #
    # }
