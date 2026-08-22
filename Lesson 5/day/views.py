from datetime import datetime
from django.http import HttpResponse


def current_day(request):
    today = datetime.now().strftime("%A")
    date_str = datetime.now().strftime("%B %d, %Y")

    html = f"""
    <!DOCTYPE html>
    <html lang="az">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Current Day</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #064e3b 50%, #022c22 100%);
                color: #f8fafc;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
            }}
            .card {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 48px 56px;
                border-radius: 24px;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
                text-align: center;
                max-width: 520px;
                width: 100%;
            }}
            .badge {{
                display: inline-block;
                padding: 6px 16px;
                background: rgba(16, 185, 129, 0.2);
                border: 1px solid rgba(16, 185, 129, 0.4);
                color: #34d399;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 20px;
                letter-spacing: 0.5px;
            }}
            .sub-title {{
                color: #94a3b8;
                font-size: 1rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            .day-title {{
                font-size: 3.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #34d399 0%, #a7f3d0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
                letter-spacing: -1px;
            }}
            .date-info {{
                color: #cbd5e1;
                font-size: 1rem;
                font-weight: 500;
                margin-bottom: 32px;
            }}
            .nav {{
                display: flex;
                gap: 10px;
                justify-content: center;
                background: rgba(15, 23, 42, 0.6);
                padding: 6px;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }}
            .nav a {{
                flex: 1;
                color: #94a3b8;
                text-decoration: none;
                font-weight: 600;
                font-size: 0.9rem;
                padding: 10px 16px;
                border-radius: 12px;
                transition: all 0.25s ease;
            }}
            .nav a.active, .nav a:hover {{
                background: #10b981;
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">DAY APP</span>
            <div class="sub-title">Cari Həftə Günü</div>
            <h1 class="day-title">{today}</h1>
            <div class="date-info">{date_str}</div>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/day/" class="active">Day App</a>
                <a href="/quote/">Quote App</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
