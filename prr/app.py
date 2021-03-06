import os 

from flask import Flask, request
from prr.haro import haro

app = Flask(__name__)

@app.route('/')
def home():
    return 'PRR server says Hello!'

@app.route('/parse-haro-email', methods = ['POST'])
def parse_haro_email():
    email_id= request.json['emailId']
    secret = request.args['secret'] if 'secret' in request.args else None
    try:
        if secret == os.getenv("PRR_SECRET"):
            return haro.convert_haro_email_to_records(email_id)
    except Exception as e:
        return "Error encountered: " + str(e)
    return "Open sesame"