(() => {
  const apiBase = String(window.EP044_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260715-ep044-garage`;
  widget.dataset.client = "ep044_mobile_mechanics_finchley_nw5";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("The demonstration assistant is currently unavailable.");
  document.head.append(widget);
})();
