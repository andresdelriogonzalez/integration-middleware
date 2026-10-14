from http.server import BaseHTTPRequestHandler,HTTPServer
import json
import re

customers = {
    1: {"id": 1, "name": "Andrés Del Río", "email": "andres@example.com"},
    2: {"id": 2, "name": "Maria Perez", "email": "maria@example.com"},
}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        match = re.match(r"^/customers/(\d+)$", self.path)
        if match:
            customer_id = int(match.group(1))
            customer = customers.get(customer_id)
            if customer:
                self._send(200,customer)
            else:
                self._send(404, {"detail": "customer not found"})
            return 
        self._send(404, {"detail": "not found"})

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8001), Handler)
    print("Mock de origen escuchando en http://localhost:8001")
    server.serve_forever()

