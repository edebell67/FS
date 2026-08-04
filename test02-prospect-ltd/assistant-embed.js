(() => {
  // Set to false to disable the AI assistant for this client without touching the HTML pages.
  // Owner-controlled override: shared tenant registration is not yet available.
const ASSISTANT_ENABLED = false;
  if (!ASSISTANT_ENABLED) return;

  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.TEST02_PROSPECT_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260803-test02-prospect`;
  widget.dataset.client = "test02_prospect_ltd";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Test02 Prospect assistant is currently unavailable.");
  document.head.append(widget);
})();
