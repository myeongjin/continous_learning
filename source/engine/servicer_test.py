import unittest
from concurrent import futures

import grpc

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error

from servicer import EngineServicer

class EngineServicerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        engine_pb2_grpc.add_EngineServicer_to_server(
            EngineServicer(), self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()

    def tearDown(self):
        self.server.stop(0)

    def test(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            stub.PutTrainData(engine_pb2.Data())

if __name__ == '__main__':
    unittest.main()
