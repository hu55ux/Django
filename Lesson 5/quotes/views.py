import random
from django.http import HttpResponse

quotes_list = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House"},
    {"text": "Simplicity is prerequisite for reliability.", "author": "Edsger W. Dijkstra"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"text": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde"}
]


def random_quote(request):
    quote = random.choice(quotes_list)
    html = f"""
    <!DOCTYPE html>
    <html lang="az">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Random Quote</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #431407 50%, #7c2d12 100%);
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
                max-width: 540px;
                width: 100%;
            }}
            .badge {{
                display: inline-block;
                padding: 6px 16px;
                background: rgba(249, 115, 22, 0.2);
                border: 1px solid rgba(249, 115, 22, 0.4);
                color: #fb923c;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 24px;
                letter-spacing: 0.5px;
            }}
            blockquote {{
                font-size: 1.25rem;
                line-height: 1.6;
                color: #ffedd5;
                font-style: italic;
                margin-bottom: 16px;
                position: relative;
            }}
            .author {{
                color: #fb923c;
                font-weight: 700;
                font-size: 1rem;
                margin-bottom: 32px;
            }}
            .refresh-btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                background: #f97316;
                color: #ffffff;
                text-decoration: none;
                font-weight: 700;
                font-size: 0.95rem;
                padding: 12px 24px;
                border-radius: 12px;
                transition: all 0.25s ease;
                box-shadow: 0 4px 14px rgba(249, 115, 22, 0.35);
                margin-bottom: 32px;
            }}
            .refresh-btn:hover {{
                background: #ea580c;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(249, 115, 22, 0.5);
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
                background: #f97316;
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">QUOTE APP</span>
            <blockquote>“{quote['text']}”</blockquote>
            <div class="author">— {quote['author']}</div>
            <div>
                <a href="/quote/" class="refresh-btn">Yeni Sitat ↻</a>
            </div>
            <div class="nav">
                <a href="/">Home</a>
                <a href="/day/">Day App</a>
                <a href="/quote/" class="active">Quote App</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
