import multiprocessing
DIR='/home/park/Smart-Share-Helmet/app/'
workers=multiprocessing.cpu_count() //2 
bind="0.0.0.0:5000"
accesslog="-"
pidfile=DIR+"pid/park_app.pid"
chdir=DIR+"webpage"
