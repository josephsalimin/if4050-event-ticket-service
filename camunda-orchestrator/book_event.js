let axios = require('axios');
let baseUrl = 'http://localhost:8080/engine-rest';
let restUrl = 'http://localhost:5050';
let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';
let { Client, Variables } = require('camunda-external-task-client-js');

// create a Client instance with custom configuration
let config = { baseUrl };
let bookEventWorker = new Client(config);
axios.defaults.headers.common['Authorization'] = jwtKey;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Set order data
let order;
let order_id;
let section_list;

bookEventWorker.subscribe('validate-booking-request', async function({ task, taskService }) {
	// Set variables
	let order = task.variables.get('order');
	let processVariables = new Variables();
	let status = false;
	// Validate order data
	order = await JSON.parse(order);
	try {
		if(order.hasOwnProperty('user_id') &&
		   order.hasOwnProperty('total_price') &&
		   order.hasOwnProperty('section_list')) {
			status = true;
			section_list = order.section_list;
			processVariables.set('validated', true);
		} else {
			processVariables.set('validated', false);
		}
	} catch(err) {
		processVariables.set('validated', false);
	}
	console.log(`Did validate-request. Set variable validated=${status}`);
	await taskService.complete(task, processVariables);
});

/* Booking Invalid */

bookEventWorker.subscribe('notify-failed-booking', async function({ task, taskService }) {
	console.log(`Did notify-failed-booking.`);
	await taskService.complete(task);
});

/* Booking Validated */

bookEventWorker.subscribe('create-order', async function({ task, taskService }) {
	// Invoke create order
	try {
		let response = await axios.post(restUrl+'/order', order);
		if(response.data.status === 'pending') {
			order_id = response.data.id;
		}
	} catch(err) {}
	console.log(`Did create-order.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('reserve-ticket', async function({ task, taskService }) {
    // Set variables
	let processVariables = new Variables();
	let status = true;
	// Invoke reserve ticket section
	try {
		let response = await axios.post(restUrl+'/ticket_section/capacity_add', section_list);
		if(response.data === true) {
			status = true;
			processVariables.set("validated", status);
		}
	} catch(err) {
		processVariables.set("validated", false);
	}
	console.log(`Did reserve-ticket. Status = ${status}`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('notify-order-detail', async function({ task, taskService }) {
	console.log(`Did notify-order-detail.`);
	await taskService.complete(task);
});

/* No Payment Request */

bookEventWorker.subscribe('cancel-order', async function({ task, taskService }) {
	try {
		let response = await axios.delete(restUrl+`/order/${order_id}`);
	} catch(err) {}
	console.log(`Did cancel-order.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('release-ticket', async function({ task, taskService }) {
	try {
		let response = await axios.post(restUrl+'/ticket_section/capacity_reduce', section_list);
	} catch(err) {}
	console.log(`Did release-ticket.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	console.log(`Did notify-booking-cancelled.`);
	await taskService.complete(task);
});

/* Payment Request Received */

bookEventWorker.subscribe('validate-payment-request', async function({ task, taskService }) {
	let processVariables = new Variables();
	processVariables.set('paymentValidated', true);
	console.log(`Did validate-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('send-payment-request', async function({ task, taskService }) {
	let processVariables = new Variables();
	processVariables.set('paymentSuccess', true);
	console.log(`Did send-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('notify-payment-success', async function({ task, taskService }) {
	console.log(`Did notify-payment-success.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('set-order-to-paid', async function({ task, taskService }) {
	try {
		let response = await axios.put(restUrl+`/order/${order_id}`);
	} catch(err) {}
	console.log(`Did set-order-to-paid.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('generate-tickets', async function({ task, taskService }) {
	try {
		let ticket = {
			order_id,
			section_list
		}
		let response = await axios.post(restUrl+`/ticket/`, ticket);
	} catch(err) {}
	console.log(`Did generate-tickets.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('notify-payment-booking-success', async function({ task, taskService }) {
	console.log(`Did notify-payment-booking-success.`);
	await taskService.complete(task);
});

module.exports = bookEventWorker;