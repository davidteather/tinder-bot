from tinder import Tinder

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import logging
import time
import json
import requests
import datetime
from random import random
import person_detector
import tensorflow as tf

import numpy as np

class Classifier():
    def __init__(self, graph, labels):

        self._graph = self.load_graph(graph)
        self._labels = self.load_labels(labels)

        self._input_operation = self._graph.get_operation_by_name("import/Placeholder")
        self._output_operation = self._graph.get_operation_by_name("import/final_result")

        self._session = tf.Session(graph=self._graph)

    def classify(self, file_name):
        t = self.read_tensor_from_image_file(file_name)

        # Open up a new tensorflow session and run it on the input
        results = self._session.run(self._output_operation.outputs[0], {self._input_operation.outputs[0]: t})
        results = np.squeeze(results)

        # Sort the output predictions by prediction accuracy
        top_k = results.argsort()[-5:][::-1]

        result = {}
        for i in top_k:
            result[self._labels[i]] = results[i]

        # Return sorted result tuples
        return result

    def close(self):
        self._session.close()


    @staticmethod
    def load_graph(model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()
        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)
        return graph

    @staticmethod
    def load_labels(label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    @staticmethod
    def read_tensor_from_image_file(file_name,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
        input_name = "file_reader"
        file_reader = tf.read_file(file_name, input_name)
        image_reader = tf.image.decode_jpeg(
            file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)
        return result

def predict_likeliness(classifier, sess, p, default_graph):
    ratings = []
    images = p['images']
    for image in images:
        req = requests.get(image)
        tmp_filename = f"images/tmp/run.jpg"
        if req.status_code == 200:
            with open(tmp_filename, "wb") as f:
                f.write(req.content)

        #multiprocessing.Process(target=person_detector.get_person, args(tmp_filename, sess))
        img = person_detector.get_person(tmp_filename, sess, default_graph)
        if img:
            img = img.convert('L')
            img.save(tmp_filename, "jpeg")
            certainty = classifier.classify(tmp_filename)
            pos = certainty["positive"]
            ratings.append(pos)
    ratings.sort(reverse=True)
    ratings = ratings[:5]
    if len(ratings) == 0:
        return 0.001

    try:
        return ratings[0]*0.6 + sum(ratings[1:])/len(ratings[1:])*0.4
    except ZeroDivisionError:
        return ratings[0]*0.6

t = Tinder()
t.login_google(os.environ['google_username'], os.environ['google_password'])

time.sleep(1)

t.slide_current()
time.sleep(2)


index_error = 0
detection_graph = person_detector.open_graph()
with detection_graph.as_default():
    logging.DEBUG
    with tf.Session() as sess:
        classifier = Classifier(graph="tf/training_output/retrained_graph.pb",
                                labels="tf/training_output/retrained_labels.txt")
            
        pos_schools = ["University of Wisconsin-Madison"]

        graph = tf.get_default_graph()
        for x in range(500):
            profile = t.extract_current()
            score = predict_likeliness(classifier, sess, profile, graph)

            if profile['school'] in pos_schools:
                score *= 1.2
            
            print(f"SCORE: {score}")
            if score > 0.75:
                t.like()
                print("LIKE")
            else:
                t.dislike()
                print("DISLIKE")


            index_error = 0

        classifier.close()