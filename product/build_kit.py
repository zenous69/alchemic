#!/usr/bin/env python3
"""
Build "Kit Autónomo España" — an Excel toolkit for Spanish freelancers.

Generates product/Kit-Autonomo-Espana.xlsx with working formulas for:
  - Facturas emitidas (IVA repercutido + retención IRPF)
  - Gastos deducibles (IVA soportado + gasto deducible IRPF)
  - Resumen trimestral: Modelo 303 (IVA) y Modelo 130 (IRPF) auto-calculados
  - Resumen anual (Modelo 390 / Renta informativo)
  - Plantilla de factura
The numbers update automatically as you fill in invoices and expenses.

Tax logic targets the common case for an autónomo en estimación directa.
It is a tool, not tax advice — see the disclaimer tab.
"""

from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

DATEFMT = "DD/MM/YYYY"

# ----- styling helpers -------------------------------------------------------
NAVY = "1F3A5F"
BLUE = "2E5C8A"
LIGHT = "DCE6F1"
ACCENT = "F2C200"
GREY = "F2F2F2"
WHITE = "FFFFFF"

EUR = '#,##0.00 "€"'
PCT = '0"%"'

H1 = Font(name="Calibri", size=18, bold=True, color=WHITE)
H2 = Font(name="Calibri", size=12, bold=True, color=WHITE)
BOLD = Font(name="Calibri", size=11, bold=True, color=NAVY)
BODY = Font(name="Calibri", size=11)
SMALL = Font(name="Calibri", size=9, italic=True, color="666666")

fill_navy = PatternFill("solid", fgColor=NAVY)
fill_blue = PatternFill("solid", fgColor=BLUE)
fill_light = PatternFill("solid", fgColor=LIGHT)
fill_grey = PatternFill("solid", fgColor=GREY)
fill_accent = PatternFill("solid", fgColor=ACCENT)

thin = Side(style="thin", color="BBBBBB")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
LASTROW = 1000  # data entry range


def header_row(ws, row, headers, start_col=1, fill=fill_blue, font=H2):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.fill = fill
        c.font = font
        c.alignment = center
        c.border = border


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


# =============================================================================
wb = Workbook()

# ---------- 1. INICIO --------------------------------------------------------
ws = wb.active
ws.title = "Inicio"
ws.sheet_view.showGridLines = False
widths(ws, {"A": 3, "B": 34, "C": 34, "D": 30, "E": 20})

ws.merge_cells("B2:E2")
ws["B2"] = "KIT AUTÓNOMO ESPAÑA"
ws["B2"].font = H1
ws["B2"].fill = fill_navy
ws["B2"].alignment = Alignment(horizontal="center", vertical="center")
ws.row_dimensions[2].height = 34
for col in "CDE":
    ws[f"{col}2"].fill = fill_navy

ws.merge_cells("B3:E3")
ws["B3"] = "Control de facturas, gastos e impuestos (IVA · IRPF · Modelo 303 · Modelo 130)"
ws["B3"].font = Font(size=11, italic=True, color=WHITE)
ws["B3"].fill = fill_blue
ws["B3"].alignment = center
for col in "CDE":
    ws[f"{col}3"].fill = fill_blue

ws["B5"] = "1 · TUS DATOS (se usan en la plantilla de factura)"
ws["B5"].font = BOLD
config = [
    ("Nombre y apellidos / Razón social", "Tu Nombre Apellidos"),
    ("NIF / DNI", "00000000X"),
    ("Dirección fiscal", "Calle Ejemplo 1, 28001 Madrid"),
    ("Email / Teléfono", "tucorreo@email.com · 600 000 000"),
    ("Ejercicio (año)", 2026),
]
r = 6
for label, val in config:
    ws.cell(row=r, column=2, value=label).font = BODY
    c = ws.cell(row=r, column=3, value=val)
    c.fill = fill_light
    c.border = border
    c.font = BODY
    r += 1

ws.cell(row=r + 1, column=2, value="2 · PREFERENCIAS FISCALES").font = BOLD
prefs = [
    ("Tipo de IVA habitual (%)", 21, "21 general · 10 reducido · 4 superreducido · 0 exento"),
    ("Tipo de retención IRPF en factura (%)", 15, "15 general · 7 nuevos autónomos (año alta + 2 siguientes)"),
    ("% de tu facturación con retención", 100, "Si ≥ 70% lleva retención, estás EXENTO de Modelo 130"),
]
r += 2
for label, val, note in prefs:
    ws.cell(row=r, column=2, value=label).font = BODY
    c = ws.cell(row=r, column=3, value=val)
    c.fill = fill_light
    c.border = border
    c.font = BODY
    c.number_format = PCT
    ws.cell(row=r, column=4, value=note).font = SMALL
    r += 1

# named cells used elsewhere
IVA_DEF = "Inicio!$C$11"   # tipo IVA habitual
IRPF_DEF = "Inicio!$C$12"  # tipo IRPF habitual

guide_rows = [
    "3 · CÓMO USAR EL KIT",
    "①  Rellena tus datos y preferencias arriba.",
    "②  Apunta cada factura emitida en la pestaña «Facturas».",
    "③  Apunta cada gasto deducible en la pestaña «Gastos».",
    "④  Mira «Resumen trimestral»: te dice qué pagar en el Modelo 303 (IVA) y 130 (IRPF).",
    "⑤  Usa «Plantilla factura» para emitir facturas con tus datos ya cargados.",
    "",
    "Las columnas en gris se calculan solas. No las toques: escribe solo en las blancas.",
]
r += 2
for i, t in enumerate(guide_rows):
    c = ws.cell(row=r, column=2, value=t)
    c.font = BOLD if i == 0 else BODY
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    c.alignment = left
    r += 1

r += 1
disc = ("AVISO: Esta hoja es una herramienta de organización, NO asesoramiento fiscal. "
        "Los tipos y reglas pueden cambiar y existen casos particulares (recargo de equivalencia, "
        "operaciones intracomunitarias, módulos, etc.). Verifica siempre con tu asesor o con la "
        "Agencia Tributaria antes de presentar cualquier modelo.")
ws.merge_cells(start_row=r, start_column=2, end_row=r + 2, end_column=5)
c = ws.cell(row=r, column=2, value=disc)
c.font = Font(size=9, italic=True, color="A00000")
c.alignment = left
c.fill = fill_grey

# ---------- LISTAS (validation source) --------------------------------------
wl = wb.create_sheet("Listas")
wl.sheet_state = "hidden"
cats = ["Suministros (luz/agua/internet)", "Material y software", "Cuota autónomos (RETA)",
        "Asesoría / gestoría", "Marketing y publicidad", "Desplazamientos", "Formación",
        "Alquiler oficina/coworking", "Telefonía", "Comisiones bancarias", "Otros"]
wl["A1"] = "IVA"
for i, v in enumerate([21, 10, 4, 0]):
    wl.cell(row=2 + i, column=1, value=v)
wl["B1"] = "IRPF"
for i, v in enumerate([15, 7, 1, 0]):
    wl.cell(row=2 + i, column=2, value=v)
wl["C1"] = "SiNo"
for i, v in enumerate(["Sí", "No"]):
    wl.cell(row=2 + i, column=3, value=v)
wl["D1"] = "Categorias"
for i, v in enumerate(cats):
    wl.cell(row=2 + i, column=4, value=v)

dv_iva = DataValidation(type="list", formula1='"21,10,4,0"', allow_blank=True)
dv_irpf = DataValidation(type="list", formula1='"15,7,1,0"', allow_blank=True)
dv_sino = DataValidation(type="list", formula1='"Sí,No"', allow_blank=True)
dv_cat = DataValidation(type="list", formula1=f"=Listas!$D$2:$D${1 + len(cats)}", allow_blank=True)


# ---------- 2. FACTURAS ------------------------------------------------------
wf = wb.create_sheet("Facturas")
wf.sheet_view.showGridLines = False
fheaders = ["Fecha", "Nº Factura", "Cliente", "NIF cliente", "Base imponible",
            "IVA %", "Cuota IVA", "IRPF %", "Retención IRPF", "Total factura",
            "¿Cobrada?", "Trim."]
ws_title = wf
wf.merge_cells("A1:L1")
wf["A1"] = "FACTURAS EMITIDAS  ·  ingresos"
wf["A1"].font = H1
wf["A1"].fill = fill_navy
wf["A1"].alignment = Alignment(horizontal="left", vertical="center")
wf.row_dimensions[1].height = 28
for col in "BCDEFGHIJKL":
    wf[f"{col}1"].fill = fill_navy
header_row(wf, 2, fheaders)
widths(wf, {"A": 12, "B": 12, "C": 24, "D": 13, "E": 14, "F": 7, "G": 12,
            "H": 7, "I": 13, "J": 13, "K": 11, "L": 7})
wf.freeze_panes = "A3"

# example rows
examples = [
    (date(2026, 1, 15), "2026-001", "Cliente Ejemplo S.L.", "B12345678", 1000, 21, 15, "Sí"),
    (date(2026, 2, 3), "2026-002", "Autónomo Pérez", "12345678Z", 450, 21, 15, "No"),
]
for k, (fecha, num, cli, nif, base, iva, irpf, cob) in enumerate(examples):
    row = 3 + k
    fc = wf.cell(row=row, column=1, value=fecha)
    fc.number_format = DATEFMT
    wf.cell(row=row, column=2, value=num)
    wf.cell(row=row, column=3, value=cli)
    wf.cell(row=row, column=4, value=nif)
    wf.cell(row=row, column=5, value=base)
    wf.cell(row=row, column=6, value=iva)
    wf.cell(row=row, column=8, value=irpf)
    wf.cell(row=row, column=11, value=cob)

for row in range(3, LASTROW + 1):
    wf.cell(row=row, column=7, value=(  # Cuota IVA
        f'=IF($E{row}="","",$E{row}*$F{row}/100)'))
    wf.cell(row=row, column=9, value=(  # Retención IRPF
        f'=IF($E{row}="","",$E{row}*$H{row}/100)'))
    wf.cell(row=row, column=10, value=(  # Total
        f'=IF($E{row}="","",$E{row}+$G{row}-$I{row})'))
    wf.cell(row=row, column=12, value=(  # Trimestre
        f'=IF($A{row}="","",ROUNDUP(MONTH($A{row})/3,0))'))
    wf.cell(row=row, column=1).number_format = DATEFMT
    for col, fmt in ((5, EUR), (6, PCT), (7, EUR), (8, PCT), (9, EUR), (10, EUR)):
        wf.cell(row=row, column=col).number_format = fmt
    for col in range(1, 13):
        cell = wf.cell(row=row, column=col)
        cell.font = BODY
        cell.border = border
        if col in (7, 9, 10, 12):
            cell.fill = fill_grey
wf.add_data_validation(dv_iva); dv_iva.add(f"F3:F{LASTROW}")
wf.add_data_validation(dv_irpf); dv_irpf.add(f"H3:H{LASTROW}")
wf.add_data_validation(dv_sino); dv_sino.add(f"K3:K{LASTROW}")


# ---------- 3. GASTOS --------------------------------------------------------
wg = wb.create_sheet("Gastos")
wg.sheet_view.showGridLines = False
gheaders = ["Fecha", "Proveedor", "NIF", "Concepto", "Categoría", "Base imponible",
            "IVA %", "Cuota IVA", "% deduc. IVA", "IVA deducible",
            "% deduc. IRPF", "Gasto deducible", "Trim."]
wg.merge_cells("A1:M1")
wg["A1"] = "GASTOS DEDUCIBLES"
wg["A1"].font = H1
wg["A1"].fill = fill_navy
wg["A1"].alignment = Alignment(horizontal="left", vertical="center")
wg.row_dimensions[1].height = 28
for col in "BCDEFGHIJKLM":
    wg[f"{col}1"].fill = fill_navy
header_row(wg, 2, gheaders)
widths(wg, {"A": 12, "B": 20, "C": 12, "D": 22, "E": 22, "F": 13, "G": 7,
            "H": 11, "I": 11, "J": 12, "K": 11, "L": 13, "M": 7})
wg.freeze_panes = "A3"

gex = [
    (date(2026, 1, 10), "Movistar", "A82018474", "Internet y móvil", cats[0], 50, 21, 100, 100),
    (date(2026, 1, 31), "Tesorería SS", "", "Cuota RETA", cats[2], 80, 0, 0, 100),
]
for k, (fecha, prov, nif, con, cat, base, iva, dv_iva_p, dv_irpf_p) in enumerate(gex):
    row = 3 + k
    gc = wg.cell(row=row, column=1, value=fecha)
    gc.number_format = DATEFMT
    wg.cell(row=row, column=2, value=prov)
    wg.cell(row=row, column=3, value=nif)
    wg.cell(row=row, column=4, value=con)
    wg.cell(row=row, column=5, value=cat)
    wg.cell(row=row, column=6, value=base)
    wg.cell(row=row, column=7, value=iva)
    wg.cell(row=row, column=9, value=dv_iva_p)
    wg.cell(row=row, column=11, value=dv_irpf_p)

for row in range(3, LASTROW + 1):
    wg.cell(row=row, column=8, value=f'=IF($F{row}="","",$F{row}*$G{row}/100)')      # cuota IVA
    wg.cell(row=row, column=10, value=f'=IF($F{row}="","",$H{row}*$I{row}/100)')     # IVA deducible
    wg.cell(row=row, column=12, value=f'=IF($F{row}="","",$F{row}*$K{row}/100)')     # gasto deducible IRPF
    wg.cell(row=row, column=13, value=f'=IF($A{row}="","",ROUNDUP(MONTH($A{row})/3,0))')
    wg.cell(row=row, column=1).number_format = DATEFMT
    for col, fmt in ((6, EUR), (7, PCT), (8, EUR), (9, PCT), (10, EUR), (11, PCT), (12, EUR)):
        wg.cell(row=row, column=col).number_format = fmt
    for col in range(1, 14):
        cell = wg.cell(row=row, column=col)
        cell.font = BODY
        cell.border = border
        if col in (8, 10, 12, 13):
            cell.fill = fill_grey
wg.add_data_validation(DataValidation(type="list", formula1='"21,10,4,0"', allow_blank=True))
_dv = wg.data_validations.dataValidation[0]; _dv.add(f"G3:G{LASTROW}")
wg.add_data_validation(dv_cat); dv_cat.add(f"E3:E{LASTROW}")


# ---------- 4. RESUMEN TRIMESTRAL -------------------------------------------
wr = wb.create_sheet("Resumen trimestral")
wr.sheet_view.showGridLines = False
wr.merge_cells("A1:M1")
wr["A1"] = "RESUMEN TRIMESTRAL  ·  Modelo 303 (IVA) y Modelo 130 (IRPF)"
wr["A1"].font = H1
wr["A1"].fill = fill_navy
wr["A1"].alignment = Alignment(horizontal="left", vertical="center")
wr.row_dimensions[1].height = 28
for col in "BCDEFGHIJKLM":
    wr[f"{col}1"].fill = fill_navy

rheaders = ["Trimestre", "IVA repercutido", "IVA soportado\ndeducible",
            "MODELO 303\n(a ingresar)", "Ingresos\n(base)", "Gastos\ndeducibles",
            "Rendimiento\nneto", "Rdto. neto\nacumulado", "20% s/\nacumulado",
            "Retenciones\nsoportadas", "Retenciones\nacumuladas",
            "Pagos 130\nanteriores", "MODELO 130\n(a ingresar)"]
header_row(wr, 2, rheaders)
widths(wr, {"A": 10, "B": 13, "C": 13, "D": 13, "E": 12, "F": 12, "G": 12,
            "H": 13, "I": 12, "J": 13, "K": 13, "L": 12, "M": 13})
wr.row_dimensions[2].height = 30

F_G, F_L = "Facturas!$G$3:$G$1000", "Facturas!$L$3:$L$1000"
F_E, F_I = "Facturas!$E$3:$E$1000", "Facturas!$I$3:$I$1000"
G_J, G_M = "Gastos!$J$3:$J$1000", "Gastos!$M$3:$M$1000"
G_L2 = "Gastos!$L$3:$L$1000"

for q in range(1, 5):
    row = 2 + q  # rows 3..6
    wr.cell(row=row, column=1, value=f"T{q}").font = BOLD
    wr.cell(row=row, column=2, value=f'=SUMIFS({F_G},{F_L},{q})')          # IVA repercutido
    wr.cell(row=row, column=3, value=f'=SUMIFS({G_J},{G_M},{q})')          # IVA soportado
    wr.cell(row=row, column=4, value=f'=B{row}-C{row}')                    # Modelo 303
    wr.cell(row=row, column=5, value=f'=SUMIFS({F_E},{F_L},{q})')          # ingresos base
    wr.cell(row=row, column=6, value=f'=SUMIFS({G_L2},{G_M},{q})')         # gastos deducibles
    wr.cell(row=row, column=7, value=f'=E{row}-F{row}')                    # rdto neto
    wr.cell(row=row, column=10, value=f'=SUMIFS({F_I},{F_L},{q})')         # retenciones
    if q == 1:
        wr.cell(row=row, column=8, value=f'=G{row}')                       # acumulado
        wr.cell(row=row, column=11, value=f'=J{row}')                      # retenc acum
        wr.cell(row=row, column=12, value=0)                               # pagos 130 ant
    else:
        wr.cell(row=row, column=8, value=f'=H{row-1}+G{row}')
        wr.cell(row=row, column=11, value=f'=K{row-1}+J{row}')
        wr.cell(row=row, column=12, value=f'=SUM($M$3:M{row-1})')
    wr.cell(row=row, column=9, value=f'=MAX(0,H{row}*0.2)')                # 20% acumulado
    wr.cell(row=row, column=13, value=f'=MAX(0,I{row}-K{row}-L{row})')     # Modelo 130
    for col in range(2, 14):
        cell = wr.cell(row=row, column=col)
        cell.number_format = EUR
        cell.font = BODY
        cell.border = border
        cell.fill = fill_grey
    wr.cell(row=row, column=4).fill = fill_accent
    wr.cell(row=row, column=4).font = BOLD
    wr.cell(row=row, column=13).fill = fill_accent
    wr.cell(row=row, column=13).font = BOLD

# total row
tr = 7
wr.cell(row=tr, column=1, value="AÑO").font = BOLD
for col in (2, 3, 4, 5, 6, 7, 10):
    L = get_column_letter(col)
    wr.cell(row=tr, column=col, value=f'=SUM({L}3:{L}6)')
wr.cell(row=tr, column=13, value="=SUM(M3:M6)")
for col in range(1, 14):
    cell = wr.cell(row=tr, column=col)
    cell.border = border
    cell.fill = fill_light
    cell.font = BOLD
    if col >= 2:
        cell.number_format = EUR

note_r = tr + 2
notes = [
    "MODELO 303 (IVA, trimestral): si el resultado es positivo, ingresas esa cantidad a Hacienda; si es negativo, queda a compensar/devolver.",
    "MODELO 130 (IRPF, pago fraccionado): 20% del rendimiento neto acumulado menos retenciones y pagos previos. Es acumulativo durante el año.",
    "EXENCIÓN del 130: si ≥70% de tus ingresos llevan retención (como suele pasar facturando a empresas), no presentas Modelo 130.",
    "Plazos: T1 abril · T2 julio · T3 octubre · T4 enero. Modelo 390 (resumen anual IVA) y Renta (Modelo 100) una vez al año.",
]
for i, n in enumerate(notes):
    wr.merge_cells(start_row=note_r + i, start_column=1, end_row=note_r + i, end_column=13)
    c = wr.cell(row=note_r + i, column=1, value="•  " + n)
    c.font = SMALL
    c.alignment = left


# ---------- 5. RESUMEN ANUAL -------------------------------------------------
wa = wb.create_sheet("Resumen anual")
wa.sheet_view.showGridLines = False
widths(wa, {"A": 3, "B": 40, "C": 18})
wa.merge_cells("B2:C2")
wa["B2"] = "RESUMEN ANUAL"
wa["B2"].font = H1
wa["B2"].fill = fill_navy
wa["B2"].alignment = Alignment(horizontal="center", vertical="center")
wa["C2"].fill = fill_navy
wa.row_dimensions[2].height = 30

rows = [
    ("INGRESOS Y GASTOS", None, True),
    ("Ingresos (base imponible)", "='Resumen trimestral'!E7", False),
    ("Gastos deducibles", "='Resumen trimestral'!F7", False),
    ("Rendimiento neto (beneficio)", "='Resumen trimestral'!G7", False),
    ("", None, None),
    ("IVA (Modelo 390 informativo)", None, True),
    ("IVA repercutido (cobrado)", "='Resumen trimestral'!B7", False),
    ("IVA soportado deducible", "='Resumen trimestral'!C7", False),
    ("Resultado IVA del año", "='Resumen trimestral'!D7", False),
    ("", None, None),
    ("IRPF", None, True),
    ("Retenciones soportadas en facturas", "='Resumen trimestral'!J7", False),
    ("Pagos fraccionados (Modelo 130)", "='Resumen trimestral'!M7", False),
    ("A cuenta de tu Renta (Modelo 100)", "='Resumen trimestral'!J7+'Resumen trimestral'!M7", False),
]
r = 4
for label, formula, is_head in rows:
    if label == "":
        r += 1
        continue
    bc = wa.cell(row=r, column=2, value=label)
    if is_head:
        bc.font = H2
        bc.fill = fill_blue
        wa.cell(row=r, column=3).fill = fill_blue
    else:
        bc.font = BODY
        cc = wa.cell(row=r, column=3, value=formula)
        cc.number_format = EUR
        cc.font = BOLD if "neto" in label or "Renta" in label else BODY
        cc.border = border
        cc.fill = fill_light if ("neto" in label or "Renta" in label) else fill_grey
    r += 1

wa.merge_cells(start_row=r + 1, start_column=2, end_row=r + 3, end_column=3)
c = wa.cell(row=r + 1, column=2,
            value="El 'rendimiento neto' es el beneficio que tributa en tu Declaración de la "
                  "Renta. Las retenciones y los pagos del Modelo 130 ya son adelantos de ese "
                  "IRPF: se restan de lo que sale a pagar en la Renta.")
c.font = SMALL
c.alignment = left


# ---------- 6. PLANTILLA FACTURA --------------------------------------------
wp = wb.create_sheet("Plantilla factura")
wp.sheet_view.showGridLines = False
widths(wp, {"A": 3, "B": 26, "C": 20, "D": 14, "E": 14, "F": 16})
wp.merge_cells("B2:C2")
wp["B2"] = "FACTURA"
wp["B2"].font = H1
wp["B2"].fill = fill_navy
wp["B2"].alignment = Alignment(horizontal="left", vertical="center")
wp["C2"].fill = fill_navy
wp.row_dimensions[2].height = 28

wp["E2"] = "Nº factura:"; wp["E2"].font = BOLD
wp["F2"] = "2026-000"; wp["F2"].fill = fill_light; wp["F2"].border = border
wp["E3"] = "Fecha:"; wp["E3"].font = BOLD
wp["F3"] = "2026-01-01"; wp["F3"].fill = fill_light; wp["F3"].border = border

wp["B4"] = "EMISOR"; wp["B4"].font = BOLD
wp["B5"] = "=Inicio!C6"; wp["B6"] = "=Inicio!C7"
wp["B7"] = "=Inicio!C8"; wp["B8"] = "=Inicio!C9"
wp["E4"] = "CLIENTE"; wp["E4"].font = BOLD
for cell in ("E5", "E6", "E7"):
    wp[cell].fill = fill_light; wp[cell].border = border
wp["E5"] = "Nombre del cliente"
wp["E6"] = "NIF del cliente"
wp["E7"] = "Dirección del cliente"

header_row(wp, 10, ["Concepto", "", "Cantidad", "Precio", "Importe"], start_col=2)
wp.merge_cells("B10:C10")
for i in range(11, 16):
    wp.merge_cells(f"B{i}:C{i}")
    wp[f"B{i}"].border = border; wp[f"B{i}"].fill = fill_grey
    wp.cell(row=i, column=4).border = border
    wp.cell(row=i, column=5).border = border
    wp.cell(row=i, column=6,
            value=f'=IF(D{i}="","",D{i}*E{i})')
    for col in (4, 5, 6):
        wp.cell(row=i, column=col).number_format = EUR
    wp.cell(row=i, column=4).number_format = "0"
wp["B11"] = "Servicio de ejemplo"; wp["D11"] = 1; wp["E11"] = 1000

# totals
wp["E17"] = "Base imponible"; wp["F17"] = "=SUM(F11:F16)"
wp["E18"] = "IVA"; wp["F18"] = f"=F17*{IVA_DEF}/100"
wp["E19"] = "Retención IRPF"; wp["F19"] = f"=-F17*{IRPF_DEF}/100"
wp["E20"] = "TOTAL"; wp["F20"] = "=F17+F18+F19"
for r2 in range(17, 21):
    wp.cell(row=r2, column=5).font = BOLD
    fc = wp.cell(row=r2, column=6)
    fc.number_format = EUR
    fc.border = border
    fc.fill = fill_accent if r2 == 20 else fill_light
    fc.font = BOLD
wp["B22"] = ("Factura exenta de IVA: art. 20 LIVA (elimina la fila de IVA si aplica). "
             "Conserva copia de todas tus facturas emitidas y recibidas durante 4 años.")
wp["B22"].font = SMALL
wp.merge_cells("B22:F23")
wp["B22"].alignment = left

# ---------- order & save -----------------------------------------------------
order = ["Inicio", "Facturas", "Gastos", "Resumen trimestral",
         "Resumen anual", "Plantilla factura", "Listas"]
wb._sheets.sort(key=lambda s: order.index(s.title))
wb.active = 0

import os
out = os.path.join(os.path.dirname(__file__), "Kit-Autonomo-Espana.xlsx")
wb.save(out)
print(f"OK -> {out}")
