let axios = require('axios');
let baseUrl = 'http://localhost:8080/engine-rest';
let ticketUrl = 'https://0c7af3cf.ngrok.io';
let orderUrl = 'https://1c856d79.ngrok.io';
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
		throw err;
		processVariables.set("validated", false);
	}

	console.log(`Did validate-request. Set variable validated=${status}`);

	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('notify-unsuccessful-booking', async function({ task, taskService }) {
	console.log(`Did notify-unsuccessful-booking.`);
	await taskService.complete(task);
});

camundaClient.subscribe('refund-payment', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);
	console.log(`Did refund-payment. Set variable success=${true}`);
	await taskService.complete(task, processVariables);
});

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

	console.log(`Did reserve-ticket. Status = ${status}`);
	await taskService.complete(task);
});

camundaClient.subscribe('send-invoice-request', async function({ task, taskService }) {
    let processVariables = new Variables();
    processVariables.set("invoiceCreated", true);
	console.log(`Did send-invoice-request with id ${task.id}. Set variable invoice_created=${true}`);
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('show-invoice-detail', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	let status = false;
	// Invoke reserve ticket section
	try {
		ticket.order_id = order_id;
		let response = await axios.post(ticketUrl+'/ticket', ticket);
		if(response.data[0].order_id === order_id) {
			status = true;
		}
	} catch(err) {
		throw err;
	}
    
	console.log(`Did show-invoice-detail`);
	await taskService.complete(task);
});

// camundaClient.start();