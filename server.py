from flask import Flask, render_template, request
from base64 import b64decode
import random
import os

def randomword(length = 50):
   return ''.join(random.choice(string.lowercase) for i in range(length))

app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/convert", methods=['POST'])
def get_image():
	# img_base64 = request.data.get('image_data')
	img_base64 = request.form['image_data'].split('data:image/png;base64,')[1]

	hash = randomword()

	with open("static/photos/{}.jpg".format(hash), 'wb') as f:
		f.write(b64decode(img_base64))

	os.system("./primitive static/photos/{}.jpg /tmp/primitive/{}.gif && mv /tmp/primitive/{}.gif static/gifs/{}.gif &")

	return "fuck"


if __name__ == "__main__":
    app.run(debug=True)
