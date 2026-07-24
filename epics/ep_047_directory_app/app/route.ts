import { proxyGitHubPagesRequest } from "@/lib/github-pages-proxy-handler";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  return proxyGitHubPagesRequest(request);
}

export async function HEAD(request: Request) {
  return proxyGitHubPagesRequest(request);
}
