#-*-coding:utf-8-*-
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys
import unittest
from zong_ti_shu_ju import test_zong_shu_ju
import HTMLTestRunner
sys.path.append(r'C:\efq_ben')
suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(test_zong_shu_ju)])
ISOTIMEFORMAT='%Y-%m-%d'
s=time.strftime( ISOTIMEFORMAT, time.localtime( time.time() ) )
filename=r'dizhi'
fp=file(filename,'wb')
runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title='Result',description='Test_Report')
runner.run(suite)