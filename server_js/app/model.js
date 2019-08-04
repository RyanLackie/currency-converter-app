// Required modules
var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

class Model {
    constructor() {}

    ping(call_back) {
        call_back({ping: 'pong!'});
    }
    
    getExchangeRates(currency, call_back) {
        // Get data from API
        const http = new XMLHttpRequest();
        const url = 'https://api.exchangeratesapi.io/latest?base='+currency;
        http.open("GET", url, false);
        http.send();
        var exchangeRates = http.responseText;
        
        // Format into consistent data
        exchangeRates = exchangeRates.substr(10);                           // Remove constant start of data - "{"rates":{"
        exchangeRates = exchangeRates.replace(/['"]+/g, "");                // Remove all '"' chars from string
        exchangeRates = exchangeRates.split(",");                           // Split by ',' chars
        exchangeRates.splice(exchangeRates.length-2, exchangeRates.length); // Remove end of data - currency base and date

        // Remove '}' char from last rate string
        var endOfArray = exchangeRates.length - 1;
        exchangeRates[endOfArray] = exchangeRates[endOfArray].substr(0, exchangeRates[endOfArray].length - 1);
        
        // Format data into objects
        for (var i = 0; i < exchangeRates.length; i++) {

            // Found an interesting event where if the currency is EUR it disapears from the output
            // I don't think this happends for any other currencies other than EUR
            // Splicing the EUR data back into where it normally is to keep the order constant
            if (i == 18 && currency == 'EUR') {
                exchangeRates.splice(18, 0, {id: 18, currency: 'EUR', rate: '1.0'});
                continue;
            }

            var temp = exchangeRates[i].split(":");
            temp = {id: i, currency: temp[0], rate: temp[1]};
            exchangeRates[i] = temp;
        }

        //console.log(exchangeRates);

        call_back(exchangeRates);
    }
    
}

module.exports = Model;