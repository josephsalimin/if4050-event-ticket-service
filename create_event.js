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

	console.log(`Did validate-request. Set variable validated=${true}`);

	soap.createClient(wsdl_url, (err, client) => {
		let args = {
		"event": {
			"id": 1,
			"name": "Biji",
			"location": "Jakarta",
			"partner_id": 1,
			"start_at": 2,
			"end_at": 3,
			"description": "Festival Biji Jakarta"
		},
			"section_list": []
		};
		let section = {
			"Section": {
				"id": 1,
				"name": "Hehe",
				"event_id": 1,
				"capacity": 100,
				"price": 500000,
				"has_seat": true
			}
		};
		args.section_list.push(section);
		console.log(args);

		client.CreateEvent(args, function(err, result) {
			console.log(result.CreateEventResult);
		});
    });

    // Complete the task
    await taskService.complete(task, processVariables);
});

camundaClient.subscribe('add-event', async function({ task, taskService }) {
	console.log(`Did add-event`);

	//console.log(`Set process variables with amount $${amount} and item ${item}`);

	// Complete the task
	await taskService.complete(task);
});

// camundaClient.start();
// var exports = module.exports = {};
// exports.camundaClient = camundaClient;