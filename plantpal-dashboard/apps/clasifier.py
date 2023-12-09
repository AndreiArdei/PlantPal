import sqlite3

import cv2 as cv
import matplotlib.image as mpimg
import numpy as np
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

from decouple import config


def classify_image(img):
    # Read an image from a file into a numpy array
    img = cv.imread(img)
    # Convert to float32
    img = img.astype(np.float32)
    # Resize to 96x96 (size the model is expecting)
    img = cv.resize(img, (96, 96))
    # Expand img dimensions from (96, 96, 3) to (1, 96, 96, 3) for set_tensor method call
    img = np.expand_dims(img, axis=0)

    tflite_model_file = 'apps/static/model/plant.tflite'

    with open(tflite_model_file, 'rb') as fid:
        tflite_model = fid.read()

    interpreter = tflite.Interpreter(model_content=tflite_model)
    interpreter.allocate_tensors()

    input_index = interpreter.get_input_details()[0]["index"]
    output_index = interpreter.get_output_details()[0]["index"]

    prediction = []
    interpreter.set_tensor(input_index, img)
    interpreter.invoke()
    prediction.append(interpreter.get_tensor(output_index))

    predicted_label = np.argmax(prediction)
    if prediction[0][0][predicted_label] < 0.5 or prediction[0][0][predicted_label] >= 1:
        print('Classifier result - unknown')
        return 'unknown'

    con = sqlite3.connect('identifier.sqlite')
    cur = con.cursor()

    class_names = cur.execute('SELECT Name FROM Plant ORDER BY Name').fetchall()
    print(class_names)
    return class_names[predicted_label]
