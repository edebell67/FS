// Canonical visitor-facing assistant functions defined by the common site
// blueprint (skills/ep044_group/ep044_common_site_blueprint/000_site_blueprint.md,
// sections 2 "Common architecture" and 4 "AI assistant requirements").
//
// This is the shared inheritance contract: category skills and client profiles
// may decide WHICH of these are available, but must not invent a different
// vocabulary. Order here is the order buttons are presented to the visitor and
// follows the blueprint's conversion hierarchy (section 5): inspire, establish
// trust, explain the service, remove objections, then request the enquiry.

// `module`  - the enabled module this function needs, when it maps to one.
// `knowledge` - true when the deterministic knowledge retriever can answer it
//               from approved client knowledge, so the function is still useful
//               on a client that has no dedicated page for it yet.
export const BLUEPRINT_FUNCTIONS = [
  { key: "services", label: "Services", prompt: "What services do you provide?", knowledge: true },
  { key: "gallery", label: "Our Work", prompt: "Can I see examples of your work?" },
  { key: "transformations", label: "Before & After", prompt: "Can I see before and after examples?" },
  { key: "reviews", label: "Reviews", prompt: "What do your customers say about you?" },
  { key: "about", label: "About Us", prompt: "Tell me about your business.", knowledge: true },
  { key: "pricing", label: "Pricing Guide", prompt: "How much do your services cost?", knowledge: true },
  { key: "areas", label: "Areas Covered", prompt: "Which areas do you cover?", knowledge: true },
  { key: "knowledge", label: "Knowledge Centre", prompt: "Do you have any helpful guides or articles?" },
  { key: "faq", label: "FAQ", prompt: "What are your most common questions?", module: "faq", knowledge: true },
  { key: "contact", label: "Contact", prompt: "How can I contact you?", module: "contact" },
  { key: "quote", label: "Request a Quote", prompt: "I would like a quote.", module: "leadCapture" },
  { key: "booking", label: "Book", prompt: "I would like to book an appointment.", module: "booking" },
  { key: "callback", label: "Request a Callback", prompt: "Please call me back.", module: "callback" }
];

export const BLUEPRINT_KEYS = new Set(BLUEPRINT_FUNCTIONS.map((item) => item.key));

// Platform demonstration workflows. These are NOT blueprint visitor functions -
// they exist to show a prospect what the platform can do, so they are resolved
// separately and presented as a visually distinct group in the widget.
export const DEMO_FUNCTIONS = [
  { key: "demoBooking", label: "Demo booking", prompt: "Show the demo booking flow", module: "demoBooking" },
  { key: "demoPayment", label: "Demo payment", prompt: "Show the demo payment checkout", module: "demoPayment" },
  { key: "demoEmail", label: "Demo email", prompt: "Preview a demo email", module: "demoEmail" },
  { key: "demoCrm", label: "Demo CRM", prompt: "Create a demo CRM lead", module: "demoCrm" }
];

/**
 * Resolve which blueprint functions a client can actually offer.
 *
 * A function is offered when any of these is true, in priority order:
 *   1. the client has a page tagged with that blueprint key (and navigation is
 *      enabled) - the button navigates straight to the real page;
 *   2. the function maps to an enabled module - the assistant handles it;
 *   3. the function is answerable from approved knowledge and the client has
 *      approved knowledge recorded.
 *
 * Anything else is hidden, so a client that has not yet been upgraded to the
 * blueprint architecture degrades gracefully instead of offering dead buttons.
 */
export function resolveBlueprintActions(client, retrieve) {
  const enabled = new Set(client.enabledModules || []);
  const hasNavigation = enabled.has("navigation");
  const pages = client.pages || [];

  const actions = [];
  for (const fn of BLUEPRINT_FUNCTIONS) {
    const page = hasNavigation ? pages.find((item) => item.blueprint === fn.key && item.url) : undefined;
    if (page) {
      actions.push({ key: fn.key, label: page.title || fn.label, type: "navigate", url: page.url, prompt: fn.prompt });
      continue;
    }
    if (fn.module && enabled.has(fn.module)) {
      actions.push({ key: fn.key, label: fn.label, type: "prompt", prompt: fn.prompt });
      continue;
    }
    // Only offer a knowledge-backed button when the retriever actually matches
    // approved knowledge for it. Blueprint sections 5 and 13 require no dead
    // ends, and an unmatched button would answer "I don't have approved
    // information for that", which is exactly that.
    if (fn.knowledge && !fn.module && typeof retrieve === "function" && retrieve(client, fn.prompt).length) {
      actions.push({ key: fn.key, label: fn.label, type: "prompt", prompt: fn.prompt });
    }
  }
  return actions;
}

/** Resolve the platform demonstration workflows a client has switched on. */
export function resolveDemoActions(client) {
  if (client.status !== "demo") return [];
  const enabled = new Set(client.enabledModules || []);
  return DEMO_FUNCTIONS
    .filter((fn) => enabled.has(fn.module))
    .map((fn) => ({ key: fn.key, label: fn.label, type: "prompt", prompt: fn.prompt }));
}
