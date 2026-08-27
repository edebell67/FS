(() => {
  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.TEST02_PROSPECT_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260805-test02-prospect`;
  widget.dataset.client = "test02_prospect_ltd";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Test02 Prospect assistant is currently unavailable. Use phone, email, or the site-visit page.");
  document.head.append(widget);
})();