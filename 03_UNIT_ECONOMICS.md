# Unit Economics & Profitability Gate

## Current Etsy fees (researched 2026-08-20, USA seller, Etsy Payments)

- Listing fee: **$0.20** per item, active 4 months or until sold (re-listing on sale is automatic and re-charges $0.20)
- Transaction fee: **6.5%** of (item price + shipping charged to buyer)
- Payment processing: **3% + $0.25** per transaction (Etsy Payments, US)
- Offsite Ads fee: **12–15%** of order value, **mandatory once a shop crosses $10,000 in trailing-12-month sales** (optional/opt-out below that threshold, but any order that came from an Offsite Ad click during the trial window is charged regardless)
- Etsy Plus (optional): $10/mo — listing credits + customizations, does not reduce transaction fees. **Not subscribing at launch** — no evidence it pays back before we have sales data.
- Etsy Ads (on-site PPC, seller-controlled budget): separate from Offsite Ads, CPC-based, budget we set directly — this is our primary paid channel, see `08_MARKETING_PLAN.md`.

Combined baseline take rate on a digital sale with no ads: **≈9.7% + $0.45** (6.5% + 3% + $0.20 + $0.25 as fixed).

## Digital product model (chosen — no physical shipping, no COGS)

Inputs held constant: no production cost, no shipping, no packaging, no
per-unit AI tool cost (design tools are a fixed monthly cost amortized below,
not per-unit).

| Price | Etsy fees (9.7% + $0.45) | Refund/replacement reserve (3%) | Contribution profit | Contribution margin |
|---|---|---|---|---|
| $9 (single template, entry) | $1.32 | $0.27 | **$7.41** | 82% |
| $18 (planner bundle) | $2.20 | $0.54 | **$15.26** | 85% |
| $35 (Life OS system, hero) | $3.85 | $1.05 | **$30.10** | 86% |
| $65 (premium full-system bundle) | $6.76 | $1.95 | **$56.29** | 87% |

Refund reserve is conservative — digital goods on Etsy see materially lower
refund rates than physical, but we hold 3% until we have our own data.

**Contribution margin floor for this category: set at 75%.** Everything above
clears it with room to spare even before touching ad spend, which is the
correct order of operations — fix the floor before layering paid acquisition
on top.

## Break-even CAC / ROAS (once we run Etsy Ads)

Using the $35 hero-bundle contribution profit of $30.10:
- **Break-even CAC = $30.10** (spend up to this per paid order and still clear zero on that unit)
- **Break-even ROAS = $35 / CAC.** At a disciplined target CAC of **$12** (40% of ceiling, leaves real profit), target ROAS is **≈2.9x**; at $8 CAC, ROAS ≈4.4x.
- **Target operating CAC ceiling for launch: $15** (well under the $30 break-even, protects margin while we're still learning what converts) — hard stop-loss if 14-day trailing CAC exceeds $20 on any campaign.

## $250 launch budget allocation

| Line item | Amount | Rationale |
|---|---|---|
| Etsy shop setup (one-time $15 fee waived in most current promos; verify at signup) | $0–15 | Etsy periodically waives this for new shops — check at signup, don't assume |
| Listing fees, 20 initial SKUs incl. variants | ~$10 | $0.20 × ~50 listing-slots (variants each cost a slot) |
| Design/production tooling (Canva Pro or Notion, 1 month) | $13 | Needed to build the templates themselves |
| Etsy Ads test budget (held in reserve, not spent day 1) | $150 | Deployed only after ≥2 weeks of organic data per `08_MARKETING_PLAN.md` |
| Pinterest/content production tooling buffer | $0 | Use free tools first (Canva free tier scheduling, native Pinterest) |
| Contingency | ~$60 | Held back — do not spend without a documented reason in the ledger |

No line item here requires banking/payment credentials to *plan* — but every
one of them requires an actual funded Etsy account to *execute*. See
`HUMAN_ACTION_REQUIRED.md`.

## Kill criteria (pre-committed, not decided after the fact)

- Any SKU with <2% conversion (views→sales) after 200 views and a completed SEO
  pass gets rewritten once; if still <2% after another 150 views, **kill**.
- Any ad campaign with trailing-14-day CAC > $20 gets paused immediately, not
  "optimized while it burns."
- If the shop as a whole hasn't reached break-even on cumulative ad spend by
  the time the $150 ad reserve is exhausted, **stop all paid spend** and
  operate organic-only until profitability is demonstrated, then reassess.
