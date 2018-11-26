let axios = require('axios');
let { Client, Variables } = require('camunda-external-task-client-js');

const baseUrl = 'http://localhost:8080/engine-rest';
const restUrl = 'http://localhost:5050';

// create a Client instance with custom configuration
let config = { baseUrl };
let bookEventWorker = new Client(config);
let axiosOptions = {}, instance;

function validateRequest(sectionList, userID) {
	for (let section of sectionList) {
		sectionValidate = section.hasOwnProperty("id") &&
						  section.hasOwnProperty("price") &&
						  section.hasOwnProperty("quantity") 
		if (!sectionValidate) break;
	}
	return userID && sectionValidate;
}

bookEventWorker.subscribe('validate-booking-request', async function({ task, taskService }) {
	// Set process variables
	let processVariables = new Variables();
	// Get all variables
	let userID = task.variables.get('user_id');
	let sectionList = task.variables.get('section_list');
	let callbackURL = task.variables.get("callback_url");
	let authKey = task.variables.get("auth_key");
	let status = false, error = "Error";

	if (userID && sectionList && callbackURL && authKey) {
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		instance = axios.create(axiosOptions);
		try {
			sectionList = await JSON.parse(sectionList);
			if (validateRequest(sectionList.section_list, userID)) {
				let response = await instance.post(`${restUrl}/ticket_section/validation`, sectionList);
				if (response.data === true) {
					sectionList = sectionList.section_list;
					processVariables.set("user_id", userID);
					processVariables.set("section_list", sectionList);
					processVariables.set("auth_key", authKey);
					processVariables.set("callback_url", callbackURL);
					status = true;
				}
			}
		} catch (err) {
			error = err.message;
			console.log(error);
		}
	}
	processVariables.set("validated", status);
	if (!status) processVariables.set("message_error", error);
	console.log(`Did validate-request. Set variable validated=${status}`);
	await taskService.complete(task, processVariables);
});

/* Booking Validated */
bookEventWorker.subscribe('calculate-order', async function({ task ,taskService}) {
	// Invoke create order
	let sectionList = task.variables.get('section_list');
	let userID = task.variables.get('user_id');
	// Set Process Variables
	let processVariables = new Variables();
	let totalPrice = 0;
	for (let section of sectionList) {
		totalPrice += (parseInt(section.quantity) * parseInt(section.price));
	}
	let order = {
		'user_id': userID,
		'total_price': totalPrice,
		'section_list': sectionList
	};
	console.log(order);
	processVariables.set('order', order);
	await taskService.complete(task, processVariables);

}); 

bookEventWorker.subscribe('create-order', async function({ task, taskService }) {
	// Invoke create order
	let processVariables = new Variables();
	let order = task.variables.get('order');
	let response = await instance.post(restUrl + '/order', order);
	processVariables.set('order_id', response.data.id);
	console.log(`Did create-order.`);
	await taskService.complete(task, processVariables);
});

/* Reserve Ticket */
bookEventWorker.subscribe('reserve-ticket', async function({ task, taskService }) {
  // Set variables
	let processVariables = new Variables();
	let status = true;
	// Get variables
	let section_list = task.variables.get('section_list');
	section_list = {
		"section_list": section_list
	};
	// Invoke reserve ticket section
	let response = await instance.post(restUrl + '/ticket_section/capacity_add', section_list);
	console.log(`Did reserve-ticket. Status = ${response.data}`);
	await taskService.complete(task, processVariables);
});

/* No Payment Request */
bookEventWorker.subscribe('cancel-booking', async function({ task, taskService }) {
	let order_id = task.variables.get('order_id');
	console.log(order_id);
	console.log(restUrl+`/order/${order_id}`);
	let response = await instance.delete(restUrl+`/order/${order_id}`);
	console.log(`Did cancel-booking.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('release-event-ticket', async function({ task, taskService }) {
	let section_list = task.variables.get('section_list');
	section_list = {
		"section_list": section_list
	};
	let response = await instance.post(restUrl+'/ticket_section/capacity_reduce', section_list);
	console.log(`Did release-event-ticket.`);
	await taskService.complete(task);
});

/* Payment Request Received */
bookEventWorker.subscribe('validate-payment-request', async function({ task, taskService }) {
	// TODO: validate
	let order_id = task.variables.get('order_id');
	let response = await instance.get(`${restUrl}/order/${order_id}`);
	let processVariables = new Variables();
	processVariables.set('paymentValidated', true);
	if (response.data.status === 'cancelled') {
		processVariables.set('paymentValidate', false);
	}
	console.log(`Did validate-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('send-payment-request', async function({ task, taskService }) {
	// TODO: SOAP
	let processVariables = new Variables();
	// processVariables.set('paymentSuccess', true);
	console.log(`Did send-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('check-payment-response', async function({ task, taskService }) {
	// TODO: check input
	let processVariables = new Variables();
	processVariables.set('paymentSuccess', true)
	console.log(`Did check-payment-response.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('set-order-to-paid', async function({ task, taskService }) {
	let order_id = task.variables.get('order_id');
	let response = await instance.put(restUrl+`/order/${order_id}`);
	console.log(`Did set-order-to-paid.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('generate-tickets', async function({ task, taskService }) {
	let order_id = task.variables.get('order_id');
	let section_list = task.variables.get('section_list');
	let ticket = {order_id, section_list}
	let response = await instance.post(restUrl+`/ticket/`, ticket);
	console.log(`Did generate-tickets.`);
	await taskService.complete(task);
});

/* Booking Invalid */
bookEventWorker.subscribe('notify-failed-booking', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	console.log(`Did notify-failed-booking.`);
	await taskService.complete(task);
});

/* Notify Order */
bookEventWorker.subscribe('notify-order-detail', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	console.log(`Did notify-order-detail.`);
	await taskService.complete(task);
});

/* Notify Booking Cancelled */
bookEventWorker.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	console.log(`Did notify-booking-cancelled.`);
	await taskService.complete(task);
});

/* Notify Booking Success */
bookEventWorker.subscribe('notify-payment-booking-success', async function({ task, taskService }) {
	let callbackURL = task.variables.get("callback_url");
	console.log(`Did notify-payment-booking-success.`);
	await taskService.complete(task);
});

module.exports = bookEventWorker;