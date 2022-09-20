# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from .he_zuo_bian_ma import *
#from  creat_dang import *
from .creat_dang_qi import *
import unittest
class zz(unittest.TestCase):
    def __init__(self):
        self.h = webdriver.Chrome()
        self.s=creat(self.h)
        self.kk=self.s.shopName
        self.k1=self.s.he_zuo_bian_ma
        self.s = creat_dang(self.h, self.s.shopName, [10,20,100]).creat()
        self.z="合作主题为:%s,合作编码为:%s,档期id为:%s",(self.kk,self.k1,self.s)
if __name__=='__main__':
    unittest.main()