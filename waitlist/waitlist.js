(() => {
  const form = document.querySelector('#waitlistForm');
  const status = document.querySelector('#formStatus');
  const button = form.querySelector('button[type="submit"]');
  const params = new URLSearchParams(window.location.search);
  const endpoint = 'https://ep052-agentic-arena.onrender.com/api/waitlist';
  const value = (key) => params.get(key) || null;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const payload = {
      email: data.get('email'),
      discoverySource: data.get('discoverySource'),
      sourceDetail: data.get('sourceDetail'),
      consent: data.get('consent') === 'on',
      company: data.get('company'),
      utmSource: value('utm_source'),
      utmMedium: value('utm_medium'),
      utmCampaign: value('utm_campaign'),
      utmContent: value('utm_content'),
      landingPath: window.location.pathname,
      referrer: document.referrer || null,
    };
    button.disabled = true;
    status.textContent = 'Registering your place…';
    try {
      const response = await fetch(endpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
      const result = await response.json();
      if (!response.ok) throw new Error(result.detail || 'Registration is unavailable.');
      status.textContent = result.duplicate ? 'You are already on the waitlist. We will keep you updated.' : 'You are on the waitlist. We will be in touch.';
      form.reset();
    } catch (error) {
      status.textContent = error.message || 'Registration is unavailable. Please try again.';
    } finally {
      button.disabled = false;
    }
  });
})();
