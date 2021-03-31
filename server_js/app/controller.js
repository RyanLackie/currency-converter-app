const express = require('express');
const Model = require('./model');

var model = new Model();

const app = express.Router();

// Methods
app.post('/ping', (req, res) => {
    model.ping(
        test => res.send(test)
    );
});

app.post('/getExchangeRates', (req, res) => {
    model.getExchangeRates(
        req.body.currency, exchangeRates => res.send(exchangeRates)
    );
});


module.exports = app;
