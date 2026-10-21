#!/usr/bin/env python3
"""Presupuesto 127 · Brava Pool · Reforma C/ Anoia (versión revisada).

Uso:  python3 presupuesto_127.py   ->  presupuesto_127.html / presupuesto_127.pdf

- Precios: rellene PRECIOS (código de partida -> precio unitario). Importes, subtotales,
  IVA, total y calendario de pagos se recalculan solos.
- Mientras haya partidas sin precio el documento se marca como «valoración parcial» y no
  presenta un total como cerrado.
"""
import html, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent

DATOS = {
    "numero": "127",
    "fecha": "21/10/2026",
    "valido_hasta": "20/11/2026",
    "cliente": "",                              # nombre del cliente (pendiente)
    "direccion": "C/ Anoia, 14 · 17251 Calonge (Girona)",
    "contacto": "Bilal",
    "telefono": "",                             # pendiente
    "email": "",                                # pendiente
    "web": "www.bravapool.com",
    "iva": 21,
    "pagos": [(20, "A la aceptación del presupuesto (reserva de obra y pedido de materiales)"),
              (30, "Al terminar la Fase 3, antes de impermeabilizar"),
              (30, "Al terminar la Fase 4, antes de colocar la cerámica"),
              (20, "Retención final: tras la Fase 8, con la piscina llena y funcionando")],
}

# código -> precio unitario (€). Solo constan los precios facilitados en el presupuesto 127 original.
PRECIOS = {"4.1": 97.50, "5.1": 34.48, "5.2": 68.86}

# (código, título, cantidad, unidad, [viñetas])
FASES = [
 ("1", "Inspección, referencias y vaciado", [
  ("1.1", "Inspección inicial y estado previo", 1, "PA", [
    "Revisión del vaso, del canal desbordante en L, de la escalera, de los bancos y de los pasamuros.",
    "Reportaje fotográfico del estado previo, que se entrega al cliente."]),
  ("1.2", "Toma de referencia de la línea de flotación", 1, "PA", [
    "Con la piscina aún llena y desbordando, se marca el nivel real del agua en todo el perímetro.",
    "Se mide la diferencia de altura entre el labio de rebose y la coronación del resto de la piscina.",
    "Estas referencias se usan después para replantear la nueva coronación."]),
  ("1.3", "Vaciado y protección de la zona de obra", 1, "PA", [
    "Vaciado de la piscina y del canal desbordante.",
    "Protección de la terraza, el jardín y las zonas de paso durante toda la obra.",
    "Retirada y reposición de mobiliario, macetas y otros elementos situados junto al vaso."])]),
 ("2", "Demoliciones", [
  ("2.1", "Desmontaje de la coronación", 37, "ml", [
    "Retirada de la coronación del borde de la piscina, del labio de rebose y del muro exterior del canal.",
    "Si es imprescindible para extraer la coronación, levantado y reposición de las piezas de pavimento colindantes y de la rejilla lineal de la terraza (condicionado a la inspección; se valora aparte)."]),
  ("2.2", "Desmontaje de la cerámica", 105, "m²", [
    "Retirada de toda la cerámica del vaso, los bancos, la escalera y el canal desbordante.",
    "Retirada de los restos de cemento cola hasta dejar el soporte limpio."]),
  ("2.3", "Eliminación de la impermeabilización antigua", 105, "m²", [
    "Picado y retirada de la impermeabilización deteriorada hasta llegar a una base sana."]),
  ("2.4", "Retirada de escombros", 1, "PA", [
    "Carga, transporte y depósito de todos los escombros en un punto limpio autorizado."])]),
 ("3", "Reparación y preparación del soporte", [
  ("3.1", "Saneado y lijado del vaso y del canal", 1, "PA", [
    "Limpieza a fondo y eliminación de partes sueltas.",
    "Lijado del soporte y reparación de fisuras.",
    "Regularización de paredes, fondo, bancos y peldaños."]),
  ("3.2", "Revisión de pasamuros y puntos singulares", 1, "PA", [
    "Revisión y sellado de los focos, las boquillas de impulsión, el sumidero de fondo y los desagües del canal, que son los puntos donde suelen producirse las fugas.",
    "Número y posición de cada elemento: se confirman en la inspección inicial."]),
  ("3.3", "Pendiente del fondo del canal", 12.5, "ml", [
    "Corrección de la pendiente del fondo del canal hacia el sumidero para que el agua no quede estancada."]),
  ("3.4", "Replanteo de la línea de flotación y del muro de rebose", 1, "PA", [
    "Replanteo con nivel láser de la cota del labio de rebose a partir de las referencias de la Fase 1.",
    "Regularización del muro de rebose para que quede nivelado en los dos tramos del canal (7,50 m y 4,00 m), con una tolerancia máxima de ±2 mm."])]),
 ("4", "Impermeabilización · sistema DryPool de Grupo Puma", [
  ("4.1", "Suministro de mortero impermeabilizante DryPool", 10, "saco", [
    "Mortero bicomponente semiflexible de Grupo Puma para impermeabilización de piscinas con presión de agua positiva.",
    "Producto y consumo definitivos según la ficha técnica del sistema vigente."]),
  ("4.2", "Aplicación de la impermeabilización", 105, "m²", [
    "Humectación del soporte.",
    "Refuerzo de esquinas, juntas y puntos singulares.",
    "Aplicación en dos capas con malla antialcalina de refuerzo entre ellas, en el vaso, los bancos, la escalera y el canal.",
    "Curado según las indicaciones del fabricante antes de pasar a la fase siguiente."])]),
 ("5", "Revestimiento cerámico Rosa Gres", [
  ("5.1", "Suministro de cerámica Rosa Gres 30 × 60 cm", 112, "m²", [
    "Porcelánico apto para inmersión permanente.",
    "Vaso de 7,50 × 4,00 m con paredes de 1,70 m y canal en L con paredes de 80 cm.",
    "112 m² frente a 105 m² de superficie: incluye reserva por cortes y roturas."]),
  ("5.2", "Suministro de piezas de peldaño Rosa Gres", 35, "ud", [
    "Pieza antideslizante a juego con el revestimiento para el banco de 7,50 m, el banco de 4,00 m y la escalera de 6 peldaños."]),
  ("5.3", "Cemento cola para piscinas", 1, "PA", [
    "Adhesivo cementoso C2 TE S1 apto para inmersión permanente."]),
  ("5.4", "Colocación de la cerámica en vaso y canal", 105, "m²", [
    "Replanteo de piezas y colocación con doble encolado.",
    "Cortes y remates en focos, boquillas, sumidero y esquinas."]),
  ("5.5", "Colocación de peldaños en bancos y escalera", 35, "ud", [
    "Colocación de las piezas de peldaño con cortes y remates."])]),
 ("6", "Coronación y labio de rebose", [
  ("6.1", "Suministro de coronación y piezas de rebose", 37, "ml", [
    "Coronación para el borde de la piscina y el muro exterior del canal.",
    "Pieza especial de labio de rebose para los tramos de 7,50 m y 4,00 m.",
    "Modelo y acabado a confirmar por escrito, a juego con la cerámica Rosa Gres."]),
  ("6.2", "Colocación nivelada de la coronación", 37, "ml", [
    "Colocación de las piezas de los extremos a la cota del láser y del resto al hilo.",
    "Nivelación pieza a pieza del labio de rebose, con tolerancia máxima de ±2 mm."]),
  ("6.3", "Prueba de lámina de agua", 1, "PA", [
    "Antes de rejuntar, llenado hasta que la piscina desborda.",
    "Comprobación de que el agua cae de forma uniforme en toda la longitud del rebose.",
    "Corrección de cualquier punto que no desborde igual."])]),
 ("7", "Rejuntado", [
  ("7.1", "Rejuntado de cerámica, peldaños y coronación", 105, "m²", [
    "Rejuntado con mortero de juntas apto para inmersión permanente (tipo y color a confirmar por escrito).",
    "Limpieza de restos de junta."])]),
 ("8", "Llenado, pruebas y entrega", [
  ("8.1", "Prueba de estanqueidad y llenado", 1, "PA", [
    "Llenado controlado de la piscina.",
    "Comprobación durante varios días de que el nivel del agua se mantiene estable."]),
  ("8.2", "Puesta en marcha y entrega", 1, "PA", [
    "Puesta en marcha de la depuración existente y del rebose del desbordante.",
    "Limpieza final de obra y retirada de protecciones.",
    "Entrega de la piscina llena y funcionando."])]),
]

e = html.escape
def n2(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def eur(x): return n2(x) + " €"
def qty(x): return (f"{x:g}").replace(".", ",")

# ---------- cálculo ----------
partidas = [(c, t, q, u, b) for _, _, ps in FASES for (c, t, q, u, b) in ps]
imp = {c: q * PRECIOS[c] for c, _, q, _, _ in partidas if c in PRECIOS}
sin_precio = [c for c, *_ in partidas if c not in PRECIOS]
parcial = bool(sin_precio)
sub = {f: sum(imp.get(c, 0) for c, *_ in ps) for f, _, ps in FASES}
base = round(sum(sub.values()), 2)
iva_imp = round(base * DATOS["iva"] / 100, 2)
total = round(base + iva_imp, 2)

def pagos():
    out, acc = [], 0.0
    for i, (pct, txt) in enumerate(DATOS["pagos"]):
        im = round(total * pct / 100, 2) if i < len(DATOS["pagos"]) - 1 else round(total - acc, 2)
        acc += im; out.append((pct, txt, im))
    return out
PAGOS = pagos()
assert abs(sum(p[2] for p in PAGOS) - total) < 0.005 and sum(p[0] for p in DATOS["pagos"]) == 100

# ---------- piezas de página ----------
paginas = []
def pagina(titulo, cuerpo, intro=None):
    paginas.append((titulo, cuerpo, intro))

def head(titulo):
    return f'<div class="eyebrow">PRESUPUESTO {DATOS["numero"]}</div><h1>{e(titulo)}</h1>'

# 1 · carta
cifras_i = [("Dimensiones interiores", "7,50 × 4,00 m"), ("Superficie de lámina", "30 m²"),
            ("Profundidad", "1,70 m constante"), ("Volumen máximo aprox.", "51 m³")]
cifras_d = [("Tipo", "Desbordante con canal en L"), ("Canal desbordante", "12,5 ml · paredes de 80 cm"),
            ("Bancos y escalera", "2 bancos (7,50 y 4,00 m) · 6 peldaños"), ("Revestimiento", "Rosa Gres 30 × 60 cm · ≈ 105 m²"),
            ("Impermeabilización", "Sistema DryPool · Grupo Puma"), ("Coronación", "Nueva · ≈ 37 ml")]
def kv(rows): return '<table class="kv">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in rows) + '</table>'
pagina("Gracias por confiar en nosotros", f'''
<p>Estimado/a cliente:</p>
<p>Le presentamos nuestra propuesta para la rehabilitación integral de su piscina desbordante en {e(DATOS["direccion"])}. Este documento recoge, por escrito y con claridad, la obra: los trabajos, los materiales, los plazos, la forma de pago y las garantías.</p>
<p>La piscina pierde agua. Para resolverlo desde el origen retiraremos toda la cerámica, la coronación y la impermeabilización antiguas, saneamos el soporte e impermeabilizamos el vaso y el canal desbordante con el sistema DryPool de Grupo Puma, un mortero bicomponente semiflexible pensado para soportar la presión del agua. Después colocamos cerámica nueva Rosa Gres de 30 × 60 cm, piezas de peldaño antideslizantes en los bancos y la escalera, y una coronación nueva con el labio del desbordante perfectamente nivelado.</p>
<p>Cada fase se revisa antes de empezar la siguiente y le entregamos la piscina llena y funcionando.</p>
<p>Quedamos a su disposición para resolver cualquier duda o ajustar la propuesta a lo que necesite.</p>
<p class="firma"><b>{e(DATOS["contacto"])}</b><br>Brava Pool</p>
<h2>Su piscina en cifras</h2><div class="cols">{kv(cifras_i)}{kv(cifras_d)}</div>
<div class="kv-wide">{kv([("Plazo estimado", "5 a 6 semanas desde el inicio de obra, a confirmar tras la inspección inicial")])}</div>
<h2>Nuestro compromiso</h2>
<div class="cards">
<div><b>Plazos por escrito</b>Planificación por fases desde el primer día y plazo de ejecución indicado en este documento.</div>
<div><b>Pagos por hitos</b>Cada pago se vincula a una fase terminada y el 20 % final queda retenido hasta la entrega.</div>
<div><b>Garantía por escrito</b>3 años en el revestimiento y 2 años en los trabajos y la mano de obra, además de las garantías legales.</div>
<div><b>Obra limpia</b>Retiramos todos los escombros a un punto limpio autorizado y entregamos la piscina y su entorno limpios.</div></div>''')

fotos = [("foto_terraza.jpg", "Vista general desde la terraza", "Piscina desbordante en ladera, con vistas al valle, coronación de piezas de gran formato y rejilla lineal en el pavimento."),
         ("foto_canal.jpg", "Canal de desbordamiento", "Canal perimetral junto al lado del valle, con su muro exterior y coronación."),
         ("foto_escalera_banco.jpg", "Escalera y banco interior", "Escalera de acceso, banco, foco y boquilla de impulsión en pared."),
         ("foto_solera.jpg", "Fondo y sumidero", "Revestimiento cerámico rectangular y sumidero de fondo.")]
pagina("Estado actual de la piscina", f'''<p class="lead">Fotografías de la piscina antes de la obra. Sirven de referencia para el replanteo y para comprobar, al terminar, que se respeta su geometría y su aspecto.</p>
<div class="gal">{"".join(f'<figure><img src="assets/{f}" alt=""><figcaption><b>{e(t)}</b>{e(d)}</figcaption></figure>' for f,t,d in fotos)}</div>
<p class="note">Fotografías del cliente tomadas antes de la intervención. Su estado real (fisuras, filtraciones, desprendimientos) se determina en la inspección técnica inicial.</p>''')

# 2 · plano
def plano_svg():
    return '''<svg viewBox="0 0 640 560" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">
<rect width="640" height="560" fill="#fff"/>
<text x="24" y="22" font-size="11" fill="#5b6b7b" letter-spacing="1.6">PLANTA</text>
<text x="600" y="22" text-anchor="end" font-size="10" fill="#5b6b7b" letter-spacing="1.2">LADO VALLE</text>
<rect x="60" y="34" width="470" height="48" fill="#cfe7f2" stroke="#1f4e79" stroke-width="2"/>
<rect x="482" y="34" width="48" height="300" fill="#cfe7f2" stroke="#1f4e79" stroke-width="2"/>
<text x="271" y="63" text-anchor="middle" font-size="13" font-weight="700" fill="#1f4e79">Canal desbordante en L · 12,5 ml</text>
<text transform="translate(512,200) rotate(90)" text-anchor="middle" font-size="11" fill="#1f4e79">Canal</text>
<rect x="60" y="82" width="422" height="252" fill="#3a8fbf" stroke="#1f4e79" stroke-width="2"/>
<rect x="60" y="82" width="46" height="252" fill="#a9d8ec"/><rect x="60" y="290" width="422" height="44" fill="#a9d8ec"/>
<g stroke="#8fb9d0" stroke-width="1.2" fill="#d7ebf5"><rect x="106" y="226" width="78" height="64"/>
<line x1="106" y1="242" x2="184" y2="242"/><line x1="106" y1="258" x2="184" y2="258"/><line x1="106" y1="274" x2="184" y2="274"/></g>
<text transform="translate(88,150) rotate(-90)" text-anchor="middle" font-size="11" font-weight="700" fill="#1f4e79">Banco 4,00 m</text>
<text x="330" y="317" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">Banco 7,50 m</text>
<text x="145" y="216" text-anchor="middle" font-size="10.5" font-weight="700" fill="#fff">Escalera</text>
<text x="300" y="170" text-anchor="middle" font-size="16" font-weight="700" fill="#fff">Vaso 7,50 × 4,00 m</text>
<text x="300" y="190" text-anchor="middle" font-size="12" fill="#e8f4fa">Profundidad 1,70 m</text>
<g stroke="#5b6b7b" stroke-width="1" fill="none"><line x1="60" y1="352" x2="482" y2="352"/><line x1="60" y1="346" x2="60" y2="358"/><line x1="482" y1="346" x2="482" y2="358"/>
<line x1="36" y1="82" x2="36" y2="334"/><line x1="30" y1="82" x2="42" y2="82"/><line x1="30" y1="334" x2="42" y2="334"/></g>
<text x="271" y="371" text-anchor="middle" font-size="12" fill="#2b3440">7,50 m</text>
<text transform="translate(22,208) rotate(-90)" text-anchor="middle" font-size="12" fill="#2b3440">4,00 m</text>
<text x="271" y="392" text-anchor="middle" font-size="9.5" fill="#5b6b7b" letter-spacing="1.2">LADO TERRAZA Y VIVIENDA</text>
<text x="24" y="430" font-size="11" fill="#5b6b7b" letter-spacing="1.6">SECCIÓN TRANSVERSAL</text>
<rect x="92" y="468" width="300" height="70" fill="#eee6d8"/>
<rect x="100" y="456" width="270" height="68" fill="#3a8fbf" stroke="#1f4e79" stroke-width="3"/>
<rect x="100" y="456" width="48" height="68" fill="#a9d8ec" stroke="#1f4e79" stroke-width="2"/>
<rect x="380" y="456" width="60" height="40" fill="#cfe7f2" stroke="#1f4e79" stroke-width="3"/>
<line x1="100" y1="468" x2="440" y2="468" stroke="#fff" stroke-dasharray="4 3" stroke-width="1.2"/>
<text x="255" y="452" text-anchor="middle" font-size="10" fill="#5b6b7b">Lámina de agua a nivel del rebose</text>
<text x="262" y="502" text-anchor="middle" font-size="11" fill="#fff">Cerámica Rosa Gres sobre DryPool</text>
<text x="124" y="494" text-anchor="middle" font-size="10" fill="#1f4e79">Banco</text>
<text x="410" y="480" text-anchor="middle" font-size="10" fill="#1f4e79">Canal</text>
<g stroke="#5b6b7b" stroke-width="1" fill="none"><line x1="78" y1="456" x2="78" y2="524"/><line x1="72" y1="456" x2="84" y2="456"/><line x1="72" y1="524" x2="84" y2="524"/>
<line x1="458" y1="456" x2="458" y2="496"/><line x1="452" y1="456" x2="464" y2="456"/><line x1="452" y1="496" x2="464" y2="496"/></g>
<text x="66" y="494" text-anchor="end" font-size="11" fill="#2b3440">1,70</text><text x="470" y="480" font-size="11" fill="#2b3440">0,80</text>
</svg>'''

pagina("Plano de la piscina", f'''<p class="lead">Distribución de la piscina de 7,50 × 4 m y situación de los elementos principales.</p>
<div class="plano">{plano_svg()}</div>
<table class="leyenda"><tr><td><b>Vaso</b></td><td>7,50 × 4,00 m · 1,70 m de profundidad</td></tr><tr><td><b>Bancos</b></td><td>2 (7,50 m y 4,00 m)</td></tr><tr><td><b>Escalera</b></td><td>1 · 6 peldaños</td></tr><tr><td><b>Canal desbordante</b></td><td>En L · 12,5 ml · paredes de 80 cm</td></tr></table>
<p class="note">Plano orientativo, sin escala. Las medidas y la posición definitiva de cada elemento se confirman con el cliente en el replanteo.</p>''')

# 3 · sistema constructivo y materiales
capas = [("Soporte saneado y regularizado", "#d9d4cb", "#2b3440"), ("Impermeabilización DryPool · 1.ª capa", "#2e6f9e", "#fff"),
         ("Malla antialcalina de refuerzo", "#7fb6d3", "#0a2540"), ("Impermeabilización DryPool · 2.ª capa", "#2e6f9e", "#fff"),
         ("Cemento cola C2 TE S1 para inmersión", "#b9c2cc", "#0a2540"), ("Cerámica Rosa Gres 30 × 60 cm", "#e9eef3", "#0a2540"),
         ("Junta para inmersión permanente", "#8a97a5", "#fff")]
capas_svg = '<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">' + ''.join(
    f'<rect x="20" y="{10 + i * 33}" width="600" height="29" fill="{c}" stroke="#fff"/><text x="40" y="{29 + i * 33}" font-size="12.5" fill="{t}" font-weight="600">{i + 1}.  {e(n)}</text>' for i, (n, c, t) in enumerate(capas)) + '<text x="610" y="245" text-anchor="end" font-size="10" fill="#5b6b7b">Esquema de capas, de dentro hacia el agua · sin escala</text></svg>'
mats = [("Impermeabilización", "Grupo Puma", "Sistema DryPool · mortero bicomponente semiflexible y malla antialcalina"),
        ("Revestimiento", "Rosa Gres", "Porcelánico 30 × 60 cm apto para inmersión (modelo y color a confirmar)"),
        ("Bancos y escalera", "Rosa Gres", "Pieza de peldaño antideslizante (referencia a confirmar)"),
        ("Cemento cola", "Por definir", "Adhesivo cementoso C2 TE S1, apto para inmersión permanente"),
        ("Rejuntado", "Por definir", "Mortero de juntas para inmersión permanente (tipo y color a confirmar)"),
        ("Coronación", "Por definir", "Modelo y acabado a confirmar por escrito")]
pagina("Sistema constructivo y materiales", f'''<p class="lead">La estanqueidad de una piscina depende del conjunto de capas, no de un solo producto. Este es el sistema previsto y su orden de ejecución.</p>
<div class="plano">{capas_svg}</div>
<h2>Materiales y marcas</h2>
<table class="eco ph"><thead><tr><th style="width:38mm">Elemento</th><th style="width:28mm">Marca</th><th>Detalle</th></tr></thead><tbody>{"".join(f'<tr><td>{e(a)}</td><td><b class="mk">{e(b)}</b></td><td>{e(c)}</td></tr>' for a,b,c in mats)}</tbody></table>
<p class="note">Los productos se aplican según las fichas técnicas vigentes de cada fabricante. Cualquier cambio de referencia se comunica al cliente por escrito antes del pedido.</p>''')

# 4 · planificación
sem = 12  # medias semanas
gantt = [("Fase 1 · Inspección, referencias y vaciado", 1, 1, ""), ("Fase 2 · Demoliciones", 2, 3, ""), ("Fase 3 · Reparación y preparación del soporte", 5, 1, ""),
         ("Fase 4 · Impermeabilización DryPool y curado", 6, 1, "cur"), ("Fase 5 · Revestimiento cerámico", 8, 2, ""), ("Fase 6 · Coronación y labio de rebose", 10, 1, ""),
         ("Fase 7 · Rejuntado", 11, 1, ""), ("Fase 8 · Llenado, pruebas y entrega", 12, 1, "")]
# curado de la fase 4: media semana adicional tras la aplicación
rows = ""
for n, s, w, k in gantt:
    cells = ""
    if k == "cur":
        cells = f'<i style="left:{(s-1)/sem*100:.3f}%;width:{w/sem*100:.3f}%"></i><i class="hat" style="left:{s/sem*100:.3f}%;width:{1/sem*100:.3f}%"></i>'
    else:
        cells = f'<i style="left:{(s-1)/sem*100:.3f}%;width:{w/sem*100:.3f}%"></i>'
    rows += f'<tr><td>{e(n)}</td><td class="gc"><div>{cells}</div></td></tr>'
pm = [("20 %", 1), ("30 %", 5), ("30 %", 6), ("20 %", 12)]
pagos_row = ''.join(f'<span style="left:{(s-1)/sem*100:.3f}%">{p}</span>' for p, s in pm)
wk = ''.join(f'<span>S{i}</span>' for i in range(1, 7))
pagos_tabla = ''.join(f'<tr><td class="pc">{pct} %</td><td>{e(txt)}</td><td class="n">{eur(im) if not parcial else "—"}</td></tr>' for pct, txt, im in PAGOS)
pagina("Planificación de la obra", f'''<p class="lead">Plazo total estimado: 5 a 6 semanas desde el inicio de obra, a confirmar tras la inspección inicial. Cada fase se verifica antes de empezar la siguiente.</p>
<table class="gt"><thead><tr><th style="width:62mm">Fase</th><th><div class="wk">{wk}</div></th></tr></thead><tbody>{rows}
<tr class="pg"><td>Pagos</td><td class="gc"><div>{pagos_row}</div></td></tr></tbody></table>
<p class="note"><span class="sw"></span> Tiempo de curado del mortero según ficha técnica del fabricante. Planificación orientativa: puede variar según el tipo de terreno, la meteorología y la entrega de materiales; cualquier cambio se comunicará con antelación.</p>
<h2>Forma de pago</h2>
<table class="eco"><thead><tr><th style="width:16mm">Pago</th><th>Hito</th><th style="width:34mm;text-align:right">Importe con IVA</th></tr></thead><tbody>{pagos_tabla}</tbody></table>
<p class="note">Forma de pago: transferencia bancaria a nombre de Brava Pool.{" Los importes se calcularán al cerrar la valoración completa." if parcial else ""}</p>''')

# 5 · descripción de trabajos (se pagina a mano por fases)
def fase_html(f, titulo, ps):
    st = eur(sub[f]) if sub[f] else "—"
    r = f'<tr class="fase"><td colspan="5"><span>{int(f):02d}</span>FASE {f} · {e(titulo).upper()}</td><td class="n">{st}</td></tr>'
    for c, t, q, u, b in ps:
        pu = n2(PRECIOS[c]) + " €" if c in PRECIOS else "—"
        im = n2(imp[c]) + " €" if c in imp else "—"
        lis = ''.join(f'<li>{e(x)}</li>' for x in b)
        r += f'<tr class="pt"><td class="cod">{c}</td><td><b>{e(t)}</b><ul>{lis}</ul></td><td class="n">{qty(q)}</td><td class="c">{u}</td><td class="n">{pu}</td><td class="n">{im}</td></tr>'
    return r
cab = '<thead><tr><th style="width:9mm">Nº</th><th>Descripción</th><th style="width:13mm">Cant.</th><th style="width:11mm">Ud.</th><th style="width:21mm">Precio</th><th style="width:24mm">Importe</th></tr></thead>'
grupos = [["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"]]
fdict = {f: (t, ps) for f, t, ps in FASES}
for gi, g in enumerate(grupos):
    body = ''.join(fase_html(f, *fdict[f]) for f in g)
    pagina("Descripción de los trabajos" + ("" if gi == 0 else " (cont.)"), f'<table class="desc">{cab}<tbody>{body}</tbody></table>' + ('<p class="note">PA = partida alzada. Las mediciones son estimadas y se ajustan con las medidas tomadas en obra. «—» indica partida pendiente de valorar.</p>' if gi == len(grupos) - 1 else ''))

# 6 · resumen
res = ''.join(f'<tr><td class="rn">{int(f):02d}</td><td>Fase {f} · {e(t)}</td><td class="n">{eur(sub[f]) if sub[f] else "—"}</td></tr>' for f, t, _ in FASES)
aviso = f'''<div class="alert"><b>Valoración parcial.</b> {len(sin_precio)} de {len(partidas)} partidas todavía no tienen precio (mano de obra, adhesivo, coronación, rejuntado y otras). Las cifras de esta página corresponden solo a las partidas valoradas y no constituyen el precio final. El total definitivo se fijará al completar la valoración.</div>''' if parcial else '<p class="lead">Precio cerrado con todos los materiales, la mano de obra, el transporte y la retirada de escombros incluidos.</p>'
pagina("Resumen de la inversión", f'''{aviso}
<table class="eco res"><thead><tr><th style="width:14mm">Cap.</th><th>Concepto</th><th style="width:34mm;text-align:right">Importe</th></tr></thead><tbody>{res}
<tr class="sub"><td colspan="2">Base imponible{" (parcial)" if parcial else ""}</td><td class="n">{eur(base)}</td></tr>
<tr><td colspan="2">IVA {DATOS["iva"]} %</td><td class="n">{eur(iva_imp)}</td></tr>
<tr class="tot"><td colspan="2">{"Total valorado hasta ahora (IVA incl.)" if parcial else "Total presupuesto (IVA incl.)"}</td><td class="n">{eur(total)}</td></tr></tbody></table>
<p class="note">El tipo de IVA aplicable depende de las condiciones de la vivienda y de la obra; se confirma al cerrar el presupuesto.</p>''')

# 7 · garantías
cl = [("Garantía en todos nuestros trabajos", ["Al tratarse de una reforma, Brava Pool garantiza el nuevo revestimiento durante 3 años y todos los trabajos realizados y la mano de obra durante 2 años. Estas garantías comerciales se suman a las garantías legales que correspondan según la normativa vigente.", "El servicio técnico y las reparaciones en garantía se atienden durante todo el año, sin limitación de temporada. Ante cualquier incidencia comunicada por teléfono, WhatsApp o correo electrónico, respondemos por escrito en un plazo máximo de 48 horas."]),
      ("Control de calidad en cada fase", ["Revisamos y fotografiamos el soporte tras la demolición, la continuidad de la impermeabilización y los puntos singulares, la colocación y el rejuntado de la cerámica. Antes de la entrega hacemos un llenado controlado y comprobamos que el nivel del agua se mantiene estable."]),
      ("Compromiso de obra limpia", ["El precio incluye la retirada de todos los escombros de la obra, su transporte y su depósito en un punto limpio autorizado.", "Durante la obra protegemos las zonas de paso y el jardín, y al terminar retiramos todos los restos de material para entregar la piscina y su entorno limpios."]),
      ("Pagos por hitos y retención final", ["Los pagos se vinculan al avance de la obra: el primero reserva la obra y el pedido de materiales y los siguientes se abonan al terminar cada hito indicado. El último 20 % queda retenido hasta la entrega de la piscina completamente llena, con el agua tratada y los equipos en marcha."])]
pagina("Garantías y compromisos", ''.join(f'<div class="clau"><span>CLÁUSULA {i+1}</span><h3>{e(t)}</h3>{"".join(f"<p>{e(x)}</p>" for x in ps)}</div>' for i, (t, ps) in enumerate(cl)))

# 8 · condiciones y aceptación
noinc = ["Reparación de daños estructurales, tuberías o pasamuros ocultos que aparezcan al desmontar (se presupuestarán aparte).", "Equipos de filtración y depuración.", "Pavimento exterior de la terraza, salvo las piezas colindantes que sea imprescindible levantar y reponer (se valoran tras la inspección).", "Agua para el llenado y productos químicos de puesta en marcha.", "Licencia o permiso de obra y tasas municipales, si fueran necesarios."]
cond = ["Cualquier trabajo no descrito en este presupuesto se presupuestará aparte y por escrito antes de realizarlo.", "El modelo y el color de la cerámica, de la coronación y de las juntas se confirmarán por escrito antes de su pedido.", "Las mediciones son estimadas y se ajustarán con las medidas tomadas en obra.", "El cliente facilitará el acceso a la obra y el suministro de agua y luz durante los trabajos.", f'Este presupuesto es válido hasta el {DATOS["valido_hasta"]}.']
imp_acept = f'por un importe total de <b>{eur(total)}</b> IVA incluido' if not parcial else 'por el importe total que se fije en la valoración definitiva: <i class="blk"></i> (IVA incl.)'
pagina("Condiciones y aceptación", f'''<div class="cols2"><div><h2>No incluye</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in noinc)}</ul></div><div><h2>Condiciones</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in cond)}</ul></div></div>
<div class="acc"><h3>Aceptación del presupuesto</h3><p>El cliente declara conocer y aceptar el presente presupuesto n.º {DATOS["numero"]}, {imp_acept}, sus condiciones y la forma de pago indicada.</p>
<div class="sig"><div><div class="line"></div><small>Nombre y apellidos</small><div class="line"></div><small>DNI / NIF</small><div class="line"></div><small>Lugar y fecha</small></div><div><div class="line big"></div><small>Firma del cliente</small><div class="line big"></div><small>Por Brava Pool</small></div></div></div>
<div class="duda"><b>¿Alguna duda?</b> {e(DATOS["contacto"])} · {e(DATOS["web"])}{(" · " + e(DATOS["telefono"])) if DATOS["telefono"] else ""}{(" · " + e(DATOS["email"])) if DATOS["email"] else ""}</div>''')

N = len(paginas) + 1
corpo = ""
for i, (t, c, _) in enumerate(paginas, start=2):
    corpo += f'''<section class="page"><header><div><div class="eyebrow">PRESUPUESTO {DATOS["numero"]}</div><h1>{e(t)}</h1></div><img src="assets/logo.png" alt="Brava Pool"></header><div class="body">{c}</div>
<footer><span>Brava Pool · {e(DATOS["web"])}</span><span>Presupuesto {DATOS["numero"]} · Página {i} de {N}</span></footer></section>'''

portada = f'''<section class="page cover"><img class="ph" src="assets/portada.jpg" alt=""><div class="duo"></div>
<svg class="waves" viewBox="0 0 210 297" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="#fff" stroke-opacity=".10" stroke-width=".25">{''.join(f'<path d="M-10 {200+i*6} C 40 {180+i*6}, 90 {225+i*6}, 130 {203+i*6} S 200 {185+i*6}, 230 {208+i*6}"/>' for i in range(16))}</g></svg>
<div class="slash"></div><div class="slash2"></div>
<div class="logo"><img src="assets/logo_blanco.png" alt="Brava Pool"></div>
<div class="num"><small>PRESUPUESTO</small><b>{DATOS["numero"]}</b></div>
<div class="tt"><div class="chip">PROPUESTA DE REFORMA</div><h1>Rehabilitación<br>integral<br><em>de piscina</em></h1><div class="rule"></div><p>Desmontaje, impermeabilización y nueva cerámica,<br>con control de calidad en cada fase.</p></div>
<div class="glass"><div><small>PREPARADO PARA</small><b>{e(DATOS["cliente"]) if DATOS["cliente"] else "Propietario/a"}</b><span>{e(DATOS["direccion"])}</span></div><div><small>FECHA</small><b>{DATOS["fecha"]}</b></div><div><small>VÁLIDO HASTA</small><b>{DATOS["valido_hasta"]}</b></div></div>
<div class="foot"><span>Brava Pool · Girona</span><span>{e(DATOS["web"])}</span><span>La teva piscina sempre a punt</span></div></section>'''

CSS = '''
@page{size:A4;margin:0}*{box-sizing:border-box}
:root{--navy:#1f4e79;--ink:#0a2540;--cy:#3fa4c8;--bg:#eef2f5;--mut:#5b6b7b;--ln:#dde3ea}
body{margin:0;font-family:Inter,Arial,sans-serif;color:#2b3440;font-size:9.4pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.page>header{position:absolute;top:12mm;left:16mm;right:16mm;height:22mm;display:flex;justify-content:space-between;align-items:flex-start;border-bottom:.35mm solid var(--navy)}
.page>header img{height:17mm;margin-top:-2mm}
.eyebrow{font-size:7pt;letter-spacing:.2em;color:var(--cy);font-weight:600}
h1{margin:.5mm 0 0;font-size:19pt;color:var(--navy);font-weight:700;letter-spacing:-.01em}
h2{font-size:7.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--navy);margin:6mm 0 2mm;font-weight:700}
h3{font-size:10.5pt;color:var(--navy);margin:0 0 1.5mm}
.body{position:absolute;top:40mm;bottom:17mm;left:16mm;right:16mm}
.page>footer{position:absolute;bottom:8mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7pt;color:var(--mut)}
p{margin:0 0 2.6mm}ul{margin:0;padding-left:4mm}li{margin-bottom:.6mm}
.lead{font-size:10pt;color:var(--ink)}.note{font-size:7.6pt;color:var(--mut)}.firma{margin-top:4mm}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm}.cols2{display:grid;grid-template-columns:1fr 1fr;gap:9mm}.cols2 h2{margin-top:0}
.kv{width:100%;border-collapse:collapse;font-size:8.6pt}.kv td{padding:1.9mm 0;border-bottom:.2mm solid var(--ln);vertical-align:top}.kv td:first-child{color:var(--mut);width:40%}.kv td:last-child{text-align:right;font-weight:600;color:var(--ink)}
.kv-wide{margin-top:1mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm}.cards div{background:var(--bg);border-top:.7mm solid var(--cy);padding:3mm 4mm;font-size:8.4pt}.cards b{display:block;color:var(--navy);font-size:9pt;margin-bottom:.8mm}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:5mm}.gal figure{margin:0}.gal img{width:100%;height:80mm;object-fit:cover;display:block}.gal figcaption{font-size:7.8pt;color:#44505d;padding:1.5mm 0 0;line-height:1.35}.gal b{display:block;color:var(--navy);font-size:8.6pt}
.plano{border:.25mm solid var(--ln);padding:3mm;margin:3mm 0}.plano svg{width:100%;height:auto;display:block}
.leyenda{width:100%;border-collapse:collapse;font-size:8.4pt;margin:3mm 0}.leyenda td{padding:1.4mm 0;border-bottom:.2mm solid var(--ln)}.leyenda td:first-child{width:38mm;color:var(--navy)}
table{border-collapse:collapse;width:100%}
.eco{font-size:8.4pt}.eco th{text-align:left;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:2mm 1.5mm;border-bottom:.35mm solid var(--navy);border-top:.35mm solid var(--navy)}
.eco td{padding:2.2mm 1.5mm;border-bottom:.2mm solid var(--ln);vertical-align:top}.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}.c{text-align:center}
.mk{color:var(--navy)}.pc{color:var(--cy);font-weight:700}
.res .rn{color:var(--cy);font-weight:700}.res td{padding:2.6mm 1.5mm}.sub td{font-weight:600;background:var(--bg)}.tot td{background:var(--navy);color:#fff;font-weight:700;font-size:10.5pt;padding:3.4mm 3mm}
.alert{border-left:1.2mm solid #c9822b;background:#fbf3e6;padding:3mm 4mm;margin-bottom:5mm;font-size:8.8pt;color:#5a3d0f}
.desc{font-size:8.2pt}.desc th{text-align:left;font-size:6.8pt;letter-spacing:.12em;color:var(--mut);padding:1.5mm 1mm;border-bottom:.35mm solid var(--ln)}
.desc td{padding:1.8mm 1mm;vertical-align:top}.desc .fase td{background:var(--navy);color:#fff;font-weight:700;letter-spacing:.06em;padding:2.2mm 2.5mm;font-size:7.8pt}.desc .fase td.n{font-size:8.4pt}
.desc .fase span{color:#8fd0e8;margin-right:3mm}.desc .pt td{border-bottom:.2mm solid var(--ln)}.desc .cod{color:var(--mut)}
.desc ul{margin-top:.8mm;font-size:7.9pt;color:#44505d}.desc .pt{page-break-inside:avoid}
.gt{font-size:8pt;margin:3mm 0}.gt th{border-bottom:.35mm solid var(--navy);text-align:left;font-size:6.8pt;letter-spacing:.12em;color:var(--mut);padding-bottom:1.5mm}
.gt td{padding:2.2mm 1.5mm 2.2mm 0;border-bottom:.2mm solid var(--ln);vertical-align:middle}
.wk{display:grid;grid-template-columns:repeat(6,1fr);text-align:center}.wk span{border-left:.2mm dashed var(--ln)}
.gc div{position:relative;height:4.2mm;background:repeating-linear-gradient(90deg,transparent 0 16.6%,#e6ebf0 16.6% calc(16.6% + .2mm))}
.gc i{position:absolute;top:0;bottom:0;background:var(--navy);border-radius:.6mm}.gc i.hat{background:repeating-linear-gradient(135deg,#c9822b 0 1mm,#f1d4a8 1mm 2mm)}
.pg td{color:var(--cy);font-weight:700}.pg .gc div{height:5mm}.pg .gc span{position:absolute;top:0;font-size:6.8pt;background:var(--cy);color:#fff;border-radius:.8mm;padding:.2mm 1.3mm}
.sw{display:inline-block;width:6mm;height:2.6mm;background:repeating-linear-gradient(135deg,#c9822b 0 1mm,#f1d4a8 1mm 2mm);vertical-align:middle;margin-right:1.5mm}
.clau{border-left:.9mm solid var(--cy);padding:0 0 0 4mm;margin:0 0 6mm}.clau span{font-size:6.8pt;letter-spacing:.2em;color:var(--cy);font-weight:700}
.acc{border:.35mm solid var(--navy);padding:5mm 6mm;margin-top:7mm}.sig{display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:3mm}
.line{border-bottom:.3mm solid #44505d;height:9mm}.line.big{height:13mm}.sig small{font-size:7pt;color:var(--mut);display:block;margin-bottom:1mm}
.blk{display:inline-block;width:34mm;border-bottom:.25mm solid #6b7785;height:4mm;vertical-align:bottom}
.duda{background:var(--bg);padding:3mm 4mm;margin-top:6mm;font-size:8.6pt}
.cover{background:#071a30;color:#fff}.cover .ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;filter:saturate(1.15)}
.cover .duo{position:absolute;inset:0;background:linear-gradient(160deg,rgba(7,26,48,.92) 0%,rgba(14,60,100,.55) 45%,rgba(7,26,48,.95) 100%)}
.cover .waves{position:absolute;inset:0;width:100%;height:100%}
.cover .slash{position:absolute;left:-30mm;top:178mm;width:290mm;height:3mm;background:#3fa4c8;transform:rotate(-14deg);box-shadow:0 0 18mm rgba(63,164,200,.7)}
.cover .slash2{position:absolute;left:-30mm;top:186mm;width:290mm;height:.7mm;background:#8fd0e8;transform:rotate(-14deg);opacity:.7}
.cover .logo{position:absolute;top:16mm;left:16mm}.cover .logo img{height:36mm}
.cover .num{position:absolute;top:18mm;right:16mm;text-align:right}.cover .num small{display:block;font-size:7pt;letter-spacing:.3em;color:#8fd0e8}.cover .num b{display:block;font-size:54pt;line-height:1;font-weight:800;letter-spacing:-.03em;background:linear-gradient(180deg,#fff,#8fd0e8);-webkit-background-clip:text;background-clip:text;color:transparent}
.cover .tt{position:absolute;left:16mm;right:16mm;top:86mm}.cover .chip{display:inline-block;border:.3mm solid #3fa4c8;color:#8fd0e8;font-size:7.6pt;letter-spacing:.3em;padding:1.6mm 4mm;border-radius:6mm;margin-bottom:7mm;background:rgba(63,164,200,.12)}
.cover h1{color:#fff;font-size:50pt;line-height:1.02;font-weight:800;letter-spacing:-.03em;margin:0}.cover h1 em{font-style:normal;color:#5cc0e0}
.cover .rule{width:26mm;height:1.2mm;background:#3fa4c8;margin:8mm 0 6mm}.cover .tt p{font-size:11.5pt;font-weight:300;opacity:.92;line-height:1.5}
.cover .glass{position:absolute;left:16mm;right:16mm;bottom:30mm;display:grid;grid-template-columns:1.7fr 1fr 1fr;gap:6mm;padding:6mm 7mm;background:rgba(255,255,255,.10);border:.25mm solid rgba(255,255,255,.28);border-radius:3mm;backdrop-filter:blur(4px)}
.cover .glass small{display:block;font-size:6.6pt;letter-spacing:.24em;color:#8fd0e8;margin-bottom:1.5mm}.cover .glass b{display:block;font-size:12pt}.cover .glass span{font-size:8.4pt;opacity:.85}
.cover .foot{position:absolute;left:16mm;right:16mm;bottom:11mm;display:flex;justify-content:space-between;font-size:7.6pt;letter-spacing:.14em;opacity:.8;text-transform:uppercase}
'''
doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Presupuesto {DATOS["numero"]} · Brava Pool</title><style>{CSS}</style></head><body>{portada}{corpo}</body></html>'
oh, op = AQUI / "presupuesto_127.html", AQUI / "presupuesto_127.pdf"
oh.write_text(doc, encoding="utf-8")
chrome = next((p for p in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(p).exists() or subprocess.call(["which", p], stdout=subprocess.DEVNULL) == 0), None)
if not chrome:
    sys.exit("HTML generado; ábralo en Chrome e imprima a PDF (A4, sin márgenes, gráficos de fondo).")
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={op}", oh.as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", op, "| base", eur(base), "| IVA", eur(iva_imp), "| total", eur(total), "| sin precio:", len(sin_precio), "partidas |", N, "páginas")
