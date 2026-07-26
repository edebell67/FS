import assert from "node:assert/strict";
import test from "node:test";

import {
  getDeliveryStatePresentation,
  type VerificationDeliveryState,
} from "../lib/verification/delivery-status";
import {
  CANONICAL_PRODUCTION_ORIGIN,
  verificationCapabilityUrl,
} from "../lib/verification/urls";

test("prepared delivery state explicitly says that nothing was sent", () => {
  assert.deepEqual(getDeliveryStatePresentation("prepared"), {
    label: "Prepared",
    explanation: "Preview created; no email has been sent.",
  });
});

test("every supported immutable delivery state has a visible label", () => {
  const states: VerificationDeliveryState[] = [
    "prepared", "sent", "opened", "clicked", "completed", "failed", "revoked",
  ];
  assert.deepEqual(
    states.map((state) => getDeliveryStatePresentation(state).label),
    ["Prepared", "Sent", "Opened (best effort)", "Clicked", "Completed", "Failed", "Revoked"],
  );
});

test("production capability links always use the canonical public origin", () => {
  const url = verificationCapabilityUrl("secret-token", {
    NODE_ENV: "production",
    NEXT_PUBLIC_SITE_URL: "http://localhost:8140",
  });
  assert.equal(url, `${CANONICAL_PRODUCTION_ORIGIN}/verify/secret-token`);
});

test("localhost capability links are retained only for genuine local development", () => {
  assert.equal(
    verificationCapabilityUrl("secret-token", {
      NODE_ENV: "development",
      NEXT_PUBLIC_SITE_URL: "http://localhost:8140/",
    }),
    "http://localhost:8140/verify/secret-token",
  );
  assert.equal(
    verificationCapabilityUrl("secret-token", {
      NODE_ENV: "production",
      NEXT_PUBLIC_SITE_URL: "http://127.0.0.1:8140",
    }),
    `${CANONICAL_PRODUCTION_ORIGIN}/verify/secret-token`,
  );
});
