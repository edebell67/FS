(() => {
  // Shared Render-hosted assistant API. The public client key remains tenant-scoped.
  const apiBase = String(window.FUNCUTS_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260715-fun-cuts-launch`;
  widget.dataset.client = "funcuts_se20";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("Fun Cuts assistant is currently unavailable.");
  document.head.append(widget);
})();
