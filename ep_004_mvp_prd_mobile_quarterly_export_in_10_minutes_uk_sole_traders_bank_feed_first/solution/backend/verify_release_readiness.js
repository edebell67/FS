const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { main: generateEvidenceUiDemo } = require("./generate_evidence_ui_demo");
const { runVerification: runBankConnectionVerification } = require("./verify_bank_connection");
const { runVerification: runTransactionImportVerification } = require("./verify_transaction_import");

const backendDir = __dirname;
const frontendDir = path.join(__dirname, "..", "frontend");

async function main() {
  process.env.BANK_TOKEN_ENCRYPTION_KEY = process.env.BANK_TOKEN_ENCRYPTION_KEY || "release-ready-demo-encryption-key";
  await generateEvidenceUiDemo();
  await runBankConnectionVerification();
  await runTransactionImportVerification();
  const { main: runFrontendVerification } = await import(pathToFileURL(path.join(frontendDir, "verify_release_ui.js")).href);
  await runFrontendVerification();

  console.log("release_readiness_ok");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
