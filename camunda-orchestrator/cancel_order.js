let axios = require('axios');
let soap = require('soap');
let { Client, Variables } = require('camunda-external-task-client-js');

const baseUrl = 'http://localhost:8080/engine-rest';
const restUrl = 'http://localhost:5050';

// Create a Client instance with custom configuration
let config = { baseUrl };
let cancelOrderWorker = new Client(config);
let axiosOptions = {}, axiosInstance;

cancelOrderWorker.subscribe('validate-request', async function({ task, taskService }) {
	// Get all variables
	let orderID = task.variables.get('order_id');
	let authKey = task.variables.get('auth_key');
	let callbackURL = task.variables.get("callback_url");
	let status = false, error = "Error";
	// Set Process Variables
	let processVariables = new Variables();
	// Validate order data
	if (orderID && authKey && callbackURL) {
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		axiosInstance = axios.create(axiosOptions);
		try {
			let response = await axiosInstance.get(`${restUrl}/order/${orderID}`);
			if (response.status === 200) {
				status = true;
				processVariables.set('order', response.data);
				processVariables.set('auth_key', authKey);
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
	/* TODO: Invoke payment service - refund payment */
	let processVariables = new Variables();
	console.log(`Did refund-payment. Set variable success=${true}`);
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
	console.log(order);
	console.log(order.id);
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
	console.log(listSection);
	console.log(order.id);
	// Add to capacity for ticket section
	await axiosInstance.post(`${restUrl}/ticket_section/capacity_add`, request);
	// If order status is paid, then we must delete ticket with that order id
	if (order.status === 'paid') {
		await axiosInstance.delete(`${restUrl}/ticket`, {"order_id": order.id});
	}
	console.log(`Did release-ticket`);
	await taskService.complete(task);
});

/* Notify Cancel Failed */
cancelOrderWorker.subscribe('notify-cancel-booking-failed', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	let error = task.variables.get("message_error");
	/* TODO: throw message to callback URL */
	console.log(`Did notify-cancel-booking-failed. error: ${error}`);
	await taskService.complete(task);
});

/* Notify Cancel Success*/
cancelOrderWorker.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	/* TODO: throw message to callback URL */
	console.log(`Did notify-booking-cancelled`);
	await taskService.complete(task);
});

module.exports = cancelOrderWorker;