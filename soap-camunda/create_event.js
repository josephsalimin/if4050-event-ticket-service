let axios = require('axios');
let restUrl = 'https://0b8d2e5c.ngrok.io';
let baseUrl = 'http://localhost:8080/engine-rest';
let eventUrl = restUrl;
let ticketUrl = restUrl;
let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';
let { Client, Variables } = require('camunda-external-task-client-js');

// Set up some configs
let config = { baseUrl };
let camundaClient = new Client(config);
axios.defaults.headers.common['Authorization'] = jwtKey;

// Set event data to be created
let data = {
	partner_id: 1,
	name: 'Event Baru Nehhhhhh',
	location: 'ITB Unpad',
	start_at: 1,
	end_at: 2
};
let tickets = {
	event_id: -1,
	section_list: [
		{
			name: "Big",
			price: 9999,
			capacity: 9999,
			has_seat: false
		},
		{
			name: "Small",
			price: 222,
			capacity: 22,
			has_seat: false
		}
	]
}
let event_id;

camundaClient.subscribe('validate-event-detail', async function({ task, taskService }) {
	let processVariables = new Variables();
	let status = true;

	processVariables.set("validated", status);
	console.log(`Did validate-event-detail. Set variable validated = ${status}`);
    await taskService.complete(task, processVariables);
});

camundaClient.subscribe('add-event', async function({ task, taskService }) {
	let response;
	// try {
	// 	response = await axios.post(eventUrl+'/event', data);
	// 	event_id = response.data.id;
	// } catch(err) {
	// 	throw err;
	// }
	// console.log(`Did add-event with event-name = ${response.data.name}`);
	console.log('Did add-event');
	await taskService.complete(task);
});

camundaClient.subscribe('issue-ticket', async function({ task, taskService }) {
	let response;
	// try {
	// 	tickets.event_id = event_id;
	// 	console.log(tickets);
	// 	response = await axios.post(ticketUrl+'/ticket_section', tickets);
	// } catch(err) {
	// 	throw err;
	// }
	console.log(`Did issue-ticket`);
	await taskService.complete(task);
});

camundaClient.subscribe('notify-partner', async function({ task, taskService }) {
	console.log(`Did notify-partner`);
	await taskService.complete(task);
});

camundaClient.subscribe('notify-failed-event', async function({ task, taskService }) {
	console.log(`Did notify-failed-event`);
	await taskService.complete(task);
});

// camundaClient.start();