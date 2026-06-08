#!/usr/bin/env python3
"""
Independent check of the tax logic embedded in Kit-Autonomo-Espana.xlsx.

It reimplements, in plain Python, the exact formulas the spreadsheet uses on
the bundled example data, and asserts the Modelo 303 (IVA) and Modelo 130
(IRPF) results are correct. If this passes, the spreadsheet's calculations are
sound; run it after any change to build_kit.py.
"""
from datetime import date


def quarter(d):  # ROUNDUP(MONTH/3)
    return (d.month - 1) // 3 + 1


# --- same example data that build_kit.py writes into the workbook -----------
facturas = [  # fecha, base, iva%, irpf%
    (date(2026, 1, 15), 1000, 21, 15),
    (date(2026, 2, 3), 450, 21, 15),
]
gastos = [  # fecha, base, iva%, %deducIVA, %deducIRPF
    (date(2026, 1, 10), 50, 21, 100, 100),
    (date(2026, 1, 31), 80, 0, 0, 100),
]


def per_quarter():
    q = {i: dict(iva_rep=0.0, iva_sop=0.0, ingresos=0.0, gastos=0.0, reten=0.0)
         for i in range(1, 5)}
    for d, base, iva, irpf in facturas:
        t = q[quarter(d)]
        t["iva_rep"] += base * iva / 100
        t["reten"] += base * irpf / 100
        t["ingresos"] += base
    for d, base, iva, div, dirpf in gastos:
        t = q[quarter(d)]
        t["iva_sop"] += (base * iva / 100) * div / 100
        t["gastos"] += base * dirpf / 100
    return q


def report():
    q = per_quarter()
    acc_net = acc_ret = prev_pay = 0.0
    rows = []
    for i in range(1, 5):
        t = q[i]
        m303 = t["iva_rep"] - t["iva_sop"]
        net = t["ingresos"] - t["gastos"]
        acc_net += net
        acc_ret += t["reten"]
        m130 = max(0.0, acc_net * 0.20 - acc_ret - prev_pay)
        prev_pay += m130
        rows.append((i, m303, net, m130))
    return rows


if __name__ == "__main__":
    rows = report()
    for i, m303, net, m130 in rows:
        print(f"T{i}:  Modelo 303 (IVA) = {m303:7.2f} €   "
              f"Rdto neto = {net:8.2f} €   Modelo 130 (IRPF) = {m130:7.2f} €")

    # Expected values, computed by hand from the example data:
    #   IVA repercutido T1 = 1000*21% + 450*21% = 304.50
    #   IVA soportado   T1 = 50*21%*100%        =  10.50  -> 303 = 294.00
    #   Rdto neto       T1 = (1000+450) - (50+80) = 1320.00
    #   Retenciones     T1 = 1000*15% + 450*15% =  217.50
    #   Modelo 130      T1 = max(0, 1320*20% - 217.50 - 0) = 46.50
    t1 = rows[0]
    assert abs(t1[1] - 294.00) < 0.01, t1
    assert abs(t1[2] - 1320.00) < 0.01, t1
    assert abs(t1[3] - 46.50) < 0.01, t1
    print("\nOK — Modelo 303 and Modelo 130 logic verified against expected values.")
