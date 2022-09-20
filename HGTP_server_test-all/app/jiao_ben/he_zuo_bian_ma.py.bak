# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#创建合作编码
class creat(object):
    def __init__(self,s):
        if isinstance(s,webdriver.chrome.webdriver.WebDriver):
            self.h=s
            #self.h=webdriver.Chrome()
            self.h.maximize_window()
            self.h.implicitly_wait(10)
            self.wait = WebDriverWait(self.h, 10)
            self.h.get('https://cas.test.vipshop.com:8443/login?service=http%3A%2F%2Fvis-admin.vip.vip.com%2Flogin.php%3FReturnUrl%3Dhttp%253A%252F%252Fvis-admin.vip.vip.com%252Flogin.php')
            self.h.find_element_by_id('UserName').send_keys('alice.xiao')
            self.h.find_element_by_id('UserName').submit()
            self.h.find_element_by_partial_link_text(u'店铺管理').click()
            self.h.find_element_by_partial_link_text(u'店铺申请').click()
            self.h.switch_to_frame(self.h.find_element_by_name('biw-ajax'))
            #self.wait.until(lambda z:z.find_element_by_xpath('//input[@data-url="/shop/ShopApply.php?act=add"]').is_displayed())
            self.h.find_element_by_xpath('//input[@data-url="/shop/ShopApply.php?act=add"]').click()
            self.h.find_element_by_name('vendorName').send_keys(u'五二二供应商')
            for i in self.h.find_elements_by_xpath('//div[@class="ac_results"]//li'):
                if u'五二二供应商(103530)'  in i.text:
                    i.click()
                    break
            self.shopName=time.strftime('%d-%H-%M',time.localtime(time.time()))
            self.h.find_element_by_name('shopName').send_keys(self.shopName)
            self.h.find_element_by_id('brandName').send_keys(u'思丽兰娜')
            time.sleep(1)
            for i in self.h.find_elements_by_xpath('//div[@class="ac_results"]//li'):
                if u'思丽兰娜'  in i.text:
                    i.click()
                    break
            self.h.find_element_by_id('brand_add').click()
            self.h.find_element_by_name('checkall').click()
            ActionChains(self.h).move_to_element(self.h.find_element_by_id('submit_btn'))
            self.h.find_element_by_id('submit_btn').click()
            time.sleep(1)
            self.h.switch_to_alert().accept()
            self.wait.until(lambda z:z.find_element_by_partial_link_text(u'审核').is_displayed())
            self.he_zuo_bian_ma=self.h.find_element_by_xpath('//div[@id="div_list"]//tr/td[1]').text
            self.h.find_element_by_partial_link_text(u'审核').click()
            self.wait.until(lambda z:z.find_element_by_id('saveY').is_displayed())
            ActionChains(self.h).move_to_element(self.h.find_element_by_id('saveY'))
            self.h.find_element_by_id('saveY').click()
            time.sleep(1)
            self.h.switch_to_alert().accept()
            time.sleep(1)
            self.h.switch_to_alert().accept()

if __name__=='__main__':
    h=webdriver.Chrome()
    u=creat(h)
    print u