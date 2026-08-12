const STOP_WORDS = new Set(["a", "an", "and", "are", "can", "do", "for", "how", "i", "in", "is", "it", "me", "of", "on", "the", "to", "what", "where", "you", "your"]);

function tokens(value) {
  return [...new Set(String(value).toLowerCase().match(/[a-z0-9£]+/g) || [])].filter((token) => token.length > 1 && !STOP_WORDS.has(token));
}

export function retrieveKnowledge(client, message, limit = 3) {
  const query = tokens(message);
  if (/how much|price|cost|charge|fee/i.test(message)) query.push("pricing", "price", "cost");
  if (/when.*open|opening time|hours/i.test(message)) query.push("hours", "opening");
  const ranked = (client.knowledge || [])
    .map((item) => {
      const titleTokens = tokens(item.title);
      const contentTokens = tokens(item.content);
      const score = query.reduce((total, token) => total + (titleTokens.includes(token) ? 4 : 0) + (contentTokens.includes(token) ? 1 : 0), 0);
      return { ...item, score };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score);
  const relevanceFloor = (ranked[0]?.score || 0) * 0.6;
  return ranked
    .filter((item) => item.score >= relevanceFloor)
    .slice(0, limit);
}

export function detectModuleResponse(client, message) {
  const normalized = message.toLowerCase();
  const enabled = new Set(client.enabledModules || []);

  if (enabled.has("navigation") && !/\bdemo\b/.test(normalized)) {
    const asksToNavigate = /\b(page|show|find|where|visit|testimonial|testimonials|review|reviews)\b|take me/.test(normalized);
    const page = asksToNavigate && (client.pages || []).find((item) => (item.keywords || []).some((keyword) => normalized.includes(keyword.toLowerCase())));
    if (page) return { text: `I found the ${page.title} page for you.`, action: { type: "navigate", label: `Open ${page.title}`, url: page.url } };
  }

  if (/book|appointment|schedule|calendar/.test(normalized) && enabled.has("demoBooking")) {
    return { text: "I can demonstrate a complete appointment journey using seeded availability. Nothing will be booked for real.", action: { type: "demo-booking", label: "Try demo booking" } };
  }

  if (/\b(pay|payment|checkout|card|receipt)\b/.test(normalized) && enabled.has("demoPayment")) {
    return { text: "I can run a simulated checkout with a fictional demo card and produce a mock receipt. No charge will be made.", action: { type: "demo-payment", label: "Try demo payment" } };
  }

  if ((/\b(email demo|demo email)\b/.test(normalized) || /\b(send|preview)\b.{0,24}\bemail\b/.test(normalized)) && enabled.has("demoEmail")) {
    return { text: "I can prepare an email preview and place it in the demo outbox. It will not be sent.", action: { type: "demo-email", label: "Try demo email" } };
  }

  if (/\bcrm\b|customer relationship|create.{0,20}\blead\b/.test(normalized) && enabled.has("demoCrm")) {
    return { text: "I can create a fictional contact in the demo CRM pipeline without connecting to a real customer system.", action: { type: "demo-crm", label: "Try demo CRM" } };
  }

  if (/book|appointment|schedule|calendar/.test(normalized)) {
    if (enabled.has("booking") && client.booking?.url) {
      return { text: `You can arrange an appointment through ${client.booking.provider || "our booking page"}.`, action: { type: "booking", label: "Book an appointment", url: client.booking.url } };
    }
    if (enabled.has("callback")) return { text: "Online booking is not available here, but I can collect a callback request.", action: { type: "callback", label: "Request a callback" } };
  }

  if (/callback|call\s+(?:me\s+)?back|phone me|ring me/.test(normalized) && enabled.has("callback")) {
    return { text: "Of course. Share a few details and the team can call you back.", action: { type: "callback", label: "Request a callback" } };
  }

  if (/quote|estimate|interested|enquiry|inquiry/.test(normalized) && enabled.has("leadCapture")) {
    return { text: "I can pass your enquiry to the team without making you repeat yourself.", action: { type: "lead", label: "Send an enquiry" } };
  }

  if (/contact|telephone|phone|email|address|location|located|open/.test(normalized) && enabled.has("contact") && client.contact) {
    const c = client.contact;
    return { text: `You can call ${c.telephone}, email ${c.email}, or visit ${c.address}. Opening hours: ${c.openingHours}.`, action: { type: "contact", label: `Call ${c.telephone}`, url: `tel:${c.telephone.replace(/\s/g, "")}` } };
  }

  return null;
}

// The single "no direct answer" reply, used by both the deterministic and
// LLM-configured paths so the fallback behaves identically either way. The
// widget (not this function) decides whether to show the full email prompt
// or a short "added to your list" acknowledgement — that depends on
// per-session state this server call has no visibility into. The action
// type is the only signal the widget needs: it means "this question has no
// approved answer", every time, regardless of session history.
function noAnswerReply() {
  return {
    text: "I don't have an approved answer for that yet, but I can get you a properly researched one by email.",
    sources: [],
    action: { type: "question-followup", label: "Email me the answer" }
  };
}

export function deterministicReply(client, message, matches) {
  const quickAnswer = client.quickAnswers?.[String(message).trim().toLowerCase()];
  if (quickAnswer) return { text: quickAnswer.text, sources: [{ id: quickAnswer.id, title: quickAnswer.title }] };
  const moduleResponse = detectModuleResponse(client, message);
  if (moduleResponse) return { ...moduleResponse, sources: [] };
  if (matches.length) {
    return {
      text: matches.map((item) => item.content).join(" "),
      sources: matches.map((item) => ({ id: item.id, title: item.title }))
    };
  }
  return noAnswerReply();
}

function extractResponseText(payload) {
  for (const item of payload.output || []) {
    if (item.type !== "message") continue;
    for (const content of item.content || []) {
      if (content.type === "output_text" && content.text) return content.text;
    }
  }
  return "";
}

export async function createAssistantReply({ client, message, history = [], env = process.env, fetchImpl = fetch }) {
  const quickAnswer = client.quickAnswers?.[String(message).trim().toLowerCase()];
  if (quickAnswer) return { text: quickAnswer.text, sources: [{ id: quickAnswer.id, title: quickAnswer.title }] };
  const matches = retrieveKnowledge(client, message);
  const moduleResponse = detectModuleResponse(client, message);
  if (moduleResponse) return { ...moduleResponse, sources: [] };
  // No approved knowledge and no module match: this is the same precise,
  // already-available "no direct answer" signal deterministicReply() uses.
  // Go straight to the email-offer fallback rather than asking the model to
  // say it doesn't know — that would need fragile prose-parsing to detect
  // reliably, and produces the same outcome either way.
  if (matches.length === 0) return noAnswerReply();
  if (!env.OPENAI_API_KEY) return deterministicReply(client, message, matches);

  const approvedContext = matches.map((item) => `[${item.title}] ${item.content}`).join("\n");
  const instructions = `You are the website assistant for ${client.businessName}. Answer professionally and concisely. Use only APPROVED KNOWLEDGE below. Never infer prices, guarantees, policies, availability, or service coverage.\n\nAPPROVED KNOWLEDGE\n${approvedContext}`;
  const input = [...history.slice(-8), { role: "user", content: message }].map((item) => ({ role: item.role, content: String(item.content).slice(0, 2000) }));
  const response = await fetchImpl(`${env.OPENAI_BASE_URL || "https://api.openai.com/v1"}/responses`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${env.OPENAI_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: env.OPENAI_MODEL || "gpt-5.4-mini", instructions, input, max_output_tokens: 350 })
  });
  if (!response.ok) throw new Error(`Model provider returned ${response.status}.`);
  const text = extractResponseText(await response.json());
  if (!text) throw new Error("Model provider returned no text.");
  return { text, sources: matches.map((item) => ({ id: item.id, title: item.title })) };
}
