var soap = require('soap');
var url = 'http://167.205.35.211:8080/easypay/PaymentService?wsdl';
var args = {name: 'value'};

function getPaymentMethods(){
    soap.createClient(url, function(err, client) {
        let args= {};
        client.getPaymentMethods(args, function(err, result) {
            console.log(result.return);
        });
    });
}

function beginPayment(paymentMethodId, amount, callback){
    soap.createClient(url, function(err, client){
        let args = {
            "paymentMethodId" : paymentMethodId, 
            "amount" : amount
        }
        client.beginPayment(args, callback);
    });
}

function getPaymentEvents(paymentId, lastEventId, callback){
    soap.createClient(url, function(err, client){
        let args = {
            "paymentId" : paymentId, 
            "lastEventId" : lastEventId
        }
        client.getPaymentEvents(args, callback);
    });
}

module.exports = {getPaymentMethods, beginPayment, getPaymentEvents}