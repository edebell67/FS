(() => {
  const apiBase = String(window.EP044_AI_API_BASE || "https://shared-website-assistant-api.onrender.com").replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260715-ep044-garage`;
  widget.dataset.client = "ep044_l_k_mobile_mechanic_nw9";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("The demonstration assistant is currently unavailable.");
  document.head.append(widget);
})();
