from flask import Flask, request
import base64
from PIL import Image
import io

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/upload', methods=['POST']) 
def upload():
	string = base64.b64decode(request.form['image'])
	image = Image.open(io.BytesIO(string))
	return "nothing";

if __name__ == "__main__":
    app.run()



