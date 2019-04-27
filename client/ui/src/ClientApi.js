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

/*function getClientId(res) {
    return fetch(RoutesList.client, {
        method: 'GET',
        accept: "application/json",
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(checkStatus)
        .then(res);
}*/

function sendFile(params, res) {
    return fetch(RoutesList.file, {
        method: 'POST',
        body: params.body
    })
        .then(checkStatus)
        .then(res);
}

function parseJSON(response) {
    return response.json();
}

const Client = { sendFile };
export default Client;


const RoutesList = {
    //client: '/api/client/id',
    file:   '/dataset'
};