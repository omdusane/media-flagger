from constants import ALLOWED_EXTENSIONS, CLASSES
from flask import url_for
import numpy as np
import keras
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# import tensorflow_text 
import pathlib
# import PIL
import assemblyai as aai
import re
import os
import fileinput

# aai.settings.api_key = "6ea41d6b1c344a54b4ef1a3fb43f8374"

# transcriber = aai.Transcriber()
# transcript = transcriber.transcribe("video.mp4")

def load_model():
    model = keras.models.load_model("." + url_for('static', filename='CNN_10e'))
    return model

def preprocess(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text
    
def output(key, values):
    dictionary = dict(zip(key, values[0]))
    max_key = max(dictionary, key=dictionary.get)
    if dictionary[max_key] >= 0.4:
        return max_key
    else:
        return "Neutral"


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def predict_category(text):
    model = load_model()
    preprocessed_text = preprocess(text)
    
    if model:
        print("model loaded")
    
    
    max_sequence_length = 100

    tokenizer = Tokenizer()
    new_sequences = tokenizer.texts_to_sequences([preprocessed_text])
    new_padded_sequences = pad_sequences(new_sequences, maxlen=max_sequence_length)
    predictions = model.predict(new_padded_sequences)
    print(predictions)
    print(output(CLASSES, predictions))
    return output(CLASSES, predictions) 
    



def allowed_file(filename):
    print(filename.rsplit('.', 1)[1])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def process_txt(file_path):
    with open(f'{file_path}', 'r') as file:
        data = file.read().replace('\n', '')    


    list = []
    for lines in fileinput.input([file_path]):
        lines.strip('\n')
        list.append(lines)
    list = [item for item in list if item.strip() != '']
    list = [item.replace('\n', '') for item in list]
    string = ''.join(list)
    print(string)
    return string


def process_media(file_path):
    aai.settings.api_key = "6ea41d6b1c344a54b4ef1a3fb43f8374"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)

    return transcript.text




