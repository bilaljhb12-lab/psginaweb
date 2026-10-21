"""Coste estándar por partida del presupuesto 127, con su origen.

Base: Generador de precios CYPE (generadordeprecios.info), precios hora de oficial 1.ª
24,83 €/h y ayudante 23,59 €/h, y tus precios de material del presupuesto 127
(cerámica 34,48 €/m², peldaños 68,86 €/ud, DryPool 97,50 €/saco de 20 kg).
Son costes directos sin gastos generales ni beneficio. Los marcados SUPUESTO no tienen fuente publicada.
"""
OF, AY = 24.83, 23.59            # €/h
JORN_EQ = 8 * OF + 8 * AY        # jornada de equipo oficial + ayudante
JORN_AY = 8 * AY                 # jornada de ayudante

# DryPool (CYPE UPY120): 4,4 kg/m² de mortero + 0,2 m²/m² de malla + 0,376 h/m² de mano de obra
SACO_KG, SACO_EUR = 20, 97.50
dp_m2 = (4.4 * SACO_EUR / SACO_KG + 0.2 * 1.94 + 0.188 * OF + 0.188 * AY) * 1.02
# Cerámica (CYPE UPT020): mano de obra 0,73 h oficial + 0,534 h ayudante; cola 6 kg/m² a 0,59 €/kg (doble encolado)
ceram_m2 = (34.48 * 112 / 105 + 6 * 0.59 + 0.73 * OF + 0.534 * AY) * 1.03
CORON_ML = (60 + 0.6 * (OF + AY))  # SUPUESTO: pieza 60 €/ml sin fuente + colocación 0,6 h de equipo/ml

# código: (coste estándar €, cómo se obtiene)
COSTE = {
 "1.1": (8 * OF, "1 jornada de oficial (CYPE 24,83 €/h)"),
 "1.2": (4 * OF + 4 * AY, "4 h de oficial + 4 h de ayudante"),
 "1.3": (JORN_EQ, "1 jornada de equipo (oficial + ayudante)"),
 "2.1": (3.1 * JORN_EQ, "37 ml a ≈12 ml/jornada de equipo (SUPUESTO de rendimiento)"),
 "2.2": (105 / 10 * JORN_AY, "105 m² a 10 m²/jornada: rendimiento de picado 8–12 m²/operario/día (piscinasdeobramadrid.com)"),
 "2.3": (105 / 12 * JORN_AY, "105 m² a ≈12 m²/jornada (SUPUESTO)"),
 "2.4": (750, "≈3 contenedores y transporte a punto limpio (SUPUESTO)"),
 "3.1": (105 * 0.25 * AY + 105 * 0.3 * 3.6 * 1.58, "0,25 h/m² de ayudante + mortero reparador Morcemrest RF35 en el 30 % (CYPE: 3,6 kg/m² a 1,58 €/kg)"),
 "3.2": (16 * (OF + AY) / 2 + 60, "16 h de equipo + materiales (SUPUESTO)"),
 "3.3": (12.5 * 0.5 * (OF + AY) + 60, "0,5 h de equipo/ml + mortero (SUPUESTO)"),
 "3.4": (12 * OF + 80, "12 h de oficial con nivel láser + mortero (SUPUESTO)"),
 "4.1": (dp_m2 * 69, "CYPE UPY120: 4,4 kg/m² de mortero (tu saco de 97,50 €/20 kg) + malla + 0,376 h/m²"),
 "4.2": (dp_m2 * 27, "idem, canal"),
 "4.3": (dp_m2 * 9, "idem, bancos y escalera"),
 "5.1": (ceram_m2 * 69, "CYPE UPT020: tu cerámica 34,48 €/m² (112 m² para 105) + cola + 1,264 h/m² de alicatador"),
 "5.2": (ceram_m2 * 27, "idem, canal"),
 "5.3": (ceram_m2 * 9, "idem, bancos y escalera"),
 "5.4": (35 * (68.86 + 0.35 * OF) * 1.03, "tu peldaño 68,86 € + 0,35 h de oficial por pieza"),
 "6.1": (37 * CORON_ML, "SUPUESTO: pieza de coronación 60 €/ml, sin fuente; pedir precio al proveedor"),
 "6.2": (4 * (OF + AY), "4 h de equipo"),
 "7.1": (105 * 0.35 * 15.88, "CYPE UPT020: mortero de juntas RG 0,35 kg/m² a 15,88 €/kg"),
 "7.2": (150, "sellador y mano de obra (SUPUESTO)"),
 "8.1": (8 * AY, "1 jornada de ayudante"),
 "8.2": (4 * OF, "4 h de oficial"),
}
PESOS = {k: v[0] for k, v in COSTE.items()}
