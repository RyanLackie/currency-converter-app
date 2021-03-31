const apiRoot = "http://localhost";
const jsPort = 8080;
const pyPort = 7000;

// Methods
export function ping_js() {
    console.log(myFetch(`${apiRoot}:${jsPort}/app/ping`, {}));
}
export function getExchangeRates_js(currency) {
    return myFetch(`${apiRoot}:${jsPort}/app/getExchangeRates`, {
        currency
    });
}

export function ping_py() {
    console.log(myFetch(`${apiRoot}:${pyPort}/ping`, {}));
}
export function getExchangeRates_py(currency) {
    return myFetch(`${apiRoot}:${pyPort}/getExchangeRates`, {
        currency
    })
}


function myFetch(url = ``, data = null) {
    let options = {
        cache: "no-cache",
        credentials: "same-origin"
    };
    if (data) {
        options = {
            ...options,
            method:  "POST",
            headers: {
                "Content-Type": "application/json; charset=utf-8",
            },
            body: JSON.stringify(data),
        };
    }
    return fetch(url, options)
    .then(response => {
        return response.json()
    });
}
