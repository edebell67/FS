-- migrations/0024_cultured_eddie_brock.sql — EP043 CRM reporting tables.
--
-- VERSION HISTORY
-- v1.0.0 · 2026-08-10 · Adds message_versions, outreach_responses, and
--   commercial_opportunities, plus verification_deliveries.message_version_id.
--   Hand-trimmed from the drizzle-kit auto-generated diff: the raw diff also
--   re-emitted CREATE TABLE for owner_review_links/owner_review_submissions/
--   owner_review_page_responses, which already exist in the live DB (created
--   by migration 0021 via hand-written SQL, never generated through
--   drizzle-kit) — the snapshot lineage under migrations/meta only has
--   0000/0002/0018, so drizzle-kit's diff engine has no record of 0019-0023's
--   hand-written changes and believed those tables were still new. Applying
--   the un-trimmed file would fail on a live DB. See task
--   workstream/200_inprogress/ep047-crm/20260810_042109_ep047_997_crm_lane2_batch_reporting.md.
CREATE TABLE "commercial_opportunities" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_id" uuid NOT NULL,
	"stage" text DEFAULT 'listing_claimed' NOT NULL,
	"claimed_at" timestamp with time zone,
	"activation_value" double precision,
	"activated_at" timestamp with time zone,
	"service_type" text,
	"service_value" double precision,
	"converted_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "commercial_opportunities_business_id_unique" UNIQUE("business_id")
);
--> statement-breakpoint
CREATE TABLE "message_versions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"template_name" text NOT NULL,
	"version_number" integer NOT NULL,
	"subject" text NOT NULL,
	"body" text NOT NULL,
	"campaign_ref" text,
	"date_introduced" timestamp with time zone DEFAULT now() NOT NULL,
	"date_retired" timestamp with time zone,
	"created_by_user_id" uuid,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "outreach_responses" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_id" uuid NOT NULL,
	"delivery_id" uuid,
	"batch_item_id" uuid,
	"message_version_id" uuid,
	"channel" text DEFAULT 'email' NOT NULL,
	"original_body" text NOT NULL,
	"classification" text NOT NULL,
	"received_at" timestamp with time zone DEFAULT now() NOT NULL,
	"recorded_by_user_id" uuid,
	"notes" text
);
--> statement-breakpoint
ALTER TABLE "verification_deliveries" ADD COLUMN "message_version_id" uuid;--> statement-breakpoint
ALTER TABLE "commercial_opportunities" ADD CONSTRAINT "commercial_opportunities_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "message_versions" ADD CONSTRAINT "message_versions_created_by_user_id_users_id_fk" FOREIGN KEY ("created_by_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_delivery_id_verification_deliveries_id_fk" FOREIGN KEY ("delivery_id") REFERENCES "public"."verification_deliveries"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_batch_item_id_verification_batch_items_id_fk" FOREIGN KEY ("batch_item_id") REFERENCES "public"."verification_batch_items"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_message_version_id_message_versions_id_fk" FOREIGN KEY ("message_version_id") REFERENCES "public"."message_versions"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "outreach_responses" ADD CONSTRAINT "outreach_responses_recorded_by_user_id_users_id_fk" FOREIGN KEY ("recorded_by_user_id") REFERENCES "public"."users"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "commercial_opportunities_stage_idx" ON "commercial_opportunities" USING btree ("stage");--> statement-breakpoint
CREATE UNIQUE INDEX "message_versions_template_version_uidx" ON "message_versions" USING btree ("template_name","version_number");--> statement-breakpoint
CREATE INDEX "message_versions_template_idx" ON "message_versions" USING btree ("template_name");--> statement-breakpoint
CREATE INDEX "outreach_responses_business_idx" ON "outreach_responses" USING btree ("business_id","received_at");--> statement-breakpoint
CREATE INDEX "outreach_responses_classification_idx" ON "outreach_responses" USING btree ("classification","received_at");--> statement-breakpoint
CREATE INDEX "outreach_responses_message_version_idx" ON "outreach_responses" USING btree ("message_version_id");--> statement-breakpoint
CREATE INDEX "outreach_responses_batch_item_idx" ON "outreach_responses" USING btree ("batch_item_id");--> statement-breakpoint
ALTER TABLE "verification_deliveries" ADD CONSTRAINT "verification_deliveries_message_version_id_message_versions_id_fk" FOREIGN KEY ("message_version_id") REFERENCES "public"."message_versions"("id") ON DELETE no action ON UPDATE no action;
