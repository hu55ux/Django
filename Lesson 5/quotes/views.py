import random
from django.http import HttpResponse

QUOTES = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"text": "Code is like humor. When you have to explain it, it’s bad.", "author": "Cory House"},
    {"text": "Simplicity is prerequisite for reliability.", "author": "Edsger W. Dijkstra"},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"text": "Experience is the name everyone gives to their mistakes.", "author": "Oscar Wilde"}
]


def random_quote(request):
    quote = random.choice(QUOTES)

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Random Quote</title>
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
                padding: 40px;
                max-width: 500px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                text-align: center;
            }}
            blockquote {{
                font-size: 1.2rem;
                color: #2d3748;
                margin: 0 0 15px 0;
                font-style: italic;
                line-height: 1.5;
            }}
            .author {{
                color: #718096;
                font-weight: 600;
                margin-bottom: 25px;
            }}
            .btn {{
                display: inline-block;
                background: #2b6cb0;
                color: white;
                text-decoration: none;
                padding: 10px 18px;
                border-radius: 6px;
                margin-bottom: 20px;
                font-weight: 500;
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
            <blockquote>“{quote['text']}”</blockquote>
            <div class="author">— {quote['author']}</div>
            <a href="/quote/" class="btn">New Quote ↻</a>
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
