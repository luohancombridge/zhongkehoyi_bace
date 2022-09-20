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
def upload_fil(func):
    func()
    def upload_fil():
      db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
      cu = db.cursor()
      if request.method == 'POST':
        file = request.files['files']
        filename = secure_filename(file.filename)
        file_path=os.path.join(current_app.config.get('LOCUST_FILE'),str(int(time.time())))
        os.makedirs(file_path)
        cu.executemany('INSERT INTO locust_file VALUES (?,?,?,?,null,?,?)',[(file_path, '', str(time.time()),'','',filename)])
        db.commit()
        id = cu.execute('select id from locust_file order by id desc limit 0,1').fetchall()[0][0]
        session['locust_update_file_id']=id
        db.close()
        try:
         file.save(os.path.join(file_path, filename))
        except:
            pass
        return redirect(url_for('second'))
    return upload_fil

def upload_fil_beizu(func):
    func()
    def upload_fil_beizu():
          db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
          cu = db.cursor()
          name = cu.execute(
              'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
          if len(name) == 0:
              return redirect(url_for('login_new'))
          else:
              name = name[0][0]
          if len(cu.execute('select id from locust_file order by id desc limit 0,1').fetchall())==0:
              id=0
              while len(cu.execute('select id from locust_file order by id desc limit 0,1').fetchall())==0:
                 pass
          else:
              id = cu.execute('select id from locust_file order by id desc limit 0,1').fetchall()[0][0]
          while id==cu.execute('select id from locust_file order by id desc limit 0,1').fetchall()[0][0]:
              pass
          id=cu.execute('select id from locust_file order by id desc limit 0,1').fetchall()[0][0]
          cu.execute('update  locust_file  set beizhu="%s", user="%s" where id=%s' %(request.args.get('beizu'),name,str(id)) )
          db.commit()
          db.close()
          return jsonify(data='success')
    return upload_fil_beizu