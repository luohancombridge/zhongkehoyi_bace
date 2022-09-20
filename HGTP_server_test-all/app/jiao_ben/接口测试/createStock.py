# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from  win_exe import *
from he_zuo_bian_ma import *
#from  creat_dang import *
from creat_dang_qi import *
import unittest
import xlrd
import json
class create_stock(object):
    def __init__(self,h):
        self.h=h
        self.h.switch_to_window(self.h.window_handles[0])
        self.data = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\createStock\createStock.xls')
        self.table = self.data.sheets()[0]
        self.s=self.table.row_values(self.table.nrows-1)
        self.z=self.h.find_elements_by_class_name('input_top')
        self.z=self.h.find_elements_by_class_name('input_top')
        for k,i in enumerate(self.s[3:-1]):
            if '.' in str(i):
             self.s[k+3]=str(i).split('.')[0]
        self.zz=self.s[3:-1]
        for k,i in enumerate(self.zz):
          self.z[k].clear()
          self.z[k].send_keys(i)
        self.h.switch_to_window(self.h.window_handles[-1])
        self.j=open(r'D:\Users\zhen03.sun\workspace\zhen\test_data\createStock\dd.txt').read()
        self.h.find_element_by_class_name('input_top').clear()
        self.creat_json()
        self.h.find_element_by_class_name('input_top').send_keys(self.j)
        self.h.find_element_by_id('sub').click()
        time.sleep(1)
        self.j=json.loads(self.h.find_element_by_id('res').text)['result']
        print((1111111111111111))
        print((self.j))
        self.h.switch_to_window(self.h.window_handles[0])
        self.z = self.h.find_elements_by_class_name('input_top')
        self.z[1].clear()
        self.z[1].send_keys(self.j)
        self.h.find_element_by_id('sub').click()
    def creat_json(self):
        self.tabl = dict(list(zip(self.table.row_values(0)[3:-1], self.zz)))
        self.j = open(r'D:\Users\zhen03.sun\workspace\zhen\test_data\createStock\dd.txt').read()
        self.j = json.loads(self.j)
        print((222233333333333333))
        print((list(self.j.keys())))
        print((list(self.tabl.keys())))
        for i in list(self.j.keys()):
            if i in list(self.tabl.keys()):
                self.j[i] = self.tabl[i]
            else:
                print((444444444444444444))
                print((type(self.j[i])))
                print((self.j[i]))
                for z in list(self.j[i][0].keys()):
                    self.j[i][0][z] = self.tabl[z]
        print((77777777777777777777))
        print((self.j['stockDetail']))
        print((type(self.j['stockDetail'])))
        self.j['stockDetail'][0]['inventory'] = int(self.j['stockDetail'][0]['inventory'])
        self.j = json.dumps(self.j)
        print((22222222222222))
        print((self.j))
