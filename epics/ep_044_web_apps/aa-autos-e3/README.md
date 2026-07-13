# Ridgeline Motor Works — Garage Sales-Demo Website Template

A static HTML/CSS/JS website template for auto garages, MOT stations and
mechanics — built to be sent as a personalised demo link to a garage owner as
part of a direct sales campaign, then converted into a live site.

Sample data throughout ("Ridgeline Motor Works") is placeholder content for
demonstration only — see [Personalisation checklist](#personalisation-checklist).

## Structure

```
garage-site/
├── index.html            Homepage — all sections, driven by config.js
├── owner-preview.html     /owner-preview route — conversion page for the garage owner
├── assets/
│   ├── css/styles.css    Design system + all component styles
│   ├── js/config.js      SINGLE SOURCE OF TRUTH — all garage content lives here
│   └── js/main.js        Rendering + interactions (reads config.js, no garage
│                          data is hard-coded here)
└── README.md
```

No build step, no framework, no dependencies beyond one Google Fonts request.
Open `index.html` directly in a browser, or serve the folder with any static
file server.

## Personalising for a new garage

Everything visible on the site is driven by four data objects in
[assets/js/config.js](assets/js/config.js). To rebrand for a new garage, edit
**only this file**:

| Object | Controls |
|---|---|
| `garageConfig` | Identity, contact, hours, colours, stats, about copy, trust indicators, why-choose-us, specialisms, social links, booking/payment links, SEO |
| `servicesData` | Service cards (homepage + quote form dropdown) |
| `reviewsData` | Review carousel — mark real reviews by removing `placeholder: true` |
| `galleryData` | Gallery captions/categories |
| `offersData` | Offer cards — toggle with `enabled: true/false` |
| `diagnosticSymptoms` | "What's wrong with your vehicle?" symptom picker |
| `paymentProducts` | Payment demonstration product list |

Brand colours (`primaryColour`, `secondaryColour`, `accentColour`,
`accentColourAlt`) are also mirrored as CSS variables at the top of
`styles.css` (`:root`) — update both places to fully re-theme.

The garage name/initials in the header logo emblem, footer, browser tab
title, and `owner-preview.html` all update automatically from
`garageConfig.businessName` / `shortName` / `emblemInitials` — no per-section
editing required.

### Personalisation checklist

- [ ] `businessName`, `shortName`, `tagline`, `emblemInitials`
- [ ] `phone`, `whatsapp`, `email`, `address`, `postcode`, `mapEmbedUrl`, `directionsUrl`
- [ ] `openingHours`
- [ ] `primaryColour` / `secondaryColour` / `accentColour` / `accentColourAlt` (config.js **and** styles.css `:root`)
- [ ] `stats` (remove `placeholder: true` once figures are verified)
- [ ] `about` (established, founder, technicians, bodyCopy, values)
- [ ] `servicesData` (edit list, prices)
- [ ] `reviewsData` (replace with genuine reviews before launch)
- [ ] `galleryData` + real photography (see [Images](#images--video))
- [ ] `offersData` (edit or disable)
- [ ] `socialLinks`
- [ ] `bookingUrl` / `paymentUrl` / `motBookingUrl` / `tyreQuoteUrl`
- [ ] `seo` block (title, description, canonicalUrl)
- [ ] Google Maps embed (`mapEmbedUrl`, iframe `src` in `index.html`)
- [ ] Legal pages linked from the footer (Privacy, Cookies, Terms, Accessibility)
- [ ] `demoMode` → `false` once a backend/payment provider is connected

## Demo mode

`garageConfig.demoMode` (default `true`) governs:

- Forms show an in-page "thank you, this was a demonstration" confirmation
  instead of sending data anywhere.
- Payment buttons open a "demonstration only" modal — no card details are
  collected.
- The discreet owner banner and `/owner-preview` page remain visible.

Set `demoMode: false` and wire `initForm()` submit handlers (in `main.js`) to
your real endpoint, and the payment buttons (`data-pay-item`,
`data-pay-generic`) to your provider's checkout, before removing the demo
labels (`.demo-flag` elements, owner banner, footer demo note).

## Images & video

No stock photography is bundled. Photo and video sections use generative
CSS/SVG placeholder panels labelled "placeholder" so nothing looks like a
broken image. Before launch:

1. Replace the hero visual, about visual, gallery items and before/after
   slider with real photography (recommended: WebP, responsive `srcset`,
   `loading="lazy"`).
2. Replace the video panel in `index.html` (`#videoPanel`) with a real
   embed (YouTube/Vimeo iframe or `<video>`), keeping `muted` autoplay off.

## Owner preview / sales flow

`owner-preview.html` is the dedicated conversion page (`/owner-preview`
route) linked from the discreet banner at the top of the homepage and from
the footer. It lists what's already built, what the garage needs to supply,
and optional add-ons, with an activation call-to-action. It does not show
pricing — add it manually if you want to quote a figure.

## Deployment

Any static host works (Netlify, Vercel static, Cloudflare Pages, S3 +
CloudFront, or a plain Apache/Nginx folder). Steps:

1. Personalise `config.js` per the checklist above.
2. Replace placeholder images/video.
3. Point the domain at the host and update `seo.canonicalUrl`.
4. Set `demoMode: false` and connect forms/payments.
5. Remove the owner banner (`.owner-banner` in `index.html`) and
   `owner-preview.html` once the sale has converted, if desired.

## Accessibility & performance notes

- Semantic landmarks (`header`, `nav`, `section`, `footer`), labelled form
  fields, visible focus states (`:focus-visible`), and
  `prefers-reduced-motion` support are built in.
- Icons are inline SVG (no icon font) sized in `em` units.
- No external JS dependencies; only one Google Fonts stylesheet request.
- Colour palette meets WCAG AA contrast for body text on both graphite and
  paper backgrounds.
