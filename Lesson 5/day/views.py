from datetime import datetime
from django.http import HttpResponse


def current_day(request):
    day_name = datetime.now().strftime("%A")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Current Day</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f4f6f8;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }}
            .card {{
                background: #ffffff;
                padding: 40px 60px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                text-align: center;
            }}
            .day-badge {{
                display: inline-block;
                background: #3182ce;
                color: #ffffff;
                font-size: 2rem;
                font-weight: 600;
                padding: 10px 24px;
                border-radius: 8px;
                margin: 15px 0 25px 0;
            }}
            p {{
                color: #666;
                margin: 0 0 10px 0;
            }}
            .nav {{
                display: flex;
                gap: 12px;
                justify-content: center;
            }}
            .nav a {{
                color: #0066cc;
                text-decoration: none;
                font-weight: 500;
                padding: 8px 14px;
                background: #edf2f7;
                border-radius: 6px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <p>Today is</p>
            <div class="day-badge">{day_name}</div>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/day/">Day App</a>
                <a href="/quote/">Quote App</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
