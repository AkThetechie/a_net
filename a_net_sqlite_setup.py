import sqlite3
from bcrypt import hashpw, gensalt

# Database and Server Name
db_name = "a_net.db"

# Connect to SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);
''')

# Create Messages table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users (id),
    FOREIGN KEY (receiver_id) REFERENCES Users (id)
);
''')

# Create Locations table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations (
    user_id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (id)
);
''')

# Insert main user "robot" with full control
username = "robot"
password = "robot_password"
hashed_password = hashpw(password.encode(), gensalt()).decode()

try:
    cursor.execute('''
    INSERT INTO Users (username, password_hash, role)
    VALUES (?, ?, ?)
    ''', (username, hashed_password, 'admin'))
    print("Admin user 'robot' created successfully.")
except sqlite3.IntegrityError:
    print("Admin user 'robot' already exists.")

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database '{db_name}' initialized successfully.")
