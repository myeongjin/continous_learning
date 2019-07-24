import os
import uuid

import redis

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error


class EngineServicer(engine_pb2_grpc.EngineServicer):

    def __init__(self):
        self.db = dict()

    def PutTrainImage(self, image, context):
        if image.id.bytes == b'':
            image.id.bytes = uuid.uuid4().bytes

        self.db[image.id.bytes] = image
        return image.id

    def GetTrainImage(self, id_, context):
        if id_.bytes not in self.db:
            return engine_pb2.Image()
        
        return self.db[id_.bytes]
