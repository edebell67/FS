import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const frontendDir = normalize(join(__filename, ".."));
const portArg = process.argv[2];
const defaultPort = Number(portArg || process.env.EVIDENCE_UI_PORT || 4173);

const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml; charset=utf-8"
};

const sharedHeaders = {
  "Cache-Control": "no-store, no-cache, must-revalidate, private",
  Pragma: "no-cache",
  Expires: "0",
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
};

function resolvePath(requestUrl) {
  const pathname = new URL(requestUrl, "http://127.0.0.1").pathname;
  const relativePath = pathname === "/" ? "index.html" : pathname.replace(/^\/+/, "");
  return normalize(join(frontendDir, relativePath));
}

export function createStaticServer() {
  return createServer(async (req, res) => {
    try {
      const filePath = resolvePath(req.url || "/");

      if (!filePath.startsWith(frontendDir)) {
        res.writeHead(403, sharedHeaders).end("Forbidden");
        return;
      }

      const body = await readFile(filePath);
      const contentType = contentTypes[extname(filePath)] || "application/octet-stream";
      res.writeHead(200, { ...sharedHeaders, "Content-Type": contentType });
      res.end(body);
    } catch (error) {
      res.writeHead(404, { ...sharedHeaders, "Content-Type": "text/plain; charset=utf-8" });
      res.end(`Not found: ${error.message}`);
    }
  });
}

export function startServer(port = defaultPort, host = "127.0.0.1") {
  const server = createStaticServer();
  return new Promise((resolve) => {
    server.listen(port, host, () => {
      console.log(`Evidence UI ready at http://${host}:${port}`);
      resolve(server);
    });
  });
}

if (process.argv[1] === __filename) {
  await startServer();
}
