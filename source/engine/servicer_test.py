import unittest
from concurrent import futures
import uuid
import time

import grpc

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error

from servicer import EngineServicer
from engine import Engine

class EngineServicerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        engine_pb2_grpc.add_EngineServicer_to_server(
            EngineServicer(), self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()

        self.engine = Engine()
        self.engine.start()

    def tearDown(self):
        self.server.stop(0)
        self.engine.stop()

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

    def test_train_label(self):
        id_ = engine_pb2.ID(bytes=uuid.uuid4().bytes)
        label = engine_pb2.Label(id=id_)
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            self.assertEqual(stub.GetTrainLabel(id_), engine_pb2.Label())
            self.assertEqual(stub.PutTrainLabel(label), id_)
            self.assertEqual(stub.GetTrainLabel(id_), label)
            id_ = stub.PutTrainLabel(engine_pb2.Label())
            self.assertNotEqual(id_, engine_pb2.ID())
            self.assertEqual(stub.GetTrainLabel(id_), engine_pb2.Label(id=id_))

    def test_train_logits(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            stub.GetTrainLogits(engine_pb2.ID())

    def test_engine(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            id_ = stub.PutTrainImage(engine_pb2.Image(path='/mnt/VOC2006/train/PNGImages/000004.png'))
            stub.PutTrainLabel(engine_pb2.Label(id=id_, one_hot_label=[0]*1000))
            id_ = stub.PutTrainImage(engine_pb2.Image(path='/mnt/VOC2006/train/PNGImages/000006.png'))
            stub.PutTrainLabel(engine_pb2.Label(id=id_, one_hot_label=[0]*1000))
            id_ = stub.PutTrainImage(engine_pb2.Image(path='/mnt/VOC2006/train/PNGImages/000008.png'))
            stub.PutTrainLabel(engine_pb2.Label(id=id_, one_hot_label=[0]*1000))
            
            time.sleep(3)
        
if __name__ == '__main__':
    unittest.main()
