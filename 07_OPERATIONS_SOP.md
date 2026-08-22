# Operations Manual & Compliance

Written so another operator (human or agent) could run the shop from this
file alone tomorrow.

## Etsy policy findings (researched 2026-08-20 — verify against Etsy's live
Seller Handbook/Creativity Standards pages at execution time, since
enforcement details shift)

- **Creativity Standards / originality:** listings must be based on the
  seller's original design; Etsy's 2026 language change removed prior
  allowance for "templated design or pattern" for POD items — reinforces our
  choice to build fully original Canva/Notion source files rather than
  reskin a purchased template pack.
- **AI disclosure:** any listing where AI materially contributed to the
  content (imagery, description copy, mockups beyond simple background
  removal) must be disclosed per Etsy's AI-content disclosure requirement.
  **Our production plan avoids AI-generated imagery entirely** (original
  Canva design work) specifically to stay clear of the current enforcement
  sweep described in research; if AI-assisted copywriting is used for
  description drafts, disclose per Etsy's current toggle/field for this at
  listing time.
- **Fees:** see `03_UNIT_ECONOMICS.md` for current schedule.
- **IP screen (mandatory before any listing goes live):** no fan art, no
  licensed characters, no sports/brand logos, no celebrity likeness, no
  copied phrases from trademarked slogans. Shop name run through a basic
  USPTO TESS + Etsy shop-name search before registration (owner should
  re-verify at signup since names get taken).

## Shop configuration checklist (for the human executing signup)

1. Create seller account, select shop name (see `04_BRAND.md` candidates), set
   shop language/currency/location.
2. Set up Etsy Payments (requires bank account + identity verification — see
   `HUMAN_ACTION_REQUIRED.md`).
3. Set shop policies: processing time (digital = instant/automatic delivery,
   state "delivered automatically upon payment"), refund policy per
   `09_CUSTOMER_RESPONSE_LIBRARY.md`, FAQ section pre-filled from that file.
4. Upload banner, icon, About story per `04_BRAND.md`.
5. Create listings using `05_PRODUCT_PORTFOLIO.md` + `06_SEO_LISTING_PLANS.md`
   as the copy/keyword source — do not free-write listing copy at upload time.
6. Enable digital-file auto-delivery for every SKU (Etsy handles this
   natively for digital listings — confirm each listing type is set to
   "Digital" not "Physical" before publishing).
7. Turn ON Etsy's AI-disclosure toggle for any listing it applies to per the
   policy note above.

## Fulfillment SOP (digital-only at launch — no physical inventory, no supplier/POD partner needed for the initial 20 SKUs)

- Delivery is automatic via Etsy's digital-download system — no manual
  fulfillment step for standard SKUs.
- Personalized SKUs (#16-17 in portfolio): buyer submits personalization
  details at checkout → committed turnaround is **48 hours** → deliver via
  Etsy's "send file"/message attachment for the finished custom file →
  mark order complete.
- QC checklist (per `05_PRODUCT_PORTFOLIO.md`) run before *every* new listing
  goes live, not just at launch.

## Refund/replacement workflow

Digital goods: no refund once downloaded, **except** — file won't open/is
corrupted (replace immediately, no argument), buyer ordered wrong
format/variant by listing ambiguity we caused (fix free), buyer is unhappy
with the design itself post-purchase (offer a different format/edition swap
first, refund only if that doesn't resolve it and it's within 24 hours of
purchase with no download registered). Never argue with a buyer in public
listing Q&A — move to private messages immediately.

## Escalation triggers (routine handling stops, human/CEO review starts)

- Any request implying legal threat, chargeback, or IP claim against us
- Any refund request over $50 cumulative for one buyer
- Any pattern of 3+ similar complaints about the same SKU (→ triggers Product
  review of that listing, logged in `00_EXECUTION_LEDGER.md`)
- Anything touching account security, suspension notices, or payment holds
