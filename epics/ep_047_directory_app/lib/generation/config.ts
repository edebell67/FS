/**
 * lib/generation/config.ts — reads which LLM provider/model the site-
 * generation loop should use, and whether it's configured yet at all.
 *
 * VERSION HISTORY
 * v1.1.0 · 2026-07-30 · Adds GENERATION_MODE ("local" | "hosted"). The
 *   subscription-driven local path (the existing 30-minute deploying agent
 *   running ep044_group skills itself, no per-call API cost) and this
 *   hosted LLM-API path must never both run against the same queue --
 *   isGenerationConfigured() now also requires GENERATION_MODE=hosted, so
 *   flipping the flag is what turns this path on, not just supplying a key.
 * v1.0.0 · 2026-07-29 · Initial version: provider/model/key come from env,
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

/**
 * Null whenever this (hosted) path should not run at all -- either because
 * GENERATION_MODE isn't "hosted" (the local subscription-agent path owns the
 * queue instead) or because the LLM isn't configured yet. Either way the
 * caller's cue is the same: skip cleanly, never fail the cron run.
 */
export function getGenerationConfig(): GenerationConfig | null {
  if (process.env.GENERATION_MODE !== "hosted") return null;

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
