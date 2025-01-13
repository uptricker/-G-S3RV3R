from flask import Flask, request, render_template_string, redirect, url_for
from instagrapi import Client
import time
import os

app = Flask(__name__)

# HTML template for the Flask web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Message Sender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        textarea, input, button {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Instagram Message Sender</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" name="username" placeholder="Enter your Instagram username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" name="password" placeholder="Enter your Instagram password" required>

            <label for="targetUsername">Target Username:</label>
            <input type="text" name="targetUsername" placeholder="Enter target username" required>

            <label for="messageFile">Message File (TXT):</label>
            <input type="file" name="messageFile" accept=".txt" required>

            <label for="delay">Delay Between Messages (seconds):</label>
            <input type="number" name="delay" value="5" min="1" required>

            <button type="submit">Start Messaging</button>
        </form>
    </div>
</body>
</html>
'''

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        target_username = request.form['targetUsername']
        delay = int(request.form['delay'])
        message_file = request.files['messageFile']

        # Save the uploaded message file
        if not message_file:
            return "No message file uploaded!"
        message_file_path = os.path.join("messages.txt")
        message_file.save(message_file_path)

        # Start messaging
        try:
            # Login to Instagram
            cl = Client()
            cl.login(username, password)

            # Get the user ID of the target
            user_id = cl.user_id_from_username(target_username)

            # Read messages from file
            with open(message_file_path, "r") as file:
                messages = file.readlines()

            # Send messages
            for message in messages:
                cl.direct_send(message.strip(), [user_id])
                print(f"Sent: {message.strip()}")
                time.sleep(delay)

            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
