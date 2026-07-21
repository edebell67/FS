(() => {
  // Set to false to disable the AI assistant for this client without touching the HTML pages.
  const ASSISTANT_ENABLED = true;
  if (!ASSISTANT_ENABLED) return;

  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.AUTOGARAGE_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260716-autogarage`;
  widget.dataset.client = "autogarage_demo";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Auto garage assistant is currently unavailable.");
  document.head.append(widget);
})();
