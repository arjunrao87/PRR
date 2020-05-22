from flask import Flask
from prr.haro import haro
app = Flask(__name__)

@app.route('/')
def home():
    return 'PRR server says Hello!'

@app.route('/parse-haro-email')
def parse_haro_email():
    return haro.convert_haro_email_to_records()