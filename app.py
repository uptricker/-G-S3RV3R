from flask import Flask, request, render_template_string, redirect, url_for
from instagrapi import Client
import threading
import time

app = Flask(__name__)
client = Client()

# Global Variables
is_running = False
stop_flag = False

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Message Sender</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        input, button, textarea { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .stop-button { background-color: #f44336; }
        .stop-button:hover { background-color: #d32f2f; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Instagram Group Message Sender</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" name="username" placeholder="Enter Instagram username" required>
            
            <label for="password">Instagram Password:</label>
            <input type="password" name="password" placeholder="Enter Instagram password" required>
            
            <label for="group_id">Group Chat ID:</label>
            <input type="text" name="group_id" placeholder="Enter group chat ID" required>
            
            <label for="messagesFile">Messages File (TXT):</label>
            <input type="file" name="messagesFile" required>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>
            
            <button type="submit">Start Sending Messages</button>
        </form>
        <form method="POST" action="/stop">
            <button type="submit" class="stop-button">Stop</button>
        </form>
    </div>
</body>
</html>
'''

# Function to send messages
def send_messages(username, password, group_id, messages, delay):
    global is_running, stop_flag
    try:
        client.login(username, password)
        is_running = True
        stop_flag = False

        for message in messages:
            if stop_flag:
                print("Stopping message sending...")
                break

            client.direct_send(message, [group_id])
            print(f"Sent message: {message}")
            time.sleep(delay)

        print("Finished sending messages.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        is_running = False
        client.logout()

@app.route('/', methods=['GET', 'POST'])
def index():
    global is_running
    if request.method == 'POST':
        if is_running:
            return "A process is already running. Please stop it before starting a new one."

        username = request.form['username']
        password = request.form['password']
        group_id = request.form['group_id']
        delay = int(request.form['delay'])

        # Read messages from the uploaded file
        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode('utf-8').splitlines()

        # Start a new thread for sending messages
        threading.Thread(target=send_messages, args=(username, password, group_id, messages, delay)).start()
        return redirect(url_for('index'))

    return render_template_string(HTML_TEMPLATE)

@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
