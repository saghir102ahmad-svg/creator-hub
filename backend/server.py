import os
import sys
import json
import sqlite3
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
DB_PATH = os.path.join(BASE_DIR, "creator_hub.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def extract_youtube_id(url):
    if not url:
        return "dQw4w9WgXcQ"
    match = re.search(r'(?:v=|\/|be\/|embed\/)([a-zA-Z0-9_-]{11})', str(url))
    return match.group(1) if match else str(url).strip()

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tagline TEXT,
            bio TEXT,
            instagram TEXT,
            youtube TEXT,
            business_email TEXT,
            avatar_url TEXT,
            subscribers_count TEXT,
            followers_count TEXT,
            students_count TEXT,
            products_count TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            youtube_url TEXT NOT NULL,
            youtube_id TEXT NOT NULL,
            category TEXT,
            duration TEXT,
            views TEXT,
            thumbnail_url TEXT,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price TEXT,
            badge TEXT,
            level TEXT,
            students TEXT,
            rating TEXT,
            curriculum TEXT,
            image_url TEXT,
            enroll_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bundles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price TEXT,
            badge TEXT,
            items_included TEXT,
            image_url TEXT,
            buy_url TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS podcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            duration TEXT,
            audio_url TEXT,
            cover_url TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (name, tagline, bio, instagram, youtube, business_email, avatar_url, subscribers_count, followers_count, students_count, products_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            "Alex Rivera",
            "Content Creator, Educator & Gamer",
            "I create in-depth videos on modern web development, gaming content, AI technology, and digital design.",
            "https://instagram.com",
            "https://youtube.com",
            "alex.rivera.biz@example.com",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=600&q=80",
            "125K+",
            "45K+",
            "8.2K+",
            "14+"
        ))

        videos_data = [
            ("Building a Modern SaaS App from Scratch", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Tutorials", "42:15", "84K", "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80", "Complete step-by-step guide to building and scaling a full-stack SaaS application."),
            ("Ultimate 4K Gaming PC Setup & Cyberpunk Gameplay", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Gaming", "28:10", "210K", "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80", "Testing the latest RTX 4090 gaming rig with ray tracing and ultra graphics settings."),
            ("AI Tools Every Creator Should Use in 2026", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Reviews", "18:40", "120K", "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80", "Breakdown of the top artificial intelligence productivity tools for modern content creators."),
            ("Top 10 Indie Games of the Year Review", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Gaming", "19:45", "145K", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80", "My top picks for the best indie game releases, gameplay breakdowns, and mechanics analysis."),
            ("Mastering UI/UX Glassmorphism & Animations", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Design", "25:10", "62K", "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=800&q=80", "Learn how to craft ultra-sleek, premium user interfaces with modern CSS & micro-interactions."),
            ("My Gaming & Content Creation Studio Tour", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "Vlogs", "15:30", "195K", "https://images.unsplash.com/photo-1598550476439-6847785fcea6?auto=format&fit=crop&w=800&q=80", "A tour of my 4K camera gear, lighting setup, audio mic rig, and gaming workstation.")
        ]
        cursor.executemany('''
            INSERT INTO videos (title, youtube_url, youtube_id, category, duration, views, thumbnail_url, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', videos_data)

        courses_data = [
            ("Full-Stack Web Development Bootcamp", "Master HTML, CSS, JavaScript, Python & Databases from absolute zero to production deployment.", "$89", "Best Seller", "Beginner to Advanced", "4,200", "4.9 ★", "Module 1: Modern HTML5 & CSS3 Architecture\nModule 2: JavaScript ES6+ & SPA State\nModule 3: Python REST APIs & SQLite Databases\nModule 4: Security, Authentication & Deployment", "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80", "#enroll"),
            ("Unreal Engine 5 Game Development Masterclass", "Learn 3D game design, C++ scripting, Blueprint visual scripting, and environment building.", "$79", "New", "All Levels", "1,850", "4.92 ★", "Module 1: UE5 Interface & Nanite Geometry\nModule 2: Blueprints & Character Movement\nModule 3: C++ Game Logic & Physics\nModule 4: Lighting, Sound & Game Release", "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80", "#enroll")
        ]
        cursor.executemany('''
            INSERT INTO courses (title, description, price, badge, level, students, rating, curriculum, image_url, enroll_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', courses_data)

        bundles_data = [
            ("The Ultimate Creator OS Bundle", "Everything you need to launch: 50+ UI Components, Video Script Templates, Thumbnail PSDs, and Creator Planner.", "$99", "50% OFF BUNDLE", "Includes: UI Kit + Course Access + 25 Notion Templates + Raw LUTs", "https://images.unsplash.com/photo-1522542550221-31fd19575a2d?auto=format&fit=crop&w=800&q=80", "#buy-bundle"),
            ("Pro Gamer & Streamer Asset Pack", "Includes OBS stream overlays, animated alerts, sound effects, thumbnail templates, and LUT color profiles.", "$49", "GAMER PACK", "Includes: 20 Stream Overlays + 50 Sound FX + 10 Thumbnail PSDs", "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80", "#buy-bundle")
        ]
        cursor.executemany('''
            INSERT INTO bundles (title, description, price, badge, items_included, image_url, buy_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', bundles_data)

    conn.commit()
    conn.close()

class CreatorHubRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def _send_json_response(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/api/'):
            try:
                conn = get_db()
                cursor = conn.cursor()

                if path == '/api/profile':
                    cursor.execute("SELECT * FROM profile LIMIT 1")
                    row = cursor.fetchone()
                    conn.close()
                    self._send_json_response(dict(row) if row else {}, 200)

                elif path == '/api/videos':
                    cursor.execute("SELECT * FROM videos ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                elif path == '/api/courses':
                    cursor.execute("SELECT * FROM courses ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                elif path == '/api/bundles':
                    cursor.execute("SELECT * FROM bundles ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                elif path == '/api/podcasts':
                    cursor.execute("SELECT * FROM podcasts ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                elif path == '/api/inquiries':
                    cursor.execute("SELECT * FROM inquiries ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                elif path == '/api/subscribers':
                    cursor.execute("SELECT * FROM subscribers ORDER BY id DESC")
                    rows = cursor.fetchall()
                    conn.close()
                    self._send_json_response([dict(r) for r in rows], 200)

                else:
                    conn.close()
                    self._send_json_response({"error": "Endpoint not found"}, 404)

            except Exception as e:
                self._send_json_response({"error": str(e)}, 500)
            return

        super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'

        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {}

        try:
            conn = get_db()
            cursor = conn.cursor()

            if path == '/api/inquiries':
                name = data.get('name', '').strip()
                email = data.get('email', '').strip()
                subject = data.get('subject', 'General Inquiry').strip()
                message = data.get('message', '').strip()

                if not name or not email or not message:
                    conn.close()
                    self._send_json_response({"error": "Name, email, and message are required."}, 400)
                    return

                cursor.execute('''
                    INSERT INTO inquiries (name, email, subject, message)
                    VALUES (?, ?, ?, ?)
                ''', (name, email, subject, message))
                conn.commit()
                conn.close()
                self._send_json_response({"success": True, "message": "Inquiry submitted successfully!"}, 201)

            elif path == '/api/subscribers':
                email = data.get('email', '').strip()
                if not email:
                    conn.close()
                    self._send_json_response({"error": "Valid email address required."}, 400)
                    return

                try:
                    cursor.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
                    conn.commit()
                    conn.close()
                    self._send_json_response({"success": True, "message": "Subscribed to newsletter!"}, 201)
                except sqlite3.IntegrityError:
                    conn.close()
                    self._send_json_response({"success": True, "message": "You are already subscribed!"}, 200)

            elif path == '/api/videos':
                yt_url = data.get('youtube_url', '').strip()
                yt_id = extract_youtube_id(yt_url or data.get('youtube_id', ''))
                
                thumb = data.get('thumbnail_url', '').strip()
                if not thumb:
                    thumb = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"

                cursor.execute('''
                    INSERT INTO videos (title, youtube_url, youtube_id, category, duration, views, thumbnail_url, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data.get('title', 'My YouTube Video'),
                    yt_url or f"https://www.youtube.com/watch?v={yt_id}",
                    yt_id,
                    data.get('category', 'Gaming'),
                    data.get('duration', '12:00'),
                    data.get('views', '1K'),
                    thumb,
                    data.get('description', '')
                ))
                conn.commit()
                row_id = cursor.lastrowid
                conn.close()
                self._send_json_response({"success": True, "id": row_id}, 201)

            else:
                conn.close()
                self._send_json_response({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json_response({"error": str(e)}, 500)

    def do_DELETE(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/api/videos/'):
            try:
                video_id = path.split('/')[-1]
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('DELETE FROM videos WHERE id = ?', (video_id,))
                conn.commit()
                conn.close()
                self._send_json_response({"success": True, "message": "Video deleted!"}, 200)
            except Exception as e:
                self._send_json_response({"error": str(e)}, 500)
            return

        self._send_json_response({"error": "Endpoint not found"}, 404)

    def do_PUT(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {}

        try:
            conn = get_db()
            cursor = conn.cursor()

            if path == '/api/profile':
                cursor.execute('''
                    UPDATE profile SET
                        name = ?, tagline = ?, bio = ?, instagram = ?, youtube = ?,
                        business_email = ?, avatar_url = ?, subscribers_count = ?,
                        followers_count = ?, students_count = ?, products_count = ?
                    WHERE id = 1
                ''', (
                    data.get('name'), data.get('tagline'), data.get('bio'),
                    data.get('instagram'), data.get('youtube'), data.get('business_email'),
                    data.get('avatar_url'), data.get('subscribers_count'),
                    data.get('followers_count'), data.get('students_count'),
                    data.get('products_count')
                ))
                conn.commit()
                conn.close()
                self._send_json_response({"success": True, "message": "Profile updated!"}, 200)
            else:
                conn.close()
                self._send_json_response({"error": "Endpoint not found"}, 404)

        except Exception as e:
            self._send_json_response({"error": str(e)}, 500)

def run_server(port=8000):
    init_db()
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, CreatorHubRequestHandler)
    print(f"Creator Hub REST API Server running on http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
