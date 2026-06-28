# Spike 001 — Digital product policy gates

## Question

Given EP038 wants digital-first arbitrage, when we look at marketplace rules, which digital product types are viable enough to research first without immediately hitting resale/platform-policy blockers?

## Evidence checked

### eBay UK — Electronically delivered items policy

Accessible page:

```text
https://www.ebay.co.uk/help/policies/prohibited-restricted-items/electronically-delivered-items-policy?id=4289
```

Key points observed:

- Electronically delivered items need to be listed in `Everything Else > Information Products` in classified ad format.
- If classified format is not available on the relevant eBay site, electronically delivered items are not allowed.
- Not allowed examples include:
  - software keys the seller is not authorised to sell;
  - digital copies/codes of movies included with a physical movie unless the physical disc is included.
- Exceptions listed include:
  - tickets;
  - domain names;
  - digital trading cards;
  - online gaming virtual items;
  - NFTs, subject to additional requirements.

### Blocked/needs manual or alternate access

The following pages were attempted but bot/login/security checks prevented useful extraction in this session:

- Etsy seller/reselling policies;
- Gumroad terms article;
- Envato Elements licence terms.

These should be checked manually or through alternate docs before relying on those platforms.

## Initial verdict: PARTIAL

Digital products are attractive operationally, but many third-party digital goods are high-risk for resale because of licence, IP, platform, and refund issues.

For EP038, the first digital-first research should not start with random software keys, streaming accounts, course accounts, ebooks, templates, or download packs unless resale rights are explicit and platform policy allows the sale.

## Category gate

Prioritise categories where ownership/transfer is more naturally recognised:

1. Domain names.
2. Digital collectibles/trading cards where marketplace rules explicitly allow them.
3. Online gaming virtual items/currencies only where the game and marketplace terms allow transfer.
4. Digital templates/assets only if source licence clearly grants resale/commercial redistribution rights and target marketplace permits the listing.
5. PLR/MRR products only after verifying exact licence and marketplace permissibility.

Avoid or deprioritise:

- unauthorised software licence keys;
- account resales;
- streaming/SAAS credits;
- coupon/code arbitrage;
- ebooks/courses/templates without explicit resale rights;
- anything requiring deception about ownership/source.

## Recommendation for real build

EP038 should use a compliance-first scoring gate:

```text
No clear resale/transfer rights = no candidate
No clear platform allowance = no candidate
No evidence of demand/sold prices = no candidate
No >=25% gross spread after fees/risks = no candidate
```
