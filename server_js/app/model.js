// Required modules
var axios = require('axios');

class Model {
    constructor() {}

    ping(call_back) {
        call_back({ ping: 'pong!' });
    }

    async getExchangeRates(currency, call_back) {
        // Get data from API
        currency = currency === undefined ? 'USD' : currency;
        const url = `https://v6.exchangerate-api.com/v6/${process.env.ACCESS_KEY}/latest/${currency}`;

        let data = '';
        let status = null;

        await axios({ url })
        // handle success
        .then((response) => {
            data = response.data.conversion_rates;
            status = response.status;
        })
        // handle error
        .catch((error) => {
            data = error.response.data
            status = error.status;
        });

        call_back({ data, status });
    }

}

module.exports = Model;
