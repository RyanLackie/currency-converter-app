<template>
    <div class="Home vcContatiner">

        <div class="centerUI">

            <div class="side">
                <div class="vcContatiner">
                    
                    <input class="currencyInput" id="amountInput" type="number" value="1.00" min="0" step="1" @input="updateExchangeRateUI()">

                    <div class="countryInput noselect" :style="styleCountryInput('input')" @click="countrySelectorClicked('countryInput')">
                        <div class="vcContatiner">{{fillCountryInfo(this.exchangeRateInput.country)}}</div>

                        <div class="optionContainer" id='countryInput' :style="styleOptionContainer('input')">
                            <div class="option" v-for="option in exchangeRates" :key="option.country" :value="option.country"
                            :style="styleOption('input', option)" @click="countryChosen('countryInput', option)">
                                {{fillCountryInfo(option.country)}}
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
                    
                    <input class="currencyInput" id="amountOutput" type="number" value="1.00" min="0" step="1" @input="updateExchangeRateUI()">
                    
                    <div class="countryInput noselect" :style="styleCountryInput('output')" @click="countrySelectorClicked('countryOutput')">
                        <div class="vcContatiner">{{fillCountryInfo(this.exchangeRateOutput.country)}}</div>

                        <div class="optionContainer" id='countryOutput' :style="styleOptionContainer('output')">
                            <div class="option" v-for="option in exchangeRates" :key="option.country" :value="option.country"
                            :style="styleOption('output', option)" @click="countryChosen('countryOutput', option)">
                                {{fillCountryInfo(option.country)}}
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
    import * as api from '@/services/api_access';

    export default {
        data() {
            return {
                exchangeRates: Array,

                exchangeRateInput: Object,
                exchangeRateInputBoolean: false,

                exchangeRateOutput: Object,
                exchangeRateOutputBoolean: false,

                serverSwitch: false
            }
        },

        methods: {
            // Data Selection
            countrySelectorClicked(id) {
                if (id == 'countryInput') {
                    this.exchangeRateInputBoolean = !this.exchangeRateInputBoolean;
                    this.exchangeRateOutputBoolean = false;
                }
                else {
                    this.exchangeRateOutputBoolean = !this.exchangeRateOutputBoolean;
                    this.exchangeRateInputBoolean = false;
                }
            },

            countryChosen(id, option) {
                if (id == 'countryInput') {
                    // Input rate was changed - need to update exchange rates
                    if (this.exchangeRateInput != option) {
                        this.exchangeRateInput = option;
                        this.updateExchangeRateData();
                    }
                }
                else {
                    // Output rate was changed - need to update UI
                    if (this.exchangeRateOutput != option) {
                        this.exchangeRateOutput = option;
                        this.updateExchangeRateUI();
                    }
                }
            },

            updateExchangeRateData() {
                if (!this.serverSwitch) {
                    api.getExchangeRates_py(this.exchangeRateInput.country).then(
                        exchangeRates => {
                            console.log('Python');
                            console.log(exchangeRates);
                            this.exchangeRates = exchangeRates;
                            this.exchangeRateInput = exchangeRates[this.exchangeRateInput.id];
                            this.exchangeRateOutput = exchangeRates[this.exchangeRateOutput.id];
                            this.updateExchangeRateUI();
                        }
                    );
                }
                else {
                    api.getExchangeRates_js(this.exchangeRateInput.country).then(
                        exchangeRates => {
                            console.log('JavaScript');
                            console.log(exchangeRates);
                            this.exchangeRates = exchangeRates;
                            this.exchangeRateInput = exchangeRates[this.exchangeRateInput.id];
                            this.exchangeRateOutput = exchangeRates[this.exchangeRateOutput.id];
                            this.updateExchangeRateUI();
                        }
                    );
                }
            },
            updateExchangeRateUI() {
                // Get value in at the output rate
                /* 
                    I was going to only take in values up to the .00 position so .009
                    wouldn't have an effect on the output, but when testing other
                    converters they did allow this so I was unsure of what was best practice
                */
                var outputRate = this.exchangeRateOutput.rate;
                var value = document.getElementById('amountInput').value * outputRate;

                value = value.toString();
                if (!value.includes("."))
                    value.concat(".00");
                value = value.slice(0, (value.indexOf(".")) + 3);
                Number(value);
                value = parseFloat(value).toFixed(2);
                document.getElementById('amountOutput').value = value;
            },

            toggleServer() {
                this.serverSwitch = !this.serverSwitch
                this.updateExchangeRateData()
            },


            // Styling methods
            styleCountryInput(section) {
                if (section == 'input') {
                    if (this.exchangeRateInputBoolean)
                        return 'border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;';
                }
                else {
                    if (this.exchangeRateOutputBoolean)
                        return 'border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;';
                }
            },
            styleOptionContainer(section) {
                if (section == 'input') {
                    if (this.exchangeRateInputBoolean)
                        return 'visibility: visible';
                }
                else {
                    if (this.exchangeRateOutputBoolean)
                        return 'visibility: visible';
                }
            },
            styleOption(section, option) {
                if (section == 'input' && option == this.exchangeRateInput)
                    return 'background-color: limegreen; color: white;';
                if (section == 'output' && option == this.exchangeRateOutput)
                    return 'background-color: limegreen; color: white;';
            },

            // Large and ugly but it does make the UI a little nicer
            fillCountryInfo(country) {
                switch(country) {
                    case 'CAD':
                        return 'Canadian Dollar (CAD)'
                    case 'HKD':
                        return 'Hong Kong Dollar (HKD)'
                    case 'ISK':
                        return 'Icelandic Króna (ISK)'
                    case 'PHP':
                        return 'Philippine Peso (PHP)'
                    case 'DKK':
                        return 'Danish Krone (PHP)'
                    case 'HUF':
                        return 'Hungarian Forint (HUF)'
                    case 'CZK':
                        return 'Czech Koruna (CZK)'
                    case 'GBP':
                        return 'Pound Sterling (GBP)'
                    case 'RON':
                        return 'Romanian Leu (RON)'
                    case 'SEK':
                        return 'Swedish Krona (SEK)'
                    case 'IDR':
                        return 'Indonesian Rupiah (IDR)'
                    case 'INR':
                        return 'Indian Rupee (INR)'
                    case 'BRL':
                        return 'Brazilian Real (BRL)'
                    case 'RUB':
                        return 'Russian Ruble (RUB)'
                    case 'HRK':
                        return 'Croatian Kuna (HRK)'
                    case 'JPY':
                        return 'Japanese Yen (JPY)'
                    case 'THB':
                        return 'Thai Baht (THB)'
                    case 'CHF':
                        return 'Swiss Franc (CHF)'
                    case 'EUR':
                        return 'Euro (EUR)'
                    case 'MYR':
                        return 'Malaysian Ringgit (MYR)'
                    case 'BGN':
                        return 'Bulgarian Lev (BGN)'
                    case 'TRY':
                        return 'Turkish lira (TRY)'
                    case 'CNY':
                        return 'Chinese Yuan (CNY)'
                    case 'NOK':
                        return 'Norwegian Krone (NOK)'
                    case 'NZD':
                        return 'New Zealand Dollar (NZD)'
                    case 'ZAR':
                        return 'South African Rand (ZAR)'
                    case 'USD':
                        return 'United States Dollar (USD)'
                    case 'MXN':
                        return 'Mexican Peso (MXN)'
                    case 'SGD':
                        return 'Singapore Dollar (SGD)'
                    case 'AUD':
                        return 'Australian Dollar (AUD)'
                    case 'ILS':
                        return 'Israeli New Shekel (ILS)'
                    case 'KRW':
                        return 'South Korean Won (KRW)'
                    case 'PLN':
                        return 'Poland Złoty (PLN)'
                }
            }
            
        },

        mounted() {
            // Init application data/*
            api.getExchangeRates_py('USD').then(
                exchangeRates => {
                    this.exchangeRates = exchangeRates;

                    // Set input to USD, use a search if API data ever returns differently
                    if (exchangeRates[26].country == 'USD')
                        this.exchangeRateInput = exchangeRates[26];
                    else {
                        for (var i = 0; i < exchangeRates.length; i++) {
                            if (exchangeRates[i].country == 'USD') {
                                this.exchangeRateInput = exchangeRates[i];
                                break;
                            }
                        }
                    }
                    
                    // Set output to the first - could be changed - normally CAD
                    this.exchangeRateOutput = exchangeRates[0];

                    this.updateExchangeRateUI();
                }
            );
        }
    }
</script>
