import http.server
import socketserver
import json
import mimetypes
import os

PORT = 3000

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/search":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body.decode("utf-8"))
                query = data.get("query", "").lower().strip()
            except Exception:
                query = ""

            with open("projects.json", "r", encoding="utf-8") as f:
                projects = json.load(f).get("projects", [])

            ranked = []
            for p in projects:
                score = 0.0
                title = p.get("title", "").lower()
                tags = [t.lower() for t in p.get("tags", [])]
                overview = p.get("overview", "").lower()
                tools = p.get("tools", "").lower()
                
                if query:
                    # Multi-tier relevance scoring
                    if query in title:
                        score = 0.96
                    elif any(query == t for t in tags):
                        score = 0.90
                    elif any(query in t for t in tags):
                        score = 0.82
                    elif query in overview:
                        score = 0.68
                    elif query in tools:
                        score = 0.58
                    else:
                        score = 0.12
                else:
                    score = 1.0
                
                ranked.append({"id": p["id"], "score": round(score, 2)})

            ranked.sort(key=lambda x: x["score"], reverse=True)
            threshold = 0.5
            matches = [r for r in ranked if r["score"] >= threshold]

            resp_json = json.dumps({
                "engine": "vector-local",
                "threshold": threshold,
                "ranked": ranked,
                "matches": matches
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(resp_json)
            return

        super().do_POST()

def run():
    mimetypes.add_type("video/mp4", ".mp4")
    mimetypes.add_type("image/svg+xml", ".svg")
    mimetypes.add_type("application/json", ".json")

    with ReusableTCPServer(("", PORT), Handler) as httpd:
        print(f"Ash — Studio Portfolio live at http://localhost:{PORT}")
        print("Press Ctrl+C to terminate.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()
