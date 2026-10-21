"""Reparto del precio cerrado del presupuesto 127 por partida.

Cada partida = material a coste + mano de obra repartida según la importancia del trabajo.
Así, si el cliente quita una partida, las demás conservan la misma relación coste/precio.

Fuentes: Generador de precios CYPE (generadordeprecios.info): oficial 1.ª 24,83 €/h, ayudante 23,59 €/h,
DryPool UPY120 (4,4 kg/m² de mortero, 0,376 h/m²) y gres UPT020 (1,264 h/m², cola, juntas RG);
rendimiento de picado 8–12 m²/operario/día (piscinasdeobramadrid.com); tus precios de material del 127.
Los marcados SUPUESTO no tienen fuente publicada.
"""
OF, AY = 24.83, 23.59
EQ = OF + AY
JEQ, JAY = 8 * EQ, 8 * AY

# material por m² (€): mortero DryPool 4,4 kg × 97,50/20 kg + malla ; cerámica 34,48 × 112/105 + cola 6 kg × 0,59
MAT_DP = 4.4 * 97.50 / 20 + 0.2 * 1.94
MAT_CE = 34.48 * 112 / 105 + 6 * 0.59
MO_DP = 0.188 * OF + 0.188 * AY
MO_CE = 0.73 * OF + 0.534 * AY

# código: (material €, mano de obra estándar €, importancia, nota)
IMPORTANCIA = {"critica": 1.25, "normal": 1.0, "baja": 0.6}
P = {
 "1.1": (0, 8 * OF, "normal", "1 jornada de oficial"),
 "1.2": (0, 4 * EQ, "critica", "referencia de flotación: de ella depende la nivelación de la coronación"),
 "1.3": (0, JEQ, "baja", "1 jornada de equipo"),
 "2.1": (0, 3.1 * JEQ, "baja", "37 ml a ≈12 ml/jornada de equipo (SUPUESTO)"),
 "2.2": (0, 105 / 10 * JAY, "baja", "105 m² a 10 m²/jornada (picado 8–12 m²/operario/día)"),
 "2.3": (0, 105 / 12 * JAY, "baja", "105 m² a ≈12 m²/jornada (SUPUESTO)"),
 "2.4": (750, 0, "baja", "contenedores y transporte a punto limpio, servicio de terceros (SUPUESTO)"),
 "3.1": (105 * 0.3 * 3.6 * 1.58, 105 * 0.25 * AY, "normal", "mortero reparador Morcemrest RF35 en el 30 % + 0,25 h/m²"),
 "3.2": (60, 8 * EQ, "critica", "pasamuros y puntos singulares: donde suelen producirse las fugas"),
 "3.3": (60, 12.5 * 0.5 * EQ, "normal", "pendiente del canal (SUPUESTO)"),
 "3.4": (80, 12 * OF, "critica", "replanteo con láser y regularización del muro de rebose"),
 "4.1": (MAT_DP * 69, MO_DP * 69, "critica", "CYPE UPY120; mortero a tu precio de 97,50 €/saco de 20 kg"),
 "4.2": (MAT_DP * 27, MO_DP * 27, "critica", "idem, canal"),
 "4.3": (MAT_DP * 9, MO_DP * 9, "critica", "idem, bancos y escalera"),
 "5.1": (MAT_CE * 69, MO_CE * 69, "critica", "CYPE UPT020; cerámica a tu precio de 34,48 €/m² (112 m² para 105)"),
 "5.2": (MAT_CE * 27, MO_CE * 27, "critica", "idem, canal"),
 "5.3": (MAT_CE * 9, MO_CE * 9, "critica", "idem, bancos y escalera"),
 "5.4": (35 * 68.86, 35 * 0.35 * OF, "normal", "peldaño a tu precio de 68,86 €/ud + 0,35 h por pieza"),
 "6.1": (37 * 60, 37 * 0.6 * EQ, "critica", "SUPUESTO: pieza de coronación a 60 €/ml, sin fuente; pedir precio al proveedor"),
 "6.2": (0, 4 * EQ, "normal", "4 h de equipo"),
 "7.1": (105 * 0.35 * 15.88, 105 * 0.05 * AY, "critica", "mortero de juntas RG 0,35 kg/m² (CYPE UPT020)"),
 "7.2": (40, 110, "normal", "sellador y mano de obra (SUPUESTO)"),
 "8.1": (0, 8 * AY, "baja", "1 jornada de ayudante"),
 "8.2": (0, 4 * OF, "baja", "4 h de oficial"),
}

# Peso de cada fase sobre el precio cerrado, según su importancia en el resultado (suman 100 %)
PCT_FASE = {"1": 3.0, "2": 11.0, "3": 11.5, "4": 14.5, "5": 40.0, "6": 15.0, "7": 4.0, "8": 1.0}
assert abs(sum(PCT_FASE.values()) - 100) < 1e-9

def pesos(precio):
    """Importe de cada partida = su material a coste + la parte de mano de obra que le toca de su fase,
    repartida por mano de obra estándar × importancia. Ninguna partida baja de su material."""
    out = {}
    for f, pct in PCT_FASE.items():
        ks = [k for k in P if k.split(".")[0] == f]
        fase = precio * pct / 100
        mat = sum(P[k][0] for k in ks)
        lw = {k: P[k][1] * IMPORTANCIA[P[k][2]] for k in ks}
        assert fase > mat, (f, fase, mat)
        for k in ks:
            out[k] = P[k][0] + (fase - mat) * lw[k] / sum(lw.values())
    return out, PCT_FASE

def horas(k):
    return P[k][1] / ((OF + AY) / 2)
