# -*- codmoke_dangbaning: utf-8 -*-
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
import requests
def appium_server(fun):
    def appium_server():
        fun()
        case_url = 'http://'+current_app.config.get('APPIUM_IP')+'/cases'
        response = requests.get(case_url)
        case_json = json.loads(response.text)['cases']
        print((9999999999999999999999999999999))
        print (case_json)
        return render_template('/hualala/jiekou_test/appium_url.html',case_json=case_json)
    return appium_server