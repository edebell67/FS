import { redirect } from "next/navigation";

// This app is mounted at thetechprinciple.com/directory and /directoryadmin
// (see PLAN.md and the epic README for why) — the bare root only matters for
// direct access (this app's own Render URL, or localhost in dev), where it
// should just land on the public directory.
export default function RootPage() {
  redirect("/directory");
}
