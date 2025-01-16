from bcrypt import hashpw, gensalt

# Example of hashing a new password
new_password = "robot123"
hashed_password = hashpw(new_password.encode(), gensalt()).decode()

print("pwd is" + "\n",hashed_password)
