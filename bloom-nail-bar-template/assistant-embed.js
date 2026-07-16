(() => {
  // Set to false to disable the AI assistant for this client without touching the HTML pages.
  const ASSISTANT_ENABLED = true;
  if (!ASSISTANT_ENABLED) return;

  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.BLOOMNAILBAR_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260716-bloomnailbar`;
  widget.dataset.client = "bloomnailbar_demo";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Bloom Nail Bar assistant is currently unavailable.");
  document.head.append(widget);
})();
