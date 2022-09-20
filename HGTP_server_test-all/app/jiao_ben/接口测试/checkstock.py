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
class check_stock(object):
    def __init__(self,h):
        self.h=h
        self.h.switch_to_window(self.h.window_handles[0])
        self.data = xlrd.open_workbook(r'D:\Users\zhen03.sun\workspace\zhen\test_data\queryStock\queryStock.xls')
        self.table = self.data.sheets()[0]
        self.s=self.table.row_values(self.table.nrows-1)
        self.z=self.h.find_elements_by_class_name('input_top')
        for k,i in enumerate(self.s[3:]):
          self.z[k].clear()
          try:
              i=int(i)
          except:
              pass
          self.z[k].send_keys(i)
        self.h.find_element_by_id('sub').click()