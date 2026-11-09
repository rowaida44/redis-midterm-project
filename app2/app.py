
from flask import Flask, render_template_string
import redis
import os

app = Flask(__name__)

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
    <title>DevOpsHub | Dashboard</title>

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
            max-width: 1100px;
            margin: 0 auto;
            padding: 50px 25px;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 25px;
            border-bottom: 1px solid #DCE7D4;
            gap: 15px;
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
            margin-bottom: 35px;
        }

        h1 {
            font-size: 34px;
            margin-bottom: 10px;
            color: #344735;
        }

        .subtitle {
            color: #7A8C75;
            font-size: 16px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 25px;
        }

        .card {
            background: #E7F0DD;
            border: 1px solid #D3E3C7;
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 8px 25px rgba(72, 104, 67, 0.05);
        }

        .card:nth-child(2) {
            background: #F0F5E9;
        }

        .icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background: #D3E5C5;
            border-radius: 14px;
            font-size: 24px;
            color: #527451;
        }

        .card-label {
            margin-top: 25px;
            font-size: 17px;
            color: #61775D;
        }

        .card-number {
            font-size: 56px;
            font-weight: 800;
            color: #344F35;
            margin: 12px 0;
        }

        .card-description {
            color: #81917C;
            font-size: 14px;
        }

        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 35px;
            gap: 15px;
        }

        .footer-text {
            color: #84937E;
            font-size: 14px;
        }

        .refresh {
            display: inline-block;
            background: #789B6C;
            color: white;
            text-decoration: none;
            padding: 14px 25px;
            border-radius: 12px;
            font-weight: 600;
            transition: background 0.2s;
        }

        .refresh:hover {
            background: #5C8054;
        }

        @media (max-width: 650px) {
            .container {
                padding: 25px 18px;
            }

            .heading {
                margin-top: 35px;
            }

            h1 {
                font-size: 28px;
            }

            .cards {
                grid-template-columns: 1fr;
            }

            .footer {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>

<body>
    <div class="container">

        <nav class="navbar">
            <div class="logo">DevOpsHub.</div>
            <div class="nav-label">Analytics Dashboard</div>
        </nav>

        <section class="heading">
            <h1>Dashboard Overview</h1>
            <p class="subtitle">
                Your message and website visit statistics.
            </p>
        </section>

        <section class="cards">

            <div class="card">
                <div class="icon">&#9993;</div>
                <div class="card-label">Total Messages</div>
                <div class="card-number">{{ messages }}</div>
                <div class="card-description">
                    Messages collected from users
                </div>
            </div>

            <div class="card">
                <div class="icon">&#9678;</div>
                <div class="card-label">Total Visits</div>
                <div class="card-number">{{ visits }}</div>
                <div class="card-description">
                    Visits to the message collection page
                </div>
            </div>

        </section>

        <div class="footer">
            <span class="footer-text">
                Statistics are retrieved from Redis.
            </span>
            <a href="/" class="refresh">
                &#8635; Refresh Statistics
            </a>
        </div>

    </div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    messages = r.llen("messages")
    visits = int(r.get("visit_count") or 0)

    return render_template_string(
        HTML,
        messages=messages,
        visits=visits
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
