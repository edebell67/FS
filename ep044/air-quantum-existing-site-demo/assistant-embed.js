(() => {
  const apiBase = String(window.AIR_QUANTUM_AI_API_BASE || 'https://shared-website-assistant-api.onrender.com').replace(/\/$/, '');
  const widget = document.createElement('script');
  widget.src = `${apiBase}/widget.js?v=20260716-air-quantum`;
  widget.dataset.client = 'air_quantum_existing_site_demo';
  widget.dataset.apiBase = apiBase;
  widget.dataset.autoOpen = 'true';
  widget.defer = true;
  widget.onerror = () => console.warn('Air Quantum demonstration assistant is unavailable.');
  document.head.append(widget);
})();
