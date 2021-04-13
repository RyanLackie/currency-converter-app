# Required modules
import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Settings
host = os.getenv('SERVER_HOST')
port = os.getenv('SERVER_PORT')
debug = os.getenv('SERVER_DEBUG')

app = Flask(__name__)

# Enable CORS
CORS(app)


# Methods
@app.route('/ping', methods=['POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getExchangeRates', methods=['POST'])
def getExchangeRates():
    # Get the currency passed
    currency = 'USD' if not 'currency' in request.json else request.json['currency']

    # Get data from API
    url = f"https://v6.exchangerate-api.com/v6/{os.getenv('ACCESS_KEY')}/latest/{currency}"
    response = requests.get(url)
    conversion_rates = response.json()['conversion_rates']
    return jsonify(conversion_rates)


# Run server
if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
