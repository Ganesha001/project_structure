# Gunicorn config variables
loglevel = 'info'
errorlog = '-'  # stderr
accesslog = '-'  # stdout
worker_tmp_dir = '/dev/shm'
bind = '0.0.0.0:5000'
workers = 2
threads = 4
worker_class = 'sync'
timeout = 120  # Increased timeout for potential slow connections
