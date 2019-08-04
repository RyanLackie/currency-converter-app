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
#app.config.from_object(__name__)

# enable CORS
CORS(app)
#CORS(app, resources={r'/*': {'origins': '*'}})

#?app.config['Access-Control-Allow-Headers'] = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
#app.config['CORS_HEADERS'] = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']

#CORS(app, support_credentials=True)
#CORS(app, resources={r"/*": {"origins": "http://"+host+":"+port}})


# Classes
class exchangeRate:
    def __init__(self, id, country, rate):
        self.id = id
        self.country = country
        self.rate = rate


# Methods
@app.route('/ping', methods=['POST'])
def ping_pong():
    return jsonify('pong!')

#@cross_origin()
@app.route('/getExchangeRates', methods=['POST'])#OPTIONS
def getExchangeRates():
    # Get the symbol passed
    symbol = request.get_json()['symbol']

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
            exchangeRates.insert(18, {'id': 18, 'country': 'EUR', 'rate': '1.0'})
            continue

        temp = item.split(":")
        temp = {'id': i, 'country': temp[0], 'rate': temp[1]}
        exchangeRates[i] = temp

    return jsonify(exchangeRates)

#@app.after_request
#def after_request(response):
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#    return response

# Run server
if __name__ == '__main__':
    app.run(host=host, port=port)