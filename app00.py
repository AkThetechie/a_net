from flask import Flask, render_template
from flask_socketio import SocketIO, send
import socket

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    print("Flask server is running...")
    server_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', server_ip=server_ip)
    

@socketio.on('message')
def handle_message(msg):
    # Print the received message to the console
    print(f"Received message from client: {msg}")
    # Send the message back to all connected clients
    send(msg, broadcast=True)

if __name__ == '__main__':
    print("Starting Flask app...")
    socketio.run(app, host='172.20.169.86', port=5000)
