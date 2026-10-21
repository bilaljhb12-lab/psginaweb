"""Dibujos técnicos de la piscina del presupuesto 127 (SVG): planta, vista 3D y secciones.

Geometría deducida de las fotografías del cliente y de la vista de satélite; medidas confirmadas por el cliente:
vaso 7,50 × 4,00 m, profundidad 1,70 m, canal en L de 12,5 ml (80 cm de ancho en el lado largo, 30 cm en el corto).
Medidas a confirmar en el replanteo: ancho del banco, nº y ancho de peldaños, aparatos en pared, altura del canal.
"""
NAVY, CY, INK, MUT = "#1f4e79", "#3fa4c8", "#2b3440", "#5b6b7b"
BENCH_W, STAIR_W, STEPS, CANAL_H = 0.40, 1.20, 6, 0.80     # banco ≈ 40 cm (cliente); resto a confirmar
STEP_W = [1.20, 1.20, 1.20, 1.20, 0.65, 0.65]               # los 2/3 primeros de 1,20 m y el resto más estrechos (cliente)

def planta_svg():
    S = 56.3                    # px por metro
    X0, Y0 = 120, 196           # esquina oeste-valle del vaso
    X = lambda m: X0 + m * S
    Y = lambda m: Y0 + m * S    # y crece hacia la terraza
    o = []
    a = o.append
    a(f'<svg viewBox="0 0 790 660" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">')
    a('<defs><pattern id="hat" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#9db98a" stroke-width="1.2"/></pattern>'
      '<pattern id="tl" width="17.45" height="35.2" patternUnits="userSpaceOnUse"><rect width="17.45" height="35.2" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width=".7"/></pattern></defs>')
    a('<rect width="790" height="660" fill="#fff"/>')
    a(f'<text x="24" y="26" font-size="12" font-weight="700" fill="{NAVY}" letter-spacing="2">PLANTA</text>')
    # ladera y terraza
    a('<rect x="24" y="44" width="740" height="60" fill="url(#hat)"/><rect x="24" y="44" width="740" height="60" fill="#dfead5" fill-opacity=".55"/>')
    a(f'<text x="394" y="80" text-anchor="middle" font-size="11" fill="#5b7a4a" letter-spacing="2">LADERA · LADO VALLE</text>')
    a(f'<rect x="24" y="104" width="740" height="540" fill="#efe6d6"/>')
    # pretil oeste
    a(f'<rect x="{X(0)-52}" y="{Y(-1.25)}" width="26" height="{4.0*S+80}" fill="#cfc3ad" stroke="#8c7f66"/>')
    a(f'<text transform="translate({X(0)-62},{Y(2)}) rotate(-90)" text-anchor="middle" font-size="9.5" fill="#6b5f48">pretil / muro exterior (lado oeste)</text>')
    # canal largo (valle): y -1.0..-0.2 ; canal corto (este): x 7.7..8.0, y -1.0..4.0
    a(f'<rect x="{X(0)-8}" y="{Y(-1.2)}" width="{S*8.2+8}" height="{S*0.2}" fill="#cfc3ad" stroke="#8c7f66"/>')   # muro exterior valle
    a(f'<rect x="{X(0)-8}" y="{Y(-1.0)}" width="{S*8.0+8}" height="{S*0.8}" fill="#dcecf3" stroke="{NAVY}" stroke-width="2"/>')
    a(f'<rect x="{X(7.7)}" y="{Y(-1.0)}" width="{S*0.3}" height="{S*5.0}" fill="#dcecf3" stroke="{NAVY}" stroke-width="2"/>')
    a(f'<rect x="{X(8.0)}" y="{Y(-1.2)}" width="{S*0.2}" height="{S*5.2}" fill="#cfc3ad" stroke="#8c7f66"/>')       # muro exterior este
    # labios y coronación
    a(f'<rect x="{X(-0.25)}" y="{Y(-0.2)}" width="{S*8.0}" height="{S*0.2}" fill="#e3d2b0" stroke="#a89878"/>')   # labio valle
    a(f'<rect x="{X(7.5)}" y="{Y(-0.2)}" width="{S*0.2}" height="{S*4.45}" fill="#e3d2b0" stroke="#a89878"/>')    # labio este
    a(f'<rect x="{X(-0.25)}" y="{Y(4.0)}" width="{S*7.95}" height="{S*0.45}" fill="#e9dcc3" stroke="#a89878"/>')    # coronación norte
    a(f'<rect x="{X(-0.25)}" y="{Y(0)}" width="{S*0.25}" height="{S*4.0}" fill="#e9dcc3" stroke="#a89878"/>')    # coronación oeste
    # vaso
    a(f'<rect x="{X(0)}" y="{Y(0)}" width="{S*7.5}" height="{S*4.0}" fill="#3a8fbf" stroke="{NAVY}" stroke-width="2.5"/>')
    a(f'<rect x="{X(0)}" y="{Y(0)}" width="{S*7.5}" height="{S*4.0}" fill="url(#tl)"/>')
    # banco oeste (ancho completo)
    a(f'<rect x="{X(0)}" y="{Y(0)}" width="{S*BENCH_W}" height="{S*4.0}" fill="#a9d8ec" stroke="{NAVY}"/>')
    a(f'<text transform="translate({X(BENCH_W/2)+4},{Y(1.2)}) rotate(-90)" text-anchor="middle" font-size="11" font-weight="700" fill="{NAVY}">Banco · 4,00 m</text>')
    # escalera desde la terraza (esquina noroeste): peldaños más anchos arriba y más estrechos abajo
    sx = X(BENCH_W)
    for i, w in enumerate(STEP_W):
        y_n = 4.0 - 0.28 * i
        a(f'<rect x="{sx}" y="{Y(y_n - 0.28)}" width="{S*w}" height="{S*0.28}" fill="#d7ebf5" stroke="{NAVY}" stroke-width="1.4"/>')
    a(f'<text x="{sx + S*STAIR_W + 8}" y="{Y(4.0 - 0.28*4.6)}" font-size="10" font-weight="700" fill="#fff">Escalera · 6 peldaños</text>')
    a(f'<text x="{sx + S*STAIR_W + 8}" y="{Y(4.0 - 0.28*4.6) + 13}" font-size="9" fill="#e8f4fa">4 de 1,20 m y 2 más estrechos</text>')
    a(f'<path d="M{sx+S*STAIR_W/2} {Y(4.0)+36} L{sx+S*STAIR_W/2} {Y(4.0)+6}" stroke="{NAVY}" stroke-width="1.6" fill="none"/><path d="M{sx+S*STAIR_W/2-5} {Y(4.0)+13} L{sx+S*STAIR_W/2} {Y(4.0)+4} L{sx+S*STAIR_W/2+5} {Y(4.0)+13}" fill="none" stroke="{NAVY}" stroke-width="1.6"/>')
    a(f'<text x="{sx+S*STAIR_W/2+10}" y="{Y(4.0)+36}" font-size="9" fill="#33698f">entrada desde la terraza</text>')
    # sumidero de fondo y del canal
    cx, cy = X(5.0), Y(2.0)
    a(f'<circle cx="{cx}" cy="{cy}" r="8" fill="#fff" stroke="{NAVY}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="3.2" fill="{NAVY}"/>')
    a(f'<text x="{cx}" y="{cy+24}" text-anchor="middle" font-size="10" fill="#fff">sumidero de fondo</text>')
    a(f'<circle cx="{X(5.6)}" cy="{Y(-0.6)}" r="6" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/><circle cx="{X(5.6)}" cy="{Y(-0.6)}" r="2" fill="{NAVY}"/>')
    a(f'<text x="{X(5.6)+11}" y="{Y(-0.6)+3.5}" font-size="9" fill="#33698f">sumidero canal</text>')
    # aparatos en pared norte
    for xm, r in ((3.3, 5.5), (4.0, 4), (5.9, 5.5)):
        a(f'<circle cx="{X(xm)}" cy="{Y(4.0)-2}" r="{r}" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/>')
    a(f'<text x="{X(4.6)}" y="{Y(4.0)+17}" font-size="9" fill="#6b5f48">aparatos en pared (focos / boquillas)</text>')
    # flechas de rebose
    for xm in (1.8, 3.4, 5.0, 6.6):
        a(f'<path d="M{X(xm)} {Y(0)+16} L{X(xm)} {Y(-0.55)}" stroke="#fff" stroke-width="2" fill="none" marker-end="url(#ar)"/>')
    a('<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#fff"/></marker></defs>')
    for ym in (1.0, 2.6):
        a(f'<path d="M{X(7.5)-18} {Y(ym)} L{X(7.5)+12} {Y(ym)}" stroke="#fff" stroke-width="1.4" stroke-dasharray="3 3" fill="none" marker-end="url(#ar)"/>')
    a(f'<text x="{X(3.75)}" y="{Y(1.55)}" text-anchor="middle" font-size="19" font-weight="700" fill="#fff">Vaso 7,50 × 4,00 m</text>')
    a(f'<text x="{X(3.75)}" y="{Y(1.55)+20}" text-anchor="middle" font-size="12" fill="#e8f4fa">profundidad 1,70 m · cerámica rectangular</text>')
    # rótulos canal
    a(f'<text x="{X(3.0)}" y="{Y(-0.57)}" text-anchor="middle" font-size="12.5" font-weight="700" fill="{NAVY}">Canal lado valle · ancho 0,80 m</text>')
    a(f'<text transform="translate({X(8.0)+36},{Y(2.0)}) rotate(90)" text-anchor="middle" font-size="10.5" font-weight="700" fill="{NAVY}">Canal lado este · ancho 0,30 m</text>')
    a(f'<text x="{X(3.0)}" y="{Y(-1.3)}" text-anchor="middle" font-size="9" fill="#6b5f48">muro exterior del canal</text>')
    # rejilla lineal terraza
    a(f'<line x1="{X(-0.25)}" y1="{Y(5.4)}" x2="{X(7.7)}" y2="{Y(5.4)}" stroke="#4a5562" stroke-width="5" stroke-dasharray="14 4"/>')
    a(f'<text x="{X(3.75)}" y="{Y(5.4)+20}" text-anchor="middle" font-size="9.5" fill="#4a5562">rejilla lineal de la terraza</text>')
    a(f'<text x="{X(3.75)}" y="{Y(6.4)}" text-anchor="middle" font-size="11" fill="#8c7f66" letter-spacing="2">TERRAZA Y VIVIENDA</text>')
    # cotas
    a(f'<g stroke="{MUT}" stroke-width="1" fill="none"><line x1="{X(0)}" y1="{Y(7.0)-18}" x2="{X(7.5)}" y2="{Y(7.0)-18}"/><line x1="{X(0)}" y1="{Y(7.0)-24}" x2="{X(0)}" y2="{Y(7.0)-12}"/><line x1="{X(7.5)}" y1="{Y(7.0)-24}" x2="{X(7.5)}" y2="{Y(7.0)-12}"/>'
      f'<line x1="{X(8.2)+22}" y1="{Y(0)}" x2="{X(8.2)+22}" y2="{Y(4.0)}"/><line x1="{X(8.2)+16}" y1="{Y(0)}" x2="{X(8.2)+28}" y2="{Y(0)}"/><line x1="{X(8.2)+16}" y1="{Y(4.0)}" x2="{X(8.2)+28}" y2="{Y(4.0)}"/></g>')
    a(f'<text x="{X(3.75)}" y="{Y(7.0)-4}" text-anchor="middle" font-size="12" fill="{INK}">7,50 m</text>')
    a(f'<text transform="translate({X(8.2)+42},{Y(2.0)}) rotate(90)" text-anchor="middle" font-size="12" fill="{INK}">4,00 m</text>')
    # norte/orientación
    a(f'<text x="24" y="648" font-size="9.5" fill="{MUT}">Esquema deducido de las fotografías. Banco, escalera y aparatos: posición y medidas orientativas, a confirmar en el replanteo.</text>')
    a('</svg>')
    return ''.join(o)

# ---------- secciones ----------
def secciones_svg():
    o = ['<svg viewBox="0 0 900 620" xmlns="http://www.w3.org/2000/svg" font-family="Inter,Arial,sans-serif">']
    a = o.append
    a('<defs><marker id="a4" markerWidth="9" markerHeight="9" refX="5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#1f4e79"/></marker></defs>')
    a('<rect width="900" height="620" fill="#fff"/>')
    # ---- Sección A-A: por el lado valle (canal de 80 cm)
    S = 90.0
    a(f'<text x="24" y="24" font-size="12" font-weight="700" fill="{NAVY}" letter-spacing="2">SECCIÓN A-A · LADO VALLE · CANAL DE 0,80 m</text>')
    x0, z0 = 150, 120
    Xa = lambda y: x0 + (y + 1.2) * S
    Za = lambda z: z0 - z * S
    a(f'<rect x="{Xa(-1.2)}" y="{Za(0.12)}" width="{S*0.2}" height="{S*(CANAL_H+0.12)}" fill="#d9ccb3" stroke="#8c7f66"/>')
    a(f'<rect x="{Xa(-1.0)}" y="{Za(-CANAL_H)}" width="{S*0.8}" height="{S*0.07}" fill="#cbd9e0" stroke="{NAVY}"/>')
    a(f'<rect x="{Xa(-0.2)}" y="{Za(0.03)}" width="{S*0.2}" height="{S*1.73}" fill="#e3d2b0" stroke="#a89878"/>')
    a(f'<rect x="{Xa(0)}" y="{Za(0)}" width="{S*4.0}" height="{S*1.7}" fill="#7cc7e0" fill-opacity=".85" stroke="{NAVY}" stroke-width="2"/>')
    a(f'<rect x="{Xa(4.0)}" y="{Za(0.08)}" width="{S*0.45}" height="{S*1.78}" fill="#e9dcc3" stroke="#a89878"/>')
    a(f'<line x1="{Xa(-1.2)-30}" y1="{Za(0)}" x2="{Xa(4.45)+20}" y2="{Za(0)}" stroke="{NAVY}" stroke-dasharray="6 4"/>')
    a(f'<text x="{Xa(4.45)+26}" y="{Za(0)+4}" font-size="10" fill="{NAVY}">nivel del agua = labio de rebose</text>')
    a(f'<path d="M{Xa(0.35)} {Za(0.0)-2} Q{Xa(-0.1)} {Za(0.16)} {Xa(-0.45)} {Za(-0.05)} L{Xa(-0.6)} {Za(-0.7)}" stroke="{NAVY}" stroke-width="3" fill="none" marker-end="url(#a4)"/>')
    a(f'<text x="{Xa(-1.2)-50}" y="62" font-size="11" font-weight="700" fill="{NAVY}">El agua rebosa por este lado</text>')
    a(f'<text x="{Xa(-1.2)-50}" y="77" font-size="10" fill="{INK}">y cae al canal de 0,80 m</text>')
    a(f'<text x="{Xa(2.0)}" y="{Za(-0.8)}" text-anchor="middle" font-size="13" font-weight="700" fill="{NAVY}">Vaso · 4,00 m de ancho</text>')
    a(f'<text x="{Xa(2.0)}" y="{Za(-0.8)+16}" text-anchor="middle" font-size="10.5" fill="{INK}">profundidad 1,70 m</text>')
    a(f'<g stroke="{MUT}" fill="none"><line x1="{Xa(-1.0)}" y1="{Za(-CANAL_H)+30}" x2="{Xa(-0.2)}" y2="{Za(-CANAL_H)+30}"/><line x1="{Xa(-1.0)}" y1="{Za(-CANAL_H)+24}" x2="{Xa(-1.0)}" y2="{Za(-CANAL_H)+36}"/><line x1="{Xa(-0.2)}" y1="{Za(-CANAL_H)+24}" x2="{Xa(-0.2)}" y2="{Za(-CANAL_H)+36}"/>'
      f'<line x1="{Xa(4.45)+14}" y1="{Za(0)}" x2="{Xa(4.45)+14}" y2="{Za(-1.7)}"/><line x1="{Xa(4.45)+8}" y1="{Za(-1.7)}" x2="{Xa(4.45)+20}" y2="{Za(-1.7)}"/></g>')
    a(f'<text x="{Xa(-0.6)}" y="{Za(-CANAL_H)+50}" text-anchor="middle" font-size="10.5" fill="{INK}">ancho 0,80 m</text>')
    a(f'<text transform="translate({Xa(4.45)+32},{Za(-0.85)}) rotate(90)" text-anchor="middle" font-size="10.5" fill="{INK}">1,70 m</text>')
    a(f'<text x="{Xa(-1.1)}" y="{Za(0.12)-7}" text-anchor="middle" font-size="9.5" fill="#6b5f48">muro exterior</text>')
    a(f'<text x="{Xa(4.22)}" y="{Za(0.08)-7}" text-anchor="middle" font-size="9.5" fill="#6b5f48">terraza</text>')
    # ---- Sección B-B: por el lado este (canal de 30 cm) y ligero desnivel
    base = 330
    a(f'<text x="24" y="{base-10}" font-size="12" font-weight="700" fill="{NAVY}" letter-spacing="2">SECCIÓN B-B · LADO ESTE · CANAL DE 0,30 m</text>')
    S2, bx = 80.0, 60
    Xb = lambda x: bx + x * S2
    zb = base + 150
    Zb = lambda z: zb - z * S2
    a(f'<rect x="{Xb(-0.25)}" y="{Zb(0.45)}" width="{S2*0.25}" height="{S2*(1.7+0.45)}" fill="#cfc3ad" stroke="#8c7f66"/>')
    a(f'<rect x="{Xb(0)}" y="{Zb(0)}" width="{S2*7.5}" height="{S2*1.7}" fill="#7cc7e0" fill-opacity=".85" stroke="{NAVY}" stroke-width="2"/>')
    a(f'<rect x="{Xb(0)}" y="{Zb(-0.45)}" width="{S2*BENCH_W}" height="{S2*1.25}" fill="#a9d8ec" stroke="{NAVY}"/>')
    a(f'<text x="{Xb(BENCH_W/2)}" y="{Zb(-0.45)+16}" text-anchor="middle" font-size="9" fill="{NAVY}">banco</text>')
    a(f'<rect x="{Xb(7.5)}" y="{Zb(0.09)}" width="{S2*0.2}" height="{S2*1.79}" fill="#e3d2b0" stroke="#a89878"/>')
    a(f'<rect x="{Xb(7.7)}" y="{Zb(-CANAL_H)}" width="{S2*0.3}" height="{S2*0.07}" fill="#cbd9e0" stroke="{NAVY}"/>')
    a(f'<rect x="{Xb(8.0)}" y="{Zb(0.12)}" width="{S2*0.2}" height="{S2*(CANAL_H+0.12)}" fill="#d9ccb3" stroke="#8c7f66"/>')
    a(f'<line x1="{Xb(-0.4)}" y1="{Zb(0)}" x2="{Xb(8.7)}" y2="{Zb(0)}" stroke="{NAVY}" stroke-dasharray="6 4"/>')
    a(f'<text x="{Xb(8.5)}" y="{Zb(0)+4}" font-size="10" fill="{NAVY}">nivel de referencia</text>')
    a(f'<g stroke="#c9822b" stroke-width="1.8" fill="none"><line x1="{Xb(7.4)}" y1="{Zb(0.09)}" x2="{Xb(7.4)}" y2="{Zb(0)}"/><line x1="{Xb(7.33)}" y1="{Zb(0.09)}" x2="{Xb(7.47)}" y2="{Zb(0.09)}"/></g>')
    a(f'<text x="{Xb(7.3)}" y="{Zb(0.09)-8}" text-anchor="end" font-size="10" font-weight="700" fill="#c9822b">ligero desnivel</text>')
    a(f'<path d="M{Xb(7.0)} {Zb(-0.05)} Q{Xb(7.55)} {Zb(0.05)} {Xb(7.85)} {Zb(-0.3)} L{Xb(7.85)} {Zb(-0.6)}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="5 3" fill="none" marker-end="url(#a4)"/>')
    a(f'<text x="{Xb(3.9)}" y="{Zb(-0.85)}" text-anchor="middle" font-size="13" font-weight="700" fill="{NAVY}">Vaso · 7,50 m de largo</text>')
    a(f'<text x="{Xb(3.9)}" y="{Zb(-0.85)+16}" text-anchor="middle" font-size="10.5" fill="{INK}">profundidad 1,70 m</text>')
    a(f'<text x="{Xb(8.1)}" y="{Zb(0.12)-8}" text-anchor="middle" font-size="9.5" fill="#6b5f48">muro exterior</text>')
    a(f'<text x="{Xb(7.85)}" y="{Zb(-CANAL_H)+22}" text-anchor="middle" font-size="10" fill="{INK}">0,30 m</text>')
    # llamada con buenas palabras
    bxx, byy = Xb(0.9), base + 4
    a(f'<rect x="{bxx}" y="{byy}" width="{S2*5.6}" height="76" rx="5" fill="#fbf3e6" stroke="#c9822b"/>')
    a(f'<text x="{bxx+12}" y="{byy+19}" font-size="11.5" font-weight="700" fill="#8a5a14">Ligero desnivel en el labio de rebose del lado este</text>')
    a(f'<text x="{bxx+12}" y="{byy+36}" font-size="9.8" fill="#5a3d0f">Entre el labio de este lado y el del lado valle hay una pequeña diferencia de altura</text>')
    a(f'<text x="{bxx+12}" y="{byy+50}" font-size="9.8" fill="#5a3d0f">(dibujada exagerada). Se mide con nivel láser y se regulariza durante la obra, con una</text>')
    a(f'<text x="{bxx+12}" y="{byy+64}" font-size="9.8" fill="#5a3d0f">tolerancia de ±2 mm, para que el agua rebose de forma uniforme en todo el perímetro.</text>')
    a('</svg>')
    return ''.join(o)

if __name__ == "__main__":
    import pathlib, sys
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    for n, f in (("planta", planta_svg), ("secciones", secciones_svg)):
        html = f'<!doctype html><meta charset="utf-8"><style>body{{margin:0;background:#fff}}</style>{f()}'
        (out / f"{n}.html").write_text(html, encoding="utf-8")
