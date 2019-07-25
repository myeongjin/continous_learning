import os
import uuid

import redis

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error


class EngineServicer(engine_pb2_grpc.EngineServicer):

    def __init__(self):
        redis_kwargs = {
            'host': os.environ['REDIS_HOST'],
            'port': int(os.environ['REDIS_PORT']) if 'REDIS_PORT' in os.environ else 6379,
        }
        self.train_images = redis.Redis(db=1, **redis_kwargs)
        self.train_labels = redis.Redis(db=2, **redis_kwargs)

    def PutTrainImage(self, image, context):
        if image.id.bytes == b'':
            image.id.bytes = uuid.uuid4().bytes

        self.train_images.set(image.id.bytes, image.SerializeToString())
        return image.id

    def GetTrainImage(self, id_, context):
        image = self.train_images.get(id_.bytes)
        if image == None:
            return engine_pb2.Image()
        
        return engine_pb2.Image.FromString(image)

    def PutTrainLabel(self, label, context):
        if label.id.bytes == b'':
            label.id.bytes = uuid.uuid4().bytes

        self.train_labels.set(label.id.bytes, label.SerializeToString())
        return label.id

    def GetTrainLabel(self, id_, context):
        label = self.train_labels.get(id_.bytes)
        if label == None:
            return engine_pb2.Label()
        
        return engine_pb2.Label.FromString(label)

    def GetTrainLogits(self, id_, context):
        return engine_pb2.Logits()
