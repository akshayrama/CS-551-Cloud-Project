from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
from keras.preprocessing import image
from keras.applications.xception import preprocess_input, decode_predictions
from keras.applications.xception import Xception
import numpy as np


app = Flask(__name__, template_folder='templates', static_folder='static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        image_file = request.files['image']
        img_bytes = image_file.read()
        img = Image.open(io.BytesIO(img_bytes))

        img = img.resize((299,299))

        # Loading the model and stuff

        model = Xception(include_top=True)
        model.load_weights("models/xception_weights_tf_dim_ordering_tf_kernels.h5")

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)

        label = decode_predictions(features, top=1)

        label = label[0][0][1]
        label = label.replace('_', ' ')

        return jsonify({'result': label.title()})

if __name__ == '__main__':
    app.run(debug=True)