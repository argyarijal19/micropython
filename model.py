import tflite
import array
import time


def load_model(model_path):
    with open(model_path, 'rb') as tf :
        model_data = tf.read()
        model = tflite.Model.GetRootAsModel(model_data, 0)
    return model

load_model('model_lstm.tflite')