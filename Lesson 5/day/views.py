from datetime import datetime
from django.http import HttpResponse


def current_day(request):
    today = datetime.now().strftime("%A")
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Current Day</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                text-align: center;
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}
            .day {{
                font-size: 28px;
                color: #e74c3c;
                font-weight: bold;
                margin: 15px 0;
            }}
            .links a {{
                margin: 0 10px;
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Today is:</h2>
            <div class="day">{today}</div>
            <div class="links">
                <a href="/">Home</a> |
                <a href="/day/">Day App</a> |
                <a href="/quote/">Quote App</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
