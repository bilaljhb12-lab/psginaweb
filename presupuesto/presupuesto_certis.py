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
     "cliente": "Certis", "tipo_cliente": "Constructora", "nif_cliente": "", "dir_cliente": "", "obra": "",
     "emisor": "Bilal El Jouhari El Bahraoui", "nif": "42366327M", "dir": "C/ Hernán Cortés 5 · Sant Feliu de Guíxols",
     "tel": "692 490 066", "web": "www.bravapool.com", "banco": "CaixaBank (La Caixa)", "iban": "ES49 2100 0597 1701 0079 4886"}
BASE = 44000.00
LINEAS = [("Piscina de arena 8 × 5 m (aprox.)", "Construcción completa: vaso de hormigón proyectado, revestimiento continuo de cuarzo con acabado arena, coronación, instalación hidráulica y equipos.", 44000.00)]
assert abs(sum(x[2] for x in LINEAS) - BASE) < .005
PAGOS = [(20, "A la aceptación del presupuesto"), (30, "Al terminar el ferrallado y el encofrado del vaso"), (30, "Al terminar la proyección del vaso"), (20, "A la entrega de la obra terminada (retención final)")]
pg = []; acc = 0.0
for i, (pct, t) in enumerate(PAGOS):
    im = round(BASE * pct / 100, 2) if i < len(PAGOS) - 1 else round(BASE - acc, 2); acc += im; pg.append((pct, t, im))

ALCANCE = [
 ("Vaso y estructura", ["Encofrado perimetral y montaje de la armadura con varilla de 10 mm en malla de 15 × 15 cm, con separadores y zunchos de 6 mm.", "Vaso de hormigón proyectado (gunita, vía húmeda).", "Solera de hormigón preparado en planta, con 400 kg de cemento por m³, servido en obra con camión hormigonera."]),
 ("Revestimiento y coronación", ["Revestimiento continuo de cuarzo con acabado arena en todo el vaso.", "Coronación con el mismo revestimiento continuo."]),
 ("Instalación hidráulica y equipos", ["Fontanería en tubería de PVC de 50 mm para 10 atmósferas.", "2 skimmers y 3 impulsores.", "1 toma para el limpiafondos y 2 sumideros.", "Sistema de autollenado de la piscina.", "Filtro de 600 con vidrio filtrante.", "Bomba autoaspirante de 1 HP de velocidad variable.", "Cuadro eléctrico temporizado.", "2 focos LED."])]
NOINC = ["Excavación, movimiento y retirada de tierras (salvo acuerdo expreso).", "Proyecto técnico, dirección facultativa, licencias y tasas.", "Acometidas de agua y electricidad hasta el punto de conexión de la obra.", "Pavimento exterior y vallado perimetral.", "Agua de llenado y productos químicos de puesta en marcha.", "Cualquier trabajo no descrito en este presupuesto."]
COND = ["Los importes no incluyen IVA, que se añadirá a la factura al tipo vigente.", "Cualquier trabajo no descrito en este presupuesto se presupuestará aparte y por escrito antes de realizarlo.", "El color y el acabado del revestimiento se eligen con el cliente y se confirman por escrito antes de empezar.", "El inicio y el plazo de ejecución se fijan de común acuerdo tras la aceptación, y dependen de las condiciones climatológicas.", "Las medidas son aproximadas y se ajustan en el replanteo.", f"Este presupuesto es válido hasta el {D['valido']}."]

alc = ''.join(f'<div class="al"><h3>{e(t)}</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in it)}</ul></div>' for t, it in ALCANCE)
lin = ''.join(f'<tr><td><b>{e(t)}</b><span>{e(d)}</span></td><td class="n">{eur(v)}</td></tr>' for t, d, v in LINEAS)
pps = ''.join(f'<div class="pp"><b>{p} %</b><i>{eur(im)}</i><span>{e(t)}</span></div>' for p, t, im in pg)
foot = lambda n: f'<footer><span>Brava Pool · {e(D["emisor"])} · NIF {e(D["nif"])}</span><span class="fol"><b>{n:02d}</b> / 04 · Presupuesto {D["numero"]}</span></footer>'
hd = lambda t: f'<div class="rail">PRESUPUESTO {D["numero"]} · PISCINA DE ARENA 8 × 5 M</div><header><div><div class="eyebrow"><span>CONSTRUCCIÓN DE PISCINAS</span><span>BRAVA POOL</span></div><h1>{e(t)}</h1></div><img src="assets/logo.png" alt="Brava Pool"></header>'
cli = f'{e(D["cliente"])} · {e(D["tipo_cliente"])}'
blank = lambda v, w="55mm": e(v) if v else f'<i class="blk" style="width:{w}"></i>'
DOC = f"""<section class="page"><div class="hero"></div><div class="hline"></div><img class="hlogo" src="assets/logo_blanco.png"><div class="hnum"><small>PRESUPUESTO</small><b>{D["numero"]}</b></div>
<div class="htit"><div class="chip3">PROPUESTA DE CONSTRUCCIÓN</div><h1>Piscina de arena <em>8 × 5 m</em></h1></div>
<div class="body" style="top:112mm"><div class="para"><small>PREPARADO PARA</small><b>{cli}</b><br>CIF: {blank(D["nif_cliente"],"34mm")} · Dirección: {blank(D["dir_cliente"],"70mm")}<br>Obra: {blank(D["obra"],"95mm")}</div>
<p class="lead2">Le presentamos nuestra propuesta para la construcción de una piscina de arena de 8 × 5 m aproximadamente. Incluye la estructura de hormigón proyectado, el revestimiento continuo de cuarzo con acabado arena y la instalación hidráulica con sus equipos.</p>
<div class="kpis"><div class="kp"><b>8 × 5 m</b><small>vaso aproximado</small></div><div class="kp"><b>Hormigón proyectado</b><small>vaso por gunita</small></div><div class="kp"><b>Acabado arena</b><small>cuarzo continuo</small></div><div class="kp"><b>Llave en mano</b><small>con equipos</small></div></div>
<div class="para" style="margin-top:6mm"><small>FECHA · VÁLIDO HASTA</small><b>{D["fecha"]} · {D["valido"]}</b></div></div>{foot(1)}</section>
<section class="page">{hd("Alcance de la obra")}<div class="body"><p class="lead3">Esto es lo que incluye la obra. Las medidas y el equipamiento se confirman en el replanteo.</p><div class="als">{alc}</div>
<div class="box"><b>Especificaciones técnicas.</b> Las características del armado, el hormigón y los equipos son las del alcance de referencia para esta piscina y se validan con la dirección técnica de la obra antes de empezar.</div></div>{foot(2)}</section>
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
out = AQUI / "presupuesto_128_certis.html"
out.write_text(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Presupuesto 128 · Brava Pool</title><style>{CSS}</style></head><body>{DOC}</body></html>', encoding="utf-8")
pdf = AQUI / "Presupuesto_128_Certis_Piscina_Arena_8x5.pdf"
ch = next((x for x in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(x).exists()), None)
subprocess.run([ch, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", out.as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", pdf, "| base", eur(BASE), "| pagos", [eur(x[2]) for x in pg], "| suma", eur(sum(x[2] for x in pg)))
