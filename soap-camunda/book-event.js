let axios = require('axios');
let baseUrl = 'http://localhost:8080/engine-rest';
let restUrl = 'https://0b8d2e5c.ngrok.io';
let ticketUrl = restUrl;
let orderUrl = restUrl;
let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';
let { Client, logger, Variables } = require('camunda-external-task-client-js');

// create a Client instance with custom configuration
let config = { baseUrl };
let camundaClient = new Client(config);
axios.defaults.headers.common['Authorization'] = jwtKey;

// Set section list
let section_list = [
	{
		id: 4,
		quantity: 10,
	}
]
// Set order data
let order = {
	user_id: 1,
	total_price: 50000,
	section_list
}
let order_id;
// Set ticket reserver
let reserve = {
	section_list
} 
// Set ticket data
let ticket = {
	order_id: -1,
	section_list
}

camundaClient.subscribe('validate-booking-request', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	let status = false;
	// Invoke create order
	try {
		let response = await axios.post(orderUrl+'/order', order);
		if(response.data.status === 'pending') {
			order_id = response.data.id;
			status = true;
			processVariables.set("validated", status);
		}
	} catch(err) {
		processVariables.set("validated", false);
		throw(err);
	}
	console.log(task.id);
	console.log(`Did validate-request. Set variable validated=${status}`);

	await taskService.complete(task, processVariables);
});

/* Booking Invalidated */

camundaClient.subscribe('notify-failed-booking', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did notify-failed-booking.`);
	await taskService.complete(task);
});

/* Booking Validated */

camundaClient.subscribe('reserve-ticket', async function({ task, taskService }) {
    // Set variables
	let processVariables = new Variables();
	let status = false;
	// Invoke reserve ticket section
	try {
		let response = await axios.post(ticketUrl+'/ticket_section/capacity_add', reserve);
		if(response.data === true) {
			status = true;
			processVariables.set("validated", status);
		}
	} catch(err) {
		console.log(err);
		processVariables.set("validated", false);
	}
	console.log(task.id);
	console.log(`Did reserve-ticket. Status = ${status}`);
	await taskService.complete(task);
});

camundaClient.subscribe('notify-order-detail', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did notify-order-detail.`);
	await taskService.complete(task);
});

/* No Payment Request */

camundaClient.subscribe('cancel-order', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did cancel-order.`);
	await taskService.complete(task);
});

camundaClient.subscribe('release-ticket', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did release-ticket.`);
	await taskService.complete(task);
});

camundaClient.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did notify-booking-cancelled.`);
	await taskService.complete(task);
});

/* Payment Request Success */

camundaClient.subscribe('validate-payment-request', async function({ task, taskService }) {
	let processVariables = new Variables();
	processVariables.set('paymentValidated', true);
	console.log(task.id);
	console.log(`Did validate-payment-request.`);
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('send-payment-request', async function({ task, taskService }) {
	let processVariables = new Variables();
	processVariables.set('paymentSuccess', true);
	console.log(task.id);
	console.log(`Did send-payment-request.`);
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('send-invoice-request', async function({ task, taskService }) {
    let processVariables = new Variables();
	processVariables.set("invoiceCreated", true);
	console.log(task.id);
	console.log(`Did send-invoice-request with id ${task.id}. Set variable invoice_created=${true}`);
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('notify-payment-success', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did notify-payment-success.`);
	await taskService.complete(task);
});

camundaClient.subscribe('set-order-to-paid', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did set-order-to-paid.`);
	await taskService.complete(task);
});

camundaClient.subscribe('generate-tickets', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did generate-tickets.`);
	await taskService.complete(task);
});

camundaClient.subscribe('notify-payment-booking-success', async function({ task, taskService }) {
	console.log(task.id);
	console.log(`Did notify-payment-booking-success.`);
	await taskService.complete(task);
});

// camundaClient.start();