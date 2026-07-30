import { sql, type SQL } from "drizzle-orm";
import { businesses } from "@/lib/db/schema";

/** The single public eligibility predicate used by every public directory query. */
export function publicScopeWhere(): SQL {
  return sql`(
    EXISTS (SELECT 1 FROM public_directory_settings s WHERE s.id = 'default'
      AND (s.town_mode = 'all' OR NOT EXISTS (SELECT 1 FROM public_town_visibility t
        WHERE t.town_key = lower(trim(${businesses.town})) AND t.is_enabled = false)))
    AND EXISTS (SELECT 1 FROM public_directory_settings s WHERE s.id = 'default'
      AND (s.category_mode = 'all' OR NOT EXISTS (SELECT 1 FROM public_category_visibility c
        WHERE c.category_key = lower(trim(${businesses.category})) AND c.is_enabled = false)))
    AND COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = ${businesses.id}), 'inherit') <> 'hide'
    AND (COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = ${businesses.id}), 'inherit') <> 'show'
      OR TRUE)
  )`;
}
