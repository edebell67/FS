(() => {
  // Set to false to disable the AI assistant for this client without HTML edits.
  const ASSISTANT_ENABLED = true;
  if (!ASSISTANT_ENABLED) return;
  // Local static QA has no registered shared-service tenant; retain direct fallback routes without a failed remote request.
  if (['127.0.0.1', 'localhost'].includes(window.location.hostname)) return;

  const apiBase = String(window.TEST02_PROSPECT_AI_API_BASE || 'https://shared-website-assistant-api.onrender.com').replace(/\/$/, '');
  const client = 'test02_prospect_ltd';
  // Verify the public tenant endpoint before loading the widget so an unavailable
  // shared service never creates a console error or blocks the local site.
  fetch(`${apiBase}/api/public/config?client=${encodeURIComponent(client)}`, { credentials: 'omit' })
    .then(response => {
      if (!response.ok) return;
      const widget = document.createElement('script');
      widget.src = `${apiBase}/widget.js?v=20260805-test02-prospect`;
      widget.dataset.client = client;
      widget.dataset.apiBase = apiBase;
      widget.defer = true;
      widget.onerror = () => console.warn('Test02 Prospect assistant is currently unavailable. Use phone, email, or the site-visit page.');
      document.head.append(widget);
    })
    .catch(() => { /* Direct phone, email and site-visit routes remain available. */ });
})();
