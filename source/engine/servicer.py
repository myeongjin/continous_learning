import uuid

import redis

import engine_pb2 #pylint: disable=import-error
import engine_pb2_grpc #pylint: disable=import-error


class EngineServicer(engine_pb2_grpc.EngineServicer):

    def __init__(self, host, port):
        self.train_images = redis.Redis(db=1, host=host, port=port)
        self.train_labels = redis.Redis(db=2, host=host, port=port)

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

if __name__ == '__main__':
    from concurrent import futures

    import grpc

    from utils import mainloop, REDIS_HOST, REDIS_PORT # pylint: disable=no-name-in-module

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    engine_pb2_grpc.add_EngineServicer_to_server(
        EngineServicer(REDIS_HOST, REDIS_PORT), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    mainloop()

    server.stop(0)
