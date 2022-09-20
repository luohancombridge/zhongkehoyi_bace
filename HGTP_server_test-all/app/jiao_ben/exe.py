# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import unittest
class sss(unittest.TestCase):
    def setUp(self):
        self.h=webdriver.Chrome()
    def test_AA(self):
        self.h.get('http://www.baidu.com')