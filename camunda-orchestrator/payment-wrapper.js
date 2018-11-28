var soap = require('soap');
var url = 'http://167.205.35.211:8080/easypay/PaymentService?wsdl';
let request = require('request');
let request_with_defaults = request.defaults({'proxy': process.env.http_proxy});
let soap_client_options = {'request': request_with_defaults};


async function getPaymentMethods() {
    let client = await soap.createClientAsync(url, soap_client_options);
    let args = {}
    let result = await client.getPaymentMethodsAsync(args);
    return result;
}

async function beginPayment(paymentMethodId, amount) {
    let client = await soap.createClientAsync(url, soap_client_options);
    let args = {
        "paymentMethodId" : paymentMethodId, 
        "amount" : amount
    }
    let result = await client.beginPaymentAsync(args);
    return result;
}

async function getPaymentEvents(paymentId, lastEventId) {
    let client = await soap.createClientAsync(url, soap_client_options);
    let args = {
        "paymentMethodId" : paymentMethodId, 
        "amount" : amount
    }
    let result = await client.getPaymentEventsAsync(args);
    return result;
}

getPaymentMethods().then((res) => {
    console.log(res);
}).catch(err => {
    console.log(err.body);
});

module.exports = {getPaymentMethods, beginPayment, getPaymentEvents}