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
from flask import Blueprint, jsonify, request
import requests
from configparser import ConfigParser
import time
import sqlite3
from flask import Flask, g
import selenium
from flask_cors import *
from flask import current_app, session
import pymysql
import redis
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

wuzhou = Blueprint('wuzhou', __name__)
# 增加节点
execute = ThreadPoolExecutor()


@wuzhou.route('/wuzhoushujuchushihua_def', methods=['POST', 'GET'])
@cross_origin()
def get_tree():
    exam_type = request.get_json()['exam_type']
    exam_id = request.get_json()['exam_id']
    try:
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
        cur = conn.cursor()
    except:
        return jsonify(status='fail', detail='连不上数据库')
    else:
        sql_data = 'SELECT   DISTINCT(student_code) FROM stu_subject_score  WHERE exam_id= {}  GROUP BY student_code HAVING SUM(total_score) = 0' .format(
            str(exam_id))
        cur.execute(sql_data)
        no_use_student_code = str(tuple([i[0] for i in cur.fetchall()]))
        sql_data = 'SELECT COUNT(DISTINCT(exam_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1 '.format(
            str(exam_id))
        cur.execute(sql_data)
        studnet_num = cur.fetchall()[0][0]
        sql_data = 'SELECT COUNT(DISTINCT(school_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1'.format(
            str(exam_id))
        cur.execute(sql_data)
        school_num = cur.fetchall()[0][0]
        sql_data = 'SELECT COUNT(DISTINCT(subject_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1'.format(
            str(exam_id))
        cur.execute(sql_data)
        csee_num = cur.fetchall()[0][0]
        if exam_type=='文理分科前':
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
        else :
            all_xueke = {
                "物理": 100003,
                "化学": 100004,
                "政治": 100007,
                "生物": 100005,
                "地理": 100008,
                '数学文': 10000201,
                '数学理': 10000202,
                "语文": 100001,
                "英语": 100016,
                "历史": 100006
            }
        score_fenxi = {}
        #查询所有总分是0的学生
        sql_data = 'SELECT   DISTINCT(student_code) FROM stu_subject_score  WHERE exam_id= {}  GROUP BY student_code HAVING SUM(total_score) = 0' .format(
            str(exam_id))
        cur.execute(sql_data)
        no_use_student_code = str(tuple([i[0] for i in cur.fetchall()]))
        for k, i in all_xueke.items():
            subject_code = i
            sql_data = 'SELECT min(total_score),max(total_score), avg(total_score) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1 ' \
                       'and subject_code = {} and student_code not in {} and total_score!=0'.format(
                str(exam_id), str(subject_code),no_use_student_code)
            cur.execute(sql_data)
            this_data_d = cur.fetchall()[0]
            if len(this_data_d) > 0:
                score_fenxi[k] = {
                    "最低分": this_data_d[0],
                    "最高分": this_data_d[1],
                    "平均分": Decimal(this_data_d[2]).quantize(Decimal("0.00")),
                }
        conn.close()
    execute.submit(chushihua_data, exam_id)
    return jsonify(statu='success', studnet_num=studnet_num, school_num=school_num, csee_num=csee_num,
                   score_fenxi=score_fenxi)
def chushihua_data(exam_id):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    try:
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
    except:
        return jsonify(status='fail', detail='连不上数据库')
    else:
        sql_data = 'SELECT * FROM stu_subject_score WHERE exam_id= {} and student_status !=1'.format(
            str(exam_id))
        cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute(sql_data)
        this_all_data = cur.fetchall()
        print(this_all_data[0])
        conn.close()
        if len(this_all_data) <= 0:
            return jsonify(status='fail', detail='该考试数据表中查不到')
@wuzhou.route('/chengjifenbu', methods=['POST', 'GET'])
@cross_origin()
def chengjifenbu():
    exam_id = request.get_json()['exam_id']
    exam_type= request.get_json()['exam_type']
    try:
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
        cur = conn.cursor()
        conn2 = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                                user='QA', password='hmk#%^&djofsdh', database='exam_databoard', charset='utf8')
        cur2 = conn2.cursor(cursor=pymysql.cursors.DictCursor)
    except:
        return jsonify(status='fail', detail='连不上数据库')
    else:
        sql_data = 'SELECT COUNT(DISTINCT(exam_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1'.format(
            str(exam_id))
        cur.execute(sql_data)
        studnet_num = cur.fetchall()[0][0]
        if exam_type=='文理分科前':
            sql_data = 'SELECT * FROM `report_param_config`  WHERE exam_id = {}'.format(str(exam_id))
            cur2.execute(sql_data)
            fensh_detail = cur2.fetchall()[0]
        else :
            fensh_detail={
                'qingbei_line_score':640,
                'qingbei_critical_threshold':5,
                'first_undergraduate_score':418,
                'first_undergraduate_critical_threshold':30,
                'second_undergraduate_score':280,
                'second_undergraduate_critical_threshold':280
            }
        cur2.close()
        qingbei = fensh_detail['qingbei_line_score']
        qingbeixian_max = fensh_detail['qingbei_line_score'] + fensh_detail['qingbei_critical_threshold']
        qingbeixian_min = fensh_detail['qingbei_line_score'] - fensh_detail['qingbei_critical_threshold']
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and ' \
                   'SUM(total_score)<={}'.format(
            str(exam_id), str(qingbeixian_min), str(qingbeixian_max))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        qingbei_lein_jie_num = len(csee_num)
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={}'.format(
            str(exam_id), str(qingbei))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        qingbei__num = len(csee_num)
        qingbei__num = str(qingbei__num) + '(' + str(
            Decimal(qingbei__num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%' + ')'
        qingbei_detail = {
            "分数线": qingbei,
            "临界生分数线": fensh_detail['qingbei_critical_threshold'],
            "上线人数": qingbei__num,
            "临界生人数": qingbei_lein_jie_num
        }
        yiben = fensh_detail['first_undergraduate_score']
        yiben_max = fensh_detail['first_undergraduate_score'] + fensh_detail['first_undergraduate_critical_threshold']
        yiben__min = fensh_detail['first_undergraduate_score'] - fensh_detail['first_undergraduate_critical_threshold']
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and ' \
                   'SUM(total_score)<={}'.format(
            str(exam_id), str(yiben__min), str(yiben_max))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        yiben_lein_jie_num = len(csee_num)
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and SUM(total_score)<{}'.format(
            str(exam_id), str(yiben),str(qingbei))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        yiben_num = len(csee_num)
        yiben_num = str(yiben_num) + '(' + str(
            Decimal(yiben_num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%' + ')'
        yiben_detail = {
            "分数线": yiben,
            "临界生分数线": fensh_detail['first_undergraduate_critical_threshold'],
            "上线人数": yiben_num,
            "临界生人数": yiben_lein_jie_num
        }
        erben = fensh_detail['second_undergraduate_score']
        erben_max = fensh_detail['second_undergraduate_score'] + fensh_detail['second_undergraduate_critical_threshold']
        erben__min = fensh_detail['second_undergraduate_score'] - fensh_detail[
            'second_undergraduate_critical_threshold']
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and ' \
                   'SUM(total_score)<={}'.format(
            str(exam_id), str(erben__min), str(erben_max))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        erben_lein_jie_num = len(csee_num)
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and SUM(total_score)<{}'.format(
            str(exam_id), str(erben),str(yiben))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        erben_num = len(csee_num)
        erben_num = str(erben_num) + '(' + str(
            Decimal(erben_num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%' + ')'
        erben_detail = {
            "分数线": erben,
            "临界生分数线": fensh_detail['first_undergraduate_critical_threshold'],
            "上线人数": erben_num,
            "临界生人数": erben_lein_jie_num
        }
        conn.close()
    return jsonify(statu='success', erben_detail=erben_detail, qingbei_detail=qingbei_detail, yiben_detail=yiben_detail)
@wuzhou.route('/chengjifenbuzhuzhuangtu', methods=['POST', 'GET'])
@cross_origin()
def chengjifenbuzhuzhuangtu():
    print_list = []
    exam_id = request.get_json()['exam_id']
    exam_type = request.get_json()['exam_type']
    conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                           user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
    cur = conn.cursor()
    if exam_type == '文理分科前':
        z = 0
        x = []
        num_list = []
        num_list_dict = {}
        for i in range(10, 1060, 10):
            x.append([z, i])
            num_list.append(0)
            num_list_dict[json.dumps([z, i])] = 0
            z = i
        sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code'.format(
            str(exam_id))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        all_score = [i[0] for i in csee_num]
        all_score = sorted(all_score)
        print(all_score[0])
        begin_list = []
        begin_num = 0
        for i in all_score:
            if begin_list == []:
                for k, z in enumerate(x):
                    if z[0] <= i < z[1]:
                        begin_list = z
                        begin_num = k
                        num_list[begin_num] = num_list[begin_num] + 1
                        num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                        break
            else:
                if begin_list[0] <= i < begin_list[1]:
                    num_list[begin_num] = num_list[begin_num] + 1
                    num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                else:
                    for k, z in enumerate(x):
                        if z[0] <= i < z[1]:
                            begin_list = z
                            begin_num = k
                            num_list[begin_num] = num_list[begin_num] + 1
                            num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                            break
    else:
        sql_data='SELECT DISTINCT(class_code),school_code  FROM stu_subject_score  WHERE exam_id= {}'.format( str(exam_id))
        cur.execute(sql_data)
        x=cur.fetchall()
        class_num = tuple( [int(i[0]) for i in x if i[0]!=None])
        sql_data='SELECT class_code  FROM school_class_ralate  WHERE class_code in {} and  class_type=1'.format( str(class_num))
        cur.execute(sql_data)
        wenkeban=tuple([str(i[0]) for  i in cur.fetchall() ])
        sql_data='SELECT class_code  FROM school_class_ralate  WHERE class_code in {} and  class_type=2'.format( str(class_num))
        cur.execute(sql_data)
        likeban=tuple([str(i[0]) for  i in cur.fetchall() ])
        wenke = {
            "政治": 100007,
            "地理": 100008,
            "英语": 100016,
            "历史": 100006,
            '数学': 10000201,
            "语文": 100001
        }
        like = {
            "物理": 100003,
            "化学": 100004,
            "生物": 100005,
            "英语": 100016,
            '数学': 10000202,
            "语文": 100001
        }
        z = 0
        x = []
        num_list = []
        num_list_dict = {}
        for i in range(10, 740, 10):
            x.append([z, i])
            num_list.append(0)
            num_list_dict[json.dumps([z, i])] = 0
            z = i
        sql_data = 'SELECT SUM(total_score),student_code  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  and subject_code in {} and class_code in {} GROUP BY exam_code'.format(
            str(exam_id),str(tuple(like.values())),str(likeban))
        cur.execute(sql_data)
        csee_num = cur.fetchall()
        all_score = [i for i in csee_num if i[0]!=0]
        all_score = sorted(all_score,key=lambda x:x[0])
        begin_list = []
        begin_num = 0
        for i in all_score:
            if begin_list == []:
                for k, z in enumerate(x):
                    if z[0] <= i[0] < z[1]:
                        if z==[100,110]:
                            print_list.append(i[1])
                        begin_list = z
                        begin_num = k
                        num_list[begin_num] = num_list[begin_num] + 1
                        num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                        break
            else:
                if begin_list[0] <= i[0] < begin_list[1]:
                    if z==[100,110]:
                        print_list.append(i[1])
                    num_list[begin_num] = num_list[begin_num] + 1
                    num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                else:
                    for k, z in enumerate(x):
                        if z[0] <= i[0] < z[1]:
                            if z == [100, 110]:
                                print_list.append(i[1])
                            begin_list = z
                            begin_num = k
                            num_list[begin_num] = num_list[begin_num] + 1
                            num_list_dict[json.dumps([z[0], z[1]])] = num_list[begin_num]
                            break
    conn.close()
    return jsonify(statu='success', data=num_list,num_list_dict=num_list_dict)
@wuzhou.route('/chengjifenbuzhuzhuangtu_duibi_def', methods=['POST', 'GET'])
@cross_origin()
def chengjifenbuzhuzhuangtu_duibi_def():
    yewu_data = json.loads(request.get_json()['yeuw_data'])
    exam_data = json.loads(request.get_json()['exam_data'])
    z = 0
    x = []
    for i in range(10, 1060, 10):
        x.append([z, i])
        z = i
    # if len(yewu_data)!=len(exam_data):
    #     detailt={
    #         "业务长度":len(yewu_data),
    #         "计算成都":len(exam_data)
    #     }
    #     return jsonify(statu='sucdess',data="长度不一致",detail=detailt)
    error_detail = {

    }
    for k, i in enumerate(exam_data):
        if int(yewu_data[k]) != int(exam_data[k]):
            error_detail[json.dumps(x[k])] = {
                "计算后数据": exam_data[k],
                "对比数据": yewu_data[k]
            }
    return jsonify(statu='success', detail=error_detail)
@wuzhou.route('/chengjifenbuzhuzhuangtu_wenli', methods=['POST', 'GET'])
@cross_origin()
def chengjifenbuzhuzhuangtu_wenli():
    exam_id = request.get_json()['exam_id']
    conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                           user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
    cur = conn.cursor()
    z = 0
    x = []
    num_list_wuli = []
    num_list_lishi = []
    num_list_scoer_wen={}
    num_list_scoer_li = {}
    for i in range(10, 1060, 10):
        x.append([z, i])
        num_list_wuli.append(0)
        num_list_lishi.append(0)
        num_list_scoer_wen[json.dumps([z, i])]=0
        num_list_scoer_li[json.dumps([z, i])] =0
        z = i
    sql_data = 'SELECT  b.student_id    FROM student_choose_subject_volunteer a LEFT OUTER JOIN student_todo  b ON b.id = a.student_todo_id WHERE b.todo_name_code = {}' \
               ' and a.choose_type=1 and  a.two_choose_one_subject_name ="物理"'.format(
        str(exam_id))
    cur.execute(sql_data)
    all_like_xuehao =str(tuple( [str(i[0] ) for i in cur.fetchall()]))
    sql_data = 'SELECT SUM(total_score),student_code  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1 ' \
               'and  student_code in {} GROUP BY exam_code'.format(
        str(exam_id),all_like_xuehao)
    cur.execute(sql_data)
    csee_num = cur.fetchall()
    all_score = sorted(csee_num,key=lambda x:x[0] )
    # all_score = [i[0] for i in csee_num]
    # all_score = sorted(all_score,key=lambda x:x[1] )
    error_detail=[]
    begin_list = []
    begin_num = 0
    for i in all_score:
        if  310<i[0]<320:
            error_detail.append(i)
        if begin_list == []:
            for k, z in enumerate(x):
                if z[0] <= i[0] < z[1]:
                    begin_list = z
                    begin_num = k
                    num_list_wuli[begin_num] = num_list_wuli[begin_num] + 1
                    num_list_scoer_li[json.dumps([z[0],z[1]])] = num_list_wuli[begin_num]
                    break
        else:
            if begin_list[0] <= i[0] < begin_list[1]:
                num_list_wuli[begin_num] = num_list_wuli[begin_num] + 1
                num_list_scoer_li[json.dumps([begin_list[0], begin_list[1]])] =   num_list_wuli[begin_num]
            else:
                for k, z in enumerate(x):
                    if z[0] <= i[0] < z[1]:
                        begin_list = z
                        begin_num = k
                        num_list_wuli[begin_num] = num_list_wuli[begin_num] + 1
                        num_list_scoer_li[json.dumps([z[0], z[1]])] = num_list_wuli[begin_num]
                        break
    sql_data = 'SELECT  b.student_id    FROM student_choose_subject_volunteer a LEFT OUTER JOIN student_todo  b ON b.id = a.student_todo_id WHERE b.todo_name_code = {}' \
               ' and a.choose_type=1 and  a.two_choose_one_subject_name ="历史"'.format(
        str(exam_id))
    cur.execute(sql_data)
    all_wenke_xuehao =str(tuple( [str(i[0]) for i in cur.fetchall()]))
    sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1 ' \
               'and  student_code in {} GROUP BY exam_code'.format(
        str(exam_id),all_wenke_xuehao)
    cur.execute(sql_data)
    csee_num = cur.fetchall()
    conn.close()
    all_score = [i[0] for i in csee_num]
    all_score = sorted(all_score)
    print(all_score[0])
    begin_list = []
    begin_num = 0
    for i in all_score:
        if begin_list == []:
            for k, z in enumerate(x):
                if z[0] <= i < z[1]:
                    begin_list = z
                    begin_num = k
                    num_list_lishi[begin_num] = num_list_lishi[begin_num] + 1
                    num_list_scoer_wen[json.dumps([z[0], z[1]])] = num_list_lishi[begin_num]
                    break
        else:
            if begin_list[0] <= i < begin_list[1]:
                num_list_lishi[begin_num] = num_list_lishi[begin_num] + 1
                num_list_scoer_wen[json.dumps([begin_list[0], begin_list[1]])] = num_list_lishi[begin_num]
            else:
                for k, z in enumerate(x):
                    if z[0] <= i < z[1]:
                        begin_list = z
                        begin_num = k
                        num_list_lishi[begin_num] = num_list_lishi[begin_num] + 1
                        num_list_scoer_wen[json.dumps([z[0], z[1]])] = num_list_lishi[begin_num]
                        break
    return jsonify(statu='success', num_list_wuli=num_list_wuli, num_list_lishi=num_list_lishi,num_list_scoer_wen=num_list_scoer_wen,
                   num_list_scoer_li=num_list_scoer_li,error_detail=error_detail)
@wuzhou.route('/xuanke_leixing_total', methods=['POST', 'GET'])
@cross_origin()
def get_xuanke_student():
    return_data = {
        "选科填报率": None,
        "总人数": 0,

            "第一志愿": {
                "人数": 0,
                "比率": None
            },
            "未填写志愿志愿": {
                "人数": 0,
                "比率": None
            },
            "第一+第二志愿": {
                "人数": 0,
                "比率": None
            },
        "选科物理类": {
            "人数": 0,
            "占比": None
        },
        "选科历史类": {
            "人数": 0,
            "占比": None
        },
    }
    exam_id = request.form['exam_id']
    conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                           user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
    cursor = conn.cursor()
    sql_data = 'SELECT student_choose_subject_volunteer.mix_subject_name,student_choose_subject_volunteer.choose_type, student_todo.student_id    FROM student_choose_subject_volunteer LEFT OUTER JOIN student_todo ON student_todo.id = student_choose_subject_volunteer.student_todo_id WHERE student_todo.todo_name_code = {}' \
               ' and student_choose_subject_volunteer.choose_type=1'.format(str(exam_id))
    cursor = conn.cursor()
    cursor.execute(sql_data)
    all_xuanke_detail_first = cursor.fetchall()
    sql_data = 'SELECT student_choose_subject_volunteer.mix_subject_name,student_choose_subject_volunteer.choose_type, student_todo.student_id    FROM student_choose_subject_volunteer LEFT OUTER JOIN student_todo ON student_todo.id = student_choose_subject_volunteer.student_todo_id WHERE student_todo.todo_name_code = {}' \
               ' and student_choose_subject_volunteer.choose_type=2 and  student_choose_subject_volunteer.mix_subject_name!="0"'.format(
        str(exam_id))
    cursor = conn.cursor()
    cursor.execute(sql_data)
    all_xuanke_detail_second = cursor.fetchall()
    if len(all_xuanke_detail_first) == 0:
        return jsonify(return_data={
            'statu': 'error',
            'detail': "找不到选科信息"
        })
    sql_data = 'SELECT COUNT(DISTINCT(exam_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1'.format(
        str(exam_id))
    cursor.execute(sql_data)
    studnet_num = cursor.fetchall()[0][0]
    return_data['总人数'] = studnet_num
    return_data["选科填报率"] = str(
        Decimal(len(all_xuanke_detail_first) * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'
    return_data['第一志愿']['人数'] = len(all_xuanke_detail_first) - len(all_xuanke_detail_second)
    thi_num = len(all_xuanke_detail_first) - len(all_xuanke_detail_second)
    return_data['第一志愿']['比率'] = str(Decimal(thi_num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'
    return_data['第一+第二志愿']['人数'] = len(all_xuanke_detail_second)
    return_data['第一+第二志愿']['比率'] = str(
        Decimal(len(all_xuanke_detail_second) * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'
    return_data['未填写志愿志愿']['人数'] = studnet_num - len(all_xuanke_detail_first)
    thi_num = studnet_num - len(all_xuanke_detail_first)
    return_data['未填写志愿志愿']['比率'] = str(Decimal(thi_num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'
    sql_data = 'SELECT student_choose_subject_volunteer.mix_subject_name,student_choose_subject_volunteer.choose_type, student_todo.student_id    FROM student_choose_subject_volunteer LEFT OUTER JOIN student_todo ON student_todo.id = student_choose_subject_volunteer.student_todo_id WHERE student_todo.todo_name_code = {}' \
               ' and student_choose_subject_volunteer.choose_type=1 and  student_choose_subject_volunteer.two_choose_one_subject_name ="物理"'.format(str(exam_id))
    cursor = conn.cursor()
    cursor.execute(sql_data)
    xuanke_wulilei=cursor.fetchall()
    return_data["选科物理类"]["人数"] = len(xuanke_wulilei)
    return_data['选科物理类']['占比'] = str(Decimal(len(xuanke_wulilei) * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'
    sql_data = 'SELECT student_choose_subject_volunteer.mix_subject_name,student_choose_subject_volunteer.choose_type, student_todo.student_id    FROM student_choose_subject_volunteer LEFT OUTER JOIN student_todo ON student_todo.id = student_choose_subject_volunteer.student_todo_id WHERE student_todo.todo_name_code = {}' \
               ' and student_choose_subject_volunteer.choose_type=1 and  student_choose_subject_volunteer.two_choose_one_subject_name ="历史"'.format(str(exam_id))
    cursor = conn.cursor()
    cursor.execute(sql_data)
    xuanke_lishilei=cursor.fetchall()
    return_data["选科历史类"]["人数"] = len(xuanke_lishilei)
    return_data['选科历史类']['占比'] = str(Decimal(len(xuanke_lishilei) * 100 / studnet_num).quantize(Decimal("0.00"))) + '%'

    sql_data = 'SELECT student_choose_subject_volunteer.mix_subject_name,student_choose_subject_volunteer.choose_type, count(*)  FROM student_choose_subject_volunteer LEFT OUTER JOIN student_todo ON student_todo.id = student_choose_subject_volunteer.student_todo_id WHERE student_todo.todo_name_code = {}' \
               ' and student_choose_subject_volunteer.choose_type=1 group by student_choose_subject_volunteer.mix_subject_name'.format(str(exam_id))
    cursor = conn.cursor()
    cursor.execute(sql_data)
    xuankezuhe_huizong={}
    for i in cursor.fetchall():
        xuankezuhe_huizong[i[0]] = i[2]
    return jsonify(statu='success', detail=return_data,xuankezuhe_huizong=xuankezuhe_huizong)
@wuzhou.route('/school_detail', methods=['POST', 'GET'])
@cross_origin()
def get_xuanke_studentq():
    exam_id = request.form['exam_id']
    school_name = request.form['school_name']
    conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                           user='QA', password='hmk#%^&djofsdh', database='exam_business2', charset='utf8')
    cursor = conn.cursor()
    sql_data='select distinct(school_code) from school_class_ralate where school_name={}'.format(school_name.strip())
    cursor.execute(sql_data)
    school_name = cursor.fetchall()
    if len(school_name)==0:
        return jsonify(statu='error',detail='查询不到学校信息')
    else:
        school_id=school_name[0][0]
        sql_data='select * from where subject_code="10000202"'
        cursor.execute(sql_data)
        if len(cursor.fetchall())>0:
            exam_type="xuanke_after"
        else:
            exam_type = "xuanke_before"
        if    exam_type == "xuanke_before":
            sql_data = 'SELECT COUNT(DISTINCT(exam_code)) FROM stu_subject_score  WHERE exam_id= {} and student_status !=1 ' \
                       '  and  school_code = {}'.format(str(exam_id),str(school_id))
            cursor.execute(sql_data)
            studnet_num = cursor.fetchall()[0][0]
            fenshu_line= request.form['fenshu_line']
            linjiefen=  request.form['linjiefen']
            sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and ' \
                       'SUM(total_score)<={}'.format(
                str(exam_id), str(fenshu_line), str(fenshu_line+linjiefen))
            cursor.execute(sql_data)
            csee_num = cursor.fetchall()
            qingbei_lein_jie_num_up = len(csee_num)
            sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={} and ' \
                       'SUM(total_score)<{}'.format(
                str(exam_id), str(fenshu_line-linjiefen), str(fenshu_line))
            cursor.execute(sql_data)
            csee_num = cursor.fetchall()
            qingbei_lein_jie_num_down = len(csee_num)
            sql_data = 'SELECT SUM(total_score)  FROM stu_subject_score  WHERE exam_id= {} and student_status !=1  GROUP BY exam_code  HAVING SUM(total_score)>={}'.format(
                str(exam_id), str(fenshu_line))
            cursor.execute(sql_data)
            csee_num = cursor.fetchall()
            qingbei__num = len(csee_num)
            qingbei__num = str(qingbei__num) + '(' + str(
                Decimal(qingbei__num * 100 / studnet_num).quantize(Decimal("0.00"))) + '%' + ')'
            return {
                "分数线": fenshu_line,
                "临界生分数线": linjiefen,
                "上线人数": qingbei__num,
                "临界生人数线下": qingbei_lein_jie_num_down,
                "临界生人数线上": qingbei_lein_jie_num_up,
            }



