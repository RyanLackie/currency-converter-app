# Required modules
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


# Settings
host = '0.0.0.0'
port = 7000
debug = False

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
    currency = request.get_json()['currency']

    # Get data from API
    url = 'https://api.exchangeratesapi.io/latest?base='+currency
    exchangeRates = requests.get(url).text

    # Format into consistent data
    exchangeRates = exchangeRates[10:]                  # Remove constant start of data - "{"rates":{"
    exchangeRates = exchangeRates.replace('"', '')      # Remove all '"' chars from string
    exchangeRates = exchangeRates.split(",")            # Split by ',' chars
    del exchangeRates[-1]                               # Remove end of data - date
    del exchangeRates[-1]                               # Remove end of data - currency base

    # Remove '}' char from last rate string
    endOfArray = len(exchangeRates) - 1
    exchangeRates[endOfArray] = exchangeRates[endOfArray][:-1]

    # Format data into objects
    for i, item in enumerate(exchangeRates):
        # Found an interesting event where if the currency is EUR it disappears from the output
        # I don't think this happens for any other currency other than EUR
        # Insert the EUR data back into where it normally is to keep the order constant
        if i == 18 and currency == 'EUR':
            exchangeRates.insert(18, {'id': 18, 'currency': 'EUR', 'rate': '1.0'})
            continue

        temp = item.split(":")
        temp = {'id': i, 'currency': temp[0], 'rate': temp[1]}
        exchangeRates[i] = temp

    return jsonify(exchangeRates)


# Run server
if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
