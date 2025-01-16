####################################################

# In this update I add a route to register a user #

####################################################



from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
import socket
import sqlite3
from bcrypt import hashpw, gensalt

app = Flask(__name__)
socketio = SocketIO(app)

# Database file name
DB_NAME = "a_net.db"

# Route for home page
@app.route('/')
def home():
    print("Flask server is running...")
    server_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', server_ip=server_ip)

# User registration route
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    # Hash the password
    hashed_password = hashpw(password.encode(), gensalt()).decode()

    try:
        # Insert the user into the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Users (username, password_hash) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Registration successful!"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists."}), 400

# SocketIO message handler
@socketio.on('message')
def handle_message(msg):
    # Print the received message to the console
    print(f"Received message from client: {msg}")
    # Send the message back to all connected clients
    send(msg, broadcast=True)

if __name__ == '__main__':
    print("Starting Flask app...")
    socketio.run(app, host='172.20.169.86', port=5000)
