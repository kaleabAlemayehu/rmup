from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    to_remove = request.form.get('toRemove', 'false').lower() == 'true'

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # TODO: change to upload to cloudinary
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        file.save(filepath)

        if to_remove:
            processed_path = remove_background(filepath)
        else:
            processed_path = filepath

        file_url = f"http://localhost:5000/{processed_path}"

        return jsonify({'url': file_url}), 200

def remove_background(filepath):

    # TODO: change to rembg but
    # For now, i’ll just rename it to simulate processing
    new_path = filepath.replace('.', '_nobg.')
    os.rename(filepath, new_path)
    return new_path

