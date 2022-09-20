# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from  .win_exe import *
from .he_zuo_bian_ma import *
#from  creat_dang import *
from .creat_dang_qi import *
import unittest
import xlrd
from .updatePriceDetailList import *
#调用web接口塞数据
class run_jie(object):
    def __init__(self):
          self.h = webdriver.Chrome()
          self.h.get('http://10.199.199.116:1082/online_test.html')
          self.data = xlrd.open_workbook(
              r'D:\Users\zhen03.sun\workspace\zhen\test_data\ModifyPriceServiceTest\testupdatePriceDetailList.xls')
          self.table = self.data.sheets()[0]
          self.num = self.table.nrows
          print((22222222222))
          print((self.num))
          self.data = self.table.row_values(self.table.nrows - 1)
          while True:
             self.z = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\ModifyPriceServiceTest\testupdatePriceDetailList.xls')
             self.table = self.z.sheets()[0]
             print((55555555555))
             print((self.table.nrows))
             if self.table.nrows!=self.num:
                 print((333333333333))
                 print((self.table.nrows))
                 pritce_detail(self.h)
                 self.num=self.table.nrows
                 self.data = self.table.row_values(self.table.nrows - 1)
             elif self.table.row_values(self.table.nrows-1)!=self.data:
                 print((333333333333))
                 print((self.table.nrows))
                 pritce_detail(self.h)
                 self.num = self.table.nrows
                 self.data = self.table.row_values(self.table.nrows - 1)
             else:
                 time.sleep(2)
if __name__=='__main__':
    run_jie()