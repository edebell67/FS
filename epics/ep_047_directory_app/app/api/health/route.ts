import { NextResponse } from "next/server";
import { sql } from "drizzle-orm";
import { db } from "@/lib/db/client";

// Must run per-request, not be statically collected at build time — there is
// no DATABASE_URL available during `next build`, only at runtime on Render.
export const dynamic = "force-dynamic";

// Render's health check hits this path (see render.yaml). It must prove the
// app can actually reach Postgres, not just that the Node process is up —
// a 200 here is what Render uses to decide the deploy is good and traffic
// can be routed to it.
export async function GET() {
  try {
    await db.execute(sql`SELECT 1`);
    return NextResponse.json(
      { status: "ok", db: "connected", timestamp: new Date().toISOString() },
      { status: 200 }
    );
  } catch (error) {
    console.error("Health check failed:", error);
    return NextResponse.json(
      {
        status: "error",
        db: "unreachable",
        timestamp: new Date().toISOString(),
      },
      { status: 503 }
    );
  }
}
