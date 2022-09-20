__author__ = 'SUNZHEN519'

from flask import Flask, render_template
import os
import sys
import platform

# from celery import Celery
# from gevent import monkey
# monkey.patch_all()
# from gevent import pywsgi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app,db
from app.db_sqlchemy_sqlite import *
if __name__ == '__main__':
    db.create_all()
    if platform.system() == 'Linux':
        app.run(host='172.16.1.134', port=5026, debug=True, threaded=True)
    else:
        app.run(host='127.0.0.1', port=5026, debug=True, threaded=True)
    # socketio.run(app, debug=False, host='0.0.0.0', port=5000, threaded=True)    # server = pywsgi.WSGIServer(('127.0.0.1', 5026), app)
    # server.serve_forever()
    # monkey.patch_all()
    # WSGIServer(('0.0.0.0', 5026), app).serve_forever()
