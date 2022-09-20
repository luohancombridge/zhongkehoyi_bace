# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
# -*- coding: utf-8 -*-
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket

import os
import json
import urllib.request, urllib.error, urllib.parse
import re
import  chardet

import time

import sqlite3

from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
def check_login():
    ip=request.headers.get('X-Real-IP')
    db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
    cu = db.cursor()
    login_check = cu.execute('select time from user where  ip="%s" ' % ip).fetchall()
    db.close()
    if len(login_check)==0 :
        return render_template('/hualala/login.html')

