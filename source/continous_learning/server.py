import os
import uuid

import redis

import continous_learning_pb2 #pylint: disable=import-error
import continous_learning_pb2_grpc #pylint: disable=import-error


train_image_conn = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=1)
train_label_conn = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=2)
evaluate_image_conn = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=3)
evaluate_label_conn = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=4)

def put_image(conn, image):
    if image.id.bytes == b'':
        image.id.bytes = uuid.uuid4().bytes

    conn.set(image.id.bytes, image.SerializeToString())
    return continous_learning_pb2.Empty()

def get_image(conn, id_):
    image = continous_learning_pb2.Image.FromString(conn.get(id_.bytes))
    return image

def get_unknown_image(conn, filter_):
    for key in conn.scan_iter():
        yield continous_learning_pb2.Image.FromString(conn.get(key))

def set_label(conn, label):
    conn.set(label.id.bytes, label.SerializeToString())
    return continous_learning_pb2.Empty()

def get_label(conn, id_):
    label = continous_learning_pb2.Label.FromString(conn.get(id_.bytes))
    return label

class ContinousLearningServicer(continous_learning_pb2_grpc.ContinousLearningServicer):

    def SetLabelName(self, request, context):
        return continous_learning_pb2.Empty()

    def PutTrainImage(self, request, context):
        return put_image(train_image_conn, request)

    def GetTrainImage(self, request, context):
        return get_image(train_image_conn, request)

    def DeleteTrainImage(self, request, context):
        return continous_learning_pb2.Empty()

    def GetUnknownTrainImage(self, request, context):
        return get_unknown_image(train_image_conn, request)

    def SetTrainLabel(self, request, context):
        return set_label(train_label_conn, request)

    def GetTrainLabel(self, request, context):
        return get_label(train_label_conn, request)

    def PutEvaluateImage(self, request, context):
        return put_image(evaluate_image_conn, request)

    def GetEvaluateImage(self, request, context):
        return get_image(evaluate_image_conn, request)

    def DeleteEvaluateImage(self, request, context):
        return continous_learning_pb2.Empty()

    def GetUnknownEvaluateImage(self, request, context):
        return get_unknown_image(evaluate_image_conn, request)

    def SetEvaluateLabel(self, request, context):
        return set_label(evaluate_label_conn, request)

    def GetEvaluateLabel(self, request, context):
        return get_label(evaluate_label_conn, request)

    def Evaluate(self, request, context):
        return continous_learning_pb2.Evaluation()

    def Predict(self, request, context):
        return continous_learning_pb2.Prediction()
