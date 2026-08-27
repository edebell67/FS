"""Minimal EP051 health/static service. Version 1.1.0 (2026-08-23)."""
import json,os,sys
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent/"health"))
from checks import liveness,readiness
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path in {"/healthz","/readyz"}:
   code,payload=liveness() if self.path=="/healthz" else readiness()
   body=json.dumps(payload).encode();self.send_response(code);self.send_header("Content-Type","application/json");self.send_header("Cache-Control","no-store");self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body);return
  super().do_GET()
if __name__=="__main__":
 os.chdir(ROOT/"workstreams"/"WF-301");ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()
