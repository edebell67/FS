import { toSlug } from "@/lib/db/queries/directory";

export interface NewsDirectoryLinkInput {
  town: string;
  categories: string[];
  publicTowns: string[];
  publicCategories: string[];
}

/** Prefer a precise town/category route, then fall back to the public town route. */
export function resolveNewsDirectoryLink(input: NewsDirectoryLinkInput): string | null {
  const town = input.town.trim();
  const publicTown = input.publicTowns.some((value) => value.trim().toLowerCase() === town.toLowerCase());
  if (!publicTown) return null;
  const category = input.categories.find((candidate) =>
    input.publicCategories.some((value) => value.trim().toLowerCase() === candidate.trim().toLowerCase())
  );
  if (category) return `/directory/town/${toSlug(town)}?category=${encodeURIComponent(category.trim())}`;
  return `/directory/town/${toSlug(town)}`;
}
