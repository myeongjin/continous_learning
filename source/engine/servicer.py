import os
import uuid

import redis

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error


class EngineServicer(engine_pb2_grpc.EngineServicer):

    def PutTrainImage(self, request, context):
        return engine_pb2.ID()

    def GetTrainImage(self, request, context):
        return engine_pb2.Image()
