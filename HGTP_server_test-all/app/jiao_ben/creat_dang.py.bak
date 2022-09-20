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
#增加商品，
class add_product(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.h=webdriver.Chrome()
        self.h.implicitly_wait(10)
        self.wait=WebDriverWait(self.h,10)
    def test_creat(self):
        self.h.get('https://vis.vip.com/login.php')
        self.h.find_element_by_id('userName').send_keys('40019')
        self.h.find_element_by_id('passWord').send_keys('123456')
        self.h.find_element_by_id('passWord').submit()
        self.h.get('http://vis.vip.com/portal.php#!/app-v/pdc-vue/product/list?t=1476153824774')
        self.h.find_element_by_partial_link_text(u'批量新增商品').click()
        self.h.find_element_by_name('brandCode').click()
        self.wait.until(lambda  z:z.find_element_by_name('brandCode').find_element_by_xpath('//option[@value = "10007700"]').is_displayed())
        self.h.find_element_by_name('brandCode').find_element_by_xpath('//option[@value = "10007700"]').click()
        self.h.find_element_by_name('file').click()
        self.s=win_exe()
        time.sleep(1)
        self.s.send([u'打开','ComboBoxEx32','ComboBox','Edit','good_data'])
        time.sleep(1)
        self.s.click([u'打开','Button'])
        time.sleep(2)
        self.h.find_element_by_xpath('//section[@class="batch-upload-btn"]/button').click()
        while u'上传中' in self.h.find_element_by_xpath('//section[@class="batch-upload-btn"]/button').text:
            time.sleep(1)
    @classmethod
    def tearDownClass(self):
        time.sleep(3)
        self.h.quit()

if __name__=='__main__':
    unittest.main()