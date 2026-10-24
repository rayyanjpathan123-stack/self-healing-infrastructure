import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

NGINX_CONTAINER = os.getenv("NGINX_CONTAINER", "self-healing-nginx")
TOKEN = os.getenv("WEBHOOK_TOKEN", "")


class RecoveryHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/alert":
            self.send_error(404)
            return

        if TOKEN and self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self.send_error(401)
            return

        length = int(self.headers.get("Content-Length", "0"))
        try:
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON")
            return

        alerts = payload.get("alerts", [])
        nginx_down = any(
            alert.get("labels", {}).get("alertname") == "NginxDown"
            and alert.get("status") == "firing"
            for alert in alerts
        )

        if not nginx_down:
            self.send_response(202)
            self.end_headers()
            self.wfile.write(b"No recovery action required")
            return

        try:
            result = subprocess.run(
                [
                    "ansible-playbook",
                    "-i", "/ansible/inventory.ini",
                    "/ansible/restart_nginx.yml",
                ],
                capture_output=True,
                text=True,
                timeout=90,
                check=False,
            )

            if result.returncode != 0:
                print(result.stdout, flush=True)
                print(result.stderr, flush=True)
                self.send_error(500, "Ansible recovery failed")
                return

            print(result.stdout, flush=True)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"NGINX recovery completed")
        except subprocess.TimeoutExpired:
            self.send_error(504, "Recovery timed out")
        except OSError as exc:
            print(str(exc), flush=True)
            self.send_error(500, "Recovery service error")

    def log_message(self, format_string, *args):
        print(format_string % args, flush=True)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), RecoveryHandler)
    print("Recovery webhook listening on port 5000", flush=True)
    server.serve_forever()
