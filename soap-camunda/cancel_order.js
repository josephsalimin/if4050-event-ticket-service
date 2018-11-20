let { Client, logger, Variables } = require('camunda-external-task-client-js');
let config = { baseUrl: 'http://localhost:8080/engine-rest' };

// create a Client instance with custom configuration
let client = new Client(config);

client.subscribe('validate-request', async function({ task, taskService }) {
	/* TODO: Invoke validate event endpoint */

  	// Set variables
	let processVariables = new Variables();
	processVariables.set("validated", true);
	processVariables.set("paid", true);

	console.log(`Did validate-request. Set variable validated=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

client.subscribe('notify-cancel-booking-failed', async function({ task, taskService }) {
	console.log(`Did notify-cancel-booking-failed.`);

	// Complete the task
	await taskService.complete(task);
});

client.subscribe('check-order-status', async function({ task, taskService }) {
	console.log(`Did check-order-status.`);

	// Complete the task
	await taskService.complete(task);
});

client.subscribe('refund-payment', async function({ task, taskService }) {
	/* TODO: Invoke payment service - refund payment */

	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);
	processVariables.set("message", "refund-notification");

	console.log(`Did refund-payment. Set variable success=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

client.subscribe('cancel-order', async function({ task, taskService }) {
	console.log(`Did cancel-order`);
	// Complete the task
	await taskService.complete(task);
});

client.subscribe('release-ticket', async function({ task, taskService }) {
	console.log(`Did release-ticket`);
	// Complete the task
	await taskService.complete(task);
});

client.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	console.log(`Did notify-booking-cancelled`);
	// Complete the task
	await taskService.complete(task);
});

// console.log(client);

client.start();