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
class delete_detail(object):
    def __init__(self,h):
        self.h=h
        self.data = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\submitPrice\submitPrice.xls')
        self.table = self.data.sheets()[0]
        self.s=self.table.row_values(self.table.nrows-1)
        self.z=self.h.find_elements_by_class_name('input_top')
        self.s[6]=str(self.s[6])[:-4]
        for k,i in enumerate(self.s[3:-1]):
          self.z[k].clear()
          if '.'  in str(i) and len(str(i).split('.')[1])>2:
              self.z[k].send_keys(''.join(str(i).split('.')))
          else:
              self.z[k].send_keys(str(i).split('.')[0])
        self.h.find_element_by_id('sub').click()