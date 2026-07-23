CREATE TABLE "businesses" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"business_ref" text NOT NULL,
	"slug" text NOT NULL,
	"business_name" text NOT NULL,
	"trading_name" text,
	"category" text NOT NULL,
	"sub_category" text,
	"email" text,
	"phone" text,
	"mobile" text,
	"website" text,
	"facebook" text,
	"instagram" text,
	"linkedin" text,
	"address" text,
	"town" text,
	"county" text,
	"postcode" text,
	"latitude" double precision,
	"longitude" double precision,
	"google_rating" double precision,
	"review_count" integer,
	"opening_hours" jsonb,
	"description" text,
	"imported_source" text NOT NULL,
	"import_batch_id" uuid,
	"import_date" timestamp with time zone DEFAULT now() NOT NULL,
	"last_updated" timestamp with time zone DEFAULT now() NOT NULL,
	"status" text DEFAULT 'active' NOT NULL,
	"current_stage_id" integer,
	"stage_entered_at" timestamp with time zone,
	"notes" text,
	"internal_notes" text,
	"tags" text[],
	CONSTRAINT "businesses_business_ref_unique" UNIQUE("business_ref"),
	CONSTRAINT "businesses_slug_unique" UNIQUE("slug")
);
--> statement-breakpoint
CREATE TABLE "category_sequences" (
	"category_code" text PRIMARY KEY NOT NULL,
	"next_val" bigint DEFAULT 1 NOT NULL
);
--> statement-breakpoint
CREATE TABLE "import_batches" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"filename" text NOT NULL,
	"source" text NOT NULL,
	"uploaded_by" text,
	"status" text DEFAULT 'processing' NOT NULL,
	"total_rows" integer DEFAULT 0 NOT NULL,
	"accepted_rows" integer DEFAULT 0 NOT NULL,
	"rejected_rows" integer DEFAULT 0 NOT NULL,
	"duplicate_rows" integer DEFAULT 0 NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"completed_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "import_row_errors" (
	"id" serial PRIMARY KEY NOT NULL,
	"batch_id" uuid NOT NULL,
	"row_number" integer NOT NULL,
	"column" text,
	"raw_value" text,
	"error_code" text NOT NULL,
	"message" text NOT NULL
);
--> statement-breakpoint
CREATE TABLE "pipeline_stages" (
	"id" serial PRIMARY KEY NOT NULL,
	"key" text NOT NULL,
	"label" text NOT NULL,
	"sort_order" integer NOT NULL,
	"board_column" text NOT NULL,
	"is_terminal" boolean DEFAULT false NOT NULL,
	"sla_hours" integer,
	CONSTRAINT "pipeline_stages_key_unique" UNIQUE("key")
);
--> statement-breakpoint
CREATE TABLE "schema_migrations" (
	"id" serial PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"applied_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "schema_migrations_name_unique" UNIQUE("name")
);
--> statement-breakpoint
CREATE TABLE "stage_transitions" (
	"id" serial PRIMARY KEY NOT NULL,
	"business_id" uuid NOT NULL,
	"from_stage_id" integer,
	"to_stage_id" integer NOT NULL,
	"occurred_at" timestamp with time zone DEFAULT now() NOT NULL,
	"actor_user_id" text,
	"source" text NOT NULL,
	"reason" text,
	"notes" text
);
--> statement-breakpoint
ALTER TABLE "businesses" ADD CONSTRAINT "businesses_import_batch_id_import_batches_id_fk" FOREIGN KEY ("import_batch_id") REFERENCES "public"."import_batches"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "businesses" ADD CONSTRAINT "businesses_current_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("current_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "import_row_errors" ADD CONSTRAINT "import_row_errors_batch_id_import_batches_id_fk" FOREIGN KEY ("batch_id") REFERENCES "public"."import_batches"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_business_id_businesses_id_fk" FOREIGN KEY ("business_id") REFERENCES "public"."businesses"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_from_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("from_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "stage_transitions" ADD CONSTRAINT "stage_transitions_to_stage_id_pipeline_stages_id_fk" FOREIGN KEY ("to_stage_id") REFERENCES "public"."pipeline_stages"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE INDEX "businesses_category_idx" ON "businesses" USING btree ("category");--> statement-breakpoint
CREATE INDEX "businesses_town_idx" ON "businesses" USING btree ("town");--> statement-breakpoint
CREATE INDEX "businesses_county_idx" ON "businesses" USING btree ("county");--> statement-breakpoint
CREATE INDEX "businesses_email_idx" ON "businesses" USING btree ("email");--> statement-breakpoint
CREATE INDEX "businesses_stage_idx" ON "businesses" USING btree ("current_stage_id");--> statement-breakpoint
CREATE INDEX "import_row_errors_batch_idx" ON "import_row_errors" USING btree ("batch_id");--> statement-breakpoint
CREATE INDEX "stage_transitions_business_idx" ON "stage_transitions" USING btree ("business_id","occurred_at");--> statement-breakpoint
CREATE INDEX "stage_transitions_stage_idx" ON "stage_transitions" USING btree ("to_stage_id","occurred_at");