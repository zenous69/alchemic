# Action plan — for the owner

Everything buildable is built. This plan is **only the things that need you**
(accounts, publishing, posting — my boundaries stop at outward-facing actions).
It's ordered so that the highest-leverage, traffic-generating steps come first,
because **traffic is the whole game** — the products are ready and waiting.

Time to first listing: ~1 hour. Each step says exactly which file to use.

## ✅ Already done (by Claude)
- Full product: `product/Kit-Autonomo-Espana.xlsx` + `Guia-Autonomo-Espana.pdf`
- Free lite version: `product/Kit-Autonomo-Espana-GRATIS.xlsx`
- Free web calculator + landing page: `web/index.html`
- Sales copy: `marketing/listing.md`
- Ready-to-post marketing content: `marketing/content-kit.md`
- SEO article to publish: `marketing/articles/modelo-303-y-130-explicados.md`
- Strategy + fallbacks (Plans A–D): `marketing/strategy.md`

## STEP 1 — Stand up the storefront (~45 min)
- [ ] Create a **Payhip or Lemon Squeezy** account (they handle EU VAT as merchant
      of record — less hassle than Gumroad for EU sales). Connect **Stripe**.
- [ ] Upload the **paid** kit (`Kit-Autonomo-Espana.xlsx` + the PDF guide) as one
      product. Price: **12 € launch / 19 € normal** (copy in `listing.md`).
- [ ] Upload the **free** version (`...-GRATIS.xlsx`) as a separate 0 € / email-gated
      product → this is your lead magnet.
- [ ] Open `Kit-Autonomo-Espana.xlsx` and take the 4 screenshots listed at the
      bottom of `listing.md`.

## STEP 2 — Publish the free calculator (~20 min) ← biggest traffic lever
- [ ] Put `web/index.html` online for free: **GitHub Pages** (Settings → Pages →
      deploy from branch) or drag-and-drop to **Netlify Drop** / **Cloudflare Pages**.
- [ ] In `index.html`, replace the 3 placeholder links (`TU-ENLACE-DE-VENTA`,
      `TU-ENLACE-GRATIS`) with your real Payhip URLs. Tell me and I can do this.
- [ ] In `build_lite.py` and the article, replace the same placeholders and
      regenerate (`python3 product/build_lite.py`) — or just tell me the URLs and
      I'll wire them everywhere.

## STEP 3 — Drive traffic (this is the real work — but it's pre-written)
Open `marketing/content-kit.md`. It's all copy-paste. Follow the 1-week cadence:
- [ ] Day 1: Post the **calculator** (free) in **r/Autonomos** + the lite version.
- [ ] Day 2: Publish the **SEO article** on Medium/LinkedIn + value replies on Rankia.
- [ ] Day 3: Facebook autónomo groups + an X thread.
- [ ] Day 4: Email **10–15 gestorías** (Plan C template in the content kit) — one
      yes can cover the month by itself.
- [ ] Day 5: Launch the calculator on Product Hunt / Indie Hackers.
- [ ] Day 6–7: Reply to every comment; ask each buyer for a review.
- [ ] Also list the paid kit on **Etsy / Creative Market** (their own buyer traffic).

## STEP 4 — Report back to me with numbers
After ~7 days tell me: visits to the calculator, sales, and where traffic came
from. That triggers the decision gate:
- **Visits ≈ 0** → distribution problem → I produce more channel content + we push
  the English/EU edition (10× the market) and marketplaces.
- **Visits OK but no sales** → trust/price problem → I adjust copy, add proof,
  tune the lead magnet.

## What I'm doing meanwhile (no input needed from you)
I keep building within my boundaries. Queued next, in priority order:
1. **English / EU-generic edition** of the kit — multiplies the addressable market.
2. **More SEO articles** ("gastos deducibles del autónomo", "alta de autónomo")
   to widen organic reach.
3. **Google Sheets version** for lower-friction buyers.
4. Tighten the landing page / add the screenshots gallery once you send URLs.

I won't wait on you to keep producing. You publish and collect; I build and market.
