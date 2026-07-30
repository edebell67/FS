/**
 * lib/generation/config.ts — reads which LLM provider/model the site-
 * generation loop should use, and whether it's configured yet at all.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-30 · Initial version: provider/model/key come from env,
 *   never hardcoded; isGenerationConfigured() is the single fail-closed gate
 *   the orchestrator checks before doing any LLM work, so an unset key skips
 *   cleanly instead of erroring the whole cron run.
 */

export type LlmProvider = "anthropic" | "openai";

export type GenerationConfig = {
  provider: LlmProvider;
  model: string;
  apiKey: string;
};

/** Null when no provider is configured yet — the caller's cue to skip generation, not fail. */
export function getGenerationConfig(): GenerationConfig | null {
  const provider = process.env.LLM_PROVIDER as LlmProvider | undefined;
  if (!provider) return null;

  if (provider !== "anthropic" && provider !== "openai") {
    throw new Error(`LLM_PROVIDER must be "anthropic" or "openai", got "${provider}".`);
  }

  const apiKey = provider === "anthropic" ? process.env.ANTHROPIC_API_KEY : process.env.OPENAI_API_KEY;
  if (!apiKey) return null;

  const model = process.env.LLM_MODEL;
  if (!model) return null;

  return { provider, model, apiKey };
}

export function isGenerationConfigured(): boolean {
  return getGenerationConfig() !== null;
}
