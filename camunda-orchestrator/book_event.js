let axios = require('axios');
let { Client, Variables } = require('camunda-external-task-client-js');

const baseUrl = 'http://localhost:8080/engine-rest';
const restUrl = 'http://localhost:5050';

// create a Client instance with custom configuration
let config = { baseUrl };
let bookEventWorker = new Client(config);
let axiosOptions = {}, instance;

function validateRequest(event) {
	let eventValidate = event.hasOwnProperty("user_id") && 
						event.hasOwnProperty('total_price') &&
						event.hasOwnProperty("location") &&
						event.hasOwnProperty("start_at") &&
						event.hasOwnProperty("end_at");
	let sectionValidate = event.hasOwnProperty('section_list');
	for (let section of sectionList) {
		sectionValidate = section.hasOwnProperty("name") &&
						  section.hasOwnProperty("price") &&
						  section.hasOwnProperty("capacity") &&
						  section.hasOwnProperty("has_seat")
		if (!sectionValidate) break;
	}
	return eventValidate && sectionValidate;
}

bookEventWorker.subscribe('validate-booking-request', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	// Get all variables
	let order = task.variables.get('order');
	let callbackURL = task.variables.get("callback_url");
	let authKey = task.variables.get("auth_key");
	let status = false, error = "Error", response;
	// Running
	if(order && callbackURL && authKey) {
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		instance = axios.create(axiosOptions);
		try {
			order = await JSON.parse(order);
			if(validateRequest(order)) {
				processVariables.set("order", order);
				processVariables.set("section_list", order.section_list);
				processVariables.set("auth_key", authKey);
				processVariables.set("callback_url", callbackURL);
				processVariables.set('validated', true);
			} else {
				processVariables.set('validated', false);
			}
		} catch(err) {
			error = err.message;
		}
	}
	if (!status) processVariables.set("message_error", error);
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
	let processVariables = new Variables();
	let order = task.variables.get('order');
	try {
		let response = await instance.post(restUrl+'/order', order);
		if(response.data.status === 'pending') {
			processVariables.set('order_id', response.data.id);
		}
	} catch(err) {}
	console.log(`Did create-order.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('reserve-ticket', async function({ task, taskService }) {
    // Set variables
	let processVariables = new Variables();
	let status = true;
	// Get variables
	let section_list = task.variables.get('section_list');
	// Invoke reserve ticket section
	try {
		let response = await instance.post(restUrl+'/ticket_section/capacity_add', section_list);
		if(response.data === true) {
			status = true;
			processVariables.set("validated", status);
		}
	} catch(err) {
		processVariables.set("validated", false);
	}
	console.log(`Did reserve-ticket. Status = ${status}`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('notify-order-detail', async function({ task, taskService }) {
	console.log(`Did notify-order-detail.`);
	await taskService.complete(task);
});

/* No Payment Request */

bookEventWorker.subscribe('cancel-order', async function({ task, taskService }) {
	let order_id = task.variables.get('order_id');
	try {
		let response = await instance.delete(restUrl+`/order/${order_id}`);
	} catch(err) {}
	console.log(`Did cancel-order.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('release-ticket', async function({ task, taskService }) {
	let section_list = task.variables.get('section_list');
	try {
		let response = await instance.post(restUrl+'/ticket_section/capacity_reduce', section_list);
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
	let order_id = task.variables.get('order_id');
	try {
		let response = await instance.put(restUrl+`/order/${order_id}`);
	} catch(err) {}
	console.log(`Did set-order-to-paid.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('generate-tickets', async function({ task, taskService }) {
	let order_id = task.variables.get('order_id');
	let section_list = task.variables.get('section_list');
	try {
		let ticket = {
			order_id,
			section_list
		}
		let response = await instance.post(restUrl+`/ticket/`, ticket);
	} catch(err) {}
	console.log(`Did generate-tickets.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('notify-payment-booking-success', async function({ task, taskService }) {
	console.log(`Did notify-payment-booking-success.`);
	await taskService.complete(task);
});

module.exports = bookEventWorker;