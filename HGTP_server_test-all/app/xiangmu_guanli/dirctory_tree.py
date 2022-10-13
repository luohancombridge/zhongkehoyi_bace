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
from app.xiangmu_guanli.db_case_run import *
xiangmuguanli = Blueprint('xiangmuguanli',__name__)
@xiangmuguanli.route('/add_xiangmu',methods=['POST','GET'])
@cross_origin()
@add_xiangmu
def add_xiangmu():
    pass

@xiangmuguanli.route('/get_all_xiangmu',methods=['POST','GET'])
@cross_origin()
@get_all_xiangmu
def get_all_xiangmu():
    pass
