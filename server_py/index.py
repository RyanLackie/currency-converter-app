# Required modules
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests


# Settings
#host = 'localhost'
host = '165.22.11.241'
port = '82'
DEBUG = True
app = Flask(__name__)

# enable CORS
CORS(app)


# Methods
@app.route('/ping', methods=['POST'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getExchangeRates', methods=['POST'])
def getExchangeRates():
    # Get the symbol passed
    symbol = request.get_json()['currency']

    # Get data from API
    url = 'https://api.exchangeratesapi.io/latest?base='+symbol
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
        # Found an interesting event where if the symbol is EUR it disapears from the output
        # I don't think this happends for any other symbols other than EUR
        # Insert the EUR data back into where it normally is to keep the order constant
        if i == 18 and symbol == 'EUR':
            exchangeRates.insert(18, {'id': 18, 'currency': 'EUR', 'rate': '1.0'})
            continue

        temp = item.split(":")
        temp = {'id': i, 'currency': temp[0], 'rate': temp[1]}
        exchangeRates[i] = temp

    return jsonify(exchangeRates)


# Run server
if __name__ == '__main__':
    app.run(host=host, port=port)