"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

/**
 * Renders the site logo + nav links.
 * On verify/claim pages (where a business owner needs to focus on a form),
 * the logo and all nav links are rendered as non-clickable text to prevent
 * navigation away.
 */
export function SiteHeaderNav() {
  const pathname = usePathname();
  const isFocusPage = pathname.startsWith("/verify/") || pathname.startsWith("/claim");

  function navLink(
    href: string,
    label: string,
    external?: boolean,
  ) {
    if (isFocusPage) {
      return (
        <span className="cursor-default text-[#9aa3a5]">
          {label}
        </span>
      );
    }
    if (external) {
      return (
        <a href={href} className="hover:text-brand-700">
          {label}
        </a>
      );
    }
    return (
      <Link href={href} className="hover:text-brand-700">
        {label}
      </Link>
    );
  }

  return (
    <>
      <div className="font-display text-2xl font-semibold tracking-[-0.04em] text-[#152022]">
        {isFocusPage ? (
          <span>
            TTP <span className="text-brand-600">Directory</span>
          </span>
        ) : (
          <Link href="/directory">
            TTP <span className="text-brand-600">Directory</span>
          </Link>
        )}
      </div>
      <nav className="flex items-center gap-6 text-sm font-medium text-[#4c5657]">
        {navLink("https://thetechprinciple.com/", "TTP", true)}
        {navLink("/directory/search", "Search")}
        {navLink("https://thetechprinciple.com/news/", "News", true)}
      </nav>
    </>
  );
}