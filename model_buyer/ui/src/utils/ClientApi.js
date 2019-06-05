function sendPing(params) {
    console.log(params)
    return fetch(RoutesList.ping, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: params
    })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .catch(response => {
            console.log(response);
        })

}

function sendPrediction(params) {
    console.log(params)
    return fetch(RoutesList.prediction, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: params
    })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .catch(response => {
            console.log(response);
        })

}


function sendOrderModel(params) {

    console.log(params)
    return fetch(RoutesList.model, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: params
    })
        .then(response => {
            console.log(response);
            return response.json();
        })
        .catch(error => {
            console.log(error);
        })

}

const Client = {sendPing, sendOrderModel, sendPrediction};
export default Client;

const RoutesList = {
    ping: 'http://localhost:9090/ping',
    model: 'http://localhost:9090/model',
    prediction: 'http://localhost:9090/prediction'
};