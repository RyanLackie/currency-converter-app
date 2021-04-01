<template>
    <div class="Home vcContatiner">

        <div class="centerUI">

            <div class="side">
                <div class="vcContatiner">

                    <input class="amountInput" id="amountInput"
                        type="number" value="1.00" min="0" step="1"
                        @input="updateExchangeRateUI()">

                    <div class="currencyInput noselect"
                        :style="styleCurrencyInput('input')"
                        @click="currencySelectorClicked('input')">

                        <div class="vcContatiner">{{fillCurrencyName(this.inputExchangeRate.currency)}}</div>

                        <div class="optionContainer" :style="styleOptionContainer('input')">
                            <div class="option" v-for="option in Object.entries(exchangeRates)" :key="option[0]"
                            :style="styleOption('input', option)" @click="optionChosen('input', option)">
                                {{fillCurrencyName(option[0])}}
                            </div>
                        </div>

                    </div>

                </div>
            </div>

            <div class="spacer">
                <div class="vcContatiner">
                    <div class="line"></div>
                </div>
            </div>

            <div class="side">
                <div class="vcContatiner">

                    <input class="amountInput" id="amountOutput"
                        type="number" value="1.00" min="0" step="1" :disabled="true"
                        @input="updateExchangeRateUI()">

                    <div class="currencyInput noselect"
                        :style="styleCurrencyInput('output')"
                        @click="currencySelectorClicked('output')">

                        <div class="vcContatiner">{{fillCurrencyName(this.outputExchangeRate.currency)}}</div>

                        <div class="optionContainer" :style="styleOptionContainer('output')">
                            <div class="option" v-for="option in Object.entries(exchangeRates)" :key="option[0]"
                            :style="styleOption('output', option)" @click="optionChosen('output', option)">
                                {{fillCurrencyName(option[0])}}
                            </div>
                        </div>

                    </div>

                </div>
            </div>

        </div>


        <div class="switchContainer">
            <label class="switch">
                <input type="checkbox" @change="toggleServer($event)">
                <span class="slider"></span>
            </label>
        </div>

    </div>
</template>

<style scoped lang="scss">
    @import "Home.sass";
</style>

<script>
    import * as api from '@/services/api_access.js';
    import currencyMap from '@/services/currency_map.js';

    export default {
        data() {
            return {
                exchangeRates: Array,

                inputExchangeRate: Object,
                inputExchangeRateBoolean: false,

                outputExchangeRate: Object,
                outputExchangeRateBoolean: false,

                server: 'python'
            }
        },

        methods: {
            // Data Selection
            currencySelectorClicked(id) {
                if (id == 'input') {
                    this.inputExchangeRateBoolean = !this.inputExchangeRateBoolean;
                    this.outputExchangeRateBoolean = false;

                } else {
                    this.outputExchangeRateBoolean = !this.outputExchangeRateBoolean;
                    this.inputExchangeRateBoolean = false;
                }
            },

            optionChosen(id, option) {
                // Input rate was changed - need to update exchange rates
                if (id == 'input') {
                    if (this.inputExchangeRate.currency != option[0]) {
                        this.inputExchangeRate = {
                            'currency': option[0],
                            'rate': this.exchangeRates[option[0]]
                        };
                        this.updateExchangeRateData();
                    }

                // Output rate was changed - need to update UI
                } else {
                    if (this.outputExchangeRate.currency != option[0]) {
                        this.outputExchangeRate = {
                            'currency': option[0],
                            'rate': this.exchangeRates[option[0]]
                        };
                        this.updateExchangeRateUI();
                    }
                }
            },

            updateExchangeRateData() {
                const currency = this.inputExchangeRate.currency ? this.inputExchangeRate.currency : 'USD';
                const requestFunction = this.server === 'python' ? api.getExchangeRates_py : api.getExchangeRates_js;

                requestFunction(currency).then(
                    exchangeRates => {
                        this.exchangeRates = exchangeRates;
                        this.inputExchangeRate = {
                            'currency': this.inputExchangeRate.currency,
                            'rate': this.exchangeRates[this.inputExchangeRate.currency]
                        };
                        this.outputExchangeRate = {
                            'currency': this.outputExchangeRate.currency,
                            'rate': this.exchangeRates[this.outputExchangeRate.currency]
                        };
                        this.updateExchangeRateUI();
                    }
                );
            },
            updateExchangeRateUI() {
                // Convert to output currency
                /*
                    I was going to only take in values up to the .00 position so .009
                    wouldn't have an effect on the output, but when testing other
                    converters they did allow this so I was unsure of what was best practice
                */
                var outputRate = this.outputExchangeRate.rate;
                var value = document.getElementById('amountInput').value * outputRate;

                value = value.toString();
                if (!value.includes(".")) {
                    value.concat(".00");
                }
                value = value.slice(0, (value.indexOf(".")) + 3);
                Number(value);
                value = parseFloat(value).toFixed(2);
                document.getElementById('amountOutput').value = value;
            },

            toggleServer() {
                this.server = this.server === 'python' ? 'javascript' : 'python';
                this.updateExchangeRateData()
            },


            // Styling methods
            styleCurrencyInput(section) {
                if (section == 'input') {
                    if (this.inputExchangeRateBoolean) {
                        return 'border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;';
                    }

                } else {
                    if (this.outputExchangeRateBoolean) {
                        return 'border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;';
                    }
                }
            },
            styleOptionContainer(section) {
                if (section == 'input') {
                    if (this.inputExchangeRateBoolean) {
                        return 'visibility: visible';
                    }

                } else {
                    if (this.outputExchangeRateBoolean) {
                        return 'visibility: visible';
                    }
                }
            },
            styleOption(section, option) {
                if (section == 'input' && option == this.inputExchangeRate) {
                    return 'background-color: limegreen; color: white;';
                }
                if (section == 'output' && option == this.outputExchangeRate) {
                    return 'background-color: limegreen; color: white;';
                }
            },

            // Large and ugly but it does make the UI a little nicer
            fillCurrencyName(currency) {
                return currencyMap[currency];
            }
        },

        mounted() {
            // Init application data/*
            api.getExchangeRates_py('USD').then(
                exchangeRates => {
                    this.exchangeRates = exchangeRates;

                    // Set default from currency to be USD
                    this.inputExchangeRate = {
                        'currency': 'USD',
                        'rate': this.exchangeRates['USD']
                    };

                    // Set output to the first alphabetical currency returned
                    const firstRate = Object.entries(this.exchangeRates)[0];
                    this.outputExchangeRate = {
                        'currency': firstRate[0],
                        'rate': firstRate[1]
                    };

                    this.updateExchangeRateUI();
                }
            );
        }
    }
</script>
