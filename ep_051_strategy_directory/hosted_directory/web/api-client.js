/* Version history: 1.5.0 (2026-08-26) reads optional user-token/user-id meta tags and attaches them as identity headers on every private request, so pages can opt into the trusted-user identity edge declaratively.
 * 1.4.0 (2026-08-24) adds intelligence finder and comparison clients.
 * 1.3.0 (2026-08-24) adds the canonical period-aware equity-curve client.
 * 1.2.0 (2026-08-24) allows slow first-run SQL aggregates up to three minutes.
 * 1.1.0 (2026-08-24) allows bounded SQL aggregate queries up to 60 seconds.
 * 1.0.0 (2026-08-23) environment-neutral directory client. */
(function () {
  const configured =
    globalThis.DNA_API_BASE_URL ||
    document.querySelector('meta[name="api-base"]')?.content ||
    "";
  const base = configured.replace(/\/$/, "");
  async function list(params = {}) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== "" && v != null),
    );
    const controller = new AbortController(),
      timer = setTimeout(() => controller.abort(), 180000);
    try {
      const response = await fetch(`${base}/api/dna/strategies?${query}`, {
        signal: controller.signal,
        headers: { Accept: "application/json" },
      });
      if (!response.ok)
        throw new Error(`Directory request failed (${response.status})`);
      const payload = await response.json();
      if (!payload?.data?.items || !Array.isArray(payload.data.items))
        throw new Error("Unexpected directory response");
      return payload;
    } finally {
      clearTimeout(timer);
    }
  }
  async function equityCurve(strategyId, params = {}) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== "" && v != null),
    );
    const response = await fetch(
      `${base}/api/dna/strategies/${encodeURIComponent(strategyId)}/equity-curve?${query}`,
      { headers: { Accept: "application/json" } },
    );
    if (!response.ok)
      throw new Error(`Equity curve request failed (${response.status})`);
    const payload = await response.json();
    if (!Array.isArray(payload.points))
      throw new Error("Unexpected equity curve response");
    return payload;
  }
  async function products() {
    const response = await fetch(`${base}/api/dna/products`, {
      headers: { Accept: "application/json" },
    });
    if (!response.ok)
      throw new Error(`Product filter request failed (${response.status})`);
    const payload = await response.json();
    if (!Array.isArray(payload.items))
      throw new Error("Unexpected product filter response");
    return payload;
  }
  async function trades(strategyId, params = {}) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== "" && v != null),
    );
    const response = await fetch(
      `${base}/api/dna/strategies/${encodeURIComponent(strategyId)}/trades?${query}`,
      { headers: { Accept: "application/json" } },
    );
    if (!response.ok)
      throw new Error(`Trade ledger request failed (${response.status})`);
    const payload = await response.json();
    if (!Array.isArray(payload.items))
      throw new Error("Unexpected trade ledger response");
    return payload;
  }
  async function rankJourney(strategyId, params = {}) {
    const query = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== "" && v != null),
    );
    const response = await fetch(
      `${base}/api/dna/strategies/${encodeURIComponent(strategyId)}/rank-journey?${query}`,
      { headers: { Accept: "application/json" } },
    );
    if (!response.ok)
      throw new Error(`Rank journey request failed (${response.status})`);
    const payload = await response.json();
    if (!Array.isArray(payload.items))
      throw new Error("Unexpected rank journey response");
    return payload;
  }
  // Identity is read from page meta tags, never hardcoded here, so it stays a
  // per-deployment configuration choice. A page with no "user-token" meta tag
  // sends no identity headers and behaves exactly as before (public endpoints
  // work, private/trusted_user endpoints 401/503 same as always).
  const identityToken = document.querySelector('meta[name="user-token"]')?.content;
  const identityUserId = document.querySelector('meta[name="user-id"]')?.content;
  const identityHeaders = identityToken && identityUserId
    ? { Authorization: `Bearer ${identityToken}`, "X-User-ID": identityUserId }
    : {};
  async function request(path, options = {}) {
    const response = await fetch(`${base}${path}`, {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...identityHeaders,
        ...(options.headers || {}),
      },
      ...options,
    });
    if (!response.ok) {
      let detail;
      try {
        detail = (await response.json()).detail;
      } catch {}
      throw new Error(
        detail || `Intelligence request failed (${response.status})`,
      );
    }
    return response.json();
  }
  const interpret = (query) =>
    request("/api/intelligence/query/interpret", {
      method: "POST",
      body: JSON.stringify({ query }),
    });
  const intelligenceSearch = (plan) =>
    request("/api/intelligence/query/search", {
      method: "POST",
      body: JSON.stringify({ plan }),
    });
  const intelligenceCompare = (ids) =>
    request(
      `/api/intelligence/compare?strategy_ids=${encodeURIComponent(ids.join(","))}`,
    );
  const watch = (strategyId) =>
    request(
      `/api/intelligence/user/watchlist/${encodeURIComponent(strategyId)}`,
      { method: "PUT" },
    );
  const userExport = () => request("/api/intelligence/user");
  const saveSearch = (name, plan) =>
    request("/api/intelligence/user/searches", {
      method: "POST",
      body: JSON.stringify({ name, plan }),
    });
  const createCollection = (payload) =>
    request("/api/intelligence/user/collections", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  const setConsent = (history) =>
    request("/api/intelligence/user/consent", {
      method: "PUT",
      body: JSON.stringify({ history }),
    });
  const setPreferences = (preferences) =>
    request("/api/intelligence/user/preferences", {
      method: "PUT",
      body: JSON.stringify({ preferences }),
    });
  const deleteUser = () =>
    fetch(`${base}/api/intelligence/user`, { method: "DELETE" }).then(
      (response) => {
        if (!response.ok) throw new Error(`Delete failed (${response.status})`);
      },
    );
  const replaySearch = (itemId) =>
    request(`/api/intelligence/user/searches/${encodeURIComponent(itemId)}/replay`, {
      method: "POST",
    });
  const regime = (market) =>
    request("/api/intelligence/regimes/classify", {
      method: "POST",
      body: JSON.stringify({ market }),
    });
  const recommend = (payload) =>
    request("/api/intelligence/recommendations", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  globalThis.DnaDirectoryApi = {
    list,
    products,
    equityCurve,
    trades,
    rankJourney,
    interpret,
    intelligenceSearch,
    intelligenceCompare,
    watch,
    userExport,
    saveSearch,
    createCollection,
    setConsent,
    setPreferences,
    deleteUser,
    replaySearch,
    regime,
    recommend,
    identityHeaders,
    base,
  };
})();
