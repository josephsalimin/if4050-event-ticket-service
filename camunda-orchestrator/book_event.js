let axios = require('axios');
let { Client, Variables } = require('camunda-external-task-client-js');
let payment = require('./payment-wrapper');

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
	let callback = task.variables.get("callback");
	let callbackType = task.variables.get("callback_type");
	let authKey = task.variables.get("auth_key");
	let status = false, error = "Error";

	if (userID && sectionList && callback && callbackType && authKey) {
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		instance = axios.create(axiosOptions);
		try {
			sectionList = await JSON.parse(sectionList);
			if (validateRequest(sectionList.section_list, userID)) {
				let response = await instance.post(`${restUrl}/ticket_section/validation`, sectionList);
				if (response.data === true) {
					sectionList = sectionList.section_list;
					processVariables.set("section_list", sectionList);
					status = true;
				}
			}
		} catch (err) {
			error = err.message;
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
	let processVariables = new Variables();
	let response = await instance.delete(restUrl+`/order/${order_id}`);
	processVariables.set("mesasage_error", "Order has been cancelled: reason exceed time limit");
	console.log(`Did cancel-booking.`);
	await taskService.complete(task, processVariables);
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
	let orderIDPymt = task.variables.get('order_id_pymt');
	let callbackPymt = task.variables.get('callback_pymt');
	let callbackPymtType = task.variables.get('callback_pymt_type');
	let method = task.variables.get('payment_method');
	let status = false, error = 'Request not validated';
	let processVariables = new Variables();
	if (orderIDPymt && callbackPymt && callbackPymtType && method) {
		try {
			let response = await instance.get(`${restUrl}/order/${orderIDPymt}`);
			status = true;
			if (response.data.status === 'cancelled') {
				status = false
			}
		} catch (e) {
			error = e.message;
		}
	}
	if (!status) processVariables.set('message_error', error);
	processVariables.set('paymentValidated', status);
	console.log(`Did validate-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('send-payment-request', async function({ task, taskService }) {
	let processVariables = new Variables();
	let method = task.variables.get('payment_method');
	let order = task.variables.get('order');
	// let res = await beginPayment(method, order.total_price);
	// processVariables.set('payment_id', res.paymentId);
	// let loop = true;
	// while (loop) {
	// 	let res = await getPaymentEvents(res.paymentId);
	// 	if (res.lastEventId) {
	// 		let events = res.events;
	// 		processVariables.set('last_event_id', res.lastEventId);
	// 		if (events[0].type === 'OPEN_URL') {
	// 			processVariables.set('payment_type', 'url');
	// 			processVariables.set('payment_data', events[0].urlToOpen);
	// 		} else {
	// 			processVariables.set('payment_type', 'acc');
	// 			processVariables.set('payment_data', events[0].accountNumber);
	// 		}
	// 		loop = false;
	// 	}
	// }
	console.log(`Did send-payment-request.`);
	await taskService.complete(task, processVariables);
});

bookEventWorker.subscribe('notify-payment-invoice', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	console.log(`Did notify-payment-invoice.`);
	await taskService.complete(task);
});

bookEventWorker.subscribe('wait-payment', async function({ task, taskService }) {
	let lastEventId = task.variables.get('last_event_id');
	let paymentId = task.variables.get('payment_id');
	let loop = true;
	let processVariables = new Variables();
`	while (loop) {
		let res = await getPaymentEvents(paymentId, lastEventId);
		let lastId = res.lastEventId;
		let events = res.events;
		if (events) {
			let event = events.find(x => (x.paymentEventId === lastId));
			if (event.type === 'SUCCESS') {
				processVariables.set('paymentSuccess', true);
				loop = false;
			} else if (event.type === 'FAILURE') {
				processVariables.set('paymentSuccess', false);
				loop = false;
			}
		}
	}`
	processVariables.set('paymentSuccess', true);
	console.log(`Did wait-payment.`);
	await taskService.complete(task, processVariables);
});

/* Payment Success */
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
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let error = task.variables.get("message_error");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"message": error
		});
	}
	console.log(`Did notify-failed-booking.`);
	await taskService.complete(task);
});

/* Notify Order */
bookEventWorker.subscribe('notify-order-detail', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let order = task.variables.get("order");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"order": order 
		});
	}
	console.log(`Did notify-order-detail.`);
	await taskService.complete(task);
});

/* Notify Booking Cancelled */
bookEventWorker.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let error = task.variables.get("message_error");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"message": error
		});
	}
	console.log(`Did notify-booking-cancelled.`);
	await taskService.complete(task);
});

/* Notify Booking Success */
bookEventWorker.subscribe('notify-payment-booking-success', async function({ task, taskService }) {
	let callbackType = task.variables.get("callback_type");
	let callback = task.variables.get("callback");
	let order = task.variables.get("order");
	if (callbackType === 'url') {
		await axiosInstance.post(callback, {
			"order": order 
		});
	}
	console.log(`Did notify-payment-booking-success.`);
	await taskService.complete(task);
});

module.exports = bookEventWorker;