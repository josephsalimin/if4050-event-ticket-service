let axios = require('axios');
let baseUrl = 'http://localhost:8080/engine-rest';
let restUrl = 'http://localhost:5050';
let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';
let { Client, Variables } = require('camunda-external-task-client-js');

// create a Client instance with custom configuration
let config = { baseUrl };
let cancelOrderWorker = new Client(config);
axios.defaults.headers.common['Authorization'] = jwtKey;
axios.defaults.headers.common['Content-Type'] = 'application/json';


// Set order data
let order;
let orderStatus;

cancelOrderWorker.subscribe('validate-request', async function({ task, taskService }) {
	// Set variables
	let orderID = task.variables.get('order_id');
	let processVariables = new Variables();
	let status = false;
	// Validate order data
	try {
		console.log(orderID);
		console.log(`${restUrl}/order/${orderID}`);
		let response = await axios.get(`http://localhost:5050/order/2`);
		console.log(response);
		if(response.status === 200) {
			status = true;
			order = response.data;
			orderStatus = order.status;
			processVariables.set('validated', true);
			processVariables.set('paid', (orderStatus === 'paid'));
			processVariables.set('cancelled', (orderStatus === 'cancelled'));
			processVariables.set('pending', (orderStatus === 'pending'));
		} else {
			processVariables.set('validated', false);
		}
	} catch(err) {
		throw err;
		processVariables.set('validated', false);
	}

	console.log(`Did validate-request. Set variable validated=${status}`);
	await taskService.complete(task, processVariables);
});

/* Booking invalid */

cancelOrderWorker.subscribe('notify-cancel-booking-failed', async function({ task, taskService }) {
	console.log(`Did notify-cancel-booking-failed.`);
	await taskService.complete(task);
});

/* Booking valid */

cancelOrderWorker.subscribe('check-order-status', async function({ task, taskService }) {
  	// Set variables
	let processVariables = new Variables();
	// processVariables.set("paid", true);

	console.log(`Did check-order-status.`);
	await taskService.complete(task, processVariables);
});

/* Order not paid */

cancelOrderWorker.subscribe('unpaid-checking', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	processVariables.set("cancelled", true);

	console.log(`Did unpaid-checking.`);
	await taskService.complete(task, processVariables);
});

/* Order status paid */

cancelOrderWorker.subscribe('refund-payment', async function({ task, taskService }) {
	/* TODO: Invoke payment service - refund payment */

	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);

	console.log(`Did refund-payment. Set variable success=${true}`);
	await taskService.complete(task, processVariables);
});

/* Refund status success */

cancelOrderWorker.subscribe('cancel-order', async function({ task, taskService }) {
	console.log(`Did cancel-order`);
	await taskService.complete(task);
});

cancelOrderWorker.subscribe('release-ticket', async function({ task, taskService }) {
	console.log(`Did release-ticket`);
	await taskService.complete(task);
});

cancelOrderWorker.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	console.log(`Did notify-booking-cancelled`);
	await taskService.complete(task);
});