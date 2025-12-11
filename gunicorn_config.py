"""Configuration Gunicorn pour production"""

import multiprocessing

# Bind
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# Logging
accesslog = "/var/log/gunicorn/kb_basedoc_access.log"
errorlog = "/var/log/gunicorn/kb_basedoc_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "kb_basedoc"

# Daemon mode (False pour systemd)
daemon = False

# PID file
pidfile = "/var/run/gunicorn/kb_basedoc.pid"

# Server mechanics
preload_app = True
reload = False

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
