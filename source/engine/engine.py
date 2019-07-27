import os
import threading

import redis
import skimage
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow import backend as K # pylint: disable=no-name-in-module

import engine_pb2 # pylint: disable=import-error


class Engine:

    def __init__(self, batch_size=8, steps=100):
        self.batch_size = batch_size
        self.steps = steps
        self.should_continue = False
        self.thread = threading.Thread(target=self.run, daemon=True)

    def generator(self):
        redis_kwargs = {
            'host': os.environ['REDIS_HOST'],
            'port': int(os.environ['REDIS_PORT']) if 'REDIS_PORT' in os.environ else 6379,
        }
        train_images = redis.Redis(db=1, **redis_kwargs)
        train_labels = redis.Redis(db=2, **redis_kwargs)

        while True:
            for id_ in train_images.scan()[1]:
                label = train_labels.get(id_)
                if label == None:
                    continue

                image = train_images.get(id_)
                image = engine_pb2.Image.FromString(image)
                image = skimage.io.imread(image.path)
                image = np.float32(image / 255.)
                image = skimage.transform.resize(image, (299, 299))

                label = engine_pb2.Label.FromString(label)
                label = label.one_hot_label

                yield image, label

    def model_fn(self, feature, labels, mode, params):
        base_model = keras.applications.Xception(
            include_top=True,
            weights='imagenet',
            input_tensor=None,
            input_shape=None,
            pooling=None,
            classes=1000,
        )
        for layer in base_model.layers:
            layer.trainable = False

        nets = base_model(feature)
        logits = K.sigmoid(nets)
        loss = keras.losses.binary_crossentropy(labels, logits)

        assert mode == tf.estimator.ModeKey.TRAIN # pylint: disable=no-member
        optimizer = tf.train.AdamOptimizer()
        train_op = optimizer.minimize(loss, tf.train.get_or_create_global_step())
        return tf.estimator.EstimatorSpec( # pylint: disable=no-member
            mode=mode,
            loss=loss,
            train_op=train_op,
        )

    def dataset_fn(self):
        dataset = tf.data.Dataset.from_generator(
            self.generator,
            output_types=(tf.float32, tf.int32),
            output_shapes=([299, 299, 3], [1000]),
        )
        dataset = dataset.batch(self.batch_size)
        return dataset

    def run(self):
        with tf.Graph().as_default(): # pylint: disable=not-context-manager
            estimator = tf.estimator.Estimator( # pylint: disable=no-member
                model_fn=self.model_fn,
            )
            while self.should_continue:
                print('start')
                estimator.train(
                    input_fn=self.dataset_fn,
                    steps=self.steps,
                )
                print('end')

    def start(self):
        self.should_continue = True
        self.thread.start()

    def stop(self):
        self.should_continue = False
        self.thread.join()
