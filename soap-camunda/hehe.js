// import 'whatwg-fetch'
let axios = require('axios');
let https = require('https');
let eventUrl = 'https://1e0818c2.ngrok.io/event/1';
let jwtKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwicGFydG5lcl9pZCI6MCwibmFtZSI6InRpY2tldHgiLCJhdXRoX3R5cGUiOiJtYXN0ZXIiLCJ0aW1lc3RhbXAiOjE1NDIzNTg2MDkzNjQuOTc3OH0.5xFtVgMrDiXR3gDUseLUkr5VMWwInmL_xZ4XUiW9_zU';

axios.defaults.headers.common['Authorization'] = jwtKey;
// let haduh = async function(hehe) {
//     try {
//         let response = await axios.get(eventUrl+'/event/history');
//         console.log(response.data)
//     } catch(e) {
//         throw e;
//     }
// }
// haduh(5);

axios.get(eventUrl)
     .then(function(response) {
         console.log(response.data);
     })
     .catch(function(error) {
         throw error;
     })

// let req = https.get(eventUrl, function(res) {
//     console.log(res);
// })
// req.on('error', function(error) {
//     throw error;
// })
// req.end()

// fetch(eventUrl+'/event/history', {
//     method: 'GET',
//     headers: {
//         'Authorization': jwtKey
//     },
// })
// .then(function(response) {
//     console.log(response.data);
// })
// .catch(function(error) {
//     console.log(error);
// })