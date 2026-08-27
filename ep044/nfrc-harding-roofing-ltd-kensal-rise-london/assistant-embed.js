(() => {
  const ASSISTANT_ENABLED = true;
  if (!ASSISTANT_ENABLED) return;
  const local = ["localhost", "127.0.0.1"].includes(location.hostname);
  const apiBase = String(window.THE_TECH_PRINCIPLE_AI_API_BASE || (local ? "http://127.0.0.1:4310" : "https://shared-website-assistant-api.onrender.com")).replace(/\/$/, "");
  const widget = document.createElement("script");
  widget.src = `${apiBase}/widget.js?v=a31871e-nfrc-harding-roofing-ltd-kensal-rise-london`;
  widget.dataset.client = "batch02_nfrc_harding_roofing_ltd_kensal_rise_london";
  widget.dataset.apiBase = apiBase;
  widget.dataset.autoOpen = "false";
  widget.defer = true;
  widget.onerror = () => console.warn("Nfrc Harding Roofing Ltd - Kensal Rise London private-review assistant is currently unavailable.");
  document.head.append(widget);
})();
