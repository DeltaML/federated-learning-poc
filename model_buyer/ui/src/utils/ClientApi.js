function checkStatus(response) {
    console.log(response);
    if (response.status === 200) {
        return response;
    }
    const error = new Error(`HTTP Error ${response.statusText}`);
    error.status = response.statusText;
    error.response = response;
    console.log(error);
    throw error;
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

    return fetch(RoutesList.model, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: params
    })
        .then(response => {
            return response.json();
        })
        .catch(error => {
            console.log(error);
        })
}

function sendFile(params, res) {
    return fetch(RoutesList.file, {
        method: 'POST',
        body: params.body
    })
        .then(checkStatus)
        .then(res);
}

const Client = {sendFile, sendOrderModel, sendPrediction};
export default Client;

const RoutesList = {
    file: 'http://localhost:9090/file',
    ping: 'http://localhost:9090/ping',
    model: 'http://localhost:9090/models',
    prediction: 'http://localhost:9090/prediction'
};