import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    # Support cloud hosting platforms (Railway, Render, Heroku) via PORT env var
    port = int(os.environ.get("PORT", 8000))

    print("=" * 60)
    print("Launching Creator Hub Full-Stack Application")
    print("=" * 60)
    print("Backend: Python HTTP REST API Server & SQLite DB")
    print("Frontend: HTML5 / CSS3 Glassmorphism SPA")
    print(f"Access App at: http://localhost:{port}")
    print("=" * 60)

    sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
    from server import run_server
    run_server(port)
