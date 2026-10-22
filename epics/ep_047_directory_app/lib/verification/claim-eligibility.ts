export function canRequestPublicClaim(stageKey: string | null | undefined): boolean {
  return stageKey === "verification_completed";
}
