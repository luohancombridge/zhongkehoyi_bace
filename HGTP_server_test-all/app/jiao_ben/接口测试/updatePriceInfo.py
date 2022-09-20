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


#调用web接口塞数据
class run_jie(object):
    def __init__(self):
          self.h = webdriver.Chrome()
          self.h.get('http://10.199.199.116:1082/online_test.html')
          self.data = xlrd.open_workbook(
              r'D:\Users\zhen03.sun\workspace\zhen\test_data\updatePriceInfo\updatePriceInfo.xls')
          self.table = self.data.sheets()[0]
          self.num = self.table.nrows
          self.data = self.table.row_values(self.table.nrows - 1)
          while True:
             self.z = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\updatePriceInfo\updatePriceInfo.xls')
             self.table = self.z.sheets()[0]
             if self.table.nrows!=self.num:
                 create_stock(self.h)
                 self.num=self.table.nrows
                 self.data = self.table.row_values(self.table.nrows - 1)
             elif self.table.row_values(self.table.nrows-1)!=self.data:
                 create_stock(self.h)
                 self.num = self.table.nrows
                 self.data = self.table.row_values(self.table.nrows - 1)
             else:
                 time.sleep(0.5)
class create_stock(object):
    def __init__(self,h):
        self.h=h
        self.h.switch_to_window(self.h.window_handles[0])
        self.data = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\updatePriceInfo\updatePriceInfo.xls')
        self.table = self.data.sheets()[0]
        self.s=self.table.row_values(self.table.nrows-1)
        self.z=self.h.find_elements_by_class_name('input_top')
        for k,i in enumerate(self.s[3:-1]):
            if isinstance(i,str):
                self.s[k + 3]=i.strip()
            if isinstance(i,float):
               self.s[k+3]=int(i)
        self.zz=self.s[3:-1]
        print((10101010101010100101))
        print((self.zz))
        for k,i in enumerate(self.zz):
          self.z[k].clear()
          try:
              str(i)
          except:
            self.z[k].send_keys(i)
          else:
              self.z[k].send_keys(str(i))
        self.h.switch_to_window(self.h.window_handles[-1])
        self.j=open(r'D:\Users\zhen03.sun\workspace\zhen\test_data\updatePriceInfo\dd.txt').read()
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
        self.num=0
        while True:
            try :
               self.h.find_element_by_id('sub').click()
            except:
                time.sleep(1)
                ActionChains(self.h).move_to_element(self.h.find_element_by_id('sub'))
                self.num+=1
                if self.num==5:
                    break
            else:
                break
    def creat_json(self):
        self.tabl = dict(list(zip(self.table.row_values(0)[3:-1], self.zz)))
        self.j = open(r'D:\Users\zhen03.sun\workspace\zhen\test_data\updatePriceInfo\dd.txt').read()
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
        self.j = json.dumps(self.j)
        print((22222222222222))
        print((self.j))
if __name__=='__main__':
    run_jie()