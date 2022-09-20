# config.py

import gevent.monkey
import multiprocessing

gevent.monkey.patch_all()

# 监听本机的5000端口
bind = '0.0.0.0:5026'
preload_app = True #开启进程#workers=4workers = multiprocessing.cpu_count() * 2 + 1 #每个进程的开启线程threads = multiprocessing.cpu_count() * 2 backlog=2048 #工作模式为geventworker_class="gevent" # debug=True #如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题daemon = True #进程名称proc_name='gunicorn.pid' #进程pid记录文件pidfile='app_pid.log' loglevel='debug'logfile = 'debug.log'accesslog = 'access.log'access_log_format = '%(h)s %(t)s %(U)s %(q)s'errorlog = 'error.log’

workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2

backlog = 2048

worker_class="gevent"
daemon = True
proc_name = 'gunicorn.pid'

# 进程pid记录文件
pidfile = 'app_pid.log'
loglevel='debug'
logfile = 'debug.log'
accesslog = 'access.log'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
errorlog = 'error.log'