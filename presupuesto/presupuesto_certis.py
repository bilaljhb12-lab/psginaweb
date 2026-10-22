#!/usr/bin/env python3
"""Presupuesto 128 · Brava Pool · Piscina de arena 8 × 5 m para Certis (constructora).

Uso: python3 presupuesto_certis.py -> Presupuesto_128_Certis_Piscina_Arena_8x5.pdf
Alcance tomado como referencia de un presupuesto de una piscina de 8 × 4 m, redactado de nuevo.
Las especificaciones técnicas deben validarse con la dirección técnica antes de enviarlo.
"""
import html, subprocess, sys
from pathlib import Path
AQUI = Path(__file__).parent
e = html.escape
def eur(x): return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

D = {"numero": "128", "fecha": "22/10/2026", "valido": "21/11/2026",
     "cliente": "Certis", "tipo_cliente": "Constructora", "nif_cliente": "A61126629", "dir_cliente": "", "obra": "",
     "emisor": "Bilal El Jouhari El Bahraoui", "nif": "42366327M", "dir": "C/ Hernán Cortés 5 · Sant Feliu de Guíxols",
     "tel": "692 490 066", "web": "www.bravapool.com", "banco": "CaixaBank (La Caixa)", "iban": "ES49 2100 0597 1701 0079 4886"}
BASE = 47320.00 if "--tecnico" in sys.argv else 44000.00
LINEAS = [("Piscina de arena naturalizada", "Construcción de piscina naturalizada, de tipología arena, con formas orgánicas en planta y desniveles, con materiales naturales y acabado de arena natural fijada con un sistema de resinas. Incluye cloración salina, regulación automática de pH, filtración y cuadro eléctrico.", BASE)]
assert abs(sum(x[2] for x in LINEAS) - BASE) < .005
PAGOS = [(20, "A la aceptación del presupuesto"), (30, "Al terminar la estructura del vaso"), (30, "Al terminar la instalación de equipos"), (20, "A la entrega de la obra terminada (retención final)")]
pg = []; acc = 0.0
for i, (pct, t) in enumerate(PAGOS):
    im = round(BASE * pct / 100, 2) if i < len(PAGOS) - 1 else round(BASE - acc, 2); acc += im; pg.append((pct, t, im))

ALCANCE = [
 ("Construcción de la piscina", ["Piscina naturalizada, de tipología arena, con formas orgánicas en planta y desniveles, según proyecto.", "Construida con materiales naturales.", "Superficie aproximada de 8 × 5 m, a confirmar con las mediciones del proyecto."]),
 ("Acabado", ["Arena natural fijada con un sistema de resinas.", "Color similar al del sauló natural de la zona."]),
 ("Cloración y control del agua", ["Sistema de cloración por electrólisis de sal, con unidad central de control y célula electrolítica autolimpiable (ref. SAL-25GR). Incluye el suministro de sal.", "Sistema de regulación automática de pH, con unidad central de control y sonda."]),
 ("Filtración y cuadro eléctrico", ["Filtro de poliéster reforzado con fibra de vidrio, con presión de prueba de 5 kg/cm².", "Carga de sílex microcalibrado, de granulometría 03/07, y válvula selectora de 6 posiciones en material anticorrosivo, con accesorios de enlace.", "Cuadro eléctrico en armario con doble protección, con contadores, relé térmico, diferencial, pilotos de señalización y rearme exterior."])]
NOINC = ["Excavación, movimiento y retirada de tierras (salvo acuerdo expreso).", "Proyecto técnico, dirección facultativa, licencias y tasas.", "Acometidas de agua y electricidad hasta el punto de conexión de la obra.", "Pavimento exterior y vallado perimetral.", "Agua de llenado y productos químicos de puesta en marcha.", "Cualquier trabajo no descrito en este presupuesto."]
COND = ["Los importes no incluyen IVA, que se añadirá a la factura al tipo vigente.", "Cualquier trabajo no descrito en este presupuesto se presupuestará aparte y por escrito antes de realizarlo.", "El color y el acabado del revestimiento se eligen con el cliente y se confirman por escrito antes de empezar.", "El inicio y el plazo de ejecución se fijan de común acuerdo tras la aceptación, y dependen de las condiciones climatológicas.", "Las medidas son aproximadas y se ajustan en el replanteo.", f"Este presupuesto es válido hasta el {D['valido']}."]

alc = ''.join(f'<div class="al"><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in it)}</ul></div>' for t, it in ALCANCE)
lin = ''.join(f'<tr><td><b>{e(t)}</b><span>{e(d)}</span></td><td class="n">{eur(v)}</td></tr>' for t, d, v in LINEAS)
pps = ''.join(f'<div class="pp"><b>{p} %</b><i>{eur(im)}</i><span>{e(t)}</span></div>' for p, t, im in pg)
foot = lambda n: f'<footer><span>Brava Pool · {e(D["emisor"])} · NIF {e(D["nif"])}</span><span class="fol"><b>{n:02d}</b> / 04 · Presupuesto {D["numero"]}</span></footer>'
hd = lambda t: f'<div class="rail">PRESUPUESTO {D["numero"]} · PISCINA NATURALIZADA DE ARENA</div><header><div><div class="eyebrow"><span>CONSTRUCCIÓN DE PISCINAS</span><span>BRAVA POOL</span></div><h1>{e(t)}</h1></div><img src="assets/logo.png" alt="Brava Pool"></header>'
cli = f'{e(D["cliente"])} · {e(D["tipo_cliente"])}'
blank = lambda v, w="55mm": e(v) if v else f'<i class="blk" style="width:{w}"></i>'
DOC = f"""<section class="page"><div class="hero"></div><div class="hline"></div><img class="hlogo" src="assets/logo_blanco.png"><div class="hnum"><small>PRESUPUESTO</small><b>{D["numero"]}</b></div>
<div class="htit"><div class="chip3">PROPUESTA DE CONSTRUCCIÓN</div><h1>Piscina naturalizada <em>de arena</em></h1></div>
<div class="body" style="top:112mm"><div class="para"><small>PREPARADO PARA</small><b>{cli}</b><br>CIF: {blank(D["nif_cliente"],"34mm")} · Dirección: {blank(D["dir_cliente"],"70mm")}<br>Obra: {blank(D["obra"],"95mm")}</div>
<p class="lead2">Le presentamos nuestra propuesta para la construcción de la piscina naturalizada de tipología arena prevista en el proyecto, de formas orgánicas y desniveles, construida con materiales naturales y con acabado de arena natural fijada con resinas. Incluye la cloración salina, la regulación automática de pH, la filtración y el cuadro eléctrico.</p>
<div class="kpis"><div class="kp"><b>≈ 8 × 5 m</b><small>superficie aproximada</small></div><div class="kp"><b>Formas orgánicas</b><small>con desniveles</small></div><div class="kp"><b>Arena natural</b><small>fijada con resinas</small></div><div class="kp"><b>Con equipos</b><small>sal, pH y filtración</small></div></div>
<div class="para" style="margin-top:6mm"><small>FECHA · VÁLIDO HASTA</small><b>{D["fecha"]} · {D["valido"]}</b></div></div>{foot(1)}</section>
<section class="page">{hd("Alcance de la obra")}<div class="body"><p class="lead3">Esto es lo que incluye la obra, según la descripción del proyecto. Las medidas se confirman en el replanteo.</p><div class="als">{alc}</div>
<div class="box"><b>Según proyecto.</b> Este alcance sigue la descripción del proyecto facilitada por la dirección facultativa. Las mediciones, las formas, los desniveles y los materiales se confirman con los planos antes de empezar.</div></div>{foot(2)}</section>
<section class="page">{hd("Inversión y forma de pago")}<div class="body"><table class="eco"><thead><tr><th>Concepto</th><th style="width:36mm;text-align:right">Importe</th></tr></thead><tbody>{lin}<tr class="tot"><td>Total presupuesto · IVA no incluido</td><td class="n">{eur(BASE)}</td></tr></tbody></table>
<div class="aviso"><b>Aviso:</b> este presupuesto no incluye IVA. El IVA se añadirá a la factura al tipo vigente.</div>
<h2>Forma de pago</h2><div class="pps">{pps}</div>
<table class="kv pago"><tr><td>Titular</td><td>{e(D["emisor"])} · NIF {e(D["nif"])}</td></tr><tr><td>Banco / IBAN</td><td><b>{e(D["banco"])} · {e(D["iban"])}</b></td></tr><tr><td>Concepto</td><td>Presupuesto {D["numero"]}</td></tr></table>
<div class="cards"><div><b>Pagos por hitos</b>Cada pago se vincula a una fase terminada y el último 20 % se retiene hasta la entrega.</div><div><b>Garantía</b>Brava Pool garantiza su trabajo y la mano de obra, además de las garantías legales.</div></div></div>{foot(3)}</section>
<section class="page">{hd("Condiciones y aceptación")}<div class="body"><div class="cols2"><div><h2 style="margin-top:0">No incluye</h2><ul class="tx">{"".join(f"<li>{e(x)}</li>" for x in NOINC)}</ul></div><div><h2 style="margin-top:0">Condiciones</h2><ul class="tx">{"".join(f"<li>{e(x)}</li>" for x in COND)}</ul></div></div>
<div class="acc"><h3>Aceptación del presupuesto</h3><p>El cliente acepta el presupuesto n.º {D["numero"]}, por un importe total de <b>{eur(BASE)}</b>, IVA no incluido, con sus condiciones y la forma de pago indicada.</p><div class="sig"><div><div class="line"></div><small>Nombre y cargo · DNI / NIF</small><div class="line"></div><small>Lugar y fecha</small></div><div><div class="line big"></div><small>Firma y sello del cliente</small></div></div></div>
<div class="aviso" style="margin-top:4mm"><b>Aviso:</b> este presupuesto no incluye IVA. El IVA se añadirá a la factura al tipo vigente.</div>
<div class="duda"><b>Brava Pool</b> · {e(D["emisor"])} · NIF {e(D["nif"])} · {e(D["dir"])}<br><b>Contacto:</b> {e(D["tel"])} · {e(D["web"])}</div></div>{foot(4)}</section>"""
CSS = """@page{size:A4;margin:0}*{box-sizing:border-box}:root{--navy:#0b2a45;--cy:#1f8aa0;--mut:#6b6455;--ln:#d9cfb8;--terra:#b8603c;--bg:#efe7d6}
body{margin:0;font-family:Inter,Arial,sans-serif;color:#2a2f36;font-size:9.4pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}.page>*{position:absolute}
.page>header{left:16mm;right:16mm;top:12mm;height:22mm;display:flex;justify-content:space-between;align-items:flex-start;border-bottom:.3mm solid var(--navy)}.page>header img{height:17mm;margin-top:-2mm}
.eyebrow{display:flex;gap:6mm;color:var(--terra);font-size:6.6pt;letter-spacing:.22em;font-weight:600}h1{margin:.5mm 0 0;font-size:25pt;font-weight:300;letter-spacing:-.03em;color:var(--navy)}
h2{font-size:7.8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--terra);margin:5mm 0 2mm;font-weight:700}h3{font-size:10.4pt;color:var(--navy);margin:0 0 1.5mm}
.body{top:40mm;bottom:17mm;left:16mm;right:16mm}.rail{left:7mm;top:0;bottom:0;width:6mm;display:flex;align-items:center;justify-content:center;writing-mode:vertical-rl;transform:rotate(180deg);font-size:6pt;letter-spacing:.34em;color:#a39a82;white-space:nowrap}
.page>footer{bottom:8mm;left:16mm;right:16mm;display:flex;justify-content:space-between;align-items:flex-end;font-size:7pt;color:var(--mut);border-top:.3mm solid var(--ln);padding-top:3mm}.fol b{font-size:15pt;font-weight:200;color:var(--navy);margin-right:1mm}
.hero{left:0;right:0;top:0;height:100mm;background:linear-gradient(160deg,rgba(6,26,48,.78),rgba(31,78,121,.35)),url(assets/portada.jpg) center/cover;clip-path:polygon(0 0,100% 0,100% 82%,0 100%)}
.hline{left:0;right:0;top:0;height:104mm;background:var(--terra);clip-path:polygon(0 100%,100% 82%,100% 83.6%,0 101.6%);z-index:2}.hlogo{left:16mm;top:11mm;height:24mm;z-index:3}
.hnum{right:16mm;top:12mm;text-align:right;color:#fff;z-index:3}.hnum small{display:block;font-size:6.5pt;letter-spacing:.3em;color:#8fd0e8}.hnum b{font-size:40pt;font-weight:900;line-height:.95}
.htit{left:16mm;right:16mm;top:50mm;z-index:3}.chip3{display:inline-block;border:.3mm solid #fff;color:#fff;font-size:6.8pt;letter-spacing:.3em;padding:1.4mm 3.6mm;border-radius:6mm;margin-bottom:3mm}.htit h1{color:#fff;font-size:30pt;font-weight:800;line-height:1.05;margin:0}.htit h1 em{font-style:normal;color:#8fd0e8}
.para{font-size:10.4pt;color:#444;margin-bottom:5mm;line-height:1.9}.para small{display:block;font-size:6.5pt;letter-spacing:.2em;color:var(--terra)}.para b{color:var(--navy)}.blk{display:inline-block;border-bottom:.25mm solid #9aa6b3;height:3.6mm;vertical-align:bottom}
.lead2{font-size:11.6pt;color:#222;margin:3mm 0 8mm;line-height:1.6}.lead3{font-size:11pt;color:var(--navy);margin-bottom:6mm}.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.kp{border-top:.7mm solid var(--terra);padding:2mm 0}.kp b{display:block;font-size:13pt;color:var(--navy);letter-spacing:-.02em;line-height:1.2}.kp small{font-size:7.3pt;color:#666}
.als{display:grid;grid-template-columns:1fr 1fr;gap:9mm 9mm}.al{border-top:.5mm solid var(--navy);padding-top:2.5mm}.al ul{margin:0;padding-left:4mm;font-size:10pt}.al li{margin-bottom:2.4mm}.al h3{font-size:11.6pt;margin-bottom:2.5mm}
.box{margin-top:9mm;border-left:1mm solid var(--terra);background:var(--bg);padding:4mm 5mm;font-size:9.6pt}
table{width:100%;border-collapse:collapse}.eco th{text-align:left;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--navy);padding:2mm 1.5mm;border-top:.45mm solid var(--navy);border-bottom:.2mm solid var(--navy)}.eco td{padding:5mm 1.5mm;border-bottom:.2mm solid var(--ln);vertical-align:top}.eco td span{display:block;font-size:8.2pt;color:#555;margin-top:.6mm}.n{text-align:right;white-space:nowrap;font-weight:700;font-size:11pt}
.tot td{background:var(--navy);color:#fff;font-weight:700;font-size:10.5pt;padding:3.4mm 3mm}
.aviso{margin:5mm 0 3mm;border:.4mm solid var(--terra);background:#f6e4d9;padding:3mm 4mm;font-size:9pt;color:#5b2a14}.aviso b{color:var(--terra);letter-spacing:.06em;text-transform:uppercase}
.pps{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-bottom:6mm}.pp{border-top:.7mm solid var(--navy);padding-top:2mm;font-size:8pt;color:#555}.pp b{display:block;font-size:13pt;color:var(--terra)}.pp i{display:block;font-style:normal;font-weight:700;color:#111;font-size:10pt}
.kv td{padding:1.2mm 0;border-bottom:.2mm solid var(--ln)}.kv td:first-child{color:var(--terra);width:34mm}.kv td:last-child{text-align:right;font-weight:600;color:var(--navy)}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:8mm}.cards div{background:var(--bg);border-left:.9mm solid var(--terra);padding:4mm 5mm;font-size:9.4pt}.cards b{display:block;color:var(--navy);margin-bottom:.6mm}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:9mm}ul.tx{margin:0;padding-left:4mm;font-size:9.8pt}ul.tx li{margin-bottom:2.4mm}
.acc{border:.4mm solid var(--navy);padding:6mm 7mm;margin-top:12mm}.acc p{font-size:10.4pt}.sig{display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:2mm}.line{border-bottom:.3mm solid #44505d;height:9mm}.line.big{height:13mm}.sig small{font-size:7pt;color:var(--mut);display:block;margin-bottom:1mm}
.duda{background:var(--bg);padding:3mm 4mm;margin-top:4mm;font-size:8.6pt}"""
if "--tecnico" in sys.argv:
    SEC = [("A–B", 0.00, 3.50, 3.50), ("B–C", 3.50, 4.13, 7.63), ("C–D", 4.13, 4.60, 8.73), ("D–E", 4.60, 3.14, 7.74), ("E–F", 3.14, 0.00, 3.14)]
    VOL = round(sum(s[3] for s in SEC), 2)   # 30,74 m³ recalculado (el plano indica 34,24 m³)
    SUP = 53.51
    T = [("1", "Instalaciones enterradas", [
          ("1.1", "Lecho de gravas para soporte de las instalaciones", 1, "PA", 0.0, ["Colocación del lecho de gravas sobre el que se apoyan las instalaciones."]),
          ("1.2", "Conductos de fontanería", 1, "PA", 10.0, ["Colocación de los conductos de fontanería de la piscina, según el esquema de instalaciones del proyecto."])]),
         ("2", "Estructura del vaso", [
          ("2.1", "Malla electrosoldada", SUP, "m²", 5.5, ["Colocación de la malla electrosoldada en toda la superficie del vaso.", "Medición en planta: la superficie desarrollada, con las pendientes y los niveles, será mayor y se ajusta en obra."]),
          ("2.2", "Gunitado del vaso, vía húmeda", SUP, "m²", 31.5, ["Proyección de hormigón gunitado por vía húmeda en toda la superficie de la piscina, para crear un revestimiento continuo, resistente y estanco.", "Gunita con 450 kg de cemento por m³ y fibras."])]),
         ("3", "Acabado de arena", [
          ("3.1", "Revestimiento de arena natural compactada fijada con resinas", SUP, "m²", 28.0, ["Arena natural compactada fijada con un sistema de resinas, de color similar al del sauló natural de la zona.", "Acabado continuo y antideslizante en toda la superficie de la piscina."])]),
         ("4", "Filtración, accesorios y tratamiento del agua", [
          ("4.1", "Bomba de recirculación AstralPool de 1,5 CV", 1, "ud", 5.0, ["Motobomba de la marca AstralPool, de 1,5 CV de potencia."]),
          ("4.2", "Filtro AstralPool 750", 1, "ud", 7.5, ["Filtro AstralPool 750 de poliéster reforzado con fibra de vidrio, con presión de prueba de 5 kg/cm².", "Carga de sílex microcalibrado, granulometría 03/07, y válvula selectora de 6 posiciones en material anticorrosivo, con accesorios de enlace."]),
          ("4.3", "Accesorios de la instalación hidráulica", 1, "PA", 4.5, ["2 skimmers.", "3 boquillas de impulsión.", "1 toma para el limpiafondos.", "2 sumideros de fondo.", "Cantidades según el esquema de instalaciones del proyecto, a confirmar."]),
          ("4.4", "Sistema de regulación automática de pH", 1, "ud", 3.5, ["Unidad central de control y sonda de pH."]),
          ("4.5", "Cuadro eléctrico", 1, "ud", 3.0, ["Armario con doble protección, con contadores, relé térmico, diferencial, pilotos de señalización y rearme exterior."]),
          ("4.6", "Equipo de cloración salina de 30 g/h · REGALO", 1, "ud", 0.0, ["Equipo de cloración por electrólisis de sal Bright Blue de 30 g/h, con unidad central de control y célula electrolítica autolimpiable (modelo exacto a confirmar).", "Incluye el suministro de sal. Regalo de Brava Pool: suministro e instalación sin coste."])]),
         ("5", "Entrega", [("5.1", "Limpieza final y entrega de la obra", 1, "PA", 1.5, ["Limpieza de la zona de obra y entrega de la piscina."])])]
    assert abs(sum(x[4] for _, _, ps in T for x in ps) - 100) < 1e-9
    part = [(c, t, q, u, b) for _, _, ps in T for (c, t, q, u, w, b) in ps]
    amt = {c: round(BASE * w / 100, 2) for _, _, ps in T for (c, t, q, u, w, b) in ps}
    amt[part[-1][0]] = round(amt[part[-1][0]] + BASE - sum(amt.values()), 2)
    PU = {c: round(amt[c] / q, 2) for c, t, q, u, b in part}
    IM = {c: round(PU[c] * q, 2) for c, t, q, u, b in part}
    IM[part[-1][0]] = round(IM[part[-1][0]] + BASE - sum(IM.values()), 2); PU[part[-1][0]] = IM[part[-1][0]]
    assert abs(sum(IM.values()) - BASE) < .005
    SUB = {f: round(sum(IM[x[0]] for x in ps), 2) for f, _, ps in T}
    n2 = lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    qy = lambda x: f"{x:g}".replace(".", ",")
    PAGOS = [(20, "A la aceptación del presupuesto"), (30, "Al terminar las instalaciones enterradas y la malla electrosoldada"), (30, "Al terminar el gunitado del vaso"), (20, "A la entrega de la obra terminada (retención final)")]
    pg = []; acc = 0.0
    for i, (pct, t) in enumerate(PAGOS):
        im = round(BASE * pct / 100, 2) if i < len(PAGOS) - 1 else round(BASE - acc, 2); acc += im; pg.append((pct, t, im))
    pps = ''.join(f'<div class="pp"><b>{p_} %</b><i>{eur(im)}</i><span>{e(t)}</span></div>' for p_, t, im in pg)
    OBRA = "La Reserva · Palamós (Girona)"
    NP = 7
    ftt = lambda n: f'<footer><span>Brava Pool · {e(D["emisor"])} · NIF {e(D["nif"])}</span><span class="fol"><b>{n:02d}</b> / {NP:02d} · Presupuesto {D["numero"]}</span></footer>'
    hdt = lambda t: f'<div class="rail">PRESUPUESTO {D["numero"]} · PISCINA NATURALIZADA DE ARENA · {e(OBRA).upper()}</div><header><div><div class="eyebrow"><span>CONSTRUCCIÓN DE PISCINAS</span><span>BRAVA POOL</span></div><h1>{e(t)}</h1></div><img src="assets/logo.png" alt="Brava Pool"></header>'
    INCLUIDAS = {"1.1"}   # partidas sin precio propio, incluidas en otra
    SIN_PRECIO = {"4"}   # fases que muestran solo el total, sin precio por partida
    def fase_t(f, t, ps):
        r = f'<tr class="fase"><td colspan="4"><span>{int(f):02d}</span>FASE {f} · {e(t).upper()}</td><td></td><td class="nn">{eur(SUB[f])}</td></tr>'
        for c, tt, q, u, w, b in ps:
            incl = c in INCLUIDAS
            gift = (w == 0) and not incl
            hide = ((f in SIN_PRECIO) and not gift) or incl
            r += f'<tr class="pt"><td class="cod">{c}</td><td><b>{e(tt)}</b><ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></td><td class="nn">{qy(q)}</td><td class="c">{u}</td><td class="nn">{"—" if (gift or hide) else n2(PU[c]) + " €"}</td><td class="nn"><b>{"REGALO" if gift else ("Incluido" if hide else n2(IM[c]) + " €")}</b></td></tr>'
        return r
    cab = '<thead><tr><th style="width:9mm">Nº</th><th>Descripción</th><th style="width:15mm">Cant.</th><th style="width:11mm">Ud.</th><th style="width:22mm">Precio</th><th style="width:24mm">Importe</th></tr></thead>'
    d1 = ''.join(fase_t(f, t, ps) for f, t, ps in T[:3]); d2 = ''.join(fase_t(f, t, ps) for f, t, ps in T[3:])
    vt = ''.join(f'<tr><td>{a_}</td><td class="nn">{n2(x_)} m²</td><td class="nn">{n2(y_)} m²</td><td class="nn">2,00 m</td><td class="nn"><b>{n2(v_)} m³</b></td></tr>' for a_, x_, y_, v_ in SEC for x_, y_ in [(x_, y_)]) if False else ''.join(f'<tr><td>{a_}</td><td class="nn">{n2(s1)} m²</td><td class="nn">{n2(s2)} m²</td><td class="nn">2,00 m</td><td class="nn"><b>{n2(v_)} m³</b></td></tr>' for a_, s1, s2, v_ in SEC)
    res = ''.join(f'<tr><td class="c2">{f}</td><td>{e(t)}</td><td class="nn">{eur(SUB[f])}</td></tr>' for f, t, _ in T)
    NOINC = ["Excavación del vaso, carga y transporte de tierras a vertedero.", "Proyecto técnico, dirección facultativa, licencias y tasas.", "Acometidas de agua y electricidad hasta el punto de conexión de la obra.", "Iluminación de la piscina, que no figura en la descripción del proyecto.", "Pavimento exterior, vallado y jardinería del entorno.", "Agua de llenado y productos químicos de puesta en marcha.", "Cualquier trabajo no descrito en este presupuesto."]
    cli2 = "Certis Constructora OIS, S.A. · Constructora"
    DOC = f"""<section class="page"><div class="hero"></div><div class="hline"></div><img class="hlogo" src="assets/logo_blanco.png"><div class="hnum"><small>PRESUPUESTO</small><b>{D["numero"]}</b></div>
<div class="htit"><div class="chip3">PRESUPUESTO TÉCNICO · CONSTRUCCIÓN</div><h1>Piscina naturalizada <em>de arena</em></h1></div>
<div class="body" style="top:112mm"><div class="para"><small>PREPARADO PARA</small><b>{cli2}</b><br>CIF: {e(D["nif_cliente"])}<br><small style="margin-top:2mm">OBRA</small><b>{e(OBRA)}</b> · bloque de 24 viviendas<br>Según plano A-057, revisión 02 (squaremmkm · 11/06/26)</div>
<p class="lead2">Le presentamos nuestra propuesta técnica y económica para la construcción de la piscina naturalizada de arena prevista en el proyecto, de formas orgánicas y entrada tipo playa, con tratamiento de agua salina.</p>
<div class="kpis"><div class="kp"><b>≈ 10,2 m</b><small>largo máximo</small></div><div class="kp"><b>≈ 8,0 m</b><small>ancho máximo</small></div><div class="kp"><b>53,51 m²</b><small>superficie en planta</small></div><div class="kp"><b>−1,40 m</b><small>profundidad máxima</small></div></div>
<div class="para" style="margin-top:6mm"><small>FECHA · VÁLIDO HASTA</small><b>{D["fecha"]} · {D["valido"]}</b></div></div>{ftt(1)}</section>
<section class="page">{hdt("El proyecto")}<div class="body"><div class="two2"><div><img class="plan" src="assets/plano_certis_planta.png" alt=""><p class="note">Planta de la piscina. Plano A-057, squaremmkm.</p></div>
<div><h2 style="margin-top:0">Datos del plano</h2><table class="kv"><tr><td>Proyecto</td><td>La Reserva · Palamós</td></tr><tr><td>Promotor</td><td>La Reserva Pinus Mare</td></tr><tr><td>Arquitectura</td><td>squaremmkm</td></tr><tr><td>Plano</td><td>A-057 · rev. 02</td></tr><tr><td>Largo máximo</td><td>≈ 10,2 m</td></tr><tr><td>Ancho máximo</td><td>≈ 8,0 m</td></tr><tr><td>Ancho medio</td><td>≈ 5,2 m</td></tr><tr><td>Superficie</td><td>53,51 m²</td></tr><tr><td>Profundidad</td><td>0,00 a −1,40 m</td></tr></table><p class="note">Medidas leídas sobre el plano, con un margen de unos 10 a 20 cm. Las cotas 9,79 × 11,60 m del plano corresponden al contorno exterior.</p>
<h2>Proceso de ejecución</h2><ol class="proc"><li>Excavación del vaso de la piscina.</li><li>Lecho de gravas para soporte de las instalaciones.</li><li>Conductos de fontanería.</li><li>Malla electrosoldada.</li><li>Hormigón gunitado en toda la superficie.</li><li>Arena natural compactada fijada con resinas.</li></ol></div></div></div>{ftt(2)}</section>
<section class="page">{hdt("Secciones y volúmenes")}<div class="body"><img class="sec" src="assets/plano_certis_secciones.png" alt=""><h2>Volumen del vaso (informativo)</h2>
<table class="eco vt"><thead><tr><th>Tramo</th><th class="r">Sección inicial</th><th class="r">Sección final</th><th class="r">Separación</th><th class="r">Volumen</th></tr></thead><tbody>{vt}<tr class="tot"><td colspan="4">Total recalculado</td><td class="nn">{n2(VOL)} m³</td></tr></tbody></table>
<div class="box"><b>Nota sobre la medición.</b> El plano indica 34,24 m³ porque suma 11,13 m³ en el tramo B–C. Con las secciones del propio plano (3,50 y 4,13 m², separadas 2,00 m) ese tramo da 7,63 m³ y el total es {n2(VOL)} m³. Este presupuesto usa el valor recalculado; conviene confirmarlo con la dirección facultativa.</div></div>{ftt(3)}</section>
<section class="page">{hdt("Descripción de los trabajos")}<div class="body"><table class="desc">{cab}<tbody>{d1}</tbody></table></div>{ftt(4)}</section>
<section class="page">{hdt("Descripción de los trabajos (cont.)")}<div class="body"><table class="desc">{cab}<tbody>{d2}</tbody></table><p class="note" style="margin-top:3mm">PA = partida alzada. El precio es cerrado, con materiales y mano de obra; el reparto por partidas es orientativo. En la fase 4 se indica solo el total de la fase, que incluye todas sus partidas. Las mediciones son las del proyecto y se ajustan en obra.</p></div>{ftt(5)}</section>
<section class="page">{hdt("Inversión y forma de pago")}<div class="body"><table class="eco"><thead><tr><th style="width:12mm">Fase</th><th>Concepto</th><th class="r" style="width:36mm">Importe</th></tr></thead><tbody>{res}<tr><td class="c2">+</td><td>Regalo: equipo de cloración salina de 30 g/h</td><td class="nn">Incluido</td></tr><tr class="tot"><td colspan="2">Total presupuesto · IVA no incluido</td><td class="nn">{eur(BASE)}</td></tr></tbody></table>
<div class="aviso"><b>Aviso:</b> este presupuesto no incluye IVA. El IVA se añadirá a la factura al tipo vigente.</div>
<h2>Forma de pago</h2><div class="pps">{pps}</div>
<table class="kv pago"><tr><td>Titular</td><td>{e(D["emisor"])} · NIF {e(D["nif"])}</td></tr><tr><td>Banco / IBAN</td><td><b>{e(D["banco"])} · {e(D["iban"])}</b></td></tr><tr><td>Concepto</td><td>Presupuesto {D["numero"]}</td></tr></table>
<div class="cards"><div><b>Pagos por hitos</b>Cada pago se vincula a una fase terminada y el último 20 % se retiene hasta la entrega.</div><div><b>Garantía</b>Brava Pool garantiza su trabajo y la mano de obra, además de las garantías legales.</div></div></div>{ftt(6)}</section>
<section class="page">{hdt("Condiciones y aceptación")}<div class="body"><div class="cols2"><div><h2 style="margin-top:0">No incluye</h2><ul class="tx">{"".join(f"<li>{e(x)}</li>" for x in NOINC)}</ul></div><div><h2 style="margin-top:0">Condiciones</h2><ul class="tx">{"".join(f"<li>{e(x)}</li>" for x in COND)}</ul></div></div>
<div class="acc"><h3>Aceptación del presupuesto</h3><p>El cliente acepta el presupuesto n.º {D["numero"]}, por un importe total de <b>{eur(BASE)}</b>, IVA no incluido, con sus condiciones y la forma de pago indicada.</p><div class="sig"><div><div class="line"></div><small>Nombre y cargo · DNI / NIF</small><div class="line"></div><small>Lugar y fecha</small></div><div><div class="line big"></div><small>Firma y sello del cliente</small></div></div></div>
<div class="aviso" style="margin-top:4mm"><b>Aviso:</b> este presupuesto no incluye IVA. El IVA se añadirá a la factura al tipo vigente.</div>
<div class="duda"><b>Brava Pool</b> · {e(D["emisor"])} · NIF {e(D["nif"])} · {e(D["dir"])}<br><b>Contacto:</b> {e(D["tel"])} · {e(D["web"])}</div></div>{ftt(7)}</section>"""
    CSS += """.two2{display:grid;grid-template-columns:92mm 1fr;gap:7mm}.plan{width:100%;display:block;border:.2mm solid var(--ln)}.sec{width:100%;max-height:100mm;object-fit:contain;display:block;border:.2mm solid var(--ln)}
.proc{margin:0;padding-left:5mm;font-size:9.4pt}.proc li{margin-bottom:2mm}.note{font-size:7.6pt;color:var(--mut);margin-top:1.5mm}
.r,.nn{text-align:right}.nn{white-space:nowrap;font-variant-numeric:tabular-nums}.c2{color:var(--terra);font-weight:700}.c{text-align:center}
.desc{font-size:8.2pt}.desc th{text-align:left;font-size:6.8pt;letter-spacing:.12em;color:var(--mut);padding:1.5mm 1mm;border-bottom:.35mm solid var(--navy)}.desc td{padding:2.2mm 1mm;vertical-align:top}
.desc .fase td{background:#e7dcc4;color:var(--navy);font-weight:700;letter-spacing:.06em;padding:2.4mm 2.5mm;font-size:7.8pt;border-top:.45mm solid var(--navy)}.desc .fase span{color:var(--terra);margin-right:3mm}
.desc .pt td{border-bottom:.2mm solid var(--ln)}.desc .cod{color:var(--terra)}.desc ul{margin:.8mm 0 0;padding-left:4mm;font-size:7.9pt;color:#44505d}.desc .pt{page-break-inside:avoid}
.eco .r{text-align:right}.tot .nn{font-size:10.5pt}.vt td{padding:2.2mm 1.5mm!important}.vt .tot td{padding:2.6mm 3mm!important}
"""

OUT_H = "presupuesto_128_certis_tecnico.html" if "--tecnico" in sys.argv else "presupuesto_128_certis.html"
out = AQUI / OUT_H
out.write_text(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Presupuesto 128 · Brava Pool</title><style>{CSS}</style></head><body>{DOC}</body></html>', encoding="utf-8")
pdf = AQUI / ("Presupuesto_128_Certis_La_Reserva_TECNICO.pdf" if "--tecnico" in sys.argv else "Presupuesto_128_Certis_Piscina_Arena_8x5.pdf")
ch = next((x for x in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(x).exists()), None)
subprocess.run([ch, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", out.as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", pdf, "| base", eur(BASE), "| pagos", [eur(x[2]) for x in pg], "| suma", eur(sum(x[2] for x in pg)))
