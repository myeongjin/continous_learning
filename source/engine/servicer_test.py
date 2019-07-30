import os
import unittest
import uuid

import grpc

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error


SERVICER_HOST = os.environ['SERVICER_HOST']
SERVICER_PORT = int(os.environ['SERVICER_PORT'])

def connect_channel():
    return grpc.insecure_channel('{}:{}'.format(SERVICER_HOST, SERVICER_PORT))

class unit_test(unittest.TestCase):

    def test_train_image(self):
        id_ = engine_pb2.ID(bytes=uuid.uuid4().bytes)
        image = engine_pb2.Image(id=id_)
        with connect_channel() as channel:
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
        with connect_channel() as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            self.assertEqual(stub.GetTrainLabel(id_), engine_pb2.Label())
            self.assertEqual(stub.PutTrainLabel(label), id_)
            self.assertEqual(stub.GetTrainLabel(id_), label)
            id_ = stub.PutTrainLabel(engine_pb2.Label())
            self.assertNotEqual(id_, engine_pb2.ID())
            self.assertEqual(stub.GetTrainLabel(id_), engine_pb2.Label(id=id_))

    def test_train_logits(self):
        with connect_channel() as channel:
            stub = engine_pb2_grpc.EngineStub(channel)
            stub.GetTrainLogits(engine_pb2.ID())

if __name__ == '__main__':
    unittest.main()
