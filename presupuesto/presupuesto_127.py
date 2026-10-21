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
MUESTRA = "--muestra" in sys.argv        # versión de muestra: marca de agua y resumen de revisión al final

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
    "precio_cerrado": 22578.00,                 # base imponible acordada (sin IVA)
    "pagos": [(20, "A la aceptación del presupuesto (reserva de obra y pedido de materiales)"),
              (30, "Al terminar la Fase 3, antes de impermeabilizar"),
              (30, "Al terminar la Fase 4, antes de colocar la cerámica"),
              (20, "Retención final: a la entrega de la obra terminada")],
}

FASES = [
 ("1", "Inspección, referencias y vaciado", [
  ("1.1", "Inspección inicial y estado previo", 1, "PA", [
    "Revisión del vaso, del canal desbordante en L, de la escalera, del banco y de los pasamuros.",
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
    "Retirada de toda la cerámica del vaso, el banco, la escalera y el canal desbordante.",
    "Retirada de los restos de cemento cola hasta dejar el soporte limpio."]),
  ("2.3", "Eliminación de la impermeabilización antigua", 105, "m²", [
    "Picado y retirada de la impermeabilización deteriorada hasta llegar a una base sana."]),
  ("2.4", "Retirada de escombros", 1, "PA", [
    "Carga, transporte y depósito de todos los escombros en un punto limpio autorizado."])]),
 ("3", "Reparación y preparación del soporte", [
  ("3.1", "Saneado y lijado del vaso y del canal", 1, "PA", [
    "Limpieza a fondo y eliminación de partes sueltas.",
    "Lijado del soporte y reparación de fisuras y coqueras con el mortero tixotrópico de alta resistencia Morcemseal Todo 1 R4 de Grupo Puma.",
    "Regularización de paredes, fondo, banco y peldaños."]),
  ("3.2", "Revisión de pasamuros y puntos singulares", 1, "PA", [
    "Revisión y sellado de los focos, las boquillas de impulsión, el sumidero de fondo y los desagües del canal, que son los puntos donde suelen producirse las fugas, con banda butílica Bandtec de Grupo Puma en los puntos críticos.",
    "Número y posición de cada elemento: se confirman en la inspección inicial."]),
  ("3.3", "Pendiente del fondo del canal", 12.5, "ml", [
    "Corrección de la pendiente del fondo del canal hacia el sumidero para que el agua no quede estancada."]),
  ("3.4", "Replanteo de la línea de flotación y del muro de rebose", 1, "PA", [
    "Replanteo con nivel láser de la cota del labio de rebose a partir de las referencias de la Fase 1.",
    "Regularización del muro de rebose para que quede nivelado en los dos tramos del canal (7,50 m y 4,00 m), con una tolerancia máxima de ±2 mm."])]),
 ("4", "Impermeabilización · sistema DryPool de Grupo Puma", [
  ("4.1", "Suministro y aplicación del sistema DryPool en solera y paredes del vaso", 69, "m²", [
    "Suministro del mortero impermeabilizante bicomponente semiflexible Morcem Dry SF Plus de Grupo Puma de la malla Drypool antialcalina de refuerzo y de la banda Bandtec para puntos críticos, según ficha técnica del sistema DryPool.",
    "Humectación del soporte y refuerzo de esquinas, juntas y puntos singulares.",
    "Aplicación en dos capas con malla entre ellas. Curado según las indicaciones del fabricante antes de pasar a la fase siguiente."]),
  ("4.2", "Suministro y aplicación del sistema DryPool en el canal desbordante", 27, "m²", [
    "Mismo sistema, en dos capas con malla, en el fondo y las paredes del canal, con refuerzo en el encuentro con el vaso y en la coronación."]),
  ("4.3", "Suministro y aplicación del sistema DryPool en banco y escalera", 9, "m²", [
    "Mismo sistema, en dos capas con malla, en el banco, los peldaños y los encuentros con el vaso."])]),
 ("5", "Revestimiento cerámico Rosa Gres", [
  ("5.1", "Suministro y colocación de cerámica Rosa Gres 31 × 62,6 cm en solera y paredes del vaso", 69, "m²", [
    "Porcelánico apto para inmersión permanente, con reserva por cortes y roturas (112 m² suministrados en total para toda la obra).",
    "Mortero-cola Pegoland Flex C2 TE S1 de Grupo Puma (sistema DryPool), con doble encolado.",
    "Replanteo de piezas y colocación, con cortes y remates en focos, boquillas, sumidero y esquinas."]),
  ("5.2", "Suministro y colocación de cerámica Rosa Gres 31 × 62,6 cm en el canal desbordante", 27, "m²", [
    "Misma cerámica y cemento cola, en el fondo y las paredes del canal, con las pendientes definidas en la fase 3."]),
  ("5.3", "Suministro y colocación de cerámica Rosa Gres 31 × 62,6 cm en banco y escalera", 9, "m²", [
    "Misma cerámica y cemento cola, en el banco y en huellas y contrahuellas de la escalera."]),
  ("5.4", "Suministro y colocación de piezas de peldaño y borde de banco Rosa Gres", 35, "ud", [
    "Piezas Rosa Gres antideslizantes L98 (97,8 × 31,7 × 3,8 cm) y L62 (62,6 × 31,7 × 3,8 cm), según despiece: forman la huella y el canto de los 6 peldaños (4 de 1,20 m y 2 más estrechos) y del borde del banco de 4,00 m × 40 cm, y dan agarre en zona mojada.",
    "Colocación con cortes y remates.",
    "No incluye piezas especiales (esquinas, piezas laterales y similares): se valoran aparte si el cliente las desea."])]),
 ("6", "Coronación y labio de rebose", [
  ("6.1", "Suministro y colocación nivelada de coronación y piezas de rebose", 37, "ml", [
    "Coronación para el borde de la piscina y el muro exterior del canal, con pieza de coronación estándar para los tramos de 7,50 m y 4,00 m del labio de rebose. No incluye piezas especiales de rebose ni de esquina: se valoran aparte si el cliente las desea.",
    "Modelo y acabado a confirmar por escrito, a juego con la cerámica Rosa Gres.",
    "Colocación de las piezas de los extremos a la cota del láser y del resto al hilo, con nivelación pieza a pieza y tolerancia máxima de ±2 mm."]),
  ("6.2", "Prueba de lámina de agua", 1, "PA", [
    "Antes de rejuntar, llenado hasta que la piscina desborda.",
    "Comprobación de que el agua cae de forma uniforme en toda la longitud del rebose.",
    "Corrección de cualquier punto que no desborde igual."])]),
 ("7", "Rejuntado y sellados", [
  ("7.1", "Suministro y aplicación de rejuntado de cerámica, peldaños y coronación", 105, "m²", [
    "Mortero de juntas epoxi Morcemcolor Epoxi RG/R2T de Grupo Puma, apto para piscinas con cloración salina (color a confirmar por escrito).",
    "Limpieza de restos de junta."]),
  ("7.2", "Juntas de dilatación y sellados elásticos perimetrales", 1, "PA", [
    "Sellado elástico en los encuentros y juntas de movimiento entre vaso, canal, escalera y coronación."])]),
 ("8", "Entrega", [
  ("8.1", "Limpieza final de obra", 1, "PA", [
    "Limpieza de acabados y de la zona de obra, y retirada de protecciones."]),
  ("8.2", "Revisión final y entrega de la obra", 1, "PA", [
    "Revisión de acabados con el cliente y acta de entrega."])]),
]

PROMO = ("Regalo promocional: cloración salina y pH automático", [
    "Equipo de cloración salina Bright Blue Pluma WP 15, con la célula de electrólisis instalada en bypass.",
    "Regulador de pH automático Sanus NG, con sonda, bomba peristáltica, punto de inyección y depósito.",
    "Suministro e instalación incluidos, sin ningún coste adicional. Puesta en marcha con la piscina llena, una vez realizado el llenado, y explicación del funcionamiento de los equipos.",
    "Garantía del fabricante: 5 años la electrónica y 4 años la célula del clorador; 2 años el regulador de pH.",
    "La instalación se realiza sobre la depuración existente, previa comprobación en la inspección inicial."])

e = html.escape
def n2(x): return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def eur(x): return n2(x) + " €"
def qty(x): return (f"{x:g}").replace(".", ",")

# ---------- cálculo ----------
# Reparto del precio cerrado: material a coste + mano de obra ponderada por importancia.
from costes_127 import pesos   # material a coste + mano de obra según importancia, ver costes_127.py
PESOS, _FACTOR_MO = pesos(DATOS["precio_cerrado"])
parcial = False
base = round(DATOS["precio_cerrado"], 2)
partidas = [x for _, _, ps in FASES for x in ps]
assert set(PESOS) == {x[0] for x in partidas}
_k = base / sum(PESOS.values())
PU, IMP = {}, {}
for c_, _, q_, _, _ in partidas:
    PU[c_] = round(PESOS[c_] * _k / q_, 2); IMP[c_] = round(PU[c_] * q_, 2)
_res = round(base - sum(IMP.values()), 2)          # ajuste de céntimos en la última partida PA
IMP["8.2"] = round(IMP["8.2"] + _res, 2); PU["8.2"] = IMP["8.2"]
assert abs(sum(IMP.values()) - base) < 0.005
sub = {f: round(sum(IMP[x[0]] for x in ps), 2) for f, _, ps in FASES}
iva_imp = round(base * DATOS["iva"] / 100, 2)
total = round(base + iva_imp, 2)

def pagos():
    out, acc = [], 0.0
    for i, (pct, txt) in enumerate(DATOS["pagos"]):
        im = round(total * pct / 100, 2) if i < len(DATOS["pagos"]) - 1 else round(total - acc, 2)
        acc += im; out.append((pct, txt, im))
    return out
PAGOS = pagos()
assert abs(sum(x[2] for x in PAGOS) - total) < 0.005 and sum(x[0] for x in DATOS["pagos"]) == 100

# ---------- piezas de página ----------
paginas = []
def pagina(titulo, cuerpo, intro=None):
    paginas.append((titulo, cuerpo, intro))

def head(titulo):
    return f'<div class="eyebrow">PRESUPUESTO {DATOS["numero"]}</div><h1>{e(titulo)}</h1>'

# 1 · carta
cifras_i = [("Dimensiones interiores", "7,50 × 4,00 m"), ("Superficie de lámina", "30 m²"),
            ("Profundidad", "1,70 m constante"), ("Volumen aprox.", "51 m³")]
cifras_d = [("Tipo", "Desbordante con canal en L"), ("Canal desbordante", "12,5 ml · 80 y 30 cm de ancho"),
            ("Banco y escalera", "Banco 4 m × 40 cm · 6 peldaños"), ("Revestimiento", "Rosa Gres 31 × 62,6 cm · ≈ 105 m²"),
            ("Impermeabilización", "Sistema DryPool · Grupo Puma"), ("Coronación", "Nueva · ≈ 37 ml")]
def kv(rows): return '<table class="kv">' + ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in rows) + '</table>'
pagina("Gracias por confiar en nosotros", f'''
<p>Estimado/a cliente:</p>
<p>Le presentamos nuestra propuesta para la rehabilitación integral de su piscina desbordante en {e(DATOS["direccion"])}. Este documento recoge, por escrito y con claridad, la obra: los trabajos, los materiales, los plazos, la forma de pago y las garantías.</p>
<p>La piscina pierde agua. Para resolverlo desde el origen retiraremos toda la cerámica, la coronación y la impermeabilización antiguas, saneamos el soporte e impermeabilizamos el vaso y el canal desbordante con el sistema DryPool de Grupo Puma, un mortero bicomponente semiflexible pensado para soportar la presión del agua. Después colocamos cerámica nueva Rosa Gres de 31 × 62,6 cm, piezas de peldaño antideslizantes en los bancos y la escalera, y una coronación nueva con el labio del desbordante perfectamente nivelado.</p>
<p>Reparación, impermeabilización, mortero-cola y juntas son de una misma marca, Grupo Puma: el sistema DryPool, específico para piscinas. El presupuesto incluye la cerámica, las piezas de coronación y los peldaños; las piezas especiales de Rosa Gres, de mayor coste, se valoran aparte si usted lo desea.</p>
<p>Cada fase se revisa antes de empezar la siguiente y le entregamos la obra terminada.</p>
<p>Quedamos a su disposición para resolver cualquier duda o ajustar la propuesta a lo que necesite.</p>
<p class="firma"><b>{e(DATOS["contacto"])}</b><br>Brava Pool</p>
<h2>Su piscina en cifras</h2><div class="cols">{kv(cifras_i)}{kv(cifras_d)}</div>
<div class="kv-wide">{kv([("Plazo estimado", "5 a 6 semanas desde el inicio de obra, a confirmar")])}</div>
<h2>Nuestro compromiso</h2>
<div class="cards">
<div><b>Plazos por escrito</b>Planificación por fases desde el primer día y plazo de ejecución indicado en este documento.</div>
<div><b>Pagos por hitos</b>Cada pago se vincula a una fase terminada y el 20 % final queda retenido hasta la entrega.</div>
<div><b>Garantía por escrito</b>3 años en el revestimiento y 2 años en los trabajos y la mano de obra, además de las garantías legales.</div>
<div><b>Obra limpia</b>Retiramos todos los escombros a un punto limpio autorizado y entregamos la piscina y su entorno limpios.</div>
<div><b>Regalo promocional</b>Cloración salina Bright Blue Pluma WP 15 con pH automático Sanus NG, instalada sin coste.</div></div>''')

fotos = [("foto_terraza.jpg", "Vista general desde la terraza", "Piscina desbordante en ladera, con vistas al valle, coronación de piezas de gran formato y rejilla lineal en el pavimento."),
         ("foto_planta.jpg", "Vaso completo", "Vaso rectangular con banco y escalera en el extremo, y revestimiento cerámico rectangular en el fondo."),
         ("foto_canal.jpg", "Canal de desbordamiento, exterior", "Canal perimetral junto al lado del valle, con su muro exterior y coronación."),
         ("foto_canal_interior.jpg", "Interior del canal", "Fondo y paredes revestidos, sumidero del canal, zonas húmedas en el fondo y manchas verdosas en la pared."),
         ("foto_escalera_banco.jpg", "Escalera y banco interior", "Escalera de acceso, banco, foco y boquilla de impulsión en pared."),
         ("foto_solera.jpg", "Fondo y sumidero", "Revestimiento cerámico rectangular y sumidero de fondo.")]
pagina("Estado actual de la piscina", f'''<p class="lead">Fotografías de la piscina antes de la obra. Sirven de referencia para el replanteo y para comprobar, al terminar, que se respeta su geometría y su aspecto.</p>
<div class="gal">{"".join(f'<figure><img src="assets/{f}" alt=""><figcaption><b>{e(t)}</b>{e(d)}</figcaption></figure>' for f,t,d in fotos)}</div>
<p class="note" style="margin-top:5mm">Fotografías del cliente tomadas antes de la intervención. Su estado real (fisuras, filtraciones, desprendimientos) se determina en la inspección técnica inicial.</p>''')

# 2 · plano
from plano_127 import planta_svg, secciones_svg
pagina("Plano de la piscina", f'''<p class="lead">Planta de la piscina deducida de sus fotografías: dónde rebosa el agua, el canal, el banco, la escalera y los elementos principales.</p>
<div class="plano">{planta_svg()}</div>
<table class="leyenda"><tr><td><b>Vaso</b></td><td>7,50 × 4,00 m · 1,70 m de profundidad · cerámica rectangular</td></tr><tr><td><b>Canal en L</b></td><td>12,5 ml · 80 cm de ancho en el lado largo (valle) y 30 cm en el lado corto (este)</td></tr><tr><td><b>Banco</b></td><td>4,00 m de largo por ≈ 40 cm de ancho, en todo el ancho del extremo oeste</td></tr><tr><td><b>Escalera</b></td><td>6 peldaños junto al banco, con acceso desde la terraza: los 4 primeros de 1,20 m y los 2 últimos más estrechos</td></tr><tr><td><b>Sumidero</b></td><td>1 de fondo y 1 en el canal</td></tr></table>
<p class="note">Plano orientativo, sin escala. Banco, escalera y aparatos en pared: posición y medidas a confirmar con el cliente en el replanteo.</p>''')

marks = [(1, 9.0, 36.0, "Canal del lado valle", "80 cm de ancho, con fondo y paredes cerámicos. El agua rebosa hacia él por el borde largo."),
         (2, 48.0, 14.3, "Canal del lado este", "30 cm de ancho. Aquí hay un ligero desnivel en el labio, que se regulariza en la obra."),
         (3, 37.3, 82.7, "Banco", "4,00 m de largo por unos 40 cm de ancho, a todo el ancho del extremo."),
         (4, 85.3, 69.0, "Escalera", "Los peldaños de arriba miden 1,20 m y los de abajo son más estrechos. Entrada desde un hueco de la coronación."),
         (5, 51.6, 38.1, "Sumidero de fondo", "Uno solo, en el centro del vaso."),
         (6, 87.6, 54.7, "Aparatos en pared", "Focos y boquillas del lado de la terraza."),
         (7, 93.0, 34.7, "Rejilla lineal", "En el pavimento de la terraza, junto a la piscina.")]
pagina("Su piscina sobre las fotos", f'''<p class="lead">Vista aérea de su piscina con los elementos que intervienen en la obra.</p>
<div class="ann"><div class="phw"><img src="assets/foto_planta.jpg" alt="">{"".join(f'<span class="pin" style="left:{x}%;top:{y}%">{n}</span>' for n,x,y,_,_ in marks)}</div>
<ol class="lg">{"".join(f'<li><span class="mk2">{n}</span><div><b>{e(t)}</b>{e(d)}</div></li>' for n,_,_,t,d in marks)}</ol></div>
<p class="note">Las marcas indican la zona aproximada de cada elemento. La posición y las medidas definitivas se confirman en el replanteo.</p>''')

pagina("Cómo desborda el agua", f'''<p class="lead">El agua rebosa por el borde del lado valle y cae a un canal de 80 cm. En el lado este el canal es más estrecho, de 30 cm, y el labio tiene un ligero desnivel que se corrige durante la obra.</p>
<div class="plano">{secciones_svg()}</div>
<p class="note">Secciones orientativas, sin escala. El desnivel está dibujado exagerado para que se aprecie; su valor real se mide con nivel láser antes de empezar (fases 1 y 3).</p>''')

# piezas Rosa Gres
piezas_inc = [("Baldosa de revestimiento", "serie del vaso (a confirmar)", "31 × 62,6 cm", "Solera, paredes del vaso y canal desbordante. Es la superficie principal de la piscina."),
              ("Peldaño-borde antideslizante", "L98", "97,8 × 31,7 × 3,8 cm", "Huella y canto de los peldaños anchos, y borde del banco. El acabado antideslizante da agarre en zona mojada."),
              ("Peldaño-borde antideslizante", "L62", "62,6 × 31,7 × 3,8 cm", "Peldaños más estrechos de la parte baja de la escalera."),
              ("Pieza de coronación", "modelo a confirmar", "—", "Borde de la piscina, labio de rebose y muro exterior del canal.")]
piezas_esp = [("Esquinas derecha / izquierda", "ED9 / EI9", "97,8 × 31,7 × 3,8 cm", "Remate de los extremos de peldaños y banco, donde el borde gira."),
              ("Borde desbordante", "647", "62,6 × 31 × 2,6 cm", "Pieza especial para el labio de rebose de los lados valle y este."),
              ("Otras piezas especiales", "según catálogo", "—", "Piezas laterales de peldaño y remates especiales, si el diseño las requiere.")]
def tabla_piezas(rows):
    return '<table class="eco ph"><thead><tr><th style="width:44mm">Pieza</th><th style="width:25mm">Referencia</th><th style="width:34mm">Medida</th><th>Dónde y para qué</th></tr></thead><tbody>' + ''.join(f'<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a,b,c,d in rows) + '</tbody></table>'
pagina("Piezas Rosa Gres de su piscina", f'''<p class="lead">Una piscina así no se reviste con un solo tipo de pieza. Cada zona lleva la suya, y todas son de Rosa Gres para que el conjunto tenga el mismo color y acabado.</p>
<h2>Incluidas en el presupuesto</h2>{tabla_piezas(piezas_inc)}
<h2>Piezas especiales · no incluidas</h2>{tabla_piezas(piezas_esp)}
<div class="box"><b>Piezas especiales.</b> Por ser piezas de mayor coste, no están incluidas en el precio. Se valorarán aparte, con su presupuesto independiente, si el cliente desea incorporarlas.</div>
<h3>Cómo se reparten en su piscina</h3>
<ul><li><b>Escalera:</b> 6 peldaños. Los 4 primeros miden 1,20 m y los 2 últimos son más estrechos, por lo que se combinan piezas de distinta anchura.</li><li><b>Banco:</b> 4,00 m de largo por unos 40 cm de ancho, en todo el ancho del extremo oeste.</li><li><b>Canal:</b> 80 cm de ancho en el lado valle y 30 cm en el lado este, revestido con la misma baldosa del vaso.</li></ul>
<p class="note">Las referencias proceden del catálogo de piscinas de Rosa Gres y de distribuidores. La combinación exacta de piezas, la cantidad de cada una, la serie y el color se fijan con el despiece, antes del pedido.</p>''')

# 3 · sistema constructivo y materiales
capas = [("Soporte saneado y reparado (Morcemseal Todo 1 R4)", "#d9d4cb", "#2b3440"), ("Impermeabilización DryPool · 1.ª capa", "#2e6f9e", "#fff"),
         ("Malla antialcalina de refuerzo", "#7fb6d3", "#0a2540"), ("Impermeabilización DryPool · 2.ª capa", "#2e6f9e", "#fff"),
         ("Mortero-cola Pegoland Flex C2 TE S1 (Puma)", "#b9c2cc", "#0a2540"), ("Cerámica Rosa Gres 31 × 62,6 cm", "#e9eef3", "#0a2540"),
         ("Junta Morcemcolor Epoxi RG/R2T (Puma)", "#8a97a5", "#fff")]
capas_svg = '<svg viewBox="0 0 640 250" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">' + ''.join(
    f'<rect x="20" y="{10 + i * 33}" width="600" height="29" fill="{c}" stroke="#fff"/><text x="40" y="{29 + i * 33}" font-size="12.5" fill="{t}" font-weight="600">{i + 1}.  {e(n)}</text>' for i, (n, c, t) in enumerate(capas)) + '<text x="610" y="245" text-anchor="end" font-size="10" fill="#5b6b7b">Esquema de capas, de dentro hacia el agua · sin escala</text></svg>'
mats = [("Reparación del soporte", "Grupo Puma", "Morcemseal Todo 1 R4 · mortero tixotrópico de alta resistencia"),
        ("Impermeabilización", "Grupo Puma", "Sistema DryPool · Morcem Dry SF Plus, malla Drypool y banda Bandtec"),
        ("Revestimiento", "Rosa Gres", "Porcelánico 31 × 62,6 cm apto para inmersión (modelo y color a confirmar)"),
        ("Bancos y escalera", "Rosa Gres", "Peldaño-borde antideslizante L98 y L62 (ver página de piezas; color a confirmar)"),
        ("Mortero-cola", "Grupo Puma", "Pegoland Flex C2 TE S1 (sistema DryPool)"),
        ("Rejuntado", "Grupo Puma", "Morcemcolor Epoxi RG/R2T, apto para piscinas con cloración salina (color a confirmar)"),
        ("Coronación", "Por definir", "Modelo y acabado a confirmar por escrito"),
        ("Cloración salina (regalo)", "Bright Blue", "Pluma WP 15 con regulador de pH automático Sanus NG")]
pagina("Sistema constructivo y materiales", f'''<p class="lead">La estanqueidad de una piscina depende del conjunto de capas, no de un solo producto. Este es el sistema previsto y su orden de ejecución.</p>
<div class="plano">{capas_svg}</div>
<h2>Materiales y marcas</h2>
<table class="eco ph"><thead><tr><th style="width:38mm">Elemento</th><th style="width:28mm">Marca</th><th>Detalle</th></tr></thead><tbody>{"".join(f'<tr><td>{e(a)}</td><td><b class="mk">{e(b)}</b></td><td>{e(c)}</td></tr>' for a,b,c in mats)}</tbody></table>
<p class="note">Los productos se aplican según las fichas técnicas vigentes de cada fabricante. Cualquier cambio de referencia se comunica al cliente por escrito antes del pedido.</p>''')

# 4 · planificación
sem = 12  # medias semanas
gantt = [("Fase 1 · Inspección, referencias y vaciado", 1, 1, ""), ("Fase 2 · Demoliciones", 2, 3, ""), ("Fase 3 · Reparación y preparación del soporte", 5, 1, ""),
         ("Fase 4 · Impermeabilización DryPool y curado", 6, 1, "cur"), ("Fase 5 · Revestimiento cerámico", 8, 2, ""), ("Fase 6 · Coronación y labio de rebose", 10, 1, ""),
         ("Fase 7 · Rejuntado", 11, 1, ""), ("Fase 8 · Entrega", 12, 1, "")]
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
pagos_tabla = ''.join(f'<tr><td class="pc">{pct} %</td><td>{e(txt)}</td><td class="n">{eur(im)}</td></tr>' for pct, txt, im in PAGOS)
pagina("Planificación de la obra", f'''<p class="lead">Plazo total estimado: 5 a 6 semanas desde el inicio de obra, a confirmar tras la inspección inicial. Cada fase se verifica antes de empezar la siguiente.</p>
<table class="gt"><thead><tr><th style="width:62mm">Fase</th><th><div class="wk">{wk}</div></th></tr></thead><tbody>{rows}
<tr class="pg"><td>Pagos</td><td class="gc"><div>{pagos_row}</div></td></tr></tbody></table>
<p class="note"><span class="sw"></span> Tiempo de curado del mortero según ficha técnica del fabricante. Planificación orientativa: puede variar según el tipo de terreno, la meteorología y la entrega de materiales; cualquier cambio se comunicará con antelación.</p>
<h2>Forma de pago</h2>
<table class="eco"><thead><tr><th style="width:16mm">Pago</th><th>Hito</th><th style="width:34mm;text-align:right">Importe con IVA</th></tr></thead><tbody>{pagos_tabla}</tbody></table>
<p class="note">Forma de pago: transferencia bancaria a nombre de Brava Pool.{" Los importes se calcularán al cerrar la valoración completa." if parcial else ""}</p>''')

# 5 · descripción de trabajos (se pagina a mano por fases)
def fase_html(f, titulo, ps):
    r = f'<tr class="fase"><td colspan="4"><span>{int(f):02d}</span>FASE {f} · {e(titulo).upper()}</td><td></td><td class="n">{eur(sub[f])}</td></tr>'
    for c, t, q, u, b in ps:
        lis = ''.join(f'<li>{e(x)}</li>' for x in b)
        r += f'<tr class="pt"><td class="cod">{c}</td><td><b>{e(t)}</b><ul>{lis}</ul></td><td class="n">{qty(q)}</td><td class="c">{u}</td><td class="n">{n2(PU[c])} €</td><td class="n"><b>{n2(IMP[c])} €</b></td></tr>'
    return r
cab = '<thead><tr><th style="width:9mm">Nº</th><th>Descripción</th><th style="width:13mm">Cant.</th><th style="width:11mm">Ud.</th><th style="width:21mm">Precio</th><th style="width:24mm">Importe</th></tr></thead>'
grupos = [["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"]]
fdict = {f: (t, ps) for f, t, ps in FASES}
for gi, g in enumerate(grupos):
    body = ''.join(fase_html(f, *fdict[f]) for f in g)
    if gi == len(grupos) - 1:
        body += f'<tr class="fase promo"><td colspan="6"><span>+</span>PROMOCIÓN</td></tr><tr class="pt"><td class="cod">R.1</td><td><b>{e(PROMO[0])}</b><ul>{''.join(f'<li>{e(x)}</li>' for x in PROMO[1])}</ul></td><td class="n">1</td><td class="c">ud</td><td class="n">—</td><td class="n"><b>REGALO</b></td></tr>'
    pagina("Descripción de los trabajos" + ("" if gi == 0 else " (cont.)"), f'<table class="desc">{cab}<tbody>{body}</tbody></table>' + ('<p class="note">PA = partida alzada. Las mediciones son estimadas y se ajustan con las medidas tomadas en obra. El precio total es cerrado e incluye materiales y mano de obra. El reparto por partidas es orientativo.</p>' if gi == len(grupos) - 1 else ''))

# 6 · resumen
res = ''.join(f'<tr><td class="rn">{int(f):02d}</td><td>Fase {f} · {e(t)}</td><td class="n">{eur(sub[f])}</td></tr>' for f, t, _ in FASES)
pagina("Resumen de la inversión", f'''<p class="lead">Precio cerrado con todos los materiales, la mano de obra, el transporte y la retirada de escombros incluidos.</p>
<table class="eco res"><thead><tr><th style="width:14mm">Cap.</th><th>Concepto</th><th style="width:34mm;text-align:right">Importe</th></tr></thead><tbody>{res}
<tr><td class="rn">+</td><td>{e(PROMO[0])}</td><td class="n">Regalo</td></tr>
<tr class="sub"><td colspan="2">Base imponible</td><td class="n">{eur(base)}</td></tr>
<tr><td colspan="2">IVA {DATOS["iva"]} %</td><td class="n">{eur(iva_imp)}</td></tr>
<tr class="tot"><td colspan="2">Total presupuesto (IVA incl.)</td><td class="n">{eur(total)}</td></tr></tbody></table>
<p class="note">Precio total cerrado. El reparto entre fases y partidas es orientativo y no modifica el total. Incluye cerámica, piezas de coronación y peldaños; no incluye piezas especiales, que se valoran aparte si el cliente las desea.</p>
<div class="box"><b>Promoción.</b> Con este presupuesto, Brava Pool regala el equipo de cloración salina Bright Blue Pluma WP 15 con regulador de pH automático Sanus NG, instalado y sin ningún coste adicional.</div>
<p class="note">El tipo de IVA aplicable depende de las condiciones de la vivienda y de la obra; se confirma al cerrar el presupuesto.</p>''')

# 7 · garantías
cl = [("Garantía en todos nuestros trabajos", ["Al tratarse de una reforma, Brava Pool garantiza el nuevo revestimiento durante 3 años y todos los trabajos realizados y la mano de obra durante 2 años. Estas garantías comerciales se suman a las garantías legales que correspondan según la normativa vigente.", "El servicio técnico y las reparaciones en garantía se atienden durante todo el año, sin limitación de temporada. Ante cualquier incidencia comunicada por teléfono, WhatsApp o correo electrónico, respondemos por escrito en un plazo máximo de 48 horas."]),
      ("Control de calidad en cada fase", ["Revisamos y fotografiamos el soporte tras la demolición, la continuidad de la impermeabilización y los puntos singulares, la colocación y el rejuntado de la cerámica. Antes de la entrega hacemos una revisión final de acabados con el cliente."]),
      ("Compromiso de obra limpia", ["El precio incluye la retirada de todos los escombros de la obra, su transporte y su depósito en un punto limpio autorizado.", "Durante la obra protegemos las zonas de paso y el jardín, y al terminar retiramos todos los restos de material para entregar la piscina y su entorno limpios."]),
      ("Pagos por hitos y retención final", ["Los pagos se vinculan al avance de la obra: el primero reserva la obra y el pedido de materiales y los siguientes se abonan al terminar cada hito indicado. El último 20 % queda retenido hasta la entrega de la obra terminada."])]
pagina("Garantías y compromisos", ''.join(f'<div class="clau"><span>CLÁUSULA {i+1}</span><h3>{e(t)}</h3>{"".join(f"<p>{e(x)}</p>" for x in ps)}</div>' for i, (t, ps) in enumerate(cl)))

# 8 · condiciones y aceptación
noinc = ["Piezas especiales de Rosa Gres (esquinas, piezas laterales y de borde desbordante): se valoran aparte si el cliente las desea, por ser piezas de mayor coste.", "Reparación de daños estructurales, tuberías o pasamuros ocultos que aparezcan al desmontar (se presupuestarán aparte).", "Equipos de filtración y depuración, salvo el equipo de sal de la promoción.", "Pavimento exterior de la terraza, salvo las piezas colindantes que sea imprescindible levantar y reponer (se valoran tras la inspección).", "Prueba de estanqueidad y llenado, agua para el llenado y productos químicos de puesta en marcha.", "Licencia o permiso de obra y tasas municipales, si fueran necesarios."]
cond = ["Cualquier trabajo no descrito en este presupuesto se presupuestará aparte y por escrito antes de realizarlo.", "El modelo y el color de la cerámica, de la coronación y de las juntas se confirmarán por escrito antes de su pedido.", "Las mediciones son estimadas y se ajustarán con las medidas tomadas en obra.", "El cliente facilitará el acceso a la obra y el suministro de agua y luz durante los trabajos.", f'Este presupuesto es válido hasta el {DATOS["valido_hasta"]}.']
imp_acept = f'por un importe total de <b>{eur(total)}</b> IVA incluido' if not parcial else 'por el importe total que se fije en la valoración definitiva: <i class="blk"></i> (IVA incl.)'
pagina("Condiciones y aceptación", f'''<div class="cols2"><div><h2>No incluye</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in noinc)}</ul></div><div><h2>Condiciones</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in cond)}</ul></div></div>
<div class="acc"><h3>Aceptación del presupuesto</h3><p>El cliente declara conocer y aceptar el presente presupuesto n.º {DATOS["numero"]}, {imp_acept}, sus condiciones y la forma de pago indicada.</p>
<div class="sig"><div><div class="line"></div><small>Nombre y apellidos</small><div class="line"></div><small>DNI / NIF</small><div class="line"></div><small>Lugar y fecha</small></div><div><div class="line big"></div><small>Firma del cliente</small><div class="line big"></div><small>Por Brava Pool</small></div></div></div>
<div class="duda"><b>¿Alguna duda?</b> {e(DATOS["contacto"])} · {e(DATOS["web"])}{(" · " + e(DATOS["telefono"])) if DATOS["telefono"] else ""}{(" · " + e(DATOS["email"])) if DATOS["email"] else ""}</div>''')

if MUESTRA:
    def lista(items): return '<ul class="rv">' + ''.join(f'<li><b>{e(t)}</b>{e(d)}</li>' for t, d in items) + '</ul>'
    pagina("Resumen de revisión · fallos corregidos", f'''<p class="lead">Fallos detectados en el presupuesto original y cómo se han corregido en esta versión.</p>
<h2>Importes y precio</h2>{lista([
("Total sin base real. ", "El original ponía 8.768,70 € como «precio cerrado» con solo 3 de 24 partidas valoradas. Ahora: 22.578,00 € sin IVA repartidos en 24 partidas."),
("Reparto sin criterio. ", "Ahora cada partida lleva su material a coste y la mano de obra se reparte según su importancia, con datos del generador de precios CYPE. Los peldaños no bajan de su precio de compra."),
("DryPool mal calculado. ", "10 sacos eran unos 1,9 kg/m²; la ficha indica 4,4 kg/m² (unos 24 sacos de 20 kg)."),
("Reserva de cerámica corta. ", "112 m² sobre 105 m² (6,7 %); con formato grande suele hacer falta más."),
("IVA sin comprobar. ", "Se mantiene el 21 %; el 10 % de rehabilitación exige que los materiales sean menos del 40 % de la base.")])}
<h2>Materiales</h2>{lista([
("Producto no verificable. ", "«Morcem Dry F» no consta; el mortero del sistema DryPool es Morcem Dry SF Plus."),
("Sistema incompleto. ", "Ahora es el sistema DryPool de Grupo Puma completo: Morcemseal Todo 1 R4, Morcem Dry SF Plus, malla Drypool, Bandtec, Pegoland Flex C2 TE S1 y Morcemcolor Epoxi."),
("Marcas mal puestas. ", "«C2TE S1» es una clase, no una marca; la coronación figuraba como «A juego»."),
("Formato de cerámica. ", "30 × 60 cm no es el de la serie de piscina; es 31 × 62,6 cm."),
("Peldaño sin referencia. ", "Ahora L98 y L62 con esquinas ED9/EI9, y borde desbordante ref. 647 (a confirmar).")])}
<h2>Geometría y diseño</h2>{lista([
("Banco de 7,50 m inexistente. ", "Es un banco de 4,00 m de largo por unos 40 cm de ancho."),
("Canal mal descrito. ", "«Paredes de 80 cm» era en realidad 80 cm de ancho en el lado valle y 30 cm en el lado este."),
("Escalera. ", "6 peldaños: los 4 primeros de 1,20 m y los 2 últimos más estrechos."),
("Ligero desnivel del lado este. ", "No estaba recogido; ahora hay sección y texto, y se corrige en la obra con nivel láser."),
("Plano genérico y leyenda errónea. ", "«Banco interior: 1» con dos bancos; ahora hay planta, foto aérea anotada y secciones.")])}''')
    pagina("Resumen de revisión · forma y pendiente", f'''<h2>Redacción y presentación</h2>{lista([
("Página de equipos errónea. ", "Decía «0 skimmers» y «0 boquillas» y describía equipos excluidos; la piscina es desbordante. Eliminada."),
("Datos erróneos. ", "«Profundidad de 1,70 a 1,70 m» y cifras duplicadas."),
("Plazo y cronograma. ", "«Plazo de Orientativo 5 a 6 semanas»; rejuntado y llenado coincidían en la misma semana."),
("Pagos contradictorios. ", "«Nunca adelanta más de lo que ya puede ver construido» frente a un 20 % a la aceptación. Reescrito por hitos."),
("Prueba de llenado. ", "Quitada, y eliminadas las frases de «piscina llena y funcionando»."),
("Forma. ", "Cliente genérico, contacto vacío, numeración desfasada y páginas casi vacías. Portada de marca en lugar de foto de archivo."),
("Terraza. ", "Faltaban el mobiliario y la rejilla lineal y el pavimento colindante, ahora como partida condicionada.")])}
<h2>Pendiente de confirmar</h2>{lista([
("Escalera y banco. ", "Anchos exactos de los 2 peldaños estrechos y ancho real del banco (≈ 40 cm)."),
("Aparatos en pared. ", "Número y posición de focos y boquillas; altura de las paredes del canal."),
("Piezas Rosa Gres. ", "Combinación exacta, serie, color y número de piezas de peldaño (el presupuesto lleva 35; el despiece indica unas 20)."),
("Coronación. ", "Precio y modelo reales; el reparto usa 60 €/ml como supuesto."),
("Piezas especiales. ", "Esquinas, borde desbordante y otras piezas especiales de Rosa Gres no están incluidas; se valoran aparte si el cliente las quiere."),
("Equipo de sal. ", "Modelo definitivo y que se instala sobre la depuración existente."),
("Junta. ", "Epoxi propuesto (apto para cloración salina) y color."),
("Cliente. ", "Nombre, teléfono, datos de pago e IVA aplicable.")])}''')

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
h2{font-size:7.8pt;letter-spacing:.18em;text-transform:uppercase;color:var(--navy);margin:4.5mm 0 1.5mm;font-weight:700}
h3{font-size:10.5pt;color:var(--navy);margin:0 0 1.5mm}
.body{position:absolute;top:40mm;bottom:17mm;left:16mm;right:16mm}
.page>footer{position:absolute;bottom:8mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:7pt;color:var(--mut)}
p{margin:0 0 2.6mm}ul{margin:0;padding-left:4mm}li{margin-bottom:.6mm}
.lead{font-size:10pt;color:var(--ink)}.note{font-size:7.6pt;color:var(--mut)}.firma{margin-top:4mm}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm}.cols2{display:grid;grid-template-columns:1fr 1fr;gap:9mm}.cols2 h2{margin-top:0}
.kv{width:100%;border-collapse:collapse;font-size:8.6pt}.kv td{padding:1.3mm 0;border-bottom:.2mm solid var(--ln);vertical-align:top}.kv td:first-child{color:var(--mut);width:40%}.kv td:last-child{text-align:right;font-weight:600;color:var(--ink)}
.kv-wide{margin-top:1mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm}.cards div{background:var(--bg);border-top:.7mm solid var(--cy);padding:2.2mm 3.5mm;font-size:8.1pt}.cards b{display:block;color:var(--navy);font-size:9pt;margin-bottom:.8mm}
.gal{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.gal figure{margin:0}.gal img{width:100%;height:52mm;object-fit:cover;display:block}.gal figcaption{font-size:7.8pt;color:#44505d;padding:1.5mm 0 0;line-height:1.35}.gal b{display:block;color:var(--navy);font-size:8.6pt}
.ann{display:grid;grid-template-columns:82mm 1fr;gap:7mm;margin-top:3mm}.phw{position:relative}.phw img{width:100%;display:block}.pin{position:absolute;transform:translate(-50%,-50%);width:6.4mm;height:6.4mm;border-radius:50%;background:#1f4e79;color:#fff;border:.45mm solid #fff;font-size:8pt;font-weight:700;display:flex;align-items:center;justify-content:center;box-shadow:0 .3mm 1mm rgba(0,0,0,.4)}.lg{margin:0;padding:0;list-style:none}.lg li{display:flex;gap:3mm;margin-bottom:4mm;font-size:8.6pt}.lg b{display:block;color:var(--navy);font-size:9.4pt}.mk2{flex:none;width:6.4mm;height:6.4mm;border-radius:50%;background:#1f4e79;color:#fff;font-size:8pt;font-weight:700;display:flex;align-items:center;justify-content:center}
.plano{border:.25mm solid var(--ln);padding:3mm;margin:3mm 0}.plano svg{width:100%;height:auto;display:block}
.leyenda{width:100%;border-collapse:collapse;font-size:8.4pt;margin:3mm 0}.leyenda td{padding:1.4mm 0;border-bottom:.2mm solid var(--ln)}.leyenda td:first-child{width:38mm;color:var(--navy)}
table{border-collapse:collapse;width:100%}
.eco{font-size:8.4pt}.eco th{text-align:left;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);padding:2mm 1.5mm;border-bottom:.35mm solid var(--navy);border-top:.35mm solid var(--navy)}
.eco td{padding:2.2mm 1.5mm;border-bottom:.2mm solid var(--ln);vertical-align:top}.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}.c{text-align:center}
.mk{color:var(--navy)}.pc{color:var(--cy);font-weight:700}
.res .rn{color:var(--cy);font-weight:700}.res td{padding:2.6mm 1.5mm}.sub td{font-weight:600;background:var(--bg)}.tot td{background:var(--navy);color:#fff;font-weight:700;font-size:10.5pt;padding:3.4mm 3mm}
.alert{border-left:1.2mm solid #c9822b;background:#fbf3e6;padding:3mm 4mm;margin-bottom:5mm;font-size:8.8pt;color:#5a3d0f}
.desc{font-size:8.2pt}.desc th{text-align:left;font-size:6.8pt;letter-spacing:.12em;color:var(--mut);padding:1.5mm 1mm;border-bottom:.35mm solid var(--ln)}
.desc td{padding:1.8mm 1mm;vertical-align:top}.desc .fase td.n{text-align:right}.desc .fase td{background:var(--navy);color:#fff;font-weight:700;letter-spacing:.06em;padding:2.2mm 2.5mm;font-size:7.8pt}.desc .fase td.n{font-size:8.4pt}
.desc .fase.promo td{background:#c9822b}.desc .fase span{color:#8fd0e8;margin-right:3mm}.desc .pt td{border-bottom:.2mm solid var(--ln)}.desc .cod{color:var(--mut)}
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
CSS += ".rv{list-style:none;padding:0;margin:0 0 2mm;font-size:8.4pt}.rv li{padding:1.6mm 0;border-bottom:.2mm solid var(--ln)}.rv b{color:var(--navy)}\n"
if MUESTRA:
    CSS += ".page::before{content:'MUESTRA';position:absolute;top:118mm;left:0;right:0;text-align:center;font-size:110pt;font-weight:800;letter-spacing:.12em;color:rgba(31,78,121,.07);transform:rotate(-30deg);z-index:50;pointer-events:none}\n"
doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Presupuesto {DATOS["numero"]} · Brava Pool</title><style>{CSS}</style></head><body>{portada}{corpo}</body></html>'
oh, op = (AQUI / "presupuesto_127_muestra.html", AQUI / "Presupuesto_127_MUESTRA.pdf") if MUESTRA else (AQUI / "presupuesto_127.html", AQUI / "presupuesto_127.pdf")
oh.write_text(doc, encoding="utf-8")
chrome = next((p for p in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(p).exists() or subprocess.call(["which", p], stdout=subprocess.DEVNULL) == 0), None)
if not chrome:
    sys.exit("HTML generado; ábralo en Chrome e imprima a PDF (A4, sin márgenes, gráficos de fondo).")
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={op}", oh.as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", op, "| base", eur(base), "| IVA", eur(iva_imp), "| total", eur(total), "|", N, "páginas")
