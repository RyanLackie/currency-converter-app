// Required modules
var axios = require('axios');

class Model {
    constructor() {}

    ping(call_back) {
        call_back({ping: 'pong!'});
    }

    async getExchangeRates(currency, call_back) {
        // Get data from API
        currency = currency === undefined ? 'USD' : currency;
        const url = `https://v6.exchangerate-api.com/v6/${process.env.ACCESS_KEY}/latest/${currency}`;
        const response = await axios({ url })
        // handle success
        .then(function (response) {
            return response.data.conversion_rates;
        })
        // handle error
        .catch(function (error) {
            return error.response.data;
        });

        call_back(response);
    }

}

module.exports = Model;
