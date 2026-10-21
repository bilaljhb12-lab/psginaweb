#!/usr/bin/env python3
"""Genera el dossier de presupuesto BRAVA POOL (HTML + PDF A4).

Uso:  python3 generar.py            -> presupuesto_brava_pool.html / .pdf
Edite DATOS (cliente) y MEDICIONES/PRECIOS: los importes y totales se calculan solos.
Una partida sin medición o sin precio queda en blanco (no se inventan cifras).
"""
import html, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent

DATOS = {
    "referencia": "BP-2026-____",
    "fecha": "21 de octubre de 2026",
    "cliente": "",            # nombre / comunidad de propietarios
    "nif": "",
    "direccion_obra": "",
    "contacto": "",
    "iva": None,              # p. ej. 21 o 10; None = a confirmar
    "validez_dias": 30,
}

# código -> (medición, precio unitario). Rellenar para que el documento calcule importes.
MEDICIONES = {
    # "01.04": (0, 0),
}

CAPITULOS = [
 ("01", "Preparación y demoliciones", [
  ("01.01", "Inspección técnica inicial del vaso, canal y escalera; toma de mediciones y registro fotográfico del estado previo.", "ud", False),
  ("01.02", "Protección de pavimentos, instalaciones y zonas colindantes; vallado y señalización de la zona de trabajo.", "ud", False),
  ("01.03", "Vaciado del vaso y gestión del agua según normativa local aplicable.", "ud", True),
  ("01.04", "Desmontaje y retirada de todo el revestimiento cerámico existente en vaso, escalera y canal de desbordamiento, con medios manuales y mecánicos de baja vibración.", "m²", False),
  ("01.05", "Picado, limpieza y retirada de la impermeabilización antigua deteriorada hasta alcanzar un soporte sano, rugoso y apto para el nuevo sistema.", "m²", False),
  ("01.06", "Carga, transporte y entrega a gestor autorizado de los residuos de obra.", "ud", False),
 ]),
 ("02", "Reparaciones y regularización de soportes", [
  ("02.01", "Saneado y limpieza de soportes (hidrolimpieza y/o aspirado) y retirada de partes no adheridas.", "m²", False),
  ("02.02", "Reparación de fisuras, coqueras y desconchones con mortero de reparación compatible con el sistema de impermeabilización.", "ml", True),
  ("02.03", "Regularización de paramentos y solera para recuperar planeidad y pendientes.", "m²", True),
  ("02.04", "Tratamiento y sellado de puntos singulares: pasamuros, boquillas, sumideros y elementos empotrados.", "ud", True),
 ]),
 ("03", "Sistema de impermeabilización", [
  ("03.01", "Preparación del soporte e imprimación, si la ficha técnica del fabricante la requiere.", "m²", False),
  ("03.02", "Banda de sellado flexible en juntas, esquinas y encuentros (gama Mapeband; modelo a confirmar con el fabricante).", "ml", False),
  ("03.03", "Impermeabilización cementosa flexible bicomponente del vaso (gama Mapelastic; producto exacto a confirmar), en las capas y espesores de la ficha técnica.", "m²", False),
  ("03.04", "Impermeabilización del canal de desbordamiento con el mismo sistema, incluidos encuentros con vaso y coronación.", "m²", False),
  ("03.05", "Prueba de estanqueidad previa al revestimiento, tras el curado indicado por el fabricante.", "ud", True),
 ]),
 ("04", "Suministro y colocación de cerámica", [
  ("04.01", "Suministro de revestimiento cerámico apto para inmersión permanente en piscina (modelo y formato a definir con el cliente).", "m²", False),
  ("04.02", "Adhesivo cementoso deformable para piscinas (gama Keraflex Maxi S1; clase y producto a confirmar), incluida su preparación y aplicación.", "m²", False),
  ("04.03", "Colocación del revestimiento: replanteo, cortes, alineación, planeidad y juntas uniformes.", "m²", False),
  ("04.04", "Piezas especiales de esquina, rincón y arista.", "ml", True),
 ]),
 ("05", "Escaleras, canal de desbordamiento y remates", [
  ("05.01", "Reparación y regularización del canal perimetral de desbordamiento: geometría, pendientes y funcionamiento hidráulico.", "ml", False),
  ("05.02", "Reparación y preparación de peldaños y superficies de la escalera de acceso.", "ud", False),
  ("05.03", "Suministro y colocación de piezas antideslizantes en peldaños (Rosa Gres; colección y referencia a confirmar).", "ml", False),
  ("05.04", "Piezas antideslizantes en otras zonas que lo requieran.", "m²", True),
  ("05.05", "Rejuntado con material apto para piscina (gama Ultracolor Plus o Kerapoxy, según exigencia química y uso; a confirmar).", "m²", False),
  ("05.06", "Juntas de dilatación y sellados elásticos perimetrales.", "ml", False),
 ]),
 ("06", "Limpieza, inspección y entrega", [
  ("06.01", "Limpieza final de acabados y de la zona de obra.", "ud", False),
  ("06.02", "Inspección final con el cliente, revisión de acabados y acta de entrega.", "ud", False),
  ("06.03", "Supervisión del llenado y puesta en servicio del vaso.", "ud", True),
 ]),
]

e = html.escape
def eur(x): return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
def num(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------- cálculo ----------
tot_cap, importes = {}, {}
for cod, _, parts in CAPITULOS:
    s = 0.0
    for p in parts:
        m = MEDICIONES.get(p[0])
        if m and m[0] and m[1]:
            importes[p[0]] = m[0] * m[1]; s += importes[p[0]]
    tot_cap[cod] = s
base = sum(tot_cap.values())
hay = bool(importes)
iva = DATOS["iva"]
iva_imp = base * iva / 100 if (hay and iva is not None) else None
total = base + iva_imp if iva_imp is not None else None

def tabla_cap(cod, nombre, parts):
    r = ""
    for c, d, u, cond in parts:
        m = MEDICIONES.get(c)
        med = num(m[0]) if m and m[0] else ""
        pu = num(m[1]) if m and m[1] else ""
        im = num(importes[c]) if c in importes else ""
        tag = '<span class="cond">Condicionada</span>' if cond else ""
        r += f'<tr><td class="c">{c}</td><td>{e(d)} {tag}</td><td class="c">{u}</td><td class="n">{med}</td><td class="n">{pu}</td><td class="n">{im}</td></tr>'
    sub = eur(tot_cap[cod]) if tot_cap[cod] else ""
    return f'''<div class="cap"><span>CAPÍTULO {cod}</span>{e(nombre)}</div>
<table class="eco"><thead><tr><th style="width:11mm">Código</th><th>Descripción técnica</th><th style="width:11mm">Ud.</th><th style="width:19mm">Medición</th><th style="width:21mm">Precio ud.</th><th style="width:23mm">Importe</th></tr></thead>
<tbody>{r}<tr class="sub"><td colspan="5">Subtotal capítulo {cod}</td><td class="n">{sub}</td></tr></tbody></table>'''

pagenum = [0]
def page(body, title, cover=False):
    pagenum[0] += 1
    if cover: return f'<section class="page cover">{body}</section>'
    return f'''<section class="page"><header><b>BRAVA POOL</b><span>Rehabilitación integral de piscina · Ref. {e(DATOS["referencia"])}</span></header>
<div class="body">{body}</div><footer><span>Documento confidencial · Propuesta sujeta a inspección técnica</span><span>{pagenum[0]}</span></footer></section>'''

def h1(n, t): return f'<div class="chap"><span>{n}</span><h1>{e(t)}</h1></div>'

blank = lambda v, w="60mm": e(v) if v else f'<i class="blk" style="width:{w}"></i>'
pages = []

# ---- portada
pages.append(page(f'''
<svg class="art" viewBox="0 0 210 297" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="#0a2540"/><stop offset=".55" stop-color="#0d3b66"/><stop offset="1" stop-color="#1b6a8f"/></linearGradient></defs>
<rect width="210" height="297" fill="url(#g)"/>
<g fill="none" stroke="#fff" stroke-opacity=".07" stroke-width=".3">
{''.join(f'<path d="M-10 {150+i*9} C 40 {130+i*9}, 80 {175+i*9}, 120 {152+i*9} S 190 {135+i*9}, 230 {158+i*9}"/>' for i in range(17))}</g>
<g fill="none" stroke="#fff" stroke-opacity=".12" stroke-width=".25">
{''.join(f'<path d="M-10 {40+i*7} C 50 {25+i*7}, 90 {60+i*7}, 140 {42+i*7} S 200 {30+i*7}, 230 {48+i*7}"/>' for i in range(7))}</g>
<rect x="0" y="228" width="210" height="69" fill="#ffffff"/>
</svg>
<div class="cv-top"><div class="logo"><svg width="46" height="46" viewBox="0 0 46 46"><circle cx="23" cy="23" r="21" fill="none" stroke="#fff" stroke-width="1.4"/><path d="M8 25c5-6 10 6 15 0s10 6 15 0" fill="none" stroke="#fff" stroke-width="1.6"/><path d="M8 32c5-6 10 6 15 0s10 6 15 0" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.6"/></svg>
<div><b>BRAVA POOL</b><small>Construcción · Rehabilitación · Mantenimiento</small></div></div></div>
<div class="cv-mid"><div class="rule"></div><p class="kick">PROPUESTA TÉCNICA Y ECONÓMICA</p>
<h1>Rehabilitación integral<br>de piscina</h1>
<p class="sub">Desmontaje, saneamiento, impermeabilización y revestimiento cerámico con control de calidad por fases</p></div>
<div class="cv-bot"><div><small>Preparada para</small><b>{blank(DATOS["cliente"],"62mm")}</b></div><div><small>Obra</small><b>{blank(DATOS["direccion_obra"],"62mm")}</b></div><div><small>Referencia · Fecha</small><b>{e(DATOS["referencia"])}<br>{e(DATOS["fecha"])}</b></div></div>''', "", cover=True))

# ---- índice
idx = [("1","Resumen ejecutivo","3"),("2","Memoria descriptiva","4"),("3","Análisis técnico y fases de intervención","5"),("4","Materiales previstos y verificación","6"),("5","Presupuesto económico","7"),("6","Planificación de obra","10"),("7","Control de calidad","11"),("8","Condiciones comerciales","12"),("9","Conclusión y aceptación","13")]
pages.append(page(h1("","Índice") + '<table class="idx">' + ''.join(f'<tr><td class="no">{a}</td><td>{e(b)}</td><td class="pg">{c}</td></tr>' for a,b,c in idx) + '</table><p class="note" style="margin-top:14mm">Este documento se ha elaborado a partir de la nota manuscrita de la obra. Las cifras económicas, las mediciones y las referencias comerciales marcadas como «a confirmar» se completarán tras la inspección técnica y la consulta de las fichas técnicas vigentes de cada fabricante.</p>', "Índice"))

# ---- resumen ejecutivo
pages.append(page(h1("1","Resumen ejecutivo") + f'''
<p class="lead">BRAVA POOL propone la rehabilitación integral del vaso, el canal de desbordamiento y la escalera de la piscina, sustituyendo el revestimiento cerámico y la impermeabilización existentes por un sistema nuevo, compatible entre sí y apto para inmersión permanente.</p>
<div class="cols"><div><h3>Alcance de la intervención</h3><ul>
<li>Desmontaje del revestimiento cerámico actual.</li><li>Eliminación de la impermeabilización antigua.</li><li>Reparación y regularización del canal de desbordamiento.</li><li>Reparación de la escalera de acceso.</li><li>Impermeabilización integral de vaso y canal.</li><li>Nueva cerámica apta para piscina y rejuntado específico.</li><li>Piezas antideslizantes en peldaños y zonas necesarias.</li></ul></div>
<div><h3>Por qué importa el método</h3><ul>
<li>La mayoría de las filtraciones se originan en una preparación deficiente o en puntos singulares mal resueltos, no solo en el material.</li><li>Cada fase se verifica antes de iniciar la siguiente.</li><li>Los productos se seleccionan por compatibilidad y se aplican según ficha técnica.</li><li>El alcance, las exclusiones y las partidas condicionadas se muestran con claridad.</li></ul></div></div>
<h3>Datos del proyecto</h3>
<table class="kv"><tr><td>Cliente</td><td>{blank(DATOS["cliente"],"90mm")}</td></tr><tr><td>NIF / CIF</td><td>{blank(DATOS["nif"],"50mm")}</td></tr><tr><td>Dirección de la obra</td><td>{blank(DATOS["direccion_obra"],"90mm")}</td></tr><tr><td>Persona de contacto</td><td>{blank(DATOS["contacto"],"70mm")}</td></tr><tr><td>Superficie de vaso / canal / escalera</td><td>{blank("","90mm")}</td></tr><tr><td>Validez de la oferta</td><td>{DATOS["validez_dias"]} días naturales desde la fecha de emisión</td></tr></table>
<div class="box"><b>Estado del presupuesto.</b> Documento preparado para su revisión. Los importes se cerrarán cuando se disponga de la inspección técnica y de las mediciones reales.</div>''', "Resumen"))

# ---- memoria
pages.append(page(h1("2","Memoria descriptiva") + '''
<h3>Objetivo</h3><p>Recuperar la estanqueidad, la seguridad y el aspecto de la piscina mediante la sustitución completa de su revestimiento y su impermeabilización, y la reparación de los elementos constructivos que lo requieran.</p>
<h3>Problemática que se pretende resolver</h3><p>El conjunto actual presenta deterioro del revestimiento y de la impermeabilización, según la nota de obra. La causa concreta, y si existe afección a la estructura, solo puede establecerse tras una inspección técnica del vaso; este documento no presupone daños estructurales.</p>
<h3>Importancia de la impermeabilización</h3><p>La impermeabilización es la barrera que protege el soporte del agua a presión permanente. Una aplicación continua, con tratamiento cuidadoso de esquinas, juntas, encuentros y pasamuros, reduce el riesgo de filtraciones, de pérdidas de agua y de desprendimiento del revestimiento. Se ejecuta sobre un soporte limpio, sano y resistente, siguiendo las capas, espesores y tiempos de curado de la ficha técnica del fabricante.</p>
<h3>Función del canal de desbordamiento</h3><p>El canal perimetral recoge el agua que rebosa de la lámina, mantiene el nivel y favorece la renovación superficial del agua. Para funcionar bien necesita geometría regular, pendientes correctas y estanqueidad continua. Por ello se repara y se impermeabiliza con el mismo rigor que el vaso.</p>
<h3>Materiales compatibles con inmersión</h3><p>Cerámica, adhesivos, rejuntados y selladores deben ser aptos para inmersión permanente y resistentes al agua tratada. Se prevé emplear un sistema coordinado de un mismo fabricante cuando sea posible, de modo que adhesivo, banda y mortero impermeable trabajen de forma compatible.</p>
<h3>Durabilidad</h3><p>La vida útil de la rehabilitación depende de la correcta ejecución, de la calidad de los soportes, del equilibrio químico del agua y del mantenimiento posterior. Por eso no se ofrecen cifras de durabilidad absolutas: se ofrecen procedimiento, control y las garantías que se detallan en las condiciones comerciales.</p>
<h3>Criterios de calidad de los acabados</h3><ul><li>Planeidad y alineación de piezas, con juntas de ancho uniforme.</li><li>Ausencia de huecos bajo la cerámica y de piezas sueltas.</li><li>Juntas completas, sin poros ni fisuras, y limpieza final sin restos de adhesivo.</li><li>Peldaños con acabado antideslizante continuo y borde bien definido.</li><li>Encuentros y juntas de dilatación selladas con material elástico.</li></ul>''', "Memoria"))

# ---- análisis técnico
fases = [("1","Inspección y evaluación inicial","Revisión del vaso, canal y escalera; mediciones; sondeo de soportes.","Confirmado"),
("2","Protección y preparación de la zona","Protección de pavimentos e instalaciones; vallado; vaciado del vaso.","Confirmado / vaciado condicionado"),
("3","Demoliciones y retirada","Desmontaje de cerámica e impermeabilización antigua; retirada de escombros.","Confirmado"),
("4","Saneamiento de soportes","Limpieza, eliminación de partes sueltas y comprobación de resistencia superficial.","Confirmado"),
("5","Reparación de elementos constructivos","Canal, escalera, fisuras, regularización y puntos singulares.","Canal y escalera confirmados; resto condicionado"),
("6","Preparación para impermeabilizar","Soporte limpio, sano, con humedad y rugosidad adecuadas; imprimación si procede.","Confirmado"),
("7","Impermeabilización","Banda en juntas y encuentros; capas del mortero impermeable; prueba de estanqueidad.","Sistema confirmado; prueba condicionada"),
("8","Revestimiento cerámico","Replanteo, adhesivo y colocación; piezas antideslizantes en peldaños.","Confirmado"),
("9","Rejuntado y acabados","Rejuntado específico, juntas elásticas, limpieza.","Confirmado"),
("10","Inspección y pruebas finales","Revisión conjunta, acta de entrega y supervisión del llenado.","Confirmado / llenado condicionado")]
pages.append(page(h1("3","Análisis técnico y fases de intervención") + '<p>La secuencia respeta el orden constructivo correcto: no se impermeabiliza hasta que el soporte está reparado y limpio, y no se reviste hasta que la impermeabilización ha curado y, cuando proceda, se ha comprobado. Los trabajos <b>condicionados</b> dependen del estado real del vaso, que solo se conoce tras la inspección y el desmontaje; se presupuestarán o descartarán entonces, con el acuerdo previo del cliente.</p><table class="eco ph"><thead><tr><th style="width:8mm">Fase</th><th style="width:48mm">Actuación</th><th>Contenido</th><th style="width:40mm">Estado en el presupuesto</th></tr></thead><tbody>' + ''.join(f'<tr><td class="c">{a}</td><td><b>{e(b)}</b></td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a,b,c,d in fases) + '</tbody></table><div class="box"><b>Sobre el estado estructural.</b> No se afirma la existencia de daños estructurales. Si la inspección o el desmontaje revelaran anomalías, se informará al cliente por escrito antes de actuar, con propuesta y valoración independientes.</div>', "Análisis"))

# ---- materiales
mats = [("Impermeabilización cementosa flexible","Mapei · gama Mapelastic (p. ej. Mapelastic / Mapelastic Smart)","Nombre de gama verificado en el catálogo del fabricante. Producto exacto, consumo y espesor: confirmar en ficha técnica para piscina e inmersión."),
("Banda de sellado de juntas y encuentros","Mapei · gama Mapeband","Gama verificada. Modelo según tipo de junta, a confirmar."),
("Adhesivo cementoso deformable","Mapei · Keraflex Maxi S1","Adhesivo deformable verificado en el catálogo; idoneidad para el formato de pieza y la inmersión, a confirmar en ficha."),
("Rejuntado","Mapei · Ultracolor Plus o Kerapoxy","Ultracolor Plus (cementoso, apto para piscinas) y Kerapoxy (epoxi, mayor resistencia química). Elección según agua, tratamiento y preferencia del cliente."),
("Cerámica / gres apto para piscina","A definir con el cliente","Debe ser apta para inmersión permanente y resistente a heladas si procede."),
("Piezas antideslizantes de peldaño","Rosa Gres (Rosagres) · acabado antideslizante","El fabricante indica que sus piezas se ofrecen en acabado antideslizante, pero no se ha podido verificar una colección ni una referencia concretas. Referencia y clase de resbaladicidad (en CTE DB-SUA, clase 3 en zonas de baño donde corresponda): a confirmar con el fabricante.")]
pages.append(page(h1("4","Materiales previstos y verificación") + '<p>Los nombres de producto se han contrastado con el catálogo público de cada fabricante. No se incorpora ninguna referencia como definitiva hasta comprobar la ficha técnica vigente, la compatibilidad del conjunto y la prescripción del fabricante para piscinas.</p><table class="eco ph"><thead><tr><th style="width:42mm">Elemento</th><th style="width:48mm">Producto previsto</th><th>Estado de verificación</th></tr></thead><tbody>' + ''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a,b,c in mats) + '</tbody></table><h3>Preparación del soporte y puntos singulares</h3><ul><li>Soporte limpio, sin polvo, grasas ni restos de materiales anteriores, con resistencia y humedad adecuadas.</li><li>Redondeo o tratamiento de esquinas y encuentros vaso–canal y vaso–escalera según el fabricante.</li><li>Banda de sellado en juntas y fisuras de movimiento; refuerzo en pasamuros, boquillas y sumideros.</li><li>Aplicación del impermeabilizante en capas sucesivas respetando tiempos de espera y curado de la ficha técnica.</li></ul>', "Materiales"))

# ---- presupuesto (3 páginas)
nota_eco = '<p class="note">Las celdas de medición y precio se completan una vez realizada la inspección. «Condicionada»: partida cuyo alcance depende del estado real del vaso.</p>'
pages.append(page(h1("5","Presupuesto económico") + nota_eco + tabla_cap(*CAPITULOS[0]) + tabla_cap(*CAPITULOS[1]), "Presupuesto"))
pages.append(page(tabla_cap(*CAPITULOS[2]) + tabla_cap(*CAPITULOS[3]), "Presupuesto"))
res = ''.join(f'<tr><td class="c">{c}</td><td>{e(n)}</td><td class="n">{eur(tot_cap[c]) if tot_cap[c] else ""}</td></tr>' for c,n,_ in CAPITULOS)
ivatxt = f"IVA ({iva}%)" if iva is not None else "IVA (tipo aplicable a confirmar)"
pages.append(page(tabla_cap(*CAPITULOS[4]) + tabla_cap(*CAPITULOS[5]) + f'''<div class="cap"><span>RESUMEN</span>Resumen económico</div>
<table class="eco res"><tbody>{res}<tr class="sub"><td colspan="2">Base imponible</td><td class="n">{eur(base) if hay else ""}</td></tr>
<tr><td colspan="2">{ivatxt}</td><td class="n">{eur(iva_imp) if iva_imp is not None else ""}</td></tr>
<tr class="tot"><td colspan="2">TOTAL PRESUPUESTO</td><td class="n">{eur(total) if total is not None else ""}</td></tr></tbody></table>
<p class="note">El tipo de IVA (general o reducido para rehabilitación de vivienda) depende de las condiciones del cliente y de la obra y se fijará en la oferta definitiva. Desglose estimativo hasta disponer de mediciones.</p>''', "Presupuesto"))

# ---- planificación
plan = [("Inspección y mediciones",0,1),("Protección y preparación",1,1),("Demoliciones y retirada",2,2),("Saneamiento y reparaciones",4,2),("Preparación e impermeabilización",6,2),("Curado y prueba de estanqueidad",8,2),("Revestimiento cerámico",10,3),("Rejuntado y acabados",13,2),("Inspección, llenado y entrega",15,1)]
bars = ''.join(f'<tr><td>{e(n)}</td><td class="gantt"><i style="margin-left:{s*5.6}%;width:{w*5.6}%" class="{"cur" if "Curado" in n else ""}"></i></td><td class="c">____</td></tr>' for n,s,w in plan)
pages.append(page(h1("6","Planificación de obra") + f'''<p>El cronograma muestra el <b>orden de ejecución</b> y las dependencias entre fases. Las duraciones se fijarán cuando se conozcan las dimensiones, la climatología prevista, la disponibilidad de materiales y los tiempos de curado de las fichas técnicas. No se establece ningún plazo definitivo en este documento.</p>
<table class="eco gt"><thead><tr><th style="width:55mm">Fase</th><th>Secuencia (sin escala temporal)</th><th style="width:24mm">Duración est.</th></tr></thead><tbody>{bars}</tbody></table>
<h3>Distinción de tiempos</h3><table class="kv"><tr><td>Trabajos</td><td>Demolición, reparaciones, aplicación, colocación y rejuntado: duración estimada tras mediciones.</td></tr><tr><td>Curado de materiales</td><td>Mortero impermeable, adhesivo y rejuntado: los tiempos de espera son los de cada ficha técnica y no se acortan.</td></tr><tr><td>Pruebas</td><td>Estanqueidad previa al revestimiento y revisión final, cuando proceda.</td></tr><tr><td>Puesta en servicio</td><td>Llenado y uso tras el curado completo indicado por los fabricantes.</td></tr></table>''', "Plan"))

# ---- calidad
qc = [("Soportes","Limpios, sanos, resistentes, con rugosidad y humedad adecuadas.","Antes de impermeabilizar"),
("Reparaciones","Canal, escalera y fisuras reparados; pendientes y geometría recuperadas.","Fin de reparaciones"),
("Continuidad de la impermeabilización","Capas completas, sin huecos, con espesor y consumo conformes a ficha.","Tras cada capa"),
("Puntos singulares","Esquinas, juntas, encuentros, pasamuros y sumideros tratados con banda y refuerzo.","Antes de la última capa"),
("Compatibilidad de materiales","Adhesivo, banda, impermeabilizante y rejuntado coherentes con las fichas técnicas.","Antes de la compra y de la aplicación"),
("Colocación cerámica","Planeidad, alineación, adherencia sin huecos y juntas uniformes.","Durante y tras colocar"),
("Rejuntado","Juntas completas, sin poros ni fisuras; limpieza de superficie.","Tras el curado del rejuntado"),
("Estanqueidad","Prueba de llenado o equivalente, cuando corresponda, con registro de nivel.","Antes del revestimiento"),
("Revisión final","Inspección conjunta, listado de repasos y acta de entrega.","Entrega")]
pages.append(page(h1("7","Control de calidad") + '<p>Protocolo de verificación previsto. Se trata de controles que se realizarán durante la obra; ninguno de ellos se ha efectuado todavía.</p><table class="eco ph"><thead><tr><th style="width:42mm">Control</th><th>Criterio de aceptación</th><th style="width:36mm">Momento</th><th style="width:12mm">V.º B.º</th></tr></thead><tbody>' + ''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td><td class="c">☐</td></tr>' for a,b,c in qc) + '</tbody></table><p class="note">Las incidencias detectadas se corregirán antes de pasar a la fase siguiente y se informará al cliente de las que afecten al alcance.</p>', "Calidad"))

# ---- condiciones
cond = [("Alcance","Los trabajos descritos en los capítulos 01 a 06. Las partidas condicionadas se ejecutarán solo si la inspección o el desmontaje lo justifican y con conformidad previa del cliente."),
("Exclusiones","Reparaciones estructurales, sustitución de equipos de filtración y depuración, tuberías, iluminación, pavimento perimetral, licencias y tasas, salvo mención expresa."),
("Materiales previstos","Los indicados en el apartado 4, pendientes de confirmación de referencia. Un cambio de producto se comunicará al cliente."),
("Trabajos adicionales","Los no previstos o derivados de hallazgos durante la obra se presupuestarán aparte y requieren aceptación escrita antes de ejecutarse."),
("Gestión de residuos","Retirada y entrega a gestor autorizado conforme a la normativa vigente."),
("Condiciones de pago","A concretar con el cliente: hitos y porcentajes ______ ."),
("Plazo estimado","A fijar tras las mediciones; sujeto a clima, materiales y curados (apartado 6)."),
(f"Validez de la oferta",f"{DATOS['validez_dias']} días naturales desde la fecha de emisión."),
("Garantías legales","Las que establezca la normativa vigente aplicable a la obra y al consumidor (p. ej. Ley de Ordenación de la Edificación y legislación de consumo), con los plazos que correspondan. Son obligatorias e independientes de este documento."),
("Garantía comercial","Cualquier garantía adicional de BRAVA POOL, o la de los fabricantes, se indicará por escrito en la oferta definitiva con su alcance y condiciones; no se ofrecen garantías absolutas.")]
pages.append(page(h1("8","Condiciones comerciales") + '<table class="kv big">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a,b in cond) + '</table>', "Condiciones"))

# ---- conclusión + aceptación
pages.append(page(h1("9","Conclusión y aceptación") + f'''<p class="lead">Una rehabilitación bien planteada no depende de un único producto, sino de hacer bien cada fase, en su orden, con materiales compatibles y con controles que puedan comprobarse. Esa es la base de esta propuesta: alcance transparente, método claro y seguimiento durante toda la obra.</p>
<p>BRAVA POOL queda a disposición del cliente para realizar la inspección técnica, resolver dudas y cerrar mediciones, producto y plazos antes de emitir la oferta definitiva.</p>
<div class="acc"><h3>Aceptación del cliente</h3><p>El cliente declara haber leído y aceptar la presente propuesta y sus condiciones, por un importe total de <i class="blk" style="width:38mm"></i> (IVA incluido / no incluido).</p>
<div class="sig"><div><b>Por BRAVA POOL</b><p>Nombre y cargo:</p><p>Fecha:</p><div class="line"></div><small>Firma y sello</small></div><div><b>El cliente</b><p>Nombre y NIF:</p><p>Fecha:</p><div class="line"></div><small>Firma</small></div></div></div>''', "Aceptación"))

CSS = '''
@page{size:A4;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:Inter,"Helvetica Neue",Arial,sans-serif;color:#2b3440;font-size:9.6pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.page>header{position:absolute;top:0;left:0;right:0;height:16mm;padding:7mm 18mm 0;display:flex;justify-content:space-between;font-size:7.5pt;letter-spacing:.08em;color:#6b7785;border-bottom:.3mm solid #dfe4ea;margin:0 18mm;padding:7mm 0 0}
.page>header b{color:#0d3b66;letter-spacing:.2em}
.page>footer{position:absolute;bottom:0;left:18mm;right:18mm;height:14mm;padding-top:4mm;display:flex;justify-content:space-between;font-size:7.5pt;color:#6b7785;border-top:.3mm solid #dfe4ea}
.body{position:absolute;top:22mm;bottom:18mm;left:18mm;right:18mm}
.chap{display:flex;align-items:flex-end;gap:5mm;margin-bottom:6mm;border-bottom:.6mm solid #0d3b66;padding-bottom:3mm}
.chap span{font-size:30pt;font-weight:200;color:#b8892f;line-height:1}
h1{margin:0;font-size:19pt;font-weight:600;color:#0a2540;letter-spacing:-.01em}
h3{font-size:10.5pt;color:#0d3b66;margin:5mm 0 1.5mm;font-weight:600}
p{margin:0 0 2.6mm}ul{margin:0 0 2mm;padding-left:4.5mm}li{margin-bottom:1mm}
.lead{font-size:11.5pt;color:#0a2540;line-height:1.55}
.note{font-size:8pt;color:#6b7785}
.box{margin-top:5mm;border-left:1mm solid #b8892f;background:#f4f6f9;padding:3mm 4mm;font-size:9pt}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
table{width:100%;border-collapse:collapse}
.kv td{padding:2mm 3mm;border-bottom:.2mm solid #e3e7ec;vertical-align:top}.kv td:first-child{width:52mm;color:#0d3b66;font-weight:600}
.kv.big td{padding:3.1mm 3mm}.kv.big td:first-child{width:38mm}
.blk{display:inline-block;border-bottom:.25mm solid #9aa6b3;height:4mm;vertical-align:bottom}
.idx td{padding:3.2mm 2mm;border-bottom:.2mm solid #e3e7ec;font-size:11pt}.idx .no{width:12mm;color:#b8892f;font-weight:600}.idx .pg{text-align:right;color:#6b7785}
.cap{background:#0d3b66;color:#fff;padding:2.2mm 4mm;margin:5mm 0 0;font-weight:600;font-size:10pt;display:flex;gap:6mm}
.cap span{font-weight:400;letter-spacing:.14em;font-size:7.5pt;opacity:.75;align-self:center}
.eco{font-size:8.1pt;margin-bottom:1mm}.eco th{background:#eef1f5;color:#0d3b66;text-align:left;padding:1.8mm 2mm;font-size:7.4pt;text-transform:uppercase;letter-spacing:.05em}
.eco td{padding:1.9mm 2mm;border-bottom:.2mm solid #e3e7ec;vertical-align:top}
.eco .c{text-align:center}.eco .n{text-align:right;font-variant-numeric:tabular-nums}
.eco td:nth-child(n+4):not(.c){background:#fafbfc}
.sub td{background:#eef1f5!important;font-weight:600;color:#0a2540}.tot td{background:#0a2540!important;color:#fff;font-weight:600;font-size:10pt}
.res td{padding:1.1mm 2mm}.res td:first-child{width:11mm}
.cond{display:inline-block;font-size:6.6pt;letter-spacing:.06em;text-transform:uppercase;color:#8a6720;border:.2mm solid #b8892f;padding:0 1.2mm;margin-left:1mm;border-radius:1mm}
.ph td:nth-child(n){background:#fff!important}.ph.eco td:nth-child(n+4):not(.c){background:#fff}
.gt td{vertical-align:middle}.gantt{background:repeating-linear-gradient(90deg,#fff 0 5.6%,#f3f5f8 5.6% 11.2%)!important;padding:1.4mm 0}
.gantt i{display:block;height:3.2mm;background:#0d3b66;border-radius:.6mm}.gantt i.cur{background:#b8892f}
.cover{background:#fff;color:#fff}.cover .art{position:absolute;inset:0;width:100%;height:100%}
.cv-top{position:absolute;top:20mm;left:20mm}.logo{display:flex;align-items:center;gap:4mm}.logo b{display:block;font-size:17pt;letter-spacing:.32em;font-weight:600}.logo small{display:block;font-size:7pt;letter-spacing:.2em;opacity:.8;margin-top:1mm}
.cv-mid{position:absolute;top:100mm;left:20mm;right:20mm}.cv-mid .rule{width:22mm;height:.8mm;background:#c9a24d;margin-bottom:7mm}
.cv-mid .kick{font-size:8.5pt;letter-spacing:.3em;opacity:.85}.cv-mid h1{color:#fff;font-size:34pt;font-weight:300;line-height:1.12;margin:3mm 0 6mm}.cv-mid .sub{max-width:115mm;font-size:11pt;opacity:.85;font-weight:300}
.cv-bot{position:absolute;bottom:14mm;left:20mm;right:20mm;display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:8mm;color:#0a2540;font-size:9pt}
.cv-bot small{display:block;font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:#6b7785;margin-bottom:1.5mm}.cv-bot b{font-weight:600;white-space:nowrap}
.acc{margin-top:8mm;border:.3mm solid #0d3b66;padding:5mm 6mm}.sig{display:grid;grid-template-columns:1fr 1fr;gap:12mm;margin-top:4mm}.sig p{margin:2mm 0;font-size:8.6pt;color:#4a5562}.sig .line{border-bottom:.3mm solid #2b3440;height:20mm}.sig small{font-size:7pt;color:#6b7785}
'''
doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>BRAVA POOL · Presupuesto de rehabilitación de piscina</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
out_html = AQUI / "presupuesto_brava_pool.html"; out_pdf = AQUI / "presupuesto_brava_pool.pdf"
out_html.write_text(doc, encoding="utf-8")
chrome = next((p for p in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(p).exists() or subprocess.call(["which", p], stdout=subprocess.DEVNULL) == 0), None)
if not chrome:
    sys.exit("HTML generado; abra en Chrome e imprima a PDF (A4, sin márgenes, gráficos de fondo).")
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html.as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", out_pdf)
