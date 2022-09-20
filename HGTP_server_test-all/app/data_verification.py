# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import chardet
import unittest
import demjson
import urllib.request, urllib.parse, urllib.error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#from  creat_dang import *
import unittest
import xlrd
import json
import urllib.request, urllib.error, urllib.parse
import os
#self.data为每列值组成的列表
class read_excel(object):
    def __init__(self,file):
        self.data = xlrd.open_workbook(file)
        self.table0 = self.data.sheets()[0]
        self.key0=self.table0.row_values(0)
        self.data0 = [self.table0.row_values(i) for i in range(1,self.table0.nrows)]
        self.table0= self.table0.row_values(0)

        self.table1 = self.data.sheets()[1]
        self.key1=self.table1.row_values(0)
        self.data1 = [self.table1.row_values(i) for i in range(1,self.table1.nrows)]
        self.table1= self.table1.row_values(0)

        self.table2 = self.data.sheets()[2]
        self.key2=self.table2.row_values(0)
        self.data2 = [self.table2.row_values(i) for i in range(1,self.table2.nrows)]
        self.table2= self.table2.row_values(0)

#查询mysql数据表返回为键值字典,只返回一条数据
class read_mysql(object):
    def __init__(self,sql):
        self.conn = MySQLdb.connect(host='10.199.129.247',port = 3309,user='vis', passwd='vispvip',db ='visAdmin', cursorclass = MySQLdb.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.data=self.cur.fetchone()
        self.conn.close()
#匹配两个数据区取出来的字段值,不匹配的值为self.error
class pipei(object):
    def __init__(self,a,b):
        self.error={}
        for i in list(a.keys()):
            if a[i].strip()==b[i].strip():
                pass
            else:
                self.error[i]=a.keys
