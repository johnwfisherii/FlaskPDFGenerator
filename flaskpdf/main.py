#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import os, json, logging
import mimerender
from flask import Flask, render_template, Response, request
from flask.ext.mail import Mail, Message
from xhtml2pdf import pisa
from cStringIO import StringIO

# Default logging config
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

# Load Settings
settings_file = open('settings.json', 'r')
settings = json.loads(settings_file.read())
settings_file.close()

# Init Flask App
app = Flask(__name__)

# Init Mail
mail = Mail(app)

# Config
app.config.update(
	DEBUG = True,
	#EMAIL SETTINGS
	MAIL_SERVER = 'smtp.mandrillapp.com',
	MAIL_PORT = 587,
	MAIL_USE_SSL = False,
	MAIL_USERNAME = settings['mail_username'],
	MAIL_PASSWORD = settings['mail_key']
	)

mimerender.register_mime('pdf', ('application/pdf',))
mimerender = mimerender.FlaskMimeRender(global_charset='UTF-8')

@app.route('/')
def main():
	return render_template('setup.html', name='setup')

@app.route('/submit', methods=['POST'])
def pdf_submission():
	
	# grab form values
	pdf_text = request.form['pdf_text']
	pdf_title = request.form['pdf_title']
	pdf_email = request.form['pdf_email']

	# generate pdf
	pdf = StringIO()
	html = render_template('pdf_template.html', pdf_text = pdf_text, pdf_title = pdf_title, pdf_email = pdf_email)
	pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
	pdf_resp = pdf.getvalue()
	pdf.close()	

	# email pdf
	msg = Message('Here is your custom PDF',sender=settings['sender_email'],recipients=[pdf_email])
	msg.body = "PDF generated from custom form is attached to this message."
	msg.attach("temppdf.pdf", "application/pdf", pdf_resp)
	mail.send(msg)

	# show response
	return render_template('complete.html', name='complete', pdf_text = pdf_text, pdf_title = pdf_title, pdf_email = pdf_email)

@app.route('/submit', methods=['GET'])
def pdf_submission_get():
	return render_template('error.html', name='error')

@app.route('/pdf')
def render_pdf():
    pdf = StringIO()
    html = render_template('pdf_template.html', pdf_text = "test", pdf_title = "test_title", pdf_email = "email")
    pisa.CreatePDF(StringIO(html.encode('utf-8')), pdf)
    resp = pdf.getvalue()
    pdf.close()
    return Response(resp, mimetype='application/pdf')

if __name__ == "__main__":
    app.run()
