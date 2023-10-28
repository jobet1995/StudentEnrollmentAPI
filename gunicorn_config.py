bind = "0.0.0.0:5000"
workers = 4

accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

errorlog = "error.log"

proc_name = "myapp"

worker_class = "sync"

threads = 2
