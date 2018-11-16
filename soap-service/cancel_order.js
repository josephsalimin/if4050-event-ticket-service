let soap = require('soap');
let { Client, logger, Variables } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
let config = { baseUrl: 'http://localhost:8080/engine-rest' };

// create a Client instance with custom configuration
let camundaClient = new Client(config);

camundaClient.subscribe('validate-request', async function({ task, taskService }) {
  	// Set variables
	let processVariables = new Variables();
	processVariables.set("amount", 1020);
	processVariables.set("item", "item-baru");
	processVariables.set("validated", true);

	console.log(`Did validate-request. Set variable validated=${true}`);

	soap.createClient('http://localhost:8000/?wsdl', (err, client) => {
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

  //console.log(`Set process variables with amount $${amount} and item ${item}`);

  // Complete the task
  await taskService.complete(task, processVariables);
});

camundaClient.subscribe('refund-payment', async function({ task, taskService }) {
	// Set variables
	let processVariables = new Variables();
	processVariables.set("success", true);

	console.log(`Did refund-payment. Set variable success=${true}`);

	//console.log(`Set process variables with amount $${amount} and item ${item}`);

	// Complete the task
	await taskService.complete(task, processVariables);
});

camundaClient.subscribe('cancel-order', async function({ task, taskService }) {
	console.log(`Did cancel-order`);

	//console.log(`Set process variables with amount $${amount} and item ${item}`);

	// Complete the task
	await taskService.complete(task);
});

camundaClient.subscribe('release-ticket', async function({ task, taskService }) {
	console.log(`Did release-ticket`);

	//console.log(`Set process variables with amount $${amount} and item ${item}`);

	// Complete the task
	await taskService.complete(task);
});


// // susbscribe to the topic: 'charge-card'
// camundaClient.subscribe('charge-card', async function({ task, taskService }) {
//   // Put your business logic here

//   // Get a process variable
//   let amount = task.variables.get('amount');
//   let item = task.variables.get('item');

//   console.log(`Charging credit card with an amount of ${amount}€ for the item '${item}'...`);

//   // Complete the task
//   await taskService.complete(task);
// });

//console.log(camundaClient);

camundaClient.start();
// var exports = module.exports = {};
// exports.camundaClient = camundaClient;

// soap.createClient('http://localhost:8000/?wsdl', (err, client) => {
// 	let args = {
// 	"event": {
// 		"id": 1,
// 		"name": "Biji",
// 		"location": "Jakarta",
// 		"partner_id": 1,
// 		"start_at": 2,
// 		"end_at": 3,
// 		"description": "Festival Biji Jakarta"
// 	},
// 		"section_list": []
// 	};
// 	let section = {
// 		"Section": {
// 			"id": 1,
// 			"name": "Hehe",
// 			"event_id": 1,
// 			"capacity": 100,
// 			"price": 500000,
// 			"has_seat": true
// 		}
// 	};
// 	args.section_list.push(section);
// 	console.log(args);

// 	client.CreateEvent(args, function(err, result) {
//         console.log(result.CreateEventResult);
//     });
// });