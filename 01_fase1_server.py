from http.server import BaseHTTPRequestHandler, HTTPServer
import json

counter = {"value": 0}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        self._send(200, counter)

    def do_POST(self):
        if self.path == "/increment":
            counter["value"] += 1
            self._send(200, counter)
        else:
            self._send(404, {"error": "not found"})

    def do_PUT(self):
        if self.path.startswith("/set/"):
            try:
                new_value = int(self.path.split("/")[-1])
                counter["value"] = new_value
                self._send(200, counter)    
            except ValueError:
                print("No es un número válido")
                self._send(422, {"error": "Unprocessable Content"})
        else:
            self._send(404, {"error": "not found"})

    def do_DELETE(self):
        if self.path == "/reset":
            counter["value"] = 0
            self._send(200, counter)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8009), Handler)
    print("Escuchando en http://localhost:8009")
    server.serve_forever()

"""
curl http://localhost:8009/                     # {"value": 0}
curl -X POST http://localhost:8009/increment    # {"value": 1}
curl -X POST http://localhost:8009/increment    # {"value": 2}  <- cambia cada vez
curl -X PUT http://localhost:8009/set/10         # {"value": 10}
curl -X PUT http://localhost:8009/set/10  
curl -X DELETE http://localhost:8009/reset

"""
