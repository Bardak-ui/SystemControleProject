// websocket.js
const socket = new WebSocket("ws://0.0.0.0:8000/ws/online_status/");

socket.onopen = function(event) {
    console.log('WebSocket подключен.');
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data.message);  // Выводим полученное сообщение
};

socket.onclose = function(event) {
    console.log('WebSocket отключен.');
};

function sendMessage(message) {
    socket.send(JSON.stringify({ 'сообщение': message }));
}
