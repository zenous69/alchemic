# CLAUDE.md

Guidance for Claude (and other AI agents) working in this repository.

## What this repo is
A small **digital-product venture** with one objective: earn enough to cover the
monthly cost of running this agent (~100 €/month) within ~1 month, legally.

The repo previously held an unused WordPress site; that was wiped (owner's call)
and replaced with the product below.

## The product: "Kit Autónomo España"
A digital toolkit for **Spanish freelancers (autónomos)** that auto-calculates
their quarterly taxes.

```
product/
  build_kit.py                  # generates the Excel toolkit (openpyxl)
  build_guide.py                # generates the companion PDF guide (reportlab)
  verify_logic.py               # asserts the IVA/IRPF/303/130 math is correct
  Kit-Autonomo-Espana.xlsx      # THE PRODUCT (generated)
  Guia-Autonomo-Espana.pdf      # THE GUIDE (generated)
marketing/
  listing.md                    # sales-page copy (Spanish) + pricing
  launch-plan.md                # distribution plan, ordered by payoff
```

### Regenerate the artifacts
```bash
pip install openpyxl reportlab
python3 product/build_kit.py      # -> product/Kit-Autonomo-Espana.xlsx
python3 product/build_guide.py    # -> product/Guia-Autonomo-Espana.pdf
python3 product/verify_logic.py   # must print "OK — ... verified"
```
Always run `verify_logic.py` after touching `build_kit.py`: it re-checks the
Modelo 303 and Modelo 130 results against hand-computed expected values.

## Domain notes (Spanish autónomo taxes — keep these correct)
- **IVA:** 21% general / 10% reducido / 4% superreducido. Modelo 303 quarterly =
  IVA repercutido − IVA soportado deducible.
- **IRPF retención** on B2B invoices: 15% general, **7%** for new autónomos (year
  of alta + 2 following years).
- **Modelo 130** (pago fraccionado): 20% of cumulative net profit − retentions −
  prior payments; never negative. **Exempt** if ≥70% of income carries retención.
- Everything is **informational, not tax advice** — the disclaimer must stay in
  both the spreadsheet and the guide.

## Operating charter (standing mandate from the owner)
1. **Obey the law and platform terms.** No spam, no deception, no scraping.
2. **Earn through legitimate value**, not gimmicks.
3. **The owner is the real-world hook:** Claude builds (code, docs, products);
   the owner holds the Stripe/autónomo account, lists products, and posts in
   communities. I produce; the owner lists and collects.
4. **Outward-facing or irreversible actions need explicit owner approval** —
   sending email, publishing, transacting, contacting customers.
5. **The Gmail and file-storage MCP tools are OFF LIMITS** (owner's instruction).
6. **Report every action** to the owner in plain language.

## Working conventions
- Python is the build tooling; keep scripts self-contained and runnable with just
  `openpyxl` + `reportlab`.
- Generated artifacts (`.xlsx`, `.pdf`) are committed so the owner can grab them
  without running anything.
