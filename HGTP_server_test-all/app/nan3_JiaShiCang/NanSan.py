from audioop import avg
from socket import MsgFlag
from flask import Blueprint,jsonify,request
import redis
import requests
import time
import sqlite3
import json
from flask import Flask, g
from flask_cors import *
from flask import current_app,session
from numpy import *
from fractions import Fraction
from itertools import groupby
from .get_DB_basedata import *


NanSan = Blueprint('NanSan',__name__)


def get_tianbaolv_list(xuankerenshu_list,entrance_count_list):
    tianbaolv_list=[]
    for n in range(len(xuankerenshu_list)):
        if int(xuankerenshu_list[n]) == 0 or int(entrance_count_list[0]) == 0:
            tianbaolv_list.append(0.0)
        else:
            tianbaolv_list.append(round(int(xuankerenshu_list[n])/int(entrance_count_list[n]),4))
    return tianbaolv_list


def get_wuli_lishi_bili(wuli_renshu, lishi_renshu):
    if lishi_renshu == 0 or wuli_renshu == 0:
        wuli_lishi_bili = [ wuli_renshu, lishi_renshu ]
    else:
        wuli_lishi = Fraction(wuli_renshu, lishi_renshu)
        wuli_lishi_bili = [ wuli_lishi.numerator, wuli_lishi.denominator ]
    return wuli_lishi_bili


def get_shangxian_lv(score_line_all, total_score_data_all, entrance_count_list):
    qingbei_lv_list, yiben_lv_list, erben_lv_list = [], [], []
    for n in range(len(total_score_data_all)):
        cankaorenshu = entrance_count_list[n]
        qingbei_renshu, yiben_renshu, erben_renshu = 0, 0, 0
        score_data_list = total_score_data_all[n]
        qingbei_line, yiben_line, erben_line = score_line_all[n]
        for score in score_data_list:
            if float(score) >= float(qingbei_line):
                qingbei_renshu += 1
                yiben_renshu += 1
                erben_renshu += 1
            elif float(score) >= float(yiben_line):
                yiben_renshu += 1
                erben_renshu += 1
            elif float(score) >= float(erben_line):
                erben_renshu += 1
        qingbei_lv_list.append(round(qingbei_renshu/cankaorenshu,3))
        yiben_lv_list.append(round(yiben_renshu/cankaorenshu,3))
        erben_lv_list.append(round(erben_renshu/cankaorenshu,3))
    return qingbei_lv_list, yiben_lv_list, erben_lv_list
        


@NanSan.route("/kaoshi/get_hexinzhibiao_data", methods=['POST','GET'])
@cross_origin()
def get_hexinzhibiao_data():
    args = request.args
    school_id=args.get('school_id', None)
    grade_id=args.get('grade_id', None)
    yearterm_id=2122  #第一版暂时写死
    if not school_id or not grade_id or not yearterm_id:
        errorlog = '''请求缺少关键参数，请检查.....例: nan3/get_DB_data?school_id=111&grade_id=111&yearterm_id=111'''
        return jsonify(msg=errorlog)
    examlist, examnamelist, entrance_count_list, entrance_list = get_kaoshi_data(school_id,grade_id,yearterm_id).get_kaoshi_basedata()
    if not examlist:
        errorlog = '''学校id: %s,年级id: %s,学年: %s, 该条件下没有查询到考试信息....'''%(school_id,grade_id,yearterm_id)
        return jsonify(msg=errorlog)

    avg_entrance_lv = mean(entrance_list)
    return_data={
        "联考次数/参考人数": "%s/%s"%(len(examlist),sum(entrance_count_list)), 
        "平均参考率": '%.1f%%' % (float(avg_entrance_lv)*100)
        }

    xuankerenshu_2to1_list, wuli_renshu_list, lishi_renshu_list, xuanke_subject_result  = get_xuanke_data(school_id,examlist).get_xuanke_2to1_data()

    tianbaolv_list = get_tianbaolv_list(xuankerenshu_2to1_list,entrance_count_list)
    wuli_lishi_bili = get_wuli_lishi_bili(wuli_renshu_list[0], lishi_renshu_list[0])
    avg_tianbaolv = mean(tianbaolv_list)
    return_data.update({
        "平均填报率": '%.1f%%' % (float(avg_tianbaolv)*100), 
        "物理选科人数": wuli_renshu_list[0], 
        "历史选科人数": lishi_renshu_list[0],
        "物理/历史选科比例":"%s : %s"%tuple(wuli_lishi_bili)
        })
    
    score_data = get_score_data(school_id,examlist)
    score_line_all = score_data.get_score_line_data()
    total_score_data_all = score_data.get_total_score_data()

    qingbei_lv_list, yiben_lv_list, erben_lv_list = get_shangxian_lv(score_line_all, total_score_data_all, entrance_count_list)
    avg_qingbei_lv = mean(qingbei_lv_list)
    avg_yiben_lv = mean(yiben_lv_list)
    avg_erben_lv = mean(erben_lv_list)
    return_data.update({
        "清北平均上线率": '%.1f%%' % (float(avg_qingbei_lv)*100), 
        "一本平均上线率": '%.1f%%' % (float(avg_yiben_lv)*100), 
        "本科平均上线率": '%.1f%%' % (float(avg_erben_lv)*100),
        })
    return jsonify(return_data)



@NanSan.route("/kaoshi/get_xuankezhibiao_data", methods=['POST','GET'])
@cross_origin()
def get_xuankezhibiao_data():
    args = request.args
    school_id=args.get('school_id', None)
    grade_id=args.get('grade_id', None)
    yearterm_id=2122  #第一版暂时写死
    if not school_id or not grade_id or not yearterm_id:
        errorlog = '''请求缺少关键参数，请检查.....例: nan3/get_DB_data?school_id=111&grade_id=111&yearterm_id=111'''
        return jsonify(msg=errorlog)
    examlist,examnamelist, entrance_count_list,entrance_list = get_kaoshi_data(school_id,grade_id,yearterm_id).get_kaoshi_basedata()
    if not examlist:
        errorlog = '''学校id: %s,年级id: %s,学年: %s, 该条件下没有查询到考试信息....'''%(school_id,grade_id,yearterm_id)
        return jsonify(msg=errorlog)

    xuankerenshu_2to1_list, wuli_renshu_list, lishi_renshu_list, xuanke_subject_result = get_xuanke_data(school_id,examlist).get_xuanke_2to1_data()
    tianbaolv_list = get_tianbaolv_list(xuankerenshu_2to1_list,entrance_count_list)
    # wuli_lishi_bili = get_wuli_lishi_bili(wuli_latest, lishi_latest)  # 该比例值直接显示两个人数即可，暂时废弃
    return_tianbaolv_data = []
    for n in range(len(examlist)):
        r_data = { "考试id" : examlist[n] }
        r_data[ "填报率" ] = '%.2f%%' % (float(tianbaolv_list[n])*100) 
        r_data[ "选课-物理占比" ] = '%.2f%%' % (int(wuli_renshu_list[n]) / int(xuankerenshu_2to1_list[n])*100) 
        r_data[ "选课-历史占比" ] = '%.2f%%' % (int(lishi_renshu_list[n]) / int(xuankerenshu_2to1_list[n])*100) 
        r_data[ "选科组合统计" ] = xuanke_subject_result[n]
        return_tianbaolv_data.append(r_data)

    return_data={"选科填报率变化": list(reversed(return_tianbaolv_data))}

    return jsonify(return_data)



@NanSan.route("/kaoshi/get_chengjifenbu_data", methods=['POST','GET'])
@cross_origin()
def get_chengjifenbu_data():
    args = request.args
    school_id=args.get('school_id', None)
    grade_id=args.get('grade_id', None)
    yearterm_id=2122  #第一版暂时写死
    if not school_id or not grade_id or not yearterm_id:
        errorlog = '''请求缺少关键参数，请检查.....例: nan3/get_DB_data?school_id=111&grade_id=111&yearterm_id=111'''
        return jsonify(msg=errorlog)
    examlist,examnamelist, entrance_count_list,entrance_list = get_kaoshi_data(school_id,grade_id,yearterm_id).get_kaoshi_basedata()
    if not examlist:
        errorlog = '''学校id: %s,年级id: %s,学年: %s, 该条件下没有查询到考试信息....'''%(school_id,grade_id,yearterm_id)
        return jsonify(msg=errorlog)

    score_data = get_score_data(school_id,examlist)
    all_subject_score_list = score_data.get_subject_score_data()
    all_score_data_list = score_data.get_total_score_data()
    all_score_line_list = score_data.get_score_line_data()

    return_data={"成绩分布展示区": score_fenbu(examlist, all_subject_score_list, all_score_data_list, all_score_line_list)}
    return jsonify(return_data)    


def score_fenbu(examlist, subject_score_list, total_score_list, score_line_list):
    fenbu_result = []
    for n in range(len(examlist)):
        total_score = total_score_list[n]
        score_line = score_line_list[n]
        subject_score = subject_score_list[n]
        exam_fenbu = {
            "A考试id": examlist[n],
            "总分情况": {
                "人数分布": list_fenbu(total_score),
                "青北线": score_line[0],
                "一本线": score_line[1],
                "二本线": score_line[2]
            },
            "各科情况": []
        }
        for subject_name in subject_score:
            score_list = subject_score.get(subject_name, [])
            exam_fenbu["各科情况"].append({
                "学科名称": subject_name,
                "人数分布": list_fenbu(score_list),
                "平均分": '%.2f' % (mean(score_list)) 
            })
        fenbu_result.append(exam_fenbu)
    return fenbu_result 


def list_fenbu(score_list, jiange = 20):
    max_score = max(score_list)
    max_fenbuzu = int(max_score/jiange) + 1
    fenbu_renshu = [ 0 for n in range(max_fenbuzu) ]
    for score in score_list:
        fenbu_renshu[int(float(score)/jiange)] += 1
    fenbu_renshu_result = [["%s-%s"%(i[0]*jiange, (i[0]+1)*jiange), i[1]] for i in list(enumerate(fenbu_renshu)) ]
    return fenbu_renshu_result





