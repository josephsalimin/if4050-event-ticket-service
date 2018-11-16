let { Client, logger, Variables } = require('camunda-external-task-client-js');
let config = { baseUrl: 'http://localhost:8080/engine-rest' };

// create a Client instance with custom configuration
let client = new Client(config);

client.subscribe('validate-booking-request', async function({ task, taskService }) {
	/* TODO: Invoke validate event endpoint */

  	// Set variables
	let processVariables = new Variables();
	processVariables.set("validated", true);
	processVariables.set("paid", true);

	console.log(`Did validate-request. Set variable validated=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

client.subscribe('notify-unsuccessful-booking', async function({ task, taskService }) {
	console.log(`Did notify-unsuccessful-booking.`);

	// Complete the task
	await taskService.complete(task);
});

client.subscribe('refund-payment', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);
	processVariables.set("message", "refund-notification");

	console.log(`Did refund-payment. Set variable success=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

client.subscribe('notify-order-detail', async function({ task, taskService }) {
    // let processVariables = new Variables();
    // processVariables.set("invoiceCreated", true);
	console.log(`Did notify-order-detail`);
	// Complete the task
	await taskService.complete(task);
});

client.subscribe('send-invoice-request', async function({ task, taskService }) {
    let processVariables = new Variables();
    processVariables.set("invoiceCreated", true);

	console.log(`Did send-invoice-request. Set variable invoice_created=${true}`);
	// Complete the task
	await taskService.complete(task, processVariables);
});

// console.log(client);

client.start();