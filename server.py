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

	os.system("primitive -i static/photos/{0}.jpg -o /tmp/{0}.gif -n 100 -m 6 && mv /tmp/{0}.gif static/gifs/{0}.gif".format(rand_string))

	return rand_string


@app.route("/mail", methods=['POST'])
def mail():
	mail_id = request.form['email']
	rand_string = request.form['hash']
	
	msg = MIMEMultipart()
	msg.attach(MIMEText('Hello from Mailgun'))
	msg['Subject'] = "Hello from SDSLabs"
	msg['From']    = "convop@srishti.sdslabs.co"
	msg['To']      = mail_id

	part = MIMEApplication(open("static/gifs/{}.gif".format(rand_string), 'rb').read(),Name=rand_string+".gif")
	part['Content-Disposition'] = "attachment; filename={}.gif".format(rand_string)
	msg.attach(part)
	s = smtplib.SMTP('smtp.mailgun.org', 587)

	s.login(config['mailgun_sandbox'], config['mailgun_key'])
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
	# mail_id = request.form['email']
	# rand_string = request.form['hash']
	# request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(config['mailgun_sandbox'])
	# r = requests.post(
	# 	request_url,
	# 	auth=('api', config['mailgun_key']),
	# 	data={
	# 		'from': 'postmaster@srishti.sdslabs.co',
	# 		'to': mail_id,
	# 		'subject': 'Hello from SDSLabs',
	# 		'text': 'Hello from Mailgun'
	# 	},
	# 	files=[("attachment", open("static/gifs/{}.gif".format(rand_string), 'rb'))]
	# )

	# print(r.status_code, r.text)

	return "Success!"


@app.route("/gifs", methods=['GET'])
def show():
	rand_string = request.args['hash']

	return render_template("show.html", hash=rand_string)


if __name__ == "__main__":
	app.run(debug=True)
