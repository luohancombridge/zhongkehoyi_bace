# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
from selenium import webdriver
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#创建档期，参数第一个为webdriver，第二个为合作编码名字，第三个为列表,传一个参数为供货价模式，传两个参数为毛利率模式
class creat_dang(object):
    def __init__(self,s,changtai,maolilv):
        if isinstance(s,webdriver.chrome.webdriver.WebDriver):
            self.h=s
        else:
         self.h=webdriver.Chrome()
        self.changtai=changtai
        self.maolilv=maolilv
        self.h.maximize_window()
        self.h.implicitly_wait(20)
        self.wait = WebDriverWait(self.h, 20)
        self.h.get(
    'https://cas.test.vipshop.com:8443/login?service=http%3A%2F%2Fvis-admin.vip.vip.com%2Flogin.php%3FReturnUrl%3Dhttp%253A%252F%252Fvis-admin.vip.vip.com%252Flogin.php')
        if 'http://vis-admin.vip.vip.com/' not in self.h.current_url:
           self.h.find_element_by_id('UserName').send_keys('alice.xiao')
           self.h.find_element_by_id('UserName').submit()
    def creat(self):
        self.h.find_element_by_partial_link_text('商务管理').click()
        self.h.find_element_by_partial_link_text('销售档期申请').click()
        self.h.find_element_by_partial_link_text('档期列表').click()
        self.h.switch_to_frame(self.h.find_element_by_name('biw-ajax'))
        self.wait.until(lambda z:z.find_element_by_id('add_apply_schedule').is_displayed())
        self.h.find_element_by_id('add_apply_schedule').click()
        self.wait.until(lambda  z:z.find_element_by_id('schedule_date_from').is_displayed())
        #选择合作模式
        self.h.find_element_by_id('selling_mode').click()
        time.sleep(0.2)
        for i  in self.h.find_element_by_id('selling_mode').find_elements_by_tag_name('option'):
            if i.text=='JIT':
                i.click()
                break
        self.h.find_element_by_id('vendor_name').send_keys('五二二')
        time.sleep(2)
        self.wait.until(lambda z:z.find_element_by_class_name('ac_even').is_displayed())
        self.h.find_element_by_class_name('ac_even').click()
        time.sleep(0.2)
        #选择品牌
        self.h.find_element_by_xpath('//span[@class="ui-icon ui-icon-triangle-1-s"]').click()
        self.wait.until(lambda z:z.find_element_by_id('ui-multiselect-brand_name-option-1').is_displayed())
        self.h.find_element_by_id('ui-multiselect-brand_name-option-1').click()
        #销售主体期数
        self.h.find_element_by_id('selling_action').send_keys('测试销售')
        time.sleep(0.2)
        self.s=self.h.find_elements_by_class_name('ac_results')[-1]
        self.wait.until(lambda z:z.find_elements_by_class_name('ac_results')[-1].find_element_by_class_name('ac_even').is_displayed())
        self.s.find_element_by_class_name('ac_even').click()
        #计划档期选择
        self.wait.until(lambda z:z.find_element_by_id('schedule_date_from').is_displayed())
        time.sleep(2)
        self.h.find_element_by_id('schedule_date_from').click()
        self.wait.until(lambda z:z.find_element_by_link_text('19').is_displayed())
        self.h.find_element_by_link_text('28').click()
        self.h.find_element_by_id('schedule_date_to').click()
        self.wait.until(lambda z: z.find_element_by_link_text('30').is_displayed())
        self.h.find_element_by_link_text('30').click()
        #所属部类 department_id
        self.h.find_element_by_id('department').click()
        self.wait.until(lambda z:z.find_element_by_xpath('//select[@id="department"]/option[@value="2"]').is_displayed())
        self.h.find_element_by_xpath('//select[@id="department"]/option[@value="2"]').click()
        self.h.find_element_by_id('department_id').click()
        self.wait.until(lambda z: z.find_element_by_xpath('//select[@id="department_id"]/option[@value]').is_displayed())
        self.h.find_elements_by_xpath('//select[@id="department_id"]/option[@value]')[2].click()
        #供应商选择
        #self.h.find_element_by_id('vendor_name').send_keys(u'五二二供应商')
        #self.h.find_element_by_xpath('//div[@class="ac_results"]/ul/li[@class="ac_even"]/strong').click()
        #self.h.find_element_by_xpath('//div[@class="ac_results"]/ul/li[@class="ac_even"]/strong').click()
        #样品预计到货日期
        self.h.find_element_by_id('sample_need_date').click()
        self.h.find_element_by_class_name('cui_today').find_element_by_xpath('./a').click()
        #大货预计到货日期
        self.h.find_element_by_id('goods_need_date').click()
        self.h.find_element_by_class_name('cui_today').find_element_by_xpath('./a').click()
        #选择是否常态
        self.h.find_element_by_id('is_normalization').click()
        self.wait.until(lambda z:z.find_element_by_id('shop_id').is_displayed())
        time.sleep(1)
        self.wait.until(lambda z:z.find_element_by_id('shop_id').is_enabled())
        self.cli_cho(['shop_id',self.changtai])
        #设置售卖时间
        self.h.find_element_by_id('real_selling_date_from').click()
        self.h.find_element_by_xpath('//td[@class="cui_today"]/following-sibling::*[1]').click()
        self.h.find_element_by_id('real_selling_date_to').click()
        self.h.find_element_by_partial_link_text('30').click()
        #self.h.find_element_by_xpath('//td[@class="cui_today"]/following-sibling::*[2]').click()
        #选择分仓
        self.h.find_element_by_id('area_gz_check').click()
        self.wait.until(lambda z:z.find_element_by_id('goods_gz_total_count').is_enabled())
        self.h.find_element_by_id('goods_gz_total_count').send_keys('1')
        self.h.find_element_by_id('goods_gz_count').send_keys('1')
        self.h.find_element_by_id('expect_gz_sell_rate').send_keys('1')
        self.h.find_element_by_id('expect_gz_discount_from').send_keys('1')
        self.h.find_element_by_id('expect_gz_discount_to').send_keys('2')
        self.h.find_element_by_id('discount_gz_amount_total').send_keys('23')
        #售卖网站
        self.s=self.h.find_element_by_id('supplier_for')
        self.s.click()
        self.s.find_elements_by_tag_name('option')[1].click()
        #商品种类
        self.h.find_element_by_id('cate_name_gather').click()
        self.wait.until(lambda z:z.find_element_by_id('cate_10102').is_displayed())
        self.h.find_element_by_id('cate_10102').click()
        ActionChains(self.h).move_to_element(self.h.find_element_by_id('bind_vendor_submit'))
        self.h.find_element_by_id('bind_vendor_submit').click()
        #综合品牌等级
        self.s=self.h.find_element_by_id('brand_multiple_level')
        self.s.click()
        self.s.find_elements_by_tag_name('option')[1].click()
        #版面归属
        self.s=self.h.find_element_by_id('page_type')
        self.s.click()
        self.s.find_elements_by_tag_name('option')[1].click()
        #x选择是否保底
        self.cli_cho(['break_even_flag','是'])
        #设置新导航
        self.h.find_element_by_id('clothesProduct').click()
        self.cli_cho(['clothesProductSel','女装'])
        #售卖平台
        ActionChains(self.h).move_to_element(self.h.find_element_by_id('last_gross_profit_rate_gz'))
        self.h.find_element_by_id('sale_platform1').click()
        #人群标记
        self.h.find_element_by_id('potential_usergroup11043').click()
        #填写毛利率
        if len(self.maolilv)>=2:
          self.h.find_element_by_id('gross_profit_rate').send_keys(self.maolilv[0])
          self.h.find_element_by_id('gross_profit_rate_end').find_element_by_tag_name('input').send_keys(self.maolilv[1])
        #填写供货价
        if len(self.maolilv)==1:
          self.h.find_element_by_id('supply_price').send_keys(self.maolilv[0])
        #采购方式
        self.cli_cho(['purchase_type','虚拟发货'])
        #采购方式
        self.cli_cho(['purchase_type','虚拟补货'])
        #抽样状况
        self.cli_cho(['sample_type', '提供图片'])
        #押金比例
        self.h.find_element_by_id('mortgage_rate').send_keys('1')
        self.h.find_element_by_id('caution_money').send_keys('2')
        #折后价格带
        self.h.find_element_by_id('discount_price_from').send_keys('100')
        self.h.find_element_by_id('discount_price_to').send_keys('200')
        #结算方式
        ActionChains(self.h). move_to_element(self.h.find_element_by_id('account_type'))
        self.cli_cho(['account_type','M1'])
        #销售金额比
        ActionChains(self.h).move_to_element(self.h.find_element_by_id('save_submit')).perform()
        self.h.find_element_by_id('sales_num_per_gz').send_keys('10')
        self.h.find_element_by_id('return_num_rate_gz').send_keys('20')
        #毛利率
        self.h.find_element_by_id('last_gross_profit_rate_gz').send_keys('10')
        self.h.find_element_by_id('po_return_num_first_rate_gz').send_keys('20')
        #折扣占比
        self.h.execute_script('scrollTo(0,3000)')
        time.sleep(2)
        self.s=self.h.find_elements_by_xpath('//input[contains(@id,"discount_rate")]')
        #self.s[-1].send_keys('10')
        for i in self.s[:-1]:
            i.send_keys('10')
        self.s[-1].send_keys('20')
        #填写上期销售额
        self.h.find_element_by_id('sales_amount_gz').send_keys('100')
        #保存并提交
        self.h.find_element_by_id('save_submit').click()
        time.sleep(1)
        self.h.switch_to_alert().accept()
        while True:
          try:
            time.sleep(1)
            self.h.switch_to_alert().accept()
          except:
              pass
          else:
              break
        self.shen_he()
        #跑脚本
        time.sleep(0.5)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/sync_to_ps_price_system.php?debug')
        time.sleep(0.5)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/ps.php?data={"timestamp":"1461513600","call_from":"PS","token":"53b0df90d5997a86bc70371807fe330e","service":"vip.scm.priceChangeApply.psAuditFeedback","productLlistId":"111","productListType":"VIS_PL","flowStatus":1," bandFlag":0}')

        time.sleep(0.5)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/get_result_from_ps.php?service=vip.scm.priceChangeApply.retrievePricingList')
        time.sleep(0.5)
        self.h.get('http://vis.api.vip.com:8000/priceChangeApply/get_result_from_ps.php?service=vip.scm.priceChangeApply.rewritePricingResultToApply')

        #返回档期id
        return self.dangqi_id
    def shen_he(self):
        self.h.switch_to_default_content()
        time.sleep(0.5)
        self.wait.until(lambda z: z.find_element_by_partial_link_text('部门审批列表').is_enabled())
        time.sleep(1)
        self.dengdai(self.h.find_element_by_partial_link_text('部门审批列表'))
        #self.h.find_element_by_partial_link_text(u'部门审批列表').click()
        self.h.switch_to_frame(self.h.find_element_by_name('biw-ajax'))
        self.wait.until(lambda z: z.find_element_by_name('select_box').is_enabled())
        self.h.find_elements_by_name('select_box')[0].click()
        self.h.find_element_by_id('all_batch_pass_button').click()
        time.sleep(0.5)
        self.h.switch_to_alert().accept()
        time.sleep(0.5)
        u=self.h.switch_to_alert()
        if '成功' in u.text:
            u.accept()
        else:
            assert '审批不通过'=='1'
        self.h.switch_to_default_content()
        time.sleep(0.5)
        self.wait.until(lambda z:z.find_element_by_partial_link_text('VP审批列表').is_enabled())
        self.dengdai(self.h.find_element_by_partial_link_text('VP审批列表'))
        #self.h.find_element_by_partial_link_text(u'VP审批列表').click()
        self.h.switch_to_frame(self.h.find_element_by_name('biw-ajax'))
        self.wait.until(lambda z: z.find_element_by_name('select_box').is_enabled())
        time.sleep(1)
        self.dangqi_id=self.h.find_element_by_xpath('//td[@col-num="data_col_1"]').text
        self.h.find_elements_by_name('select_box')[0].click()
        self.h.find_element_by_id('all_batch_pass_button').click()
        time.sleep(0.5)
        self.h.switch_to_alert().accept()
        time.sleep(0.5)
        u=self.h.switch_to_alert()
        if '成功' in u.text:
            u.accept()
            time.sleep(1)
            try:
                self.h.switch_to_alert().accept()
            except:
                pass
        else:
            assert '审批不通过'=='1'
        # 返回档期id

    #选择下拉列表，并根据值选择点击那一个
    def cli_cho(self,z):
        self.wait.until(lambda x:x.find_element_by_id(z[0]).is_displayed())
        time.sleep(1)
        self.h.find_element_by_id(z[0]).click()
        #self.wait.until(lambda  x:x.find_element_by_id(z[0]).find_element_by_tag_name('option').is_dispalyed())
        while True:
            try:
                self.h.find_element_by_id(z[0]).find_elements_by_tag_name('option')
            except:
                time.sleep(0.1)
            else:
                break
        for i in self.h.find_element_by_id(z[0]).find_elements_by_tag_name('option'):
            if z[1] in i.text:
                ActionChains(self.h).move_to_element(i)
                i.click()
                break
    def dengdai(self,click):
        while True:
          self.num=0
          try:
            self.num+=1
            time.sleep(1)
            click.click()
          except:
              if self.num==10:
                  break
              else:
                 pass
          else:
              break

if __name__=='__main__':
    h=webdriver.Chrome()
    k=creat_dang(h,'10353090',['100'])
    k.creat()







