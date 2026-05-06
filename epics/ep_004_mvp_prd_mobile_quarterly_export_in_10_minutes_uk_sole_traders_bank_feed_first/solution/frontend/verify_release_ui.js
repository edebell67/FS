import { readFile } from "node:fs/promises";
import { performance } from "node:perf_hooks";
import http from "node:http";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { startServer } from "./server.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const port = 4317;
const requiredPaths = ["/", "/app.js", "/state.js", "/styles.css", "/data/evidence-match-demo.json"];

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function request(pathname) {
  return new Promise((resolve, reject) => {
    const startedAt = performance.now();
    http
      .get(
        {
          hostname: "127.0.0.1",
          port,
          path: pathname
        },
        (response) => {
          let body = "";
          response.setEncoding("utf8");
          response.on("data", (chunk) => {
            body += chunk;
          });
          response.on("end", () => {
            resolve({
              pathname,
              statusCode: response.statusCode,
              headers: response.headers,
              body,
              elapsedMs: performance.now() - startedAt
            });
          });
        }
      )
      .on("error", reject);
  });
}

async function waitForServer() {
  for (let attempt = 0; attempt < 20; attempt += 1) {
    try {
      const response = await request("/");
      if (response.statusCode === 200) {
        return;
      }
    } catch {
      // Retry until the server is ready.
    }
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error("frontend_server_not_ready");
}

export async function main() {
  const appSource = await readFile(join(__dirname, "app.js"), "utf8");
  assert(appSource.includes('data-testid="legal-disclaimer"'), "legal_disclaimer_component_missing");

  const server = await startServer(port);

  try {
    await waitForServer();
    const totalStartedAt = performance.now();
    const responses = await Promise.all(requiredPaths.map((pathname) => request(pathname)));
    const totalElapsedMs = performance.now() - totalStartedAt;

    for (const response of responses) {
      assert(response.statusCode === 200, `request_failed:${response.pathname}`);
      assert(String(response.headers["cache-control"] || "").includes("no-store"), `cache_control_missing:${response.pathname}`);
      assert(Boolean(response.headers["content-security-policy"]), `csp_missing:${response.pathname}`);
      assert(response.elapsedMs < 2000, `single_request_slow:${response.pathname}:${Math.round(response.elapsedMs)}`);
    }

    assert(totalElapsedMs < 2000, `aggregate_load_slow:${Math.round(totalElapsedMs)}`);

    const payloadResponse = responses.find((entry) => entry.pathname === "/data/evidence-match-demo.json");
    const payload = JSON.parse(payloadResponse.body);
    assert(/not tax advice/i.test(payload.legalDisclaimer?.title || ""), "legal_disclaimer_title_missing");
    assert(/remain responsible/i.test(payload.legalDisclaimer?.responsibility || ""), "legal_disclaimer_responsibility_missing");

    console.log("release_ui_ok");
    console.log(`aggregate_load_ms=${Math.round(totalElapsedMs)}`);
    console.log("cache_headers_ok=yes");
    console.log("legal_disclaimer_ok=yes");
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) {
          reject(error);
          return;
        }
        resolve();
      });
    });
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    console.error(error.message);
    process.exit(1);
  });
}
