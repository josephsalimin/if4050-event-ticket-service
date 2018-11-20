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

camundaClient.subscribe('validate-request', async function({ task, taskService }) {
	/* TODO: Invoke validate event endpoint */

  	// Set variables
	let processVariables = new Variables();
	processVariables.set("validated", true);
	processVariables.set("paid", false);

	console.log(`Did validate-request. Set variable validated=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('notify-cancel-booking-failed', async function({ task, taskService }) {
	console.log(`Did notify-cancel-booking-failed.`);

	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('check-order-status', async function({ task, taskService }) {
  	// Set variables
	let processVariables = new Variables();
	// processVariables.set("paid", true);

	console.log(`Did check-order-status.`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('unpaid-checking', async function({ task, taskService }) {
	// Set variables
  let processVariables = new Variables();
  processVariables.set("cancelled", true);

  console.log(`Did unpaid-checking.`);

  // Complete the task
  await taskService.complete(task, processVariables);
});


// camundaClient.subscribe('check-order-status', async function({ task, taskService }) {
// 	let processVariables = new Variables();
// 	processVariables.set("paid", true);

// 	console.log(`Did check-order-status.`);

// 	// Complete the task
// 	await taskService.complete(task, processVariables);
// });

camundaClient.subscribe('refund-payment', async function({ task, taskService }) {
	/* TODO: Invoke payment service - refund payment */

	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);
	processVariables.set("message", "refund-notification");

	console.log(`Did refund-payment. Set variable success=${true}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('cancel-order', async function({ task, taskService }) {
	console.log(`Did cancel-order`);
	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('release-ticket', async function({ task, taskService }) {
	console.log(`Did release-ticket`);
	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('notify-booking-cancelled', async function({ task, taskService }) {
	console.log(`Did notify-booking-cancelled`);
	// Complete the task
	await taskService.complete(task);
});

// console.log(client);

// client.start();