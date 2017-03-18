from flask import Flask, render_template, request
from base64 import b64decode
import requests
import random
import string
import os
from config import config
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello():
	return render_template("index.html")


@app.route("/convert", methods=['POST'])
def get_image():
	# img_base64 = request.data.get('image_data')
	img_base64 = request.form['image_data'].split('data:image/png;base64,')[1]

	rand_string = str(random.getrandbits(31)) + 'a'

	with open("static/photos/{}.jpg".format(rand_string), 'wb') as f:
		f.write(b64decode(img_base64))

	os.system("""convert static/photos/{0}.jpg -resize 256x256 static/photos/{0}.jpg &&
		primitive -i static/photos/{0}.jpg -o /tmp/{0}.gif -n 50 -m 8 &&
		convert -delay 10x100 /tmp/{0}.gif \( +clone -set delay 500 \) +swap +delete /tmp/{0}.gif &&
		mv /tmp/{0}.gif static/gifs/{0}.gif""".format(rand_string))

	return rand_string


@app.route("/mail", methods=['POST'])
def mail():
	mail_id = request.form['email']
	rand_string = request.form['hash']

	msg = MIMEMultipart()
	msg.attach(MIMEText('Greetings from SDSLabs!\n Welcome to Srishti 2017. Thanks for checking out Primer-"Convex optimization based gif generator". We hope you have best expeience during Srishti at SDSLabs. \nYou will find your image and GIF generated attached here.\n\n Cheers!'))
	msg['Subject'] = "Welcome to Srishti'17 at SDSLabs"
	msg['From']    = "convop@srishti.sdslabs.co"
	msg['To']      = mail_id

	part = MIMEApplication(open("static/gifs/{}.gif".format(rand_string), 'rb').read(),Name=rand_string+".gif")
	part['Content-Disposition'] = "attachment; filename={}.gif".format(rand_string)
	msg.attach(part)
	part = MIMEApplication(open("static/photos/{}.jpg".format(rand_string), 'rb').read(),Name=rand_string+".gif")
	part['Content-Disposition'] = "attachment; filename={}.jpg".format(rand_string)
	msg.attach(part)
	s = smtplib.SMTP('smtp.mailgun.org', 587)

	s.login(config['mailgun_sandbox'], config['mailgun_key'])
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()

	return "Success!"


@app.route("/gifs", methods=['GET'])
def show():
	rand_string = request.args['hash']
	return render_template("show.html", hash=rand_string)


if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.run(host='0.0.0.0', ssl_context=context, threaded=True, debug=True)
