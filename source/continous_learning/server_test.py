import unittest
from concurrent import futures

import grpc

import continous_learning_pb2 #pylint: disable=import-error
import continous_learning_pb2_grpc #pylint: disable=import-error

from server import ContinousLearningServicer

class ContinousLearningServicerTestCase(unittest.TestCase):

    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        continous_learning_pb2_grpc.add_ContinousLearningServicer_to_server(
            ContinousLearningServicer(), self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()

    def tearDown(self):
        self.server.stop(0)

    def test(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = continous_learning_pb2_grpc.ContinousLearningStub(channel)
            stub.SetLabelName(continous_learning_pb2.LabelName())
            stub.DeleteTrainImage(continous_learning_pb2.Image())
            stub.DeleteEvaluateImage(continous_learning_pb2.Image())
            stub.Evaluate(continous_learning_pb2.Empty())
            stub.Predict(continous_learning_pb2.Image())

    def test_put_train_image_and_get_unknown_image(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = continous_learning_pb2_grpc.ContinousLearningStub(channel)
            stub.PutTrainImage(continous_learning_pb2.Image(path='test'))
            image = next(stub.GetUnknownTrainImage(continous_learning_pb2.Filter()))
            self.assertEqual(image.path, 'test')

    def test_put_train_image_and_label(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = continous_learning_pb2_grpc.ContinousLearningStub(channel)
            stub.PutTrainImage(
                continous_learning_pb2.Image(
                    id=continous_learning_pb2.ID(bytes=b'123'),
                    path='test',
            ))
            stub.SetTrainLabel(
                continous_learning_pb2.Label(
                    id=continous_learning_pb2.ID(bytes=b'123'),
                    label=2,
            ))
            image = stub.GetTrainImage(continous_learning_pb2.ID(bytes=b'123'))
            label = stub.GetTrainLabel(continous_learning_pb2.ID(bytes=b'123'))
            self.assertEqual(image.id.bytes, b'123')
            self.assertEqual(image.path, 'test')
            self.assertEqual(label.id.bytes, b'123')
            self.assertEqual(label.label, 2)

    def test_put_evaluate_image_and_get_unknown_image(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = continous_learning_pb2_grpc.ContinousLearningStub(channel)
            stub.PutEvaluateImage(continous_learning_pb2.Image(path='test'))
            image = next(stub.GetUnknownEvaluateImage(continous_learning_pb2.Filter()))
            self.assertEqual(image.path, 'test')

    def test_put_evaluate_image_and_label(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = continous_learning_pb2_grpc.ContinousLearningStub(channel)
            stub.PutEvaluateImage(
                continous_learning_pb2.Image(
                    id=continous_learning_pb2.ID(bytes=b'123'),
                    path='test',
            ))
            stub.SetEvaluateLabel(
                continous_learning_pb2.Label(
                    id=continous_learning_pb2.ID(bytes=b'123'),
                    label=2,
            ))
            image = stub.GetEvaluateImage(continous_learning_pb2.ID(bytes=b'123'))
            label = stub.GetEvaluateLabel(continous_learning_pb2.ID(bytes=b'123'))
            self.assertEqual(image.id.bytes, b'123')
            self.assertEqual(image.path, 'test')
            self.assertEqual(label.id.bytes, b'123')
            self.assertEqual(label.label, 2)

if __name__ == '__main__':
    unittest.main()
