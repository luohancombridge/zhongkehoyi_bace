# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from app.directory_tree.db_case_run import *
from flask import Blueprint,jsonify,request
from app.vue_yonghu.db_case_run import *
vueyonghu = Blueprint('vueyonghu',__name__)
@vueyonghu.route('/add_uzhi',methods=['POST','GET'])
@cross_origin()
@add_uzhi
def add_uzhi():
    pass
@vueyonghu.route('/get_zuzhi',methods=['POST','GET'])
@cross_origin()
@get_zuzhi
def get_zuzhi():
    pass

@vueyonghu.route('/delete_zuzhi',methods=['POST','GET'])
@cross_origin()
@delete_zuzhi
def delete_zuzhi():
    pass
@vueyonghu.route('/get_all_user',methods=['POST','GET'])
@cross_origin()
@get_all_user
def get_all_user():
    pass
@vueyonghu.route('/delete_user',methods=['POST','GET'])
@cross_origin()
@delete_user
def delete_user():
    pass

@vueyonghu.route('/user_zuzhijiagou_change',methods=['POST','GET'])
@cross_origin()
@user_zuzhijiagou_change
def user_zuzhijiagou_change():
    pass

@vueyonghu.route('/change_password',methods=['POST','GET'])
@cross_origin()
@change_password
def change_password():
    pass

@vueyonghu.route('/get__all_quanxian',methods=['POST','GET'])
@cross_origin()
@get_vip_user
def get_vip_user():
    pass

@vueyonghu.route('/add_gongneng',methods=['POST','GET'])
@cross_origin()
@add_gongneng
def add_gongneng():
    pass

@vueyonghu.route('/get_gongneng_def',methods=['POST','GET'])
@cross_origin()
@get_gongneng_def
def get_gongneng_def():
    pass


@vueyonghu.route('/add_quanxiandian',methods=['POST','GET'])
@cross_origin()
@add_quanxiandian
def add_quanxiandian():
    pass


@vueyonghu.route('/get_all_quanxian',methods=['POST','GET'])
@cross_origin()
@get_all_quanxian
def get_all_quanxian():
    pass

@vueyonghu.route('/bianji_quanxian_def',methods=['POST','GET'])
@cross_origin()
@bianji_quanxian_def
def bianji_quanxian_def():
    pass

@vueyonghu.route('/delete_quianxian',methods=['POST','GET'])
@cross_origin()
@delete_quianxian
def delete_quianxian():
    pass

@vueyonghu.route('/delete_gongneng',methods=['POST','GET'])
@cross_origin()
@delete_gongneng
def delete_gongneng():
    pass

@vueyonghu.route('/get_quanxian_user',methods=['POST','GET'])
@cross_origin()
@get_quanxian_user
def get_quanxian_user():
    pass
