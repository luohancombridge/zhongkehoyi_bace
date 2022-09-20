# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket

import os
import json
import urllib.request, urllib.error, urllib.parse
import re
import  chardet

import time

import sqlite3

from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import xlrd
import xlwt
def phone_changliang_add(func):
    def phone_changliang_add():
        func()
        type=request.form['type']
        detail=request.form['detail']
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        if len( cu.execute('select * from changliang  where type="%s" and detail="%s"' % (type,detail)).fetchall())!=0:
            resp=jsonify(statu='信息重复')
        else:
            cu.executemany('INSERT INTO changliang VALUES (?,?)',
                           [(type,detail)])
            resp=jsonify(statu='success')
        db.commit()
        db.close()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return phone_changliang_add

def add_phone_modal(func):
    def add_phone_modal():
        func()
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        add_pinpai =request.form['add_pinpai']
        add_jixing = request.form['add_jixing']
        add_xitong = request.form['add_xitong']
        add_chicun = request.form['add_chicun']
        add_fenbianlv = request.form['add_fenbianlv']
        add_mima = request.form['add_mima']
        add_shoushimima = request.form['add_shoushimima']
        add_xuliehao = request.form['add_xuliehao']
        add_yanse = request.form['add_yanse']
        cu.executemany('INSERT INTO phone_detail VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       [(add_pinpai,add_jixing,add_xitong,add_chicun,add_xuliehao,add_fenbianlv,add_mima,add_shoushimima,'','','','未出借',add_yanse)])
        db.commit()
        db.close()
        resp=jsonify(statu="success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return add_phone_modal



def bianji_phone_modal(func):
    def bianji_phone_modal():
        func()
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        bianji_pinpai =request.form['bianji_pinpai']
        bianji_jixing = request.form['bianji_jixing']
        bianji_xitong = request.form['bianji_xitong']
        bianji_chicun = request.form['bianji_chicun']
        bianji_fenbianlv = request.form['bianji_fenbianlv']
        bianji_mima = request.form['bianji_mima']
        bianji_shoushimima = request.form['bianji_shoushimima']
        bianji_xuliehao = request.form['bianji_xuliehao']
        bianji_yanse = request.form['bianji_yanse']
        bianji_chujieren = request.form['bianji_chujieren']
        bianji_chujieriqi = request.form['bianji_chujieriqi']
        biaji_guihuanriqi = request.form['biaji_guihuanriqi']
        bianji_zhuangtai=request.form['bianji_zhuangtai']
        cu.execute('update phone_detail set pinpai=?,jixing=?,xitong=?,chicun=?,xuliehao=?,fenbianlv=?,mima=?,shoushimima=?,jieyongrenyuan=?,jieyongriqi=?,guihuanriqi=?,yanse=?,statu=?,yanse=?  where id=?',
                       (bianji_pinpai,bianji_jixing,bianji_xitong,bianji_chicun,bianji_xuliehao,bianji_fenbianlv,bianji_mima,bianji_shoushimima,bianji_chujieren,bianji_chujieriqi,biaji_guihuanriqi,bianji_yanse,bianji_zhuangtai,bianji_yanse,request.form['row_id']))
        db.commit()
        db.close()
        resp=jsonify(statu="success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return bianji_phone_modal

def shouye(func):
    def shouye():
        func()
        riqi = time.strftime("%Y-%m-%d", time.localtime())
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        phone_detail=cu.execute('select * from phone_detail where statu  in ("未出借","已出借","已预订") ').fetchall()
        all_pinpai=cu.execute('select detail from changliang where type="%s"' %('all_pinpai') ).fetchall()
        all_xitong = cu.execute('select detail from changliang where type="%s"' % ('all_xitong')).fetchall()
        all_chicun = cu.execute('select detail from changliang where type="%s"' % ('all_chicun')).fetchall()
        all_fenbianlv = cu.execute('select detail from changliang where type="%s"' % ('all_fenbianlv')).fetchall()
        db.close()
        g.db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        g.cu = g.db.cursor()
        user= g.cu.execute('select name from user where ip="%s"' % (request.headers.get('X-Real-IP'))).fetchall()[0][0]
        if  user in current_app.config.get('ZICHAN_QUANXIAN').split(','):
             user_statu=1
        else:
            user_statu=0
        return render_template('/phoine_guanli/phone.html', phone_detail=phone_detail,all_pinpai=all_pinpai,
                               all_xitong=all_xitong,all_chicun=all_chicun,all_fenbianlv=all_fenbianlv,user_statu=user_statu,today=riqi
                               )
    return shouye

def phone_changliang_delete(func):
    def phone_changliang_delete():
        func()
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        row_id=request.form['row_id']
        cu.execute('delete from phone_detail where id="%s"' % (row_id))
        db.commit()
        db.close()
        return jsonify(statu="success")
    return phone_changliang_delete

def phone_simple_caozuo(func):
    def phone_simple_caozuo(name):
        func(name)
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        if name=='guihuan':
            id=request.form['row_id']
            detail=cu.execute('select statu from phone_detail where id="%s"'  %(id)).fetchall()
            if len(detail)==0:
                return jsonify(statu="信息不存在")
            else:
                if detail[0][0]=='已出借':
                    riqi=time.strftime("%Y-%m-%d", time.localtime())
                    cu.execute(
                        'update phone_detail set  statu="未出借",guihuanriqi=? where id=?',
                        (riqi,id))
                    db.commit()
                    db.close()
                    return jsonify(statu="success",riqi=riqi)
                else:
                    return jsonify(statu="该设备未在使用中")
        elif name=='yuding':
            id=request.form['row_id']
            yuding_user=request.form['yuding_user']
            guihuanriqi = request.form['guihuanriqi']
            yudingriq = request.form['yudingriq']
            if  yuding_user.strip()=='':
                return jsonify(statu="预订人员不能为空")
            try:
                if guihuanriqi.strip()!='':
                    timeArray = time.strptime(guihuanriqi, "%Y-%m-%d")
                    timeStamp = int(time.mktime(timeArray))
            except:
                return jsonify(statu="归还日期格式不对")
            try:
                if yudingriq.strip()=='':
                    return jsonify(statu="借用日期不能为空")
                timeArray = time.strptime(yudingriq, "%Y-%m-%d")
                timeStamp = int(time.mktime(timeArray))
            except:
                return jsonify(statu="借用日期格式不对")
            detail=cu.execute('select statu from phone_detail where id="%s"'  %(id)).fetchall()
            if len(detail)==0:
                return jsonify(statu="信息不存在")
            else:
                if detail[0][0]=='未出借':
                    riqi=time.strftime("%Y-%m-%d", time.localtime())
                    cu.execute(
                        'update phone_detail set  statu="已预订",guihuanriqi=?,jieyongrenyuan=?,jieyongriqi=? where id=?',
                        (guihuanriqi,yuding_user,yudingriq,id))
                    db.commit()
                    db.close()
                    return jsonify(statu="success",riqi=riqi)
                else:
                    return jsonify(statu="该设备未在空闲中")
        elif name=='chujie':
            id=request.form['row_id']
            detail=cu.execute('select statu from phone_detail where id="%s"'  %(id)).fetchall()
            if len(detail)==0:
                return jsonify(statu="信息不存在")
            else:
                if detail[0][0]=='已预订':
                    riqi=time.strftime("%Y-%m-%d", time.localtime())
                    cu.execute(
                        'update phone_detail set  statu="已出借",jieyongriqi=? where id=?',
                        (riqi,id))
                    db.commit()
                    db.close()
                    return jsonify(statu="success",riqi=riqi)
                else:
                    return jsonify(statu="该设备未被预订")
        elif name=='shanchu':
            id=request.form['row_id']
            detail=cu.execute('select statu from phone_detail where id="%s"'  %(id)).fetchall()
            if len(detail)==0:
                return jsonify(statu="信息不存在")
            else:
                if detail[0][0]=='未出借':
                    riqi=time.strftime("%Y-%m-%d", time.localtime())
                    # cu.execute(
                    #     'delete from  phone_detail  where id=?',
                    #     (id))
                    db.commit()
                    db.close()
                    return jsonify(statu="success",riqi=riqi)
                else:
                    return jsonify(statu="该设备在使用中")
    return phone_simple_caozuo



def phone_submit(func):
    def phone_submit():
        func()
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        file = request.files['files']
        filename = secure_filename(file.filename)
        file_path=os.path.join(current_app.config.get('PHONE_FILE'),str(int(time.time())))
        os.makedirs(file_path)
        file.save(os.path.join(file_path, filename))
        workbook = xlrd.open_workbook(os.path.join(file_path, filename))
        sheet2 = workbook.sheet_by_index(0)
        rows = sheet2.row_values(0)
        detail = {}
        duiying1 = ['pinpai', 'jixing', 'xitong', 'chicun', 'xuliehao', 'fenbianlv', 'mima', 'shoushimima',
                    'jieyongrenyuan', 'jieyongriqi', 'guihuanriqi', 'statu', 'yanse']
        duiying = ['品牌', '机型', '系统', '尺寸', '资产编号', '分辨率', '密码', '业务线', '借用人员', '借用日期', '归还日期', '状态', '颜色']
        for i in range(sheet2.ncols):
            data = sheet2.col_values(i)
            detail[data[0]] = data[1:]
        for i in list(detail.keys()):
            if i not in duiying:
                print(i)
        for i in  range(len(detail['品牌'])):
            cu.executemany('INSERT INTO phone_detail VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                           [(detail[duiying[0]][i],detail[duiying[1]][i],detail[duiying[2]][i],detail[duiying[3]][i],detail[duiying[4]][i],detail[duiying[5]][i],detail[duiying[6]][i],detail[duiying[7]][i],detail[duiying[8]][i],detail[duiying[9]][i],detail[duiying[10]][i],detail[duiying[11]][i],detail[duiying[12]][i])])
        db.commit()
        db.close()
        os.remove(os.path.join(file_path, filename))
        return redirect(url_for('shouye'))
    return phone_submit
def excel_daochu(func):
    def excel_daochu():
        func()
        for i in os.listdir(current_app.config.get('PHONE_FILE_DOWNLOAD')):
            path_file = os.path.join(current_app.config.get('PHONE_FILE_DOWNLOAD'), i)
            try:
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    del_file(path_file)
            except:
                pass
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        duiying = ['品牌', '机型', '系统', '尺寸', '资产编号', '分辨率', '密码', '业务线', '借用人员', '借用日期', '归还日期', '状态', '颜色']
        file = xlwt.Workbook()
        table = file.add_sheet('sheet name')
        for k,i in enumerate(duiying):
            table.write(0, k, i)
        for k,i in enumerate([i[1:] for i in cu.execute('select * from phone_detail').fetchall()]):
            for z,u in enumerate(i):
                table.write(k+1, z, u)
        file_name='资产列表.xls'
        file_path=os.path.join(current_app.config.get('PHONE_FILE_DOWNLOAD'),str(time.time()))
        os.mkdir(file_path)
        file.save(os.path.join(file_path,file_name))
        return send_from_directory(file_path, file_name, as_attachment=True)
    return excel_daochu

def all_phone_delete(func):
    def all_phone_delete():
        func()
        db = sqlite3.connect(current_app.config.get('PHONE_DB'))
        cu = db.cursor()
        str_time='已删除'+str(time.time())
        cu.execute(
            'update phone_detail set  statu="%s"'  % (str_time))
        db.commit()
        db.close()
        return jsonify(statu="success")
    return all_phone_delete