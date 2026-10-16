from http.server import BaseHTTPRequestHandler, HTTPServer
import json


created_customers = {}
next_id = {"value": 100}
failure_counts = {}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        if self.path == "/customers":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))

            simulate_failures = int(self.headers.get("X-Simulate-Failures", 0))
            key = self.headers.get("Idempotency-Key", "no-key")
            seen = failure_counts.get(key, 0)
            if seen < simulate_failures:
                failure_counts[key] = seen + 1
                self._send(503, {"detail": "simulated failure"})
                return

            new_id = next_id["value"]
            next_id["value"] += 1
            record = {"id": new_id, "name": data.get("name"), "email": data.get("email")}
            created_customers[new_id] = record
            self._send(201, record)
            return
        self._send(404, {"detail": "not found"})

    def do_GET(self):
        if self.path.startswith("/customers/"):
            customer_id = int(self.path.split("/")[-1])
            record = created_customers.get(customer_id)
            if record:
                self._send(200, record)
            else:
                self._send(404, {"detail": "customer not found"})
            return
        self._send(404, {"detail": "not found"})

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8002), Handler)
    print("Target mock escuchando en http://localhost:8002")
    server.serve_forever()