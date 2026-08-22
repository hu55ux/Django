from django.http import HttpResponse


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home - Hello World</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #f4f6f8;
                margin: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            .card {
                background: #ffffff;
                padding: 40px 60px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                text-align: center;
            }
            h1 {
                color: #1a1a1a;
                margin: 0 0 15px 0;
                font-size: 2.2rem;
            }
            p {
                color: #666;
                margin: 0 0 20px 0;
            }
            .nav {
                display: flex;
                gap: 12px;
                justify-content: center;
            }
            .nav a {
                color: #0066cc;
                text-decoration: none;
                font-weight: 500;
                padding: 8px 14px;
                background: #edf2f7;
                border-radius: 6px;
                transition: background 0.2s;
            }
            .nav a:hover {
                background: #e2e8f0;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Hello, World!</h1>
            <p>Welcome to our Django multi-app project.</p>
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
