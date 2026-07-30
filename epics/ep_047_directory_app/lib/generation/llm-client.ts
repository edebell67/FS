/**
 * lib/generation/llm-client.ts — thin, provider-agnostic call to whichever
 * LLM the generation loop is configured to use.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-30 · Initial version: plain fetch against the Anthropic
 *   Messages API or the OpenAI Chat Completions API, no SDK dependency added
 *   until a provider is actually chosen. Single-call, no tool use -- the
 *   model returns the finished file set as one structured response (see
 *   run-generation.ts for the expected shape).
 */

import type { GenerationConfig } from "@/lib/generation/config";

/** Sends one prompt, returns the model's raw text response. */
export async function callLlm(config: GenerationConfig, systemPrompt: string, userPrompt: string): Promise<string> {
  if (config.provider === "anthropic") {
    return callAnthropic(config, systemPrompt, userPrompt);
  }
  return callOpenAi(config, systemPrompt, userPrompt);
}

async function callAnthropic(config: GenerationConfig, systemPrompt: string, userPrompt: string): Promise<string> {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": config.apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: config.model,
      max_tokens: 16000,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }],
    }),
  });

  if (!res.ok) {
    throw new Error(`Anthropic API error ${res.status}: ${await res.text()}`);
  }

  const data = (await res.json()) as { content: { type: string; text?: string }[] };
  const text = data.content.find((block) => block.type === "text")?.text;
  if (!text) throw new Error("Anthropic response contained no text content.");
  return text;
}

async function callOpenAi(config: GenerationConfig, systemPrompt: string, userPrompt: string): Promise<string> {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${config.apiKey}`,
    },
    body: JSON.stringify({
      model: config.model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
    }),
  });

  if (!res.ok) {
    throw new Error(`OpenAI API error ${res.status}: ${await res.text()}`);
  }

  const data = (await res.json()) as { choices: { message: { content: string } }[] };
  const text = data.choices[0]?.message?.content;
  if (!text) throw new Error("OpenAI response contained no text content.");
  return text;
}
