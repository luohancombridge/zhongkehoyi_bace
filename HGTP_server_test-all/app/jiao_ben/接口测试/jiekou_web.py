# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from submitPrice import *
from deletePrice import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from  win_exe import *
from he_zuo_bian_ma import *
#from  creat_dang import *
from creat_dang_qi import *
from createStock import *
import unittest
import xlrd
from checkstock import *
from updatePriceDetailList import *
#调用web接口塞数据
class run_jie(object):
    def __init__(self):
          self.h = webdriver.Chrome()
          self.h.get('http://10.199.199.116:1082/online_test.html')
          self.data = xlrd.open_workbook(
              r'D:\Users\zhen03.sun\workspace\zhen\test_data\creatPricelist\createPriceList.xls')
          self.table = self.data.sheets()[0]
          self.num = self.table.nrows
          self.data = self.table.row_values(self.table.nrows - 1)
          while True:
             self.z = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\creatPricelist\createPriceList.xls')
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
if __name__=='__main__':
    run_jie()