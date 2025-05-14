from flask import Flask,request

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    return request.data 
    # if request.method == 'POST':
    #     if "file" in request.files:
    #         return "No file"
    #     f = request.files['image']
    #     f.save("./test/image.png")
