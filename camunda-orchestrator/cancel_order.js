let axios = require('axios');
let soap = require('soap');
let { Client, Variables } = require('camunda-external-task-client-js');

const baseUrl = 'http://localhost:8080/engine-rest';
const restUrl = 'http://localhost:5050';

// Create a Client instance with custom configuration
let config = { baseUrl };
let cancelOrderWorker = new Client(config);
let axiosOptions = {};
let axiosInstance;

cancelOrderWorker.subscribe('validate-request', async function({ task, taskService }) {
	// Get all variables
	let orderID = task.variables.get('order_id');
	let authKey = task.variables.get('auth_key');
	let method = task.variables.get('payment_method');
	let callback = task.variables.get("callback");
	let callbackType = task.variables.get("callback_type");
	let status = false, error = "Error";
	// Set Process Variables
	let processVariables = new Variables();
	// Validate order data
	if (orderID && authKey && callback && callbackType && method) {
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		axiosInstance = axios.create(axiosOptions);
		try {
			let response = await axiosInstance.get(`${restUrl}/order/${orderID}`);
			if (response.status === 200) {
				status = true;
				processVariables.set('order', response.data);
			} 
		} catch(err) {
			error = err.message;
		}
	}
	if (!status) processVariables.set("message_error", error);
	processVariables.set('validated', status);
	console.log(`Did validate-request. Set variable validated=${status}`);
	await taskService.complete(task, processVariables);
});

/* Check if order is paid or not */
cancelOrderWorker.subscribe('paid-order-checking', async function({ task, taskService }) {
	// Get variables
	let orderStatus = task.variables.get("order").status;
	// Set Process Variables
	let processVariables = new Variables();
	if (orderStatus == 'paid') processVariables.set('paid', true);
	else processVariables.set('paid', false);
	console.log(`Did check-order-status.`);
	await taskService.complete(task, processVariables);
});

/* Check if order is cancelled or pending */
cancelOrderWorker.subscribe('unpaid-order-checking', async function({ task, taskService }) {
	// Get variables
	let orderStatus = task.variables.get("order").status;
	// Set Process Variables
	let processVariables = new Variables();
	if (orderStatus == 'cancelled') {
		processVariables.set('cancelled', true);
	} else {
		processVariables.set('cancelled', false);
	}
	console.log(`Did unpaid-checking.`);
	await taskService.complete(task, processVariables);
});

/* Order status paid */
cancelOrderWorker.subscribe('refund-payment', async function({ task, taskService }) {
	let processVariables = new Variables();
	let method = task.variables.get('payment_method');
	let order = task.variables.get('order');
	let res = await beginPayment(method, order.total_price);
	processVariables.set('payment_id', res.paymentId);
	let loop = true;
	while (loop) {
		let res = await getPaymentEvents(res.paymentId);
		if (res.lastEventId) {
			let events = res.events;
			processVariables.set('last_event_id', res.lastEventId);
			if (events[0].type === 'OPEN_URL') {
				processVariables.set('payment_type', 'url');
				processVariables.set('payment_data', events[0].urlToOpen);
			} else {
				processVariables.set('payment_type', 'acc');
				processVariables.set('payment_data', events[0].accountNumber);
			}
			loop = false;
		}
	}
	await taskService.complete(task);
});

cancelOrderWorker.subscribe('notify-refund', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	console.log(`Did notify-refund.`);
	await taskService.complete(task);
});

cancelOrderWorker.subscribe('waiting-refund', async function({ task, taskService }) {
	let lastEventId = task.variables.get('last_event_id');
	let paymentId = task.variables.get('payment_id');
	let loop = true;
	let processVariables = new Variables();
	while (loop) {
		let res = await getPaymentEvents(paymentId, lastEventId);
		let lastId = res.lastEventId;
		let events = res.events;
		if (events) {
			let event = events.find(x => (x.paymentEventId === lastId));
			if (event.type === 'SUCCESS') {
				processVariables.set('success', true);
				loop = false;
			} else if (event.type === 'FAILURE') {
				processVariables.set('success', false);
				processVariables.set('message_error', 'Refund Failure. Try Again');
				loop = false;
			}
		}
	}
	console.log(`Did waiting-refund.`);
	await taskService.complete(task, processVariables);
});

/* Check refund response */
cancelOrderWorker.subscribe('check-refund-response', async function({ task, taskService}) {
	/* TODO: Check refund response */
	let processVariables = new Variables();
	processVariables.set('success', true);
	console.log(`Did check-refund-response`);
	await taskService.complete(task, processVariables);
});

/* Refund Status Success */
cancelOrderWorker.subscribe('cancel-order', async function({ task, taskService }) {	
	// Get variables
	let order = task.variables.get('order');
	let response, listSection;
	// Set Process Variables
	let processVariables = new Variables();
	response = await axiosInstance.delete(`${restUrl}/order/${order.id}`, {});
	listSection = response.data;
	processVariables.set('section_list', listSection);
	console.log(`Did cancel-order`);
	await taskService.complete(task, processVariables);
});

/* Release Ticket */
cancelOrderWorker.subscribe('release-ticket', async function({ task, taskService }) {
	let listSection = task.variables.get('section_list');
	let order = task.variables.get('order');
	let request = {"section_list": listSection};
	// Add to capacity for ticket section
	await axiosInstance.post(`${restUrl}/ticket_section/capacity_add`, request);
	// If order status is paid, then we must delete ticket with that order id
	if (order.status === 'paid') {
		await axiosInstance.delete(`${restUrl}/ticket`, {body: {"order_id": order.id}});
	}
	console.log(`Did release-ticket`);
	await taskService.complete(task);
});

/* Notify Cancel Failed */
cancelOrderWorker.subscribe('notify-cancel-booking-failed', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let error = task.variables.get("message_error");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"message": error
		});
	}
	console.log(`Did notify-cancel-booking-failed. error: ${error}`);
	await taskService.complete(task);
});

/* Notify Cancel Success*/
cancelOrderWorker.subscribe('notify-order-cancelled', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let order = task.variables.get("order");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"message": "order cancelled",
			"order": order
		});
	}
	console.log(`Did notify-order-cancelled`);
	await taskService.complete(task);
});

module.exports = cancelOrderWorker;