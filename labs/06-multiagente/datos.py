"""Datos del Lab 06. No lo tocás.

- PREGUNTA_DEL_CLIENTE: lo que le llega al coordinador.
- HISTORIAL_COORDINADOR: la conversación del coordinador hasta ahora (largo y con ruido).
- RESUMEN_EXPLORADOR / RESUMEN_CONSULTOR: lo que devuelve cada subagente al terminar
  (solo su mensaje final; todo lo que leyó en el camino queda en su propio contexto).
"""

PREGUNTA_DEL_CLIENTE = (
    "¿Por qué [Ventas Netas] de octubre da $1.250.430 en el reporte y el ERP dice $1.310.000?"
)

# Lo que el coordinador fue acumulando en su ventana de contexto. Fijate cuánto ocupa.
HISTORIAL_COORDINADOR = [
    {"role": "user", "content": "Hola, buen día. Te escribo por el reporte de ventas de la hormigonera."},
    {"role": "assistant", "content": "¡Buen día! Contame qué está pasando con el reporte."},
    {"role": "user", "content": PREGUNTA_DEL_CLIENTE},
    {"role": "assistant", "content": "Voy a revisar el modelo y el DWH en paralelo. " * 3},
] + [
    {"role": "user", "content": f"[tool_result #{i}] " + "fila de log de refresh sin relevancia; " * 40}
    for i in range(12)
]

RESUMEN_EXPLORADOR = (
    "Hallazgo: [Ventas Netas] = CALCULATE(SUM(fVentas[Importe]), fVentas[Estado] = \"Facturada\"). "
    "Excluye remitos en estado 'Pendiente'. "
    "Fuente: definition/tables/fVentas.tmdl, línea 41."
)

RESUMEN_CONSULTOR = (
    "Hallazgo: en octubre hay 37 remitos 'Pendiente' que suman $59.570 "
    "(1.310.000 − 1.250.430 = 59.570). "
    "Fuente: SELECT SUM(importe) FROM dwh.ventas WHERE mes = '2026-10' AND estado = 'Pendiente'."
)
