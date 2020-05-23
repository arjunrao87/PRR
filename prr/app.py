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
    try:
        if len(args) > 0 and 'secret' in args and args['secret'] == os.getenv("PRR_SECRET"):
            if 'email_id' in args:
                return haro.convert_haro_email_to_records(args['email_id'])
    except Exception as e:
        return "Error encountered: " + str(e)
    return "Open sesame"