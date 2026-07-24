import { requireAdminUserForPage } from "@/lib/auth/require";
import ImportPageClient from "./ImportPageClient";

export const dynamic = "force-dynamic";

// Server wrapper — the actual page is a client component (drag-and-drop
// state, XHR upload progress), but the auth check must run server-side
// (getCurrentUser touches the DB and reads an httpOnly cookie, neither of
// which a client component can do).
export default async function ImportPage() {
  await requireAdminUserForPage("/directoryadmin/import");
  return <ImportPageClient />;
}
