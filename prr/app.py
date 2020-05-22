import os 

from flask import Flask, request
from prr.haro import haro

app = Flask(__name__)

@app.route('/')
def home():
    return 'PRR server says Hello!'

@app.route('/parse-haro-email')
def parse_haro_email():
    args = request.args
    if len(args)>0:
        if 'secret' in args and args['secret']==os.getenv("PRR_SECRET"):
            return haro.convert_haro_email_to_records()
    return "Open sesame"