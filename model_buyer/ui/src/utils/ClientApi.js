function sendOrderModel(params, response) {
    return fetch(RoutesList.ping, {
        method: 'POST',
        body: params.body
    })
       .then(response => {
        console.log(response);
        return response;
      })

}


const Client = { sendOrderModel };
export default Client;

const RoutesList = {
    ping:   '/ping'
};