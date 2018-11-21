let axios = require('axios');
let restUrl = 'http://localhost:5050';
let baseUrl = 'http://localhost:8080/engine-rest';
// let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';
let { Client, Variables } = require('camunda-external-task-client-js');
// Set up configs
let config = { baseUrl };
let createEventWorker = new Client(config);
let axiosOptions = {};
let instance;

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
	let event = task.variables.get("event");
	let sectionList = task.variables.get("section_list");
	let callbackURL = task.variables.get("callback_url");
	let authKey = task.variables.get("auth_key");
	let processVariables = new Variables();
	let status = false, error = "Error", response;
	// Running
	if (event && sectionList && callbackURL && authKey) {	
		axiosOptions.headers = {'Authorization': authKey, 'Content-Type': 'application/json'};
		instance = axios.create(axiosOptions);
		try {
			event = await JSON.parse(event);
			sectionList = await JSON.parse(sectionList);
			if (validateRequest(event, sectionList) && event.start_at < event.end_at) {
				response = await instance.get(`${restUrl}/partner/${event.partner_id}`, {});
				if (response.status == 200) {
					response = await instance.get(`${restUrl}/event/partner`);
					processVariables.set("event", event);
					processVariables.set("auth_key", authKey);
					processVariables.set("section_list", sectionList);
					processVariables.set("callback_url", callbackURL);
					processVariables
					status = true;
				}
			}
		} catch (err) {
			error = err.message
		}
	}
	if (!status) processVariables.set("message_error", error);
	// Set validated
	processVariables.set("validated", status);
	console.log(`Did validate-event-detail. Set variable validated = ${status}`);
  await taskService.complete(task, processVariables);
});

createEventWorker.subscribe('add-event', async function({ task, taskService }) {
	let event = task.variables.get("event");
	let processVariables = new Variables();
	let success = false, error = "Error", response;

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
	let event = task.variables.get("event");
	let sectionList = task.variables.get("section_list");
	let processVariables = new Variables();
	let success = false;
	let error = "Error";
	let response;

	try {
		let payload = {
			"event_id": event.id,
			"section_list": sectionList
		}
		response = await instance.post(`${restUrl}/ticket_section/`, payload);
		if (response.status < 400) {
			success = response.data;
			console.log(success);
		} 
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