import os


HOST = os.environ['REDIS_HOST'],
PORT = int(os.environ['REDIS_PORT']) if 'REDIS_PORT' in os.environ else 6379
