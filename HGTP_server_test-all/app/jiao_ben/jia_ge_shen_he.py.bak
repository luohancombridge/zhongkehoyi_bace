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
import MySQLdb
#价格审核
class price_shen(object):
    def __init__(self):
        self.h=webdriver.Chrome()
        self.h.maximize_window()
        self.h.get('http://vis-admin.vip.vip.com/portal.php#!/app-i/biw-ajax/normalitySell/priceChangeApplyAudit.php?t=1476956670317')
        self.wait = WebDriverWait(self.h, 10)
        self.h.find_element_by_id('UserName').send_keys('alice.xiao')
        self.h.find_element_by_id('UserName').submit()
        self.wait.until(lambda z:z.find_element_by_partial_link_text(u'常态销售').is_displayed())
        self.h.find_element_by_partial_link_text(u'常态销售').click()
        self.wait.until(lambda z: z.find_element_by_partial_link_text(u'常态商品价格审核').is_displayed())
        self.h.find_element_by_partial_link_text(u'常态商品价格审核').click()
        self.wait.until(lambda z: z.find_element_by_name('biw-ajax').is_displayed())
        self.h.switch_to_frame(self.h.find_element_by_name('biw-ajax'))
        #点击第一个审核按钮，弹出页面
        self.wait.until(lambda z:z.find_element_by_xpath('//font[@color="blue"]').is_displayed())
        self.s=self.h.find_elements_by_xpath('//font[@color="blue"]')
        self.s[0].click()
        self.wait.until(lambda z:z.find_element_by_class_name('pop_part').is_displayed())
        u = self.h.find_element_by_class_name('pop_part').find_elements_by_tag_name('input')
        #审核按钮为第二个
        for i in u :
            if u'审核通过'  in  i.get_attribute('value'):
                i.click()
                break
        time.sleep(1)
        self.h.switch_to_alert().accept()
        time.sleep(1)
        #推送到价格系统
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/sync_to_ps_price_system.php?debug')
        time.sleep(1)
        self.h.get(' http://10.199.173.167/index.do')
        ActionChains(self.h).move_to_element(self.h.find_element_by_id('menu1_ps'))
        self.wait.until(lambda z: z.find_element_by_id('menu1_ps').is_displayed())
        self.h.find_element_by_id('menu1_ps').click()
        self.wait.until(lambda z:z.find_element_by_id('menu2_ps_priceCheck_list').is_displayed())
        self.h.find_element_by_id('menu2_ps_priceCheck_list').click()
        #修改数据库标志
        self.conn = MySQLdb.connect(host="10.199.174.26", user="ps", passwd="vipshop", db="vip_fcs_ps_flow_003", port=3306)
        self.cur=self.conn.cursor()
        self.cur.execute('UPDATE ps_apply_head  SET check_status = 2')
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        #搜索主题
        self.wait.until(lambda z: z.find_element_by_name('checkboxHeadId').is_displayed())
        self.h.find_element_by_name('subject').send_keys(u'测试销售主题')
        self.h.find_element_by_class_name('glyphicon-search').click()
        time.sleep(1)
        #self.h.find_element_by_class_name('ui-dialog-autofocus').click()
        self.wait.until(lambda z:z.find_element_by_name('checkboxHeadId').is_displayed())
        self.h.find_element_by_name('checkboxHeadId').click()
        self.h.find_element_by_id('exceptionCheckBtn').click()
        time.sleep(1)
        self.wait.until(lambda z:z.find_element_by_class_name('ui-dialog-autofocus').is_displayed())
        self.s=self.h.find_element_by_class_name('ui-dialog-autofocus')
        self.s.click()
        #确认价格
        self.wait.until(lambda z: z.find_element_by_id('currentId_0').is_displayed())
        self.h.execute_script('scrollTo(1000,0)')
        self.h.find_element_by_xpath('//button[@ng-hide="!(pscheck.status == 9 && pscheck.exptStatus == 2) "]').click()
        self.wait.until(lambda z:z.find_element_by_xpath('//button[@style="text-align: left;"]').is_displayed())
        self.h.find_element_by_xpath('//button[@style="text-align: left;"]').click()
        time.sleep(1)
        self.h.find_element_by_xpath('//button[@i-id="ok"]').click()
        time.sleep(1)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/get_result_from_ps.php?service=vip.scm.priceChangeApply.retrievePricingList')
        time.sleep(1)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/get_result_from_ps.php?service=vip.scm.priceChangeApply.rewritePricingResultToApply')
        time.sleep(1)
if __name__=='__main__':
        k=price_shen()



