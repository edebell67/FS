export const CANONICAL_PRODUCTION_ORIGIN = "https://thetechprinciple.com";

type VerificationUrlEnvironment = Partial<
  Record<"NODE_ENV" | "NEXT_PUBLIC_SITE_URL", string | undefined>
>;

function configuredOrigin(env: VerificationUrlEnvironment): string | null {
  const configured = env.NEXT_PUBLIC_SITE_URL?.trim();
  if (!configured) return null;
  try {
    const url = new URL(configured);
    if (!["http:", "https:"].includes(url.protocol)) return null;
    return url.origin;
  } catch {
    return null;
  }
}

export function verificationCapabilityOrigin(
  env: VerificationUrlEnvironment = process.env,
): string {
  if (env.NODE_ENV === "production") return CANONICAL_PRODUCTION_ORIGIN;

  const configured = configuredOrigin(env);
  if (configured) return configured;

  return env.NODE_ENV === "development"
    ? "http://localhost:8140"
    : CANONICAL_PRODUCTION_ORIGIN;
}

export function verificationCapabilityUrl(
  rawToken: string,
  env: VerificationUrlEnvironment = process.env,
): string {
  return `${verificationCapabilityOrigin(env)}/verify/${encodeURIComponent(rawToken)}`;
}

export function businessListingUrl(
  slug: string,
  env: VerificationUrlEnvironment = process.env,
): string {
  return `${verificationCapabilityOrigin(env)}/directory/business/${encodeURIComponent(slug)}`;
}

export function trackingClickUrl(
  deliveryId: string, trackingKey: string, rawToken: string,
  env: VerificationUrlEnvironment = process.env,
): string {
  return `${verificationCapabilityOrigin(env)}/v/c/${encodeURIComponent(deliveryId)}/${encodeURIComponent(trackingKey)}/${encodeURIComponent(rawToken)}`;
}

export function trackingPixelUrl(
  deliveryId: string, trackingKey: string,
  env: VerificationUrlEnvironment = process.env,
): string {
  return `${verificationCapabilityOrigin(env)}/v/o/${encodeURIComponent(deliveryId)}/${encodeURIComponent(trackingKey)}.gif`;
}
