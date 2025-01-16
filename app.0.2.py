from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, send
import socket
import sqlite3
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'your_secret_key'  # Secure your app with a secret key

# Database file name
DB_NAME = "a_net.db"

# Route for home page
@app.route('/')
def home():
    print("Flask server is running...")
    server_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', server_ip=server_ip)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    print(f"Request method: {request.method}")

    # Check if the method is POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Debug: print the form data
        print(f"Form data: {request.form}")

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        # Hash the password
        hashed_password = hashpw(password.encode(), gensalt()).decode()

        try:
            # Insert the user into the database
            conn = sqlite3.connect(DB_NAME, check_same_thread=False)  # Updated line
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO Users (username, password_hash) VALUES (?, ?)
            ''', (username, hashed_password))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()  # Make sure to close the connection
            
            print(f"User {username} added successfully.")
            return jsonify({"message": "Registration successful!"}), 200
        except sqlite3.IntegrityError:
            print(f"Error: Username {username} already exists.")
            return jsonify({"error": "Username already exists."}), 400
        except Exception as e:
            print(f"Error occurred: {e}")
            return jsonify({"error": "An error occurred while registering."}), 500

    # If the method is GET, just return the registration page
    return render_template('register.html')



# SocketIO message handler
@socketio.on('message')
def handle_message(msg):
    # Print the received message to the console
    print(f"Received message from client: {msg}")
    # Send the message back to all connected clients
    send(msg, broadcast=True)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check credentials from the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM Users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and checkpw(password.encode(), user[1].encode()):
            # Store user session
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

# Chat route - after login
@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not authenticated

    return render_template('chat.html', username=session['username'])


if __name__ == '__main__':
    print("Starting Flask app...")
    socketio.run(app, host='172.20.169.86', port=5000)
