import os
import random
import string
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask import Flask,request,jsonify
from rembg import remove
from dotenv import load_dotenv

# loading env variables
load_dotenv()
print(os.environ.get("CLOUD_NAME", "NOPE"))

cloudinary.config( 
    cloud_name = os.environ["CLOUD_NAME"], 
    api_key = os.environ["API_KEY"], 
    api_secret = os.environ["API_SECRET"],
    secure=True
)

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    to_remove = request.form.get('toRemove', 'false').lower() == 'true'
    filename = request.form.get('filename',"").lower()
    if filename == "":
        return jsonify({'error': 'No filename stated'}), 400
    # adding random value to deferentiat uploads
    filename = filename.join(random.choices(string.ascii_letters+ string.digits, k=8))
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        if to_remove:
            image = remove_background(file )
        else:
            image = file
        uploadedStr = upload_image(image, filename)

        return jsonify({'url': uploadedStr}), 200

def remove_background(file):
    img = file.read()
    output = remove(img)
    return output


def upload_image(image, filename ):
    # Upload an image
    upload_result = cloudinary.uploader.upload(image,public_id=filename)
    # print(upload_result["secure_url"])
    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url(filename, fetch_format="auto", quality="auto")
    print("optimized", optimize_url)
    return optimize_url
