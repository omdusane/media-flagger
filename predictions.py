# import fileinput

# list = []
# for lines in fileinput.input(['sample.txt']):
#     lines.strip('\n')
#     list.append(lines)

# list = [item for item in list if item.strip() != '']
# list = [item.replace('\n', '') for item in list]
# str = ''.join(list)
# print(str)
import keras
import pickle
from tensorflow.keras.preprocessing import text, sequence


from flask import url_for


def load_model(input):
    model = keras.models.load_model("." + url_for('static', filename='multi_label_model.h5'))
    print("model loaded")
    try:
        with open("." + url_for('static', filename='multilabel_tokenizer.pickle'), 'rb') as handle:
            tokenizer = pickle.load(handle)
            print("loaded tokanizer")

            # input_text = "im going on a vacation"

            # Tokenize the input text
            text_sequence = tokenizer.texts_to_sequences([input])
            # Pad sequences

            max_text_length=400
            text_sequence_padded = sequence.pad_sequences(text_sequence, maxlen=max_text_length)
            # Make prediction
            prediction = model.predict(text_sequence_padded)
            # Convert probabilities to binary labels based on threshold (default is 0.5)
            threshold = 0.5
            toxicity_labels = (prediction > threshold).astype(int)

            key = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
            dictionary = dict(zip(key, toxicity_labels[0]))
            max_key = max(dictionary, key=dictionary.get)
            result_keys=[]
            for k, v in dictionary.items():
                if v == 1:
                    result_keys.append(k)
            if len(result_keys) ==0:
                result_keys.append("Neutral")
            return result_keys
    except FileNotFoundError:
        print("Tokenizer file not found. Please ensure the file exists in the specified location.")
    except (pickle.PickleError, EOFError) as e:
        print("Error loading tokenizer:", e)
    return model



print("hello")

# load_model()