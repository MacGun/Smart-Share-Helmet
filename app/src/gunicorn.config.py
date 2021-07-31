import multiprocessing
import logging.config

DIR='/home/park/Smart-Share-Helmet/app/'
workers=multiprocessing.cpu_count() //2 
bind="0.0.0.0:5000"
accesslog="-"
access_log_format='%(t)s %(p)s %(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" “%(a)s”'
pidfile=DIR+"pid/park_app.pid"
chdir=DIR+"webpage"


