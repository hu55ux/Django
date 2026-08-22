import random
from django.http import HttpResponse

quotes_list = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "Simplicity is prerequisite for reliability. - Edsger W. Dijkstra",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Experience is the name everyone gives to their mistakes. - Oscar Wilde"
]


def random_quote(request):
    selected_quote = random.choice(quotes_list)
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Random Quote</title>
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
                max-width: 500px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }}
            .quote {{
                font-size: 18px;
                color: #34495e;
                font-style: italic;
                margin-bottom: 20px;
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
            <div class="quote">"{selected_quote}"</div>
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
