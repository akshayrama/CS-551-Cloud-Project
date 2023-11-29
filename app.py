from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
from torchvision import models, transforms
import torch.nn
from torch import max, unsqueeze
import os

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' in request.files:
        image_file = request.files['image']
        img_bytes = image_file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # Loading the model and stuff

        model = models.alexnet(weights=models.AlexNet_Weights.IMAGENET1K_V1)
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )])

        img_t = transform(img)
        batch_t = unsqueeze(img_t, 0)
        out = model(batch_t)

        with open('imagenet_classes.txt') as f:
            classes = [line.strip() for line in f.readlines()]

        _, index = max(out, 1)

        x = classes[index[0]].split(',')[1].strip().replace('_', ' ').title()

        return jsonify({'result': x})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host='0.0.0.0', port=port)
