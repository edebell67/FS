# Fun Cuts — current website + AI assistant approach package

**Status:** prepared for Ed's review. No external message has been sent.

## Commercial objective

Use the current-site-plus-assistant demonstration to open a **permission-based conversation**, not to force an immediate sale. The primary outcome of each first contact is a clear, replyable status:

```text
interested in activation / callback requested / not now / do-not-contact
```

A rejection is still a recorded outcome, but it is **not permission for continued marketing**. If someone asks to be left alone, record the suppression and do not contact them again about this offer. If they opt in to future updates, retain that explicit permission and the context of their response.

## Offer positioning

**Lead offer:** add a guided website assistant to the business's existing website experience.

**Do not lead with:** a website rebuild, generic “AI”, a claim of lost revenue, or a promise of live bookings/CRM/payment.

**What the demonstration proves:** visitors can find services, opening hours, contact routes, and explore simulated enquiry journeys without requiring a redesign first.

## Links

| Purpose | Link |
|---|---|
| Current Fun Cuts website style + assistant demonstration | https://edebell67.github.io/epics/funcuts/ |
| Structured reply hub | https://edebell67.github.io/epics/funcuts/reply.html |
| Direct reply address | mailto:edandhermes@gmail.com |

The reply hub offers three explicit email actions, all addressed to `edandhermes@gmail.com`:

1. **Discuss activation** — a conversation only; it does not activate anything.
2. **Request a callback** — asks the recipient for name, phone number, and best calling time.
3. **Not for us — close the preview** — records a do-not-contact instruction for this offer.

## First-contact email

**Subject options**

1. A short Fun Cuts website-assistant demonstration
2. An assistant layer for the site you already have
3. Fun Cuts website + assistant — private review link

**Body**

> Hello Fun Cuts team,
>
> I have put together a short private demonstration using the current Fun Cuts website style with an assistant added:
> https://edebell67.github.io/epics/funcuts/
>
> The idea is not a website rebuild. It is an assistant layer that could help visitors find services, opening hours and contact options, and guide an enquiry before someone has to call.
>
> The page is an independent demonstration, not your official website. Any booking, payment, email or CRM journey shown is simulated only — nothing is booked, charged, emailed or connected without your approval.
>
> If you have a minute to look at it, choose the response that fits best here:
> https://edebell67.github.io/epics/funcuts/reply.html
>
> You can choose to discuss activation, ask for a callback, or say it is not for you. Each option opens an email reply directly to me.
>
> Best,
> Ed
> edandhermes@gmail.com

## WhatsApp / SMS version

> Hello Fun Cuts team — I made a short independent demonstration using the current Fun Cuts website style with an assistant added: https://edebell67.github.io/epics/funcuts/
>
> It is not a rebuild or your official site, and all booking/payment/email examples are simulations only. If you look at it, you can choose discuss / callback / not for us here: https://edebell67.github.io/epics/funcuts/reply.html — each option replies directly to Ed at edandhermes@gmail.com.

## Telephone delivery-channel script

Use a phone call only to find the correct owner/manager email or mobile. Do not pitch at length.

> Hello. Could you tell me the best email address or mobile number to send a short private website-assistant demonstration to the owner or manager? It is simply a review link they can look at in their own time. It also gives them a one-click choice to discuss it, request a callback, or decline.

## Response handling: preserve context without ignoring preferences

| Inbound response | Lead status | Action | Future contact rule |
|---|---|---|---|
| Discuss activation | `interested_discussion` | Reply personally within one business day; clarify their approved questions, services, and desired hand-off. | Continue only in the active discussion. |
| Callback requested | `callback_requested` | Confirm agreed call time by email first. | Contact only for the requested callback / follow-up. |
| Not now, but no opt-out | `not_now` | Thank them; ask **once** whether they would like an occasional, relevant product update. | No further outreach unless they explicitly opt in. |
| Not for us / close preview | `rejected_do_not_contact` | Confirm the preview will be closed; suppress that route/business from this offer. | No further marketing contact. |
| No reply | `sent_no_response` | One brief check-in after 5–7 business days, then stop. | Do not keep chasing. |
| Wrong person | `wrong_contact` | Ask once for the appropriate owner/manager route. | Use only an official business route supplied or publicly listed. |

## Minimal lead record

Maintain one record per business, under EP034 operations, with:

```text
business_name
public_contact_route
contacted_at
message_version
current_demo_url
response_status
last_inbound_or_outbound_at
permission_for_future_updates (yes / no / unknown)
do_not_contact (yes / no)
next_permitted_action
notes
```

This is the continuity mechanism: keep the conversation history and outcome, not an excuse to message someone after they have declined.

## Pre-send control

Before any real send:

- [ ] Verify the recipient is a current Fun Cuts business route or authorised decision-maker.
- [ ] Re-open both public links on mobile and desktop.
- [ ] Confirm the reply hub opens `mailto:edandhermes@gmail.com` for all three actions.
- [ ] Record the exact recipient and send time in the lead record.
- [ ] Obtain Ed's approval for the exact recipient and final copy.
