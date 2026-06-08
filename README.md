# Kit Autónomo España

A digital toolkit that helps Spanish freelancers (*autónomos*) keep their books
and know exactly what to pay each quarter — **Modelo 303 (IVA)** and **Modelo 130
(IRPF)** calculated automatically.

This repository is a self-contained product venture: the goal is to earn enough
to cover the cost of the AI agent that builds it. See `CLAUDE.md` for the full
charter.

## Contents
| Path | What it is |
|---|---|
| `product/Kit-Autonomo-Espana.xlsx` | The product — a 6-tab Excel/Sheets toolkit |
| `product/Guia-Autonomo-Espana.pdf` | Companion guide (Spanish) |
| `product/build_kit.py` | Regenerates the spreadsheet |
| `product/build_guide.py` | Regenerates the guide |
| `product/verify_logic.py` | Verifies the tax math (run after edits) |
| `marketing/listing.md` | Sales-page copy + pricing |
| `marketing/launch-plan.md` | How to distribute and sell it |

## Build
```bash
pip install openpyxl reportlab
python3 product/build_kit.py
python3 product/build_guide.py
python3 product/verify_logic.py   # -> "OK — ... verified"
```

## Disclaimer
The spreadsheet and guide are organizational tools for informational purposes and
are **not tax, accounting, or legal advice**. Spanish tax rules and rates change
and have many special cases. Always verify your situation with a qualified adviser
or the Agencia Tributaria before filing.
