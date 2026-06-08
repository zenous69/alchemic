# Strategy & contingency plan

The goal is fragile if it rests on one product + cold-start distribution. This
file is the portfolio of bets, the failure triggers, and the fallbacks. It is
also Claude's memory of the strategy across sessions.

## The one structural constraint
Claude cannot transact, publish, or contact anyone. **The owner is the only
real-world hook.** Therefore every plan is designed to (a) minimize owner effort
per euro earned, and (b) front-load everything Claude can build alone, so the
owner's job is a few high-leverage actions, not daily grind.

## Risk register — why Plan A might fail
| # | Risk | Likelihood | Why it kills us |
|---|------|-----------|-----------------|
| R1 | **No distribution** — cold launch, no audience, communities reject self-promo | High | The default outcome of any indie launch: zero traffic = zero sales |
| R2 | **No conversion / low trust** — "it's just a spreadsheet", unknown seller, tax accuracy fear | Med-High | Money-adjacent products have a high trust bar |
| R3 | **Competition** — free templates + established SaaS (Quipu, Declarando, Holded, Infoautónomos) with free tiers | Med | Hard to be seen next to funded incumbents |
| R4 | **Owner bandwidth** — setup/posting never happens | Med | Plan A never even launches |
| R5 | **Single-shot timing** — one niche, one month, no recovery room | Med | A miss = no time to retry from scratch |

The dominant risk is **R1 (distribution)**. Most mitigations below attack it.

---

## PLAN A — primary (built, ready to list)
Kit Autónomo España on Gumroad/Payhip + value-first seeding in Spanish freelancer
communities. ~7 sales/mo @ 15 € covers the cost.

**Kill-criteria:** if ~10 days after going live there are **< ~50 visits or 0
sales**, R1/R2 have triggered → escalate to B, then C/D.

---

## PLAN B — same engine, wider funnel (Claude builds in parallel, now)
Don't change the bet; remove its single points of failure. All reuse the
openpyxl build engine, so each new SKU is cheap to produce.

- **Free "lite" lead magnet** (Facturas + Gastos + IVA total only; no Modelo 130,
  no guide). A *free* asset that communities accept and that warms buyers →
  upsell to the full kit. Attacks R2 + R4.
- **English / EU-generic edition** ("Freelancer Finance & Tax Tracker",
  configurable tax rates). Same engine, **10–50× the addressable market**. The
  single biggest lever on R1 — removes the Spain-only ceiling. Sells on the same
  listing with no extra owner setup.
- **Marketplaces with native buyer traffic:** Etsy digital downloads, Creative
  Market, Notion/Sheets template galleries. Distribution is *provided* by the
  platform → directly attacks R1.
- **Google Sheets version** — lower friction; many autónomos prefer it. Attacks R2.
- **Free web calculator + landing page + SEO articles** ("calculadora IVA/IRPF",
  "Modelo 303 explicado"). Evergreen organic traffic. Compounds *beyond* month 1
  — this is the sustainability play, not the month-1 rescue.

## PLAN C — change the model (if B2C templates don't convert)
Fewer customers, higher ticket, distribution via the owner's network instead of
cold strangers. One deal can cover the month.

- **Productized service:** Claude produces the deliverables, owner sells them —
  custom financial models/dashboards, data analysis, automation scripts, report
  generation. 1–2 clients @ 50–150 € covers the month. Distribution = owner's
  existing contacts, not cold traffic.
- **B2B license to a gestoría/asesoría:** white-label the kit engine to one
  accountancy that serves many autónomos. One warm outreach by the owner; one
  deal > dozens of B2C sales. Sidesteps R1 entirely.

## PLAN D — different value prop (backstop; most reliably covers ~100 €)
Pull-based income, where the customer already wants to pay.

- **One small freelance gig.** Owner takes a ~100–200 € gig (Upwork/Fiverr/Malt/
  local) in a category Claude executes end-to-end: landing pages, spreadsheets/
  automation, content, data cleaning, translation, small scripts. Claude does the
  work; owner is the front and collects. **A single gig closes the goal
  regardless of product-market fit.** This is the safety net under everything.
- **OSS popularity → consulting funnel** — slower; a sustainability option, not a
  month-1 lever.

---

## Timeline & decision gates (the glue)
- **Days 1–3:** Owner lists Plan A. Claude builds Plan B assets in parallel
  (lite lead magnet, then English edition).
- **Day ~7 — gate 1:** Read the metrics. Traffic is the gap → push English
  edition + marketplaces (B). Conversion is the gap → lead magnet, price, proof,
  reviews (B).
- **Day ~14 — gate 2:** If B2C is still ~0 → activate Plan C (service / B2B) and
  **queue a Plan D gig** as guaranteed cover.
- **Days 14–30:** Double down on whatever shows signal. Plan D gig as the
  backstop that ensures the month is covered even if every product bet misses.

## Metrics to watch
Visits, visit→sale conversion (1–3% = normal cold), refund rate (<5%), reviews
(first 5 matter most). If visits are fine but sales are 0 → it's R2 (fix trust/
price/proof). If visits are ~0 → it's R1 (fix channel: English edition,
marketplaces, gig).
