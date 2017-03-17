from flask import Flask, render_template, request
from base64 import b64decode
import random
import os
import string


app = Flask(__name__)

@app.route("/")
def hello():
	return render_template("index.html")

@app.route("/convert", methods=['POST'])
def get_image():
	# img_base64 = request.data.get('image_data')
	img_base64 = request.form['image_data'].split('data:image/png;base64,')[1]

	rand_string = random.getrandbits(128)

	with open("static/photos/{}.jpg".format(rand_string), 'wb') as f:
		f.write(b64decode(img_base64))

	os.system("primitive -i static/photos/{0}.jpg -o /tmp/{0}.gif -n 100 -m 6 && mv /tmp/{0}.gif static/gifs/{0}.gif".format(rand_string))

	return "static/gifs/{0}.gif".format(rand_string)

@app.route("/mail", methods=['POST'])
def mail():
	mail_id = request.form['email']
	rand_string = request.form['hash']

	# Mail here!

	return "Success!"

if __name__ == "__main__":
    app.run(debug=True)
