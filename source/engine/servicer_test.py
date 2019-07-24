import unittest
from concurrent import futures
import uuid

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

    def test_train_image(self):
        id_ = engine_pb2.ID(bytes=uuid.uuid4().bytes)
        image = engine_pb2.Image(id=id_)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            self.assertEqual(stub.GetTrainImage(id_), engine_pb2.Image())
            self.assertEqual(stub.PutTrainImage(image), id_)
            self.assertEqual(stub.GetTrainImage(id_), image)
            id_ = stub.PutTrainImage(engine_pb2.Image())
            self.assertNotEqual(id_, engine_pb2.ID())
            self.assertEqual(stub.GetTrainImage(id_), engine_pb2.Image(id=id_))

if __name__ == '__main__':
    unittest.main()
