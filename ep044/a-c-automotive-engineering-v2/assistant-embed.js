(() => {
  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.HOXTANS_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260714-demo-workflows-2`;
  widget.dataset.client = "auto_ac_goldhawk";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Hoxtans assistant is currently unavailable.");
  document.head.append(widget);
})();
