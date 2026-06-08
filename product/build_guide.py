#!/usr/bin/env python3
"""
Build the companion PDF guide for Kit Autónomo España.
Output: product/Guia-Autonomo-Espana.pdf
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, ListFlowable, ListItem)

NAVY = colors.HexColor("#1F3A5F")
BLUE = colors.HexColor("#2E5C8A")
ACCENT = colors.HexColor("#F2C200")
LIGHT = colors.HexColor("#DCE6F1")
GREY = colors.HexColor("#666666")

ss = getSampleStyleSheet()
styles = {
    "title": ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold",
                            fontSize=30, textColor=NAVY, leading=34, spaceAfter=6),
    "sub": ParagraphStyle("sub", fontSize=13, textColor=BLUE, alignment=TA_CENTER,
                          spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,
                         spaceBefore=14, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, textColor=BLUE,
                         spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                           spaceAfter=6),
    "li": ParagraphStyle("li", fontSize=10.5, leading=14),
    "small": ParagraphStyle("small", fontSize=8.5, textColor=GREY, leading=11),
    "discl": ParagraphStyle("discl", fontSize=8.5, textColor=colors.HexColor("#A00000"),
                            leading=11, alignment=TA_JUSTIFY),
}

S = lambda h=6: Spacer(1, h)


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, styles["li"]), leftIndent=10, value="•") for t in items],
        bulletType="bullet", start="•", leftIndent=12, spaceAfter=6)


def calendario_table():
    data = [["Modelo", "Qué es", "Plazo de presentación"],
            ["303", "IVA trimestral", "T1: 1–20 abr · T2: 1–20 jul · T3: 1–20 oct · T4: 1–30 ene"],
            ["130", "Pago a cuenta IRPF", "Mismos plazos que el 303 (si no estás exento)"],
            ["390", "Resumen anual de IVA", "1–30 de enero"],
            ["100", "Declaración de la Renta", "Abril–junio del año siguiente"]]
    t = Table(data, colWidths=[20*mm, 45*mm, 100*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BBBBBB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6)]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(20*mm, 12*mm, "Kit Autónomo España — Guía práctica")
    canvas.drawRightString(190*mm, 12*mm, f"Página {doc.page}")
    canvas.setStrokeColor(LIGHT)
    canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
    canvas.restoreState()


def build():
    out = os.path.join(os.path.dirname(__file__), "Guia-Autonomo-Espana.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, topMargin=22*mm, bottomMargin=20*mm,
                            leftMargin=20*mm, rightMargin=20*mm,
                            title="Guía Autónomo España", author="Kit Autónomo España")
    e = []

    # ---- cover ----
    e += [S(60),
          Paragraph("Guía del Autónomo", styles["title"]),
          Paragraph("Entiende y controla tus impuestos sin agobios", styles["sub"]),
          S(10),
          Table([[""]], colWidths=[60*mm], rowHeights=[3],
                style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)])),
          S(30),
          Paragraph("IVA · IRPF · Modelo 303 · Modelo 130 · Calendario fiscal · "
                    "Gastos deducibles", styles["sub"]),
          S(120),
          Paragraph("Acompaña a la hoja de cálculo «Kit Autónomo España». "
                    "Léela una vez y tendrás claro qué pagas, cuándo y por qué.",
                    ParagraphStyle("c", parent=styles["small"], alignment=TA_CENTER)),
          PageBreak()]

    # ---- 1 ----
    e += [Paragraph("1 · Cómo funciona ser autónomo (en 2 minutos)", styles["h2"]),
          Paragraph("Como autónomo en estimación directa, tu relación con Hacienda gira en "
                    "torno a dos impuestos: el <b>IVA</b> y el <b>IRPF</b>. El truco es entender "
                    "que casi nada de lo que cobras con esos conceptos es tuyo: lo recaudas y "
                    "luego lo liquidas.", styles["body"]),
          Paragraph("El IVA", styles["h3"]),
          Paragraph("Cuando emites una factura añades un IVA (normalmente el 21%). Ese dinero "
                    "<b>no es tuyo</b>: lo cobras por cuenta de Hacienda. A cambio, el IVA que "
                    "pagas en tus gastos del negocio te lo puedes deducir. Cada trimestre "
                    "presentas el <b>Modelo 303</b> y pagas la diferencia:", styles["body"]),
          Paragraph("IVA repercutido (el de tus facturas) − IVA soportado (el de tus gastos) "
                    "= lo que ingresas en el 303", styles["h3"]),
          Paragraph("El IRPF", styles["h3"]),
          Paragraph("El IRPF es tu impuesto sobre la renta: grava tu <b>beneficio</b> "
                    "(ingresos − gastos deducibles). Se adelanta de dos formas durante el año "
                    "y se ajusta en la Declaración de la Renta:", styles["body"]),
          bullets([
              "<b>Retenciones:</b> si facturas a empresas, normalmente retienen un 15% (7% los "
              "nuevos autónomos durante el año de alta y los dos siguientes). Ese 15% lo "
              "ingresa tu cliente en tu nombre.",
              "<b>Modelo 130:</b> un pago fraccionado trimestral del 20% de tu beneficio "
              "acumulado, del que se descuentan las retenciones y los pagos anteriores."]),
          Paragraph("Exención del Modelo 130", styles["h3"]),
          Paragraph("Si al menos el <b>70% de tus ingresos</b> ya llevan retención (lo habitual "
                    "si facturas sobre todo a empresas), <b>no tienes que presentar el Modelo "
                    "130</b>. La hoja lo calcula igualmente para que veas la cifra, pero revisa "
                    "tu caso.", styles["body"])]

    # ---- 2 ----
    e += [Paragraph("2 · Calendario fiscal", styles["h2"]),
          Paragraph("Estas son las citas que no puedes saltarte. Apunta los plazos: presentar "
                    "fuera de fecha conlleva recargos.", styles["body"]),
          calendario_table(),
          S(6),
          Paragraph("Consejo: aparta cada mes el IVA y el IRPF estimados en una cuenta "
                    "separada. Así, cuando llegue el trimestre, el dinero ya está y no te "
                    "llevas sustos.", styles["small"])]

    # ---- 3 ----
    e += [Paragraph("3 · Gastos que sí puedes deducir", styles["h2"]),
          Paragraph("Para deducir un gasto debe estar <b>vinculado a tu actividad</b>, "
                    "<b>justificado con factura</b> (no vale el ticket simple para el IVA) y "
                    "<b>registrado</b>. Los más habituales:", styles["body"]),
          bullets([
              "Cuota de autónomos (RETA) — deducible en IRPF.",
              "Asesoría o gestoría.",
              "Software, herramientas y suscripciones profesionales.",
              "Material de oficina y equipo informático.",
              "Telefonía e internet (la parte afecta a la actividad).",
              "Coworking o alquiler de oficina.",
              "Formación relacionada con tu actividad.",
              "Marketing, publicidad y página web.",
              "Comisiones e intereses bancarios de la cuenta del negocio.",
              "Suministros del hogar si trabajas en casa: deducible un 30% sobre el "
              "porcentaje de vivienda afecto a la actividad."]),
          Paragraph("Guarda todas las facturas (emitidas y recibidas) durante al menos "
                    "<b>4 años</b>.", styles["small"])]

    # ---- 4 ----
    e += [Paragraph("4 · Cómo usar la hoja de cálculo", styles["h2"]),
          bullets([
              "<b>Inicio:</b> pon tus datos y tus tipos habituales de IVA e IRPF.",
              "<b>Facturas:</b> una línea por factura emitida. Las columnas grises (cuota IVA, "
              "retención, total, trimestre) se calculan solas.",
              "<b>Gastos:</b> una línea por gasto. Indica el % deducible de IVA y de IRPF "
              "(100% en la mayoría de casos).",
              "<b>Resumen trimestral:</b> aquí ves, por trimestre, lo que sale en el Modelo "
              "303 y en el Modelo 130. Las casillas amarillas son lo que ingresas.",
              "<b>Resumen anual:</b> tu beneficio del año y los totales para la Renta.",
              "<b>Plantilla factura:</b> emite facturas con tus datos ya cargados."]),
          Paragraph("Escribe solo en las celdas blancas. Las grises contienen fórmulas; si las "
                    "borras, deja de calcular.", styles["small"])]

    # ---- 5 ----
    e += [Paragraph("5 · Errores comunes que cuestan dinero", styles["h2"]),
          bullets([
              "Gastarte el IVA cobrado: no es tuyo, lo devolverás en el 303.",
              "No guardar las facturas de gasto: sin factura no hay deducción de IVA.",
              "Olvidar un trimestre: presenta aunque salga a cero o negativo.",
              "Mezclar cuentas personales y del negocio: complica todo y resta deducciones.",
              "No revisar si te toca el Modelo 130 o estás exento."]),
          S(10),
          Paragraph("Aviso importante", styles["h3"]),
          Paragraph("Esta guía y la hoja de cálculo son herramientas de organización con fines "
                    "informativos y <b>no constituyen asesoramiento fiscal, contable ni legal</b>. "
                    "La normativa y los tipos pueden cambiar y existen situaciones particulares "
                    "(recargo de equivalencia, operaciones intracomunitarias, estimación "
                    "objetiva/módulos, etc.). Antes de presentar cualquier modelo, verifica tu "
                    "caso con un asesor fiscal o con la Agencia Tributaria. El autor no se "
                    "responsabiliza de decisiones tomadas a partir de este material.",
                    styles["discl"])]

    doc.build(e, onFirstPage=lambda c, d: None, onLaterPages=header_footer)
    print(f"OK -> {out}")


if __name__ == "__main__":
    build()
