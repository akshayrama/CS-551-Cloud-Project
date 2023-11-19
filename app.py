from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

app = Flask(__name__, template_folder='templates', static_folder='static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        image = request.files['image']
        img_bytes = image.read()
        img = Image.open(io.BytesIO(img_bytes))

        return jsonify({'result': 'heeee'})

if __name__ == '__main__':
    app.run(debug=True)