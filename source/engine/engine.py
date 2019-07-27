import os
import threading

import redis

import engine_pb2 # pylint: disable=import-error


class Engine:

    def __init__(self):
        self.should_continue = False
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        redis_kwargs = {
            'host': os.environ['REDIS_HOST'],
            'port': int(os.environ['REDIS_PORT']) if 'REDIS_PORT' in os.environ else 6379,
        }
        train_images = redis.Redis(db=1, **redis_kwargs)
        train_labels = redis.Redis(db=2, **redis_kwargs)

        while self.should_continue:
            for id_ in train_images.scan()[1]:
                label = train_labels.get(id_)
                if label == None:
                    continue

                image = train_images.get(id_)
                image = engine_pb2.Image.FromString(image)
                label = engine_pb2.Label.FromString(label)

                import time
                print(image)
                print(label)

    def start(self):
        self.should_continue = True
        self.thread.start()

    def stop(self):
        self.should_continue = False
        self.thread.join()
