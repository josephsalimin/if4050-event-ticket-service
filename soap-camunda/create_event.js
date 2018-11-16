let soap = require('soap');
let wsdl_url = 'http://localhost:8000/?wsdl';
let { Client, logger, Variables } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
let config = { baseUrl: 'http://localhost:8080/engine-rest' };

// create a Client instance with custom configuration
let camundaClient = new Client(config);

camundaClient.subscribe('validate-event-detail', async function({ task, taskService }) {
  	// Set variables
	let processVariables = new Variables();
	processVariables.set("validated", true);

	console.log(`Did validate-event-detail. Set variable validated=${true}`);

    // Complete the task
    await taskService.complete(task, processVariables);
});

camundaClient.subscribe('add-event', async function({ task, taskService }) {
	console.log(`Did add-event`);
	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('issue-ticket', async function({ task, taskService }) {
	console.log(`Did issue-ticket`);
	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('notify-partner', async function({ task, taskService }) {
	console.log(`Did notify-partner`);
	// Complete the task
	await taskService.complete(task);
});

camundaClient.start();