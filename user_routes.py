from flask import Blueprint, request, jsonify
import sqlite3
from bcrypt import hashpw, gensalt

# Create a Blueprint for user-related routes
user_bp = Blueprint('user', __name__)
DB_NAME = "a_net.db"

@user_bp.route('/register', methods=['POST'])
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
