const WebSocket = require('./node_modules/ws');
const socket = new WebSocket('ws://192.168.45.216:8080');

socket.on('open', () => {
    console.log('Connected to the server');
    socket.send('Fuck off');
});

socket.on('message', (message) => {
    console.log(`Received: ${message}`);
});

socket.on('close', () => {
    console.log('Disconnected from the server');
});