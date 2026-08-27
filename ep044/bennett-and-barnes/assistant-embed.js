(() => {
  const apiBase = "https://shared-website-assistant-api.onrender.com";
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=20260715-ep044-garage`;
  widget.dataset.client = "ep044_bennett_and_barnes";
  widget.dataset.apiBase = apiBase;
  widget.defer = true;
  widget.onerror = () => console.warn("The demonstration assistant is currently unavailable.");
  document.head.append(widget);
})();
