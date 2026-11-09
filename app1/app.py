
from flask import Flask, request, render_template_string, redirect, url_for, flash
import redis
import os

app = Flask(__name__)
app.secret_key = "devopshub-secret-key"

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOpsHub | Message Collector</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background: #F8FAF4;
            color: #344735;
        }

        .container {
            max-width: 850px;
            margin: auto;
            padding: 40px 25px;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 25px;
            border-bottom: 1px solid #DCE7D4;
        }

        .logo {
            font-size: 25px;
            font-weight: 800;
            color: #527451;
        }

        .nav-label {
            color: #71846C;
            font-size: 14px;
        }

        .heading {
            margin-top: 55px;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 34px;
            margin-bottom: 10px;
            color: #344735;
        }

        .subtitle {
            color: #7A8C75;
            font-size: 16px;
            line-height: 1.6;
        }

        .card {
            background: #E7F0DD;
            border: 1px solid #D3E3C7;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 8px 25px rgba(72, 104, 67, 0.05);
        }

        .icon {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #D3E5C5;
            border-radius: 14px;
            font-size: 25px;
        }

        h2 {
            font-size: 23px;
            margin-top: 25px;
            color: #405B3F;
        }

        textarea {
            width: 100%;
            min-height: 160px;
            padding: 18px;
            margin-top: 15px;
            border: 1px solid #C9D9BD;
            border-radius: 12px;
            background: #F8FAF4;
            color: #344735;
            font-family: inherit;
            font-size: 15px;
            resize: vertical;
            outline: none;
        }

        textarea:focus {
            border-color: #789B6C;
        }

        button {
            margin-top: 20px;
            padding: 14px 28px;
            background: #789B6C;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #5C8054;
        }

        .success {
            margin-top: 20px;
            padding: 15px;
            background: #DCEBD2;
            border: 1px solid #C6DDB9;
            border-radius: 12px;
            color: #42623D;
        }

        .footer {
            margin-top: 30px;
            color: #84937E;
            font-size: 14px;
            text-align: center;
        }

        @media (max-width: 600px) {
            .container {
                padding: 25px 18px;
            }

            h1 {
                font-size: 27px;
            }

            .card {
                padding: 25px;
            }
        }
    </style>
</head>

<body>
    <div class="container">

        <nav class="navbar">
            <div class="logo">DevOpsHub.</div>
            <div class="nav-label">Message Collector</div>
        </nav>

        <section class="heading">
            <h1>Message Collector</h1>
            <p class="subtitle">
                Share your feedback with us.
                Your messages are securely collected and stored.
            </p>
        </section>

        <div class="card">

            <div class="icon">&#9993;</div>

            <h2>Send Your Feedback</h2>

            <form method="POST">
                <textarea
                    name="message"
                    required
                    placeholder="Write your message here..."
                ></textarea>

                <button type="submit">
                    Submit Message
                </button>
               
            </form>
                <button type="button" onclick="window.location.reload()"
                    style="background: #A3B98F; margin-left: 10px;">
                        Refresh Page
                </button>

           {% with messages = get_flashed_messages() %}
               {% if messages %}
                   {% for message in messages %}
                     <div class="success">
                     {{ message }}
                     </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>

        <div class="footer">
            DevOpsHub Message Collection System
        </div>

    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        message = request.form.get("message", "").strip()

        if message:
            r.rpush("messages", message)
            flash("Message submitted successfully!")

        return redirect(url_for("home"))

    r.incr("visit_count")

    return render_template_string(HTML)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
