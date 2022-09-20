# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
sys.path.append("../../")
import json
import demjson
#-*-coding:utf-8-*-
#将结果json和excel中的result的json做对比
class assert_run(object):
    def __init__(self):
       pass
    #第一个依据第二个为接口输出结果
    def walk_find(self,v,j):
       if type(v)==dict:
            for k,i in list(v.items()):
                if type(i)!=dict and  type(i)!=list:
                     if i=='*':
                        try:
                           assert str(j[k])
                        except:
                            return False
                     else:
                         try:
                             assert i==j[k]
                         except:
                             return False
            for k,i in list(v.items()):
                 if type(i)==dict:
                     self.walk_find(i,j[k])
                 if type(i)==list:
                     for b in i:
                         statu = 0
                         for z in j[k]:
                             for u,a in list(b.items()):
                                 if  type(u)!=list and type(u)!=dict :
                                     if u in list(z.keys()) and  a==z[u]:
                                           pass
                                     else:
                                         statu = 1
                                         break
                             if statu==0:
                                 break
                         self.walk_find(b,z)
       return 1

