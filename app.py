from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def home():
    # Get the server's IP address
    server_ip = socket.gethostbyname(socket.gethostname())
    return render_template('index.html', server_ip=server_ip)

if __name__ == '__main__':
    app.run(host='172.20.169.86', port=8080)
