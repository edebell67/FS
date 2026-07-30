/**
 * tests/preview-delivery.test.ts — covers the six message templates, the
 * fail-closed sending gate, and prepare/send separation.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version.
 */

import assert from "node:assert/strict";
import test from "node:test";
import { readFile } from "node:fs/promises";
import {
  previewReadyMessage, etaMessage, readyForActivationMessage,
  reminderIntakeMessage, reminderReviewMessage, reminderActivationMessage,
  previewDeliveryEnabled,
} from "../lib/verification/preview-delivery";

const root = new URL("..", import.meta.url);
async function source(path: string) { return readFile(new URL(path, root), "utf8"); }

test("preview-ready message includes the generated site link, benefits, and the news link", () => {
  const message = previewReadyMessage("Test Prospect Ltd", "https://example.com/preview/test-prospect");
  assert.match(message.subject, /Test Prospect Ltd/);
  assert.match(message.text, /https:\/\/example\.com\/preview\/test-prospect/);
  assert.match(message.text, /no action required/i);
  assert.match(message.text, /https:\/\/thetechprinciple\.com\/news\//);
});

test("ETA message states a date without implying automatic activation", () => {
  const message = etaMessage("Test Prospect Ltd", new Date("2026-08-15T00:00:00Z"));
  assert.match(message.text, /2026-08-15/);
  assert.doesNotMatch(message.text, /activat(ed|ion) automatically/i);
});

test("ready-for-activation message does not itself claim the site is live", () => {
  const message = readyForActivationMessage("Test Prospect Ltd");
  assert.doesNotMatch(message.text, /is now live/i);
  assert.match(message.text, /separate step you control/i);
});

test("reminder messages are distinct per trigger condition", () => {
  const intake = reminderIntakeMessage("Test Prospect Ltd");
  const review = reminderReviewMessage("Test Prospect Ltd");
  const activation = reminderActivationMessage("Test Prospect Ltd");
  assert.notEqual(intake.text, review.text);
  assert.notEqual(review.text, activation.text);
  assert.match(review.text, /need a little more information/i);
  assert.match(activation.text, /still waiting to be activated|still valid/i);
});

test("preview delivery fails closed without explicit mode, approval, and allowlist", () => {
  delete process.env.PREVIEW_DELIVERY_MODE;
  delete process.env.PREVIEW_DELIVERY_APPROVED;
  delete process.env.PREVIEW_RECIPIENT_ALLOWLIST;
  assert.equal(previewDeliveryEnabled(), false);
  process.env.PREVIEW_DELIVERY_MODE = "gmail-api";
  process.env.PREVIEW_DELIVERY_APPROVED = "true";
  process.env.PREVIEW_RECIPIENT_ALLOWLIST = "edebell@gmail.com";
  assert.equal(previewDeliveryEnabled(), true);
  delete process.env.PREVIEW_DELIVERY_MODE;
  delete process.env.PREVIEW_DELIVERY_APPROVED;
  delete process.env.PREVIEW_RECIPIENT_ALLOWLIST;
});

test("sending a preview message is a distinct, explicit action from preparing one", async () => {
  const module = await source("lib/verification/preview-delivery.ts");
  assert.match(module, /export async function preparePreviewMessage/);
  assert.match(module, /export async function sendPreparedPreviewMessage/);
  assert.match(module, /status: input\.recipientAddress \? "prepared" : "failed"/);
  assert.match(module, /Recipient is not allowlisted/);
  assert.match(module, /Gmail API handoff failed/);
});

test("preview delivery messages table supports every message type as its own record", async () => {
  const schema = await source("lib/db/schema.ts");
  const migration = await source("migrations/0014_preview_delivery_and_review.sql");
  assert.match(schema, /previewDeliveryMessages/);
  assert.match(schema, /messageType: text\("message_type"\)/);
  for (const type of ["preview_ready", "eta", "ready_for_activation", "reminder_intake", "reminder_review", "reminder_activation"]) {
    assert.match(migration, new RegExp(type));
  }
});
