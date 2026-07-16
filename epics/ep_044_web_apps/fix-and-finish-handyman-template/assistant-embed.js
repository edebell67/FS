(() => {
  // Set to false to disable the AI assistant for this client without touching index.html/gallery.html.
  const ASSISTANT_ENABLED = true;
  if (!ASSISTANT_ENABLED) return;

  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.FIXFINISH_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260716-fixfinish`;
  widget.dataset.client = "fixfinish_demo";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Fix & Finish assistant is currently unavailable.");
  document.head.append(widget);
})();
