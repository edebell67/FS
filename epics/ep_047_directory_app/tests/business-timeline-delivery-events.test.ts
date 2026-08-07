// tests/business-timeline-delivery-events.test.ts
//
// VERSION HISTORY
// v1.0.0 · 2026-08-06 · Initial version: covers the getBusinessTimeline() fix
//   in lib/db/queries/pipeline.ts v1.1.0 (gap `verificationstage` on
//   EP047_end_to_end_workflow_gap_register.html). Tests mergeAndSortTimelineEntries
//   directly with fabricated data -- a genuine unit test, not source-text
//   matching, since it is a pure function with no database dependency (the
//   `db` proxy in lib/db/client.ts only connects lazily on first property
//   access, which this function never triggers). No local Postgres instance
//   was available this session to run getBusinessTimeline()/getDeliveryEventEntries()
//   themselves end-to-end -- that remains a real gap in this evidence, not one
//   this test can close.
import assert from "node:assert/strict";
import test from "node:test";
import { mergeAndSortTimelineEntries, type TimelineEntry } from "../lib/db/queries/pipeline";

function stageEntry(id: string, occurredAt: string, toStageLabel: string): TimelineEntry {
  return {
    id, kind: "stage_transition", fromStageLabel: null, toStageLabel,
    occurredAt: new Date(occurredAt), source: "admin", reason: null, notes: null,
  };
}

function deliveryEntry(id: string, occurredAt: string, toStageLabel: string): TimelineEntry {
  return {
    id, kind: "delivery_event", fromStageLabel: null, toStageLabel,
    occurredAt: new Date(occurredAt), source: "delivery_event", reason: null, notes: "owner@example.com",
  };
}

test("merges stage transitions and delivery events into one chronologically sorted timeline", () => {
  const stages = [
    stageEntry("stage:1", "2026-08-01T09:00:00Z", "Verification sent"),
    stageEntry("stage:2", "2026-08-03T09:00:00Z", "Business claimed"),
  ];
  const deliveries = [
    deliveryEntry("delivery:a:sent", "2026-08-01T09:05:00Z", "Preview email sent"),
    deliveryEntry("delivery:a:opened", "2026-08-02T14:30:00Z", "Preview opened"),
  ];

  const merged = mergeAndSortTimelineEntries(stages, deliveries);

  assert.equal(merged.length, 4);
  // Must be interleaved by time, not grouped by kind.
  assert.deepEqual(
    merged.map((e) => e.id),
    ["stage:1", "delivery:a:sent", "delivery:a:opened", "stage:2"],
  );
});

test("an empty delivery list still returns the stage timeline unchanged", () => {
  const stages = [stageEntry("stage:1", "2026-08-01T09:00:00Z", "Verification sent")];
  const merged = mergeAndSortTimelineEntries(stages, []);
  assert.deepEqual(merged, stages);
});

test("delivery events carry kind: delivery_event so the UI can distinguish them", () => {
  const merged = mergeAndSortTimelineEntries(
    [stageEntry("stage:1", "2026-08-01T09:00:00Z", "Verification sent")],
    [deliveryEntry("delivery:a:sent", "2026-08-01T09:05:00Z", "Preview email sent")],
  );
  const delivery = merged.find((e) => e.id === "delivery:a:sent")!;
  const stage = merged.find((e) => e.id === "stage:1")!;
  assert.equal(delivery.kind, "delivery_event");
  assert.equal(stage.kind, "stage_transition");
});

test("stable sort preserves relative order for entries at the exact same timestamp", () => {
  const sameTime = "2026-08-01T09:00:00Z";
  const merged = mergeAndSortTimelineEntries(
    [stageEntry("stage:1", sameTime, "A")],
    [deliveryEntry("delivery:a:sent", sameTime, "B")],
  );
  assert.deepEqual(merged.map((e) => e.id), ["stage:1", "delivery:a:sent"]);
});
