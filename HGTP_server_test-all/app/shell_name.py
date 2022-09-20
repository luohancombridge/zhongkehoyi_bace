# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import os
from flask import Flask, render_template, session
class file(object):
    def __init__(self,*mulu):

        if  len(mulu)==0:
            self.cd =r'D:\efq_ben'
        else:
            self.cd='D:\\'+mulu[0]+'\\'
    def xx(self):
        files=[]
        for parent,dirnames,filenames in os.walk(self.cd):
            for i in filenames:
                if '.py' in i and '.pyc' not in i and 'mulu44' not in i:
                    files.append(i)
                #files.append(i)
        return files



