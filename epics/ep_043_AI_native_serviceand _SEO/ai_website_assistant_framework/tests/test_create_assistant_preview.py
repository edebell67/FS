import http.server
import json
import socketserver
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "create_assistant_preview.py"

PAGE = b"""<!doctype html><html><head><title>Example Motors | Repairs in E3</title><meta name=\"description\" content=\"MOT, servicing and diagnostics in Bow.\"></head><body><header><nav><a>Home</a><a>Services</a><a>Contact</a></nav></header><main><h1>Example Motors</h1></main></body></html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(PAGE)
    def log_message(self, *_):
        pass

class PreviewGeneratorTests(unittest.TestCase):
    def test_creates_safe_original_shell_and_tenant_draft(self):
        with socketserver.TCPServer(("127.0.0.1", 0), Handler) as server, tempfile.TemporaryDirectory() as tmp:
            threading.Thread(target=server.serve_forever, daemon=True).start()
            root = Path(tmp)
            manifest = root / "prospect.json"
            output = root / "output"
            manifest.write_text(json.dumps({
                "business_name": "Example Motors",
                "source_url": f"http://127.0.0.1:{server.server_address[1]}/",
                "tenant_key": "auto_example_motors",
                "area": "Bow, London",
                "phone": "+442012345678",
                "services": ["Demo MOT enquiry", "Demo vehicle service", "Demo diagnostics"],
                "accent": "#147a78",
                "allowed_origins": ["http://127.0.0.1:8096"]
            }))
            result = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(manifest), "--output", str(output)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "capture.json").exists())
            self.assertTrue((output / "index.html").exists())
            self.assertTrue((output / "assistant-embed.js").exists())
            tenant = json.loads((output / "tenant-draft.json").read_text())
            self.assertEqual(tenant["clientKey"], "auto_example_motors")
            self.assertEqual(tenant["mode"], "demo")
            self.assertIn("demoBooking", tenant["enabledModules"])
            shell = (output / "index.html").read_text()
            self.assertIn("PRIVATE CONCEPT", shell)
            self.assertIn("Example Motors", shell)
            self.assertIn("assistant-embed.js", shell)
            self.assertNotIn(PAGE.decode(), shell)
            capture = json.loads((output / "capture.json").read_text())
            self.assertEqual(capture["page_title"], "Example Motors | Repairs in E3")
            self.assertEqual(capture["navigation_labels"], ["Home", "Services", "Contact"])
            server.shutdown()

if __name__ == "__main__":
    unittest.main()
