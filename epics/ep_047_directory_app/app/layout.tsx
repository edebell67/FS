import type { Metadata } from "next";
import "./globals.css";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { SITE_NAME, SITE_URL } from "@/lib/site-config";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: `${SITE_NAME} — Find a business you can trust`,
    template: `%s — ${SITE_NAME}`,
  },
  description:
    "A searchable directory of local businesses, from first import to active subscriber.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#f6f3ed] text-[#152022] antialiased">
        <SiteHeader />
        {children}
      </body>
    </html>
  );
}
