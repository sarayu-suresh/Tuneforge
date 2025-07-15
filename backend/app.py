# backend/app.py
from flask import Flask, request, jsonify
import os
from train import fine_tune_model
from train import training_status
from inference import generate_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'datasets'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'path': file_path})

@app.route('/train', methods=['POST'])
def train():
    data = request.json
    dataset_path = data['dataset_path']
    base_model = data['base_model']
    output_dir = f"backend/models/{base_model.replace('/', '_')}_finetuned"
    fine_tune_model(dataset_path, base_model, output_dir)
    return jsonify({'message': 'Training started', 'model_path': output_dir})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model_path = data['model_path']
    prompt = data['prompt']
    response = generate_response(prompt, model_path)
    return jsonify({'response': response})


@app.route('/train/status', methods=['GET'])
def get_status():
    return jsonify(training_status)


if __name__ == '__main__':
    app.run(debug=True)
