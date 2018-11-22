let axios = require('axios');
let { Client, Variables } = require('camunda-external-task-client-js');

const restUrl = 'http://localhost:5050';
const baseUrl = 'http://localhost:8080/engine-rest';

// Create a Client instance with custom configuration
let config = { baseUrl };
let createEventWorker = new Client(config);
let axiosOptions = {}, instance;

function validateRequest(event, sectionList) {
	let eventValidate = event.hasOwnProperty("partner_id") && 
											event.hasOwnProperty("name") && 
											event.hasOwnProperty("location") &&
											event.hasOwnProperty("start_at") &&
											event.hasOwnProperty("end_at");
	let sectionValidate = true;
	for (let section of sectionList) {
		sectionValidate = section.hasOwnProperty("name") &&
											section.hasOwnProperty("price") &&
											section.hasOwnProperty("capacity") &&
											section.hasOwnProperty("has_seat")
		if (!sectionValidate) break;
	}
	return sectionValidate && eventValidate;
}

createEventWorker.subscribe('validate-event-detail', async function({ task, taskService }) {
	// Get all variables
	let event = task.variables.get("event");
	let sectionList = task.variables.get("section_list");
	let callbackURL = task.variables.get("callback_url");
	let authKey = task.variables.get("auth_key");
	let status = false, error = "Error", response;
	// Set Process Variables
	let processVariables = new Variables();
	// Running
	if (event && sectionList && callbackURL && authKey) {	
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		instance = axios.create(axiosOptions);
		try {
			event = await JSON.parse(event);
			sectionList = await JSON.parse(sectionList);
			if (validateRequest(event, sectionList) && event.start_at < event.end_at) {
				response = await instance.get(`${restUrl}/partner/${event.partner_id}`);
				if (response.status == 200) {
					processVariables.set("event", event);
					processVariables.set("auth_key", authKey);
					processVariables.set("section_list", sectionList);
					processVariables.set("callback_url", callbackURL);
					status = true;
				}
			}
		} catch (err) {
			error = err.message
		}
	}
	if (!status) processVariables.set("message_error", error);
	processVariables.set("validated", status);
	console.log(`Did validate-event-detail. Set variable validated = ${status}`);
  	await taskService.complete(task, processVariables);
});

createEventWorker.subscribe('add-event', async function({ task, taskService }) {
	// Get all variables
	let event = task.variables.get("event");
	let success = false, error = "Error", response;
	// Set Process Variables
	let processVariables = new Variables();

	try {
		response = await instance.post(`${restUrl}/event/`, event);
		success = true;
		processVariables.set("event", response.data);
	} catch (err) {
		error = err.message;
	}
	if (!success) processVariables.set("message_error", error);
	processVariables.set("success", success);
	console.log('Did add-event');
	await taskService.complete(task, processVariables);
});

createEventWorker.subscribe('issue-ticket', async function({ task, taskService }) {
	// Get all variables
	let event = task.variables.get("event");
	let sectionList = task.variables.get("section_list");
	let success = false, error = "Error", response;
	// Set process variables
	let processVariables = new Variables();
	try {
		let payload = {"event_id": event.id, "section_list": sectionList}
		response = await instance.post(`${restUrl}/ticket_section/`, payload);
		if (response.status < 400) success = response.data;
	} catch (err) {
		error = err.message;
	}
	if (!success) processVariables.set("message_error", error);
	processVariables.set("success", success);
	console.log(`Did issue-ticket`);
	await taskService.complete(task, processVariables);
});

createEventWorker.subscribe('delete-event', async function({ task, taskService}) {
	let event = task.variables.get("event");
	try {
		await instance.delete(`${restUrl}/event/${event.id}`);
	} catch (err) {
		console.log(err);
	}
	await taskService.complete(task, processVariables);
});

createEventWorker.subscribe('notify-partner', async function({ task, taskService }) {
	console.log(`Did notify-partner`);
	await taskService.complete(task);
});

createEventWorker.subscribe('notify-failed-event', async function({ task, taskService }) {
	console.log(`Did notify-failed-event`);
	let msgError = task.variables.get("message_error");
	console.log(msgError);
	await taskService.complete(task);
});

module.exports = createEventWorker;