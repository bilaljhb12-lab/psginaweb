#!/usr/bin/env python3
"""Presupuesto 129 · Brava Pool · Piscina de obra 6 × 2,5 m · Joan Carles (Platja d'Aro). Catalán.

Uso: python3 presupuesto_129.py -> Presupuesto_129_Joan_Carles_Platja_dAro.pdf
Rehecho a partir del presupuesto 128 enviado a Joan Carles; mismo precio y reparto por capítulos.
"""
import ast, html, subprocess
from pathlib import Path
AQUI = Path(__file__).parent
e = html.escape
def eur(x): return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

# CSS «Carta de obra» compartido con presupuesto_certis.py (mismo diseño)
_src = ast.parse((AQUI / "presupuesto_certis.py").read_text(encoding="utf-8"))
_css = [ast.literal_eval(n.value) for n in _src.body if (isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CSS")]
_aug = [ast.literal_eval(n.value) for n in ast.walk(_src) if isinstance(n, ast.AugAssign) and getattr(n.target, "id", "") == "CSS"]
CSS = _css[0] + _aug[0]

D = {"numero": "129", "fecha": "24/10/2026", "valido": "23/11/2026", "cliente": "Joan Carles", "lugar": "Platja d'Aro (Girona)",
     "emisor": "Bilal El Jouhari El Bahraoui", "nif": "42366327M", "dir": "C/ Hernán Cortés 5 · Sant Feliu de Guíxols",
     "tel": "692 490 066", "web": "www.bravapool.com", "banco": "CaixaBank (La Caixa)", "iban": "ES49 2100 0597 1701 0079 4886"}
BASE = 18068.34
# (capítulo, título, [(código, título, cant, ud, importe, [viñetas])]) · importes cerrados del presupuesto original
T = [
 ("1", "Construcció del vas", [("1.1", "Construcció del vas de la piscina de 6 × 2,5 m, profunditat 1,20 / 1,60 m", 1, "ut", 7932.00, [
     "Col·locació de totxana per formar el perímetre de la piscina com a encofrat perdut.",
     "Armat del vas amb malles electrosoldades 15 × 15 Ø 5, barres Ø 10 i Ø 8 i cèrcols de 8 × 11 Ø 8.",
     "Formigó projectat (gunita) per via humida, amb una dosificació de 450 kg/m³, amb un gruix aproximat de 15 cm a les parets i 20 cm a la llosa, amb acabat rugós."])]),
 ("2", "Escala i banc d'obra", [("2.1", "Construcció d'escala interior i banc", 1, "ut", 921.00, [
     "Esglaonat d'escala recta de 5 graons i una bancada per al vas, fets amb encofrat perdut de totxana i reblerts amb graves.",
     "Es deixa tot a punt per a la col·locació del revestiment."])]),
 ("3", "Impermeabilització", [("3.1", "Impermeabilització del vas", 1, "PA", 1090.00, [
     "Impermeabilització amb morter flexible monocomponent Grupo Puma Morcem Dry Fix, de 3 mm de gruix, aplicat en capes i armat amb malla Drypool.",
     "Tractament dels punts singulars (mitges canyes, encontres i juntes) abans de l'aplicació."])]),
 ("4", "Revestiment i coronament", [("4.1", "Subministrament i col·locació del revestiment i del coronament", 1, "PA", 5710.00, [
     "Revestiment ceràmic de Cerámicas Mayor o Rosa Gres, a escollir pel client, col·locat amb ciment cola flexible Pegoland Profesional Flex C2 TE S1 i rejuntat específic per a piscines.",
     "Inclou el coronament perimetral de la mateixa gamma."])]),
 ("5", "Filtració, tractament de l'aigua i posada en marxa", [("5.1", "Subministrament i instal·lació de l'equip de filtració i tractament", 1, "PA", 2415.34, [
     "Filtre AstralPool 500 amb vàlvula selectora.",
     "Electrobomba AstralPool de 0,75 CV monofàsica, amb prefiltre.",
     "Quadre elèctric.",
     "Equip d'electròlisi salina Bright Blue, amb cèl·lula electrolítica.",
     "Controlador automàtic de pH, amb sonda i bomba dosificadora.",
     "3 broquets d'impulsió, 1 sumider de fons, 1 presa de netejafons i 1 skimmer.",
     "2 focus LED.",
     "Productes per al tractament de l'aigua i la posada a punt: clor, sal i corrector de pH."])]),
]
SUB = {f: round(sum(p[4] for p in ps), 2) for f, _, ps in T}
assert abs(sum(SUB.values()) - BASE) < .005
SIN_PRECIO = {"5"}   # el capítulo 5 muestra solo el total

PAGOS = [(20, "A l'acceptació del pressupost"), (30, "En acabar el vas i la gunita"), (30, "En acabar el revestiment i el coronament"), (20, "En acabar l'obra, amb la piscina plena i funcionant (retenció final)")]
pg = []; acc = 0.0
for i, (pct, t) in enumerate(PAGOS):
    im = round(BASE * pct / 100, 2) if i < len(PAGOS) - 1 else round(BASE - acc, 2); acc += im; pg.append((pct, t, im))
assert abs(sum(x[2] for x in pg) - BASE) < .005

NOINC = ["Projecte tècnic bàsic i executiu i direcció d'obra.", "Tràmits administratius, llicències i permisos d'ocupació de via.", "Gestió de runes i notificació d'obra.", "Pla de seguretat i salut i el seu seguiment.",
         "Excavació, preparació i neteja del terreny, rases per a canonades, reblert del perímetre del vas i de les rases, retirada de terres i anivellament del terreny.", "Reblert amb grava al voltant de la piscina (es valora a part).", "Aigua per a l'ompliment de la piscina."]
COND = ["Els preus d'aquest pressupost no inclouen l'IVA, que s'aplicarà a la factura al tipus vigent.", "Qualsevol treball no descrit en aquest pressupost es pressupostarà a part i per escrit abans de fer-lo.",
        "El model i el color del revestiment i del coronament es confirmaran per escrit abans de la comanda.", "El client facilitarà l'accés a l'obra i el subministrament d'aigua i llum durant els treballs.",
        "Les mides i la posició dels elements es confirmen amb el client en el replantejament.", f"Aquest pressupost és vàlid fins al {D['valido']}."]

n2 = lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
NP = 9
EXC = 2100.00   # importe (sin IVA) de la excavación si la hace Brava Pool
ftt = lambda n: f'<footer><span>Brava Pool · {e(D["emisor"])} · NIF {e(D["nif"])}</span><span class="fol"><b>{n:02d}</b> / {NP:02d} · Pressupost {D["numero"]}</span></footer>'
hdt = lambda t: f'<div class="rail">PRESSUPOST {D["numero"]} · PISCINA D\'OBRA 6 × 2,5 M · PLATJA D\'ARO</div><header><div><div class="eyebrow"><span>CONSTRUCCIÓ DE PISCINES</span><span>BRAVA POOL</span></div><h1>{e(t)}</h1></div><img src="assets/logo.png" alt="Brava Pool"></header>'
pps = ''.join(f'<div class="pp"><b>{p_} %</b><i>{eur(im)}</i><span>{e(t)}</span></div>' for p_, t, im in pg)

def fase(f, t, ps):
    r = f'<tr class="fase"><td colspan="4"><span>{int(f):02d}</span>{e(t).upper()}</td><td></td><td class="nn">{eur(SUB[f])}</td></tr>'
    for c, tt, q, u, im, b in ps:
        hide = f in SIN_PRECIO
        r += f'<tr class="pt"><td class="cod">{c}</td><td><b>{e(tt)}</b><ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></td><td class="nn">{q}</td><td class="c">{u}</td><td class="nn">{"—" if hide else n2(im) + " €"}</td><td class="nn"><b>{"Inclòs" if hide else n2(im) + " €"}</b></td></tr>'
    return r
cab = '<thead><tr><th style="width:9mm">Núm.</th><th>Descripció</th><th style="width:13mm">Quant.</th><th style="width:11mm">Ut.</th><th style="width:22mm">Preu</th><th style="width:24mm">Import</th></tr></thead>'
desc = ''.join(fase(f, t, ps) for f, t, ps in T)
res = ''.join(f'<tr><td class="c2">{f}</td><td>{e(t)}</td><td class="nn">{eur(SUB[f])}</td></tr>' for f, t, _ in T)

# ---- plano (planta + sección) en SVG ----
K = 80  # px por metro
x0, y0 = 70, 40; W, H = 6 * K, 2.5 * K
planta = f'''<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif" font-size="11">
<rect x="{x0-22}" y="{y0-22}" width="{W+44}" height="{H+44}" fill="#e9eef1" stroke="#0b2a45" stroke-width="1"/>
<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="#dff0f5" stroke="#0b2a45" stroke-width="2"/>
<g fill="#c4e1ea" stroke="#0b2a45" stroke-width=".8"><rect x="{x0+0}" y="{y0}" width="20" height="96"/><rect x="{x0+20}" y="{y0}" width="20" height="96"/><rect x="{x0+40}" y="{y0}" width="20" height="96"/><rect x="{x0+60}" y="{y0}" width="20" height="96"/><rect x="{x0+80}" y="{y0}" width="20" height="96"/><rect x="{x0}" y="{y0+96}" width="32" height="{H-96}"/></g>
<text x="{x0+50}" y="{y0+52}" text-anchor="middle" fill="#0b2a45" font-weight="700">E</text><text x="{x0+16}" y="{y0+150}" text-anchor="middle" fill="#0b2a45" font-weight="700">B</text>
<line x1="{x0}" y1="{y0-30}" x2="{x0+W}" y2="{y0-30}" stroke="#0b2a45"/><text x="{x0+W/2}" y="{y0-34}" text-anchor="middle" font-weight="700" fill="#0b2a45">6,00 m</text>
<text x="{x0-30}" y="{y0+H/2}" transform="rotate(-90 {x0-30} {y0+H/2})" text-anchor="middle" font-weight="700" fill="#0b2a45">2,50 m</text>
<line x1="{x0+150}" y1="{y0+100}" x2="{x0+300}" y2="{y0+100}" stroke="#1f8aa0" stroke-dasharray="5 4" marker-end="url(#a)"/><text x="{x0+225}" y="{y0+92}" text-anchor="middle" fill="#1f8aa0" font-weight="600">Pendent del fons</text>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#1f8aa0"/></marker></defs>
<text x="{x0+130}" y="{y0+H-22}" fill="#0b2a45" font-weight="700">Prof. 1,20 m</text><text x="{x0+W-100}" y="{y0+H-22}" fill="#0b2a45" font-weight="700">Prof. 1,60 m</text>
<g fill="#fff" stroke="#0b2a45" stroke-width="1.2" font-weight="700" fill-opacity="1" text-anchor="middle">
<rect x="{x0+W/2-10}" y="{y0-17}" width="20" height="14"/><text x="{x0+W/2}" y="{y0-6}" fill="#0b2a45" stroke="none">S</text>
<circle cx="{x0+150}" cy="{y0+H}" r="9"/><circle cx="{x0+270}" cy="{y0+H}" r="9"/><circle cx="{x0+390}" cy="{y0+H}" r="9"/>
<text x="{x0+150}" y="{y0+H+4}" fill="#0b2a45" stroke="none">I</text><text x="{x0+270}" y="{y0+H+4}" fill="#0b2a45" stroke="none">I</text><text x="{x0+390}" y="{y0+H+4}" fill="#0b2a45" stroke="none">I</text>
<rect x="{x0+205}" y="{y0+H+4}" width="20" height="14"/><rect x="{x0+325}" y="{y0+H+4}" width="20" height="14"/>
<text x="{x0+215}" y="{y0+H+15}" fill="#0b2a45" stroke="none">F</text><text x="{x0+335}" y="{y0+H+15}" fill="#0b2a45" stroke="none">F</text>
<rect x="{x0+W-92}" y="{y0+H/2-8}" width="16" height="16"/><text x="{x0+W-84}" y="{y0+H/2+4}" fill="#0b2a45" stroke="none">D</text>
<circle cx="{x0+W}" cy="{y0+H/2}" r="9"/><text x="{x0+W}" y="{y0+H/2+4}" fill="#0b2a45" stroke="none">A</text></g>
</svg>'''
sy = 20; sx = 70
d120, d160 = 1.20 * K, 1.60 * K
seccio = f'''<svg viewBox="0 0 640 200" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif" font-size="11">
<rect x="{sx-30}" y="{sy}" width="30" height="6" fill="#fff" stroke="#0b2a45"/><rect x="{sx+W}" y="{sy}" width="30" height="6" fill="#fff" stroke="#0b2a45"/>
<polygon points="{sx},{sy+6} {sx+W},{sy+6} {sx+W},{sy+6+d160} {sx},{sy+6+d120}" fill="#dff0f5"/>
<polygon points="{sx-12},{sy+6} {sx},{sy+6} {sx},{sy+6+d120} {sx+W},{sy+6+d160} {sx+W},{sy+6} {sx+W+12},{sy+6} {sx+W+12},{sy+6+d160+14} {sx-12},{sy+6+d120+14}" fill="#c9cfd4" stroke="#0b2a45" stroke-width="1"/>
<polygon points="{sx},{sy+6} {sx},{sy+6+d120} {sx+W},{sy+6+d160} {sx+W},{sy+6}" fill="#dff0f5"/>
<g fill="#aeb6bc" stroke="#0b2a45" stroke-width=".8"><rect x="{sx+0}" y="{sy+6+1*d120/6}" width="20" height="{d120-1*d120/6+1.3}"/><rect x="{sx+20}" y="{sy+6+2*d120/6}" width="20" height="{d120-2*d120/6+2.6}"/><rect x="{sx+40}" y="{sy+6+3*d120/6}" width="20" height="{d120-3*d120/6+3.9}"/><rect x="{sx+60}" y="{sy+6+4*d120/6}" width="20" height="{d120-4*d120/6+5.2}"/><rect x="{sx+80}" y="{sy+6+5*d120/6}" width="20" height="{d120-5*d120/6+6.5}"/></g>
<text x="{sx+W/2}" y="{sy+40}" text-anchor="middle" fill="#1f8aa0" font-weight="700">Làmina d'aigua</text>
<text x="{sx+W/2}" y="{sy+d160+40}" text-anchor="middle" fill="#555" font-size="10">Vas de gunita: parets 15 cm · fons 20 cm · impermeabilitzat i revestit</text>
<text x="{sx+165}" y="{sy+6+d120-8}" fill="#0b2a45" font-weight="700">1,20 m</text><text x="{sx+W-60}" y="{sy+6+d160-8}" fill="#0b2a45" font-weight="700">1,60 m</text>
</svg>'''
LEG = [("S", "Skimmer", 1), ("I", "Broquet d'impulsió", 3), ("F", "Focus LED", 2), ("A", "Presa de netejafons", 1), ("D", "Sumider de fons", 1), ("E", "Escala d'obra, 5 graons", 1), ("B", "Banc interior", 1)]
leg = ''.join(f'<div class="lg"><i>{a}</i><span>{e(b)}</span><b>{c}</b></div>' for a, b, c in LEG)

# ---- funcionamiento ----
PASOS = [("Aspiració", "L'aigua surt de la piscina pel skimmer, el sumider de fons i la presa de netejafons."), ("Bomba", "Electrobomba AstralPool de 0,75 CV amb prefiltre, que reté fulles i cabells."),
         ("Filtre", "Filtre AstralPool 500 amb vàlvula selectora, que reté la brutícia fina i permet rentar-lo."), ("Electròlisi salina", "La cèl·lula Bright Blue produeix el clor a partir de la sal de l'aigua."),
         ("Control de pH", "La sonda mesura el pH i la bomba dosificadora injecta el corrector quan cal."), ("Impulsió", "L'aigua neta i tractada torna a la piscina per 3 broquets d'impulsió.")]
flow = ''.join(f'<div class="st"><i>{i+1}</i><b>{e(a)}</b><span>{e(b)}</span></div>' for i, (a, b) in enumerate(PASOS))

MAT = [("Estructura del vas", "Gunita per via humida", "450 kg/m³, parets 15 cm i fons 20 cm, armada amb malla electrosoldada"), ("Impermeabilització", "Grupo Puma · Morcem Dry Fix", "Morter flexible de 3 mm armat amb malla Drypool"),
       ("Ciment cola", "Grupo Puma · Pegoland Profesional Flex C2 TE S1", "Adhesiu cimentós flexible per a zones humides"), ("Rejuntat", "Grupo Puma · Pegoland Profesional Junta CG2 A W", "Morter de rejuntat per a piscines"),
       ("Revestiment i coronament", "Cerámicas Mayor o Rosa Gres", "A escollir pel client, amb peça de coronament perimetral"), ("Filtre", "AstralPool 500", "Amb vàlvula selectora"), ("Bomba", "AstralPool 0,75 CV", "Monofàsica, amb prefiltre"),
       ("Electròlisi salina", "Bright Blue", "Amb cèl·lula electrolítica"), ("Regulació de pH", "Controlador automàtic", "Sonda i bomba dosificadora"), ("Il·luminació", "LED", "2 focus")]
mat = ''.join(f'<tr><td>{e(a)}</td><td><b>{e(b)}</b></td><td>{e(c)}</td></tr>' for a, b, c in MAT)

GANTT = [("Construcció del vas i gunita", [1, 1, 0, 0]), ("Escala i banc", [0, 1, 0, 0]), ("Impermeabilització", [0, 0, 1, 0]), ("Revestiment i coronament", [0, 0, 1, 1]), ("Filtració i equips", [0, 0, 1, 1]), ("Ompliment i posada en marxa", [0, 0, 0, 1])]
gt = '<table class="gt"><thead><tr><th>FASE</th>' + ''.join(f'<th>S{i}</th>' for i in range(1, 5)) + '</tr></thead><tbody>' + ''.join(f'<tr><td>{e(a)}</td>' + ''.join(f'<td class="{"on" if x else ""}"></td>' for x in r) + '</tr>' for a, r in GANTT) + '<tr class="pg"><td>Pagaments</td><td>20 %</td><td>30 %</td><td></td><td>30 % · 20 %</td></tr></tbody></table>'

if EXC is None:
    exc_row = '<tr><td>Excavació del vas i càrrega de terres a camió</td><td class="nn">Import a confirmar</td></tr>'
    exc_tot = ''
else:
    exc_row = f'<tr><td>Excavació del vas i càrrega de terres a camió</td><td class="nn">{eur(EXC)}</td></tr>'
    exc_tot = f'<tr class="tot"><td>Total amb excavació · IVA no inclòs</td><td class="nn">{eur(BASE + EXC)}</td></tr>'
EXCPAG = f"""<section class="page">{hdt("Excavació del terreny (opcional)")}<div class="body"><p class="lead3" style="font-size:10pt">L'excavació no està inclosa al pressupost. El client pot contractar-la pel seu compte o encarregar-la a Brava Pool; en tots dos casos ha d'estar acabada abans de començar la construcció del vas.</p>
<div class="cols2"><div class="opt"><h3>Opció A · La contracta el client</h3><ul class="tx1"><li>El client contracta l'excavació amb l'empresa que triï.</li><li>Brava Pool facilita les dimensions de l'excavació en el replantejament.</li><li>L'excavació inclou la càrrega i la retirada de les terres sobrants.</li><li>Si apareix pedra o roca, el sobrecost és a càrrec del client.</li></ul></div>
<div class="opt"><h3>Opció B · La fa Brava Pool</h3><ul class="tx1"><li>Brava Pool encarrega i coordina l'excavació, amb càrrega de les terres a camió.</li><li>L'import s'afegeix al pressupost com a partida opcional, sense IVA.</li><li>Si apareix pedra o roca, les hores de martell picador es cobren a part, amb l'import comunicat al client per escrit abans de fer-les.</li></ul></div></div>
<h2>Import de l'opció B</h2><table class="eco"><thead><tr><th>Concepte</th><th class="r" style="width:40mm">Import</th></tr></thead><tbody><tr><td>Total pressupost (sense excavació) · IVA no inclòs</td><td class="nn">{eur(BASE)}</td></tr>{exc_row}{exc_tot}</tbody></table>
<p class="note" style="margin-top:3mm">En cap de les dues opcions s'inclou el reblert amb grava al voltant de la piscina, que es valora a part segons la necessitat de l'obra.</p><h2>Dades de referència</h2><table class="kv"><tr><td>Piscina interior</td><td>6,00 × 2,50 m</td></tr><tr><td>Profunditat</td><td>1,20 a 1,60 m</td></tr><tr><td>Mides definitives de l'excavació</td><td>Es confirmen en el replantejament</td></tr></table>
<div class="acc"><h3>Opció escollida pel client</h3><p><span class="ck"></span> Opció A: contracto l'excavació pel meu compte.&nbsp;&nbsp;&nbsp;&nbsp;<span class="ck"></span> Opció B: encarrego l'excavació a Brava Pool.</p><div class="sig"><div><div class="line"></div><small>Nom i cognoms · DNI / NIF</small></div><div><div class="line big"></div><small>Signatura del client</small></div></div></div></div>{ftt(9)}</section>"""
DOC = f"""<section class="page"><div class="hero"></div><div class="hline"></div><img class="hlogo" src="assets/logo_blanco.png"><div class="hnum"><small>PRESSUPOST</small><b>{D["numero"]}</b></div>
<div class="htit"><div class="chip3">PROPOSTA DE CONSTRUCCIÓ</div><h1>Piscina d'obra <em>6 × 2,5 m</em></h1></div>
<div class="body" style="top:112mm"><div class="para"><small>PREPARAT PER A</small><b>{e(D["cliente"])}</b><br>{e(D["lugar"])}<br><small style="margin-top:2mm">DATA · VÀLID FINS AL</small><b>{D["fecha"]} · {D["valido"]}</b></div>
<p class="lead2">Li presentem la nostra proposta per a la construcció de la seva piscina d'obra a Platja d'Aro: vas de gunita armada, impermeabilització flexible, revestiment ceràmic i filtració amb electròlisi salina i control automàtic del pH.</p>
<div class="kpis"><div class="kp"><b>6,00 × 2,50 m</b><small>dimensions interiors</small></div><div class="kp"><b>1,20 a 1,60 m</b><small>profunditat</small></div><div class="kp"><b>21 m³</b><small>volum aproximat</small></div><div class="kp"><b>4 setmanes</b><small>termini d'execució</small></div></div></div>
<div class="body" style="top:auto;bottom:22mm;font-size:8pt;color:#6b6455"><b style="color:#0b2a45">Brava Pool</b> · {e(D["emisor"])} · {e(D["tel"])} · {e(D["web"])}</div>{ftt(1)}</section>
<section class="page">{hdt("Gràcies per confiar en nosaltres")}<div class="body"><p class="lead3">Benvolgut Joan Carles,</p>
<p class="para" style="line-height:1.6">Li presentem la nostra proposta per a la construcció de la seva piscina d'obra de 6 × 2,50 m a Platja d'Aro. Hem preparat aquest document perquè tingui, de manera clara i per escrit, tot el que inclou la seva piscina: els treballs, els materials i equips, els terminis, la forma de pagament i les garanties.<br><br>Construïm el vas amb formigó projectat (gunita) per via humida i armat, l'impermeabilitzem amb morter flexible, el revestim amb ceràmica per a piscines i hi instal·lem tota la filtració amb electròlisi salina i control automàtic del pH. Li lliurem la piscina plena, amb l'aigua tractada i a punt per al bany.<br><br>Restem a la seva disposició per resoldre qualsevol dubte.<br><b>Bilal</b> · Brava Pool</p>
<h2>La seva piscina en xifres</h2><table class="kv"><tr><td>Dimensions interiors</td><td>6,00 × 2,50 m</td></tr><tr><td>Profunditat</td><td>1,20 a 1,60 m</td></tr><tr><td>Superfície de làmina</td><td>15 m²</td></tr><tr><td>Volum aproximat</td><td>21 m³</td></tr><tr><td>Sistema constructiu</td><td>Gunita armada per via humida, 450 kg/m³</td></tr><tr><td>Revestiment i coronament</td><td>Cerámicas Mayor o Rosa Gres, a escollir</td></tr><tr><td>Filtració</td><td>Filtre AstralPool 500 + bomba AstralPool 0,75 CV</td></tr><tr><td>Tractament de l'aigua</td><td>Electròlisi salina Bright Blue i pH automàtic</td></tr></table>
<h2>El nostre compromís</h2><div class="cards"><div><b>Terminis per escrit</b>Planificació per fases des del primer dia i termini d'execució indicat en aquest document.</div><div><b>Pagaments segons l'avanç</b>Cada pagament es vincula a una fase acabada. L'últim 20 % només es paga amb la piscina plena i funcionant.</div><div><b>Garantia per escrit</b>10 anys en l'estanquitat del vas i 3 anys en equips i materials.</div><div><b>Servei tècnic tot l'any</b>Resposta per escrit en menys de 48 hores davant de qualsevol incidència.</div></div></div>{ftt(2)}</section>
<section class="page">{hdt("Plànol de la piscina")}<div class="body"><p class="note" style="font-size:9pt;margin:0 0 3mm">Distribució de la piscina de 6 × 2,50 m i situació dels elements principals.</p><div class="svgbox"><small>PLANTA</small>{planta}<small>SECCIÓ LONGITUDINAL</small>{seccio}</div><div class="lgs">{leg}</div><p class="note">Plànol orientatiu, sense escala. Les mides i la posició definitiva de cada element es confirmen amb el client en el replantejament.</p></div>{ftt(3)}</section>
<section class="page">{hdt("Instal·lació i planificació")}<div class="body"><p class="lead3" style="font-size:10pt">L'aigua s'aspira, passa per la bomba i el filtre, es desinfecta amb sal, se'n corregeix el pH i torna neta a la piscina. La depuradora funciona diverses hores al dia, de manera automàtica.</p><div class="flow">{flow}</div>
<div class="box"><b>Tot en una caseta tècnica.</b> Els equips (bomba, filtre, quadre elèctric, cèl·lula de sal i control de pH) s'instal·len junts, amb vàlvules que permeten aïllar cada element per al manteniment sense aturar la filtració.</div>
<h2>Planificació de l'obra</h2><p class="note" style="font-size:9pt;margin:0 0 2mm">Termini total estimat de 4 setmanes des de l'inici de l'obra. Cada pagament es fa en completar la fase corresponent.</p>{gt}<p class="note">Planificació orientativa. Pot variar segons el tipus de terreny, la meteorologia i el lliurament de materials; qualsevol canvi se li comunicarà amb antelació.</p></div>{ftt(4)}</section>
<section class="page">{hdt("Materials i marques")}<div class="body"><table class="eco mt"><thead><tr><th>Element</th><th>Marca i model</th><th>Detall</th></tr></thead><tbody>{mat}</tbody></table><h2>Elements de la instal·lació</h2><table class="kv"><tr><td>Aspiració</td><td>1 skimmer · 1 sumider de fons · 1 presa de netejafons</td></tr><tr><td>Impulsió</td><td>3 broquets d'impulsió</td></tr><tr><td>Il·luminació</td><td>2 focus LED</td></tr><tr><td>Equips</td><td>Filtre i bomba AstralPool · electròlisi salina Bright Blue · pH automàtic · quadre elèctric</td></tr></table>
</div>{ftt(5)}</section>
<section class="page">{hdt("Descripció dels treballs")}<div class="body"><table class="desc">{cab}<tbody>{desc}</tbody></table><p class="note" style="margin-top:3mm">PA = partida alçada. Preu tancat, amb materials i mà d'obra. En el capítol 5 s'indica només el total del capítol, que inclou tots els seus elements.</p></div>{ftt(6)}</section>
<section class="page">{hdt("Inversió i forma de pagament")}<div class="body"><table class="eco"><thead><tr><th style="width:12mm">Cap.</th><th>Concepte</th><th class="r" style="width:36mm">Import</th></tr></thead><tbody>{res}<tr class="tot"><td colspan="2">Total pressupost · IVA no inclòs</td><td class="nn">{eur(BASE)}</td></tr></tbody></table>
<div class="aviso"><b>Avís:</b> aquest pressupost no inclou l'IVA. L'IVA s'afegirà a la factura al tipus vigent.</div>
<div class="aviso"><b>Avís:</b> l'excavació no està inclosa, i els treballs extres es pressuposten a part i per escrit (vegi les pàgines 8 i 9).</div>
<h2>Forma de pagament</h2><div class="pps">{pps}</div>
<table class="kv pago"><tr><td>Titular</td><td>{e(D["emisor"])} · NIF {e(D["nif"])}</td></tr><tr><td>Banc / IBAN</td><td><b>{e(D["banco"])} · {e(D["iban"])}</b></td></tr><tr><td>Concepte</td><td>Pressupost {D["numero"]}</td></tr></table>
<div class="cards"><div><b>Pagaments per fites</b>Cada pagament es vincula a una fase acabada i l'últim 20 % es reté fins al lliurament de la piscina plena, amb l'aigua tractada i els equips en marxa.</div><div><b>Garantia</b>Brava Pool garanteix l'estanquitat del vas durant 10 anys davant de defectes de construcció, i els equips i materials durant 3 anys segons la garantia de cada fabricant.</div></div></div>{ftt(7)}</section>
<section class="page">{hdt("Condicions i acceptació")}<div class="body"><div class="cols2"><div><h2 style="margin-top:0">No inclou</h2><ul class="tx1">{"".join(f"<li>{e(x)}</li>" for x in NOINC)}</ul></div><div><h2 style="margin-top:0">Condicions</h2><ul class="tx1">{"".join(f"<li>{e(x)}</li>" for x in COND)}</ul></div></div>
<div class="box" style="margin-top:5mm"><b>Excavació i treballs addicionals</b><br>Aquest pressupost no inclou l'excavació, la preparació i neteja del terreny, les rases per a canonades, el reblert del perímetre del vas i de les rases, la retirada de terres ni l'anivellament del terreny. Aquests treballs es fan a part, amb pressupost propi, i han d'estar acabats abans de començar la construcció del vas.<br><br><b>Reblert amb grava al voltant de la piscina.</b> No està inclòs en el preu. Es valora a part, segons l'acabat de la piscina i el buit sobrant entre el vas i el terreny. Es recomana reblir-lo amb grava compactada per tongades, que afavoreix el drenatge al voltant del vas i evita que s'acumuli aigua darrere de les parets.<br><br><b>Pedra o roca a l'excavació.</b> Si en excavar apareix pedra o roca, les hores de martell picador es cobren a part, per hores, amb l'import comunicat al client per escrit abans de fer-les.<br><br><b>Treballs extres.</b> Qualsevol treball no descrit en aquest pressupost, o que calgui per imprevistos del terreny o per canvis demanats pel client, es pressuposta a part i per escrit. No es fa cap treball extra sense l'acceptació prèvia del client, que en coneix l'import abans que s'executi.</div>
<div class="acc"><h3>Acceptació del pressupost</h3><p>El client declara conèixer i acceptar el present pressupost núm. {D["numero"]}, per un import total de <b>{eur(BASE)}</b>, IVA no inclòs, les seves condicions i la forma de pagament indicada.</p><div class="sig"><div><div class="line"></div><small>Nom i cognoms · DNI / NIF</small><div class="line"></div><small>Lloc i data</small></div><div><div class="line big"></div><small>Signatura del client</small></div></div></div>
</div>{ftt(8)}</section>"""

DOC += EXCPAG
CSS += """.opt h3{font-size:10.4pt;margin-bottom:2mm}.ck{display:inline-block;width:4mm;height:4mm;border:.3mm solid var(--navy);vertical-align:-1mm;margin-right:1.5mm}.svgbox{border:.2mm solid var(--ln);padding:3mm 4mm}.svgbox small{display:block;font-size:6.6pt;letter-spacing:.2em;color:var(--mut);margin:2mm 0 1mm;font-weight:700}.svgbox svg{width:100%;display:block}
.lgs{display:grid;grid-template-columns:1fr 1fr;gap:0 9mm;margin:4mm 0 2mm}.lg{display:flex;align-items:center;gap:3mm;padding:1.8mm 0;border-bottom:.2mm solid var(--ln);font-size:9pt}.lg i{width:5.5mm;height:5.5mm;border:.3mm solid var(--navy);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-style:normal;font-size:7pt;font-weight:700;color:var(--navy)}.lg span{flex:1}.lg b{color:var(--navy)}
.flow{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm 5mm;margin:4mm 0 6mm}.st{border-top:.5mm solid var(--navy);padding-top:2.4mm;position:relative}.st i{font-style:normal;color:var(--terra);font-weight:700;font-size:15pt;font-weight:300;display:block}.st b{display:block;color:var(--navy);font-size:10.4pt;margin:.5mm 0 1.5mm}.st span{font-size:8.8pt;color:#44505d;line-height:1.5}
.mt td{padding:2.6mm 2mm!important;font-size:8.8pt}.mt td:nth-child(1){color:var(--mut)}.gt{font-size:8.4pt;margin-top:2mm;table-layout:fixed}.gt th:not(:first-child),.gt td:not(:first-child){width:25mm}.gt th{text-align:center;font-size:6.8pt;letter-spacing:.14em;color:var(--mut);padding:1.4mm;border-bottom:.3mm solid var(--navy)}.gt th:first-child,.gt td:first-child{text-align:left;width:50mm}
.gt td{border-bottom:.2mm solid var(--ln);padding:2.4mm 1.5mm;height:7mm}.gt td.on{background:linear-gradient(var(--cy),var(--cy)) center/92% 55% no-repeat}.gt .pg td{font-size:7.6pt;color:var(--terra);font-weight:700;text-align:center}.gt .pg td:first-child{text-align:left}
.eco td{padding:3.8mm 1.5mm}.kv td{padding-top:1.5mm!important;padding-bottom:1.5mm!important}.cards div{padding:3mm 4mm!important}.tx1{margin:0;padding-left:4mm;font-size:8.8pt}.tx1 li{margin-bottom:1.6mm}"""

(AQUI / "presupuesto_129.html").write_text(f'<!doctype html><html lang="ca"><head><meta charset="utf-8"><title>Pressupost 129 · Brava Pool</title><style>{CSS}</style></head><body>{DOC}</body></html>', encoding="utf-8")
pdf = AQUI / "Presupuesto_129_Joan_Carles_Platja_dAro.pdf"
ch = next((x for x in ["/opt/pw-browsers/chromium", "chromium", "google-chrome"] if Path(x).exists()), None)
subprocess.run([ch, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", (AQUI / "presupuesto_129.html").as_uri()], check=True, stderr=subprocess.DEVNULL)
print("OK", pdf.name, "| total", eur(BASE), "| pagos", [eur(x[2]) for x in pg])
