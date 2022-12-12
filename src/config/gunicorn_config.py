command = '/home/admin/app/eccosy/eccosy_env/bin/gunicorn'
pythonpath = '/home/admin/app/eccosy/src'
bind = 'eccosy.webtm.ru:8000'
workers = 3

loglevel = 'debug'
accesslog = '/home/admin/app/eccosy/log/gunicorn.access.log'
errorlog =  '/home/admin/app/eccosy/log/gunicorn.error.log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
