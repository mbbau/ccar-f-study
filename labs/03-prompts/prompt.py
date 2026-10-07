"""Lab 03 · Prompt de revisión de medidas DAX.

Completá los 3 huecos marcados con ___ y corré: python check.py
No hace falta API key: el autocorrector revisa cómo está armado el prompt.
"""

# ---------------------------------------------------------------------------
# System prompt: el rol. Una oración alcanza (doc: "Give Claude a role").
# ---------------------------------------------------------------------------
SYSTEM = (
    "Sos un revisor de modelos semánticos de Power BI especializado en DAX. "
    "Tus reportes los leen analistas que deciden si publicar un informe, "
    "así que cada hallazgo que reportás les cuesta tiempo de revisión."
)

# La versión que NO queremos (la trampa típica del día). No la uses.
CRITERIOS_VAGOS = "Revisá las medidas con cuidado y reportá solo los problemas importantes."

# ---------------------------------------------------------------------------
# HUECO 1 · Criterios explícitos.
# Reemplazá cada ___ por una CATEGORÍA concreta (qué tipo de problema).
# Prohibido: "cuidado", "importante", "conservador", "alta confianza", "seguro".
# ---------------------------------------------------------------------------
REPORTAR = [
    "Medidas que pueden devolver un resultado incorrecto o un error visible (p. ej. división por cero sin DIVIDE).",
    "Medidas que atentan contra la performance del reporte. Por ejemplo usando la función filter dentro de calculate sobre una tabla de hecho entera.",
    "Medidas cuyo resultado es correcto en algunos contextos pero engañoso en otros (p. ej. AVERAGE(Despachos[Precio_m3]))"
]

NO_REPORTAR = [
    "Medidas que no estan bien formateadas para facilitar la lectura humana, por ejemplo sin indentado.",
    "Medidas con nombres ambiguos o poco claros, o que no tengan descripción.",
]

# Severidad con un ejemplo concreto por nivel (task statement 4.1). Ya está completa.
SEVERIDAD = """\
alta: el número que ve el usuario es incorrecto o aparece un error. Ej.: [Margen] / [Ventas] devuelve infinito si Ventas = 0.
media: el número es correcto en algunos contextos y engañoso en otros. Ej.: un total que ignora un filtro del informe sin que el nombre lo diga.
baja: el resultado es correcto pero hay un riesgo de mantenimiento. Ej.: una constante de negocio escrita a mano en la fórmula (0.21 en vez de una medida [Tasa IVA])."""

# ---------------------------------------------------------------------------
# Few-shot: casos límite, con el razonamiento de por qué se eligió una acción.
# Los ejemplos 1 y 2 están completos. El 3 lo completás vos.
# ---------------------------------------------------------------------------
EJEMPLOS = [
    {
        "medida": "Margen % = [Margen] / [Ventas]",
        "decision": "reportar",
        "severidad": "alta",
        "razonamiento": (
            "Si una planta no tuvo ventas en el período, la división devuelve infinito y el visual "
            "muestra ∞. Es un resultado incorrecto visible. Fix: DIVIDE([Margen], [Ventas])."
        ),
    },
    {
        "medida": "Ventas Todas las Plantas = CALCULATE([Ventas], REMOVEFILTERS(Planta))",
        "decision": "omitir",
        "severidad": "-",
        "razonamiento": (
            "Parece un bug porque ignora el filtro de planta, pero es intencional: es el denominador "
            "de una participación y el nombre lo dice. Es un patrón aceptable, no un problema."
        ),
    },
    # HUECO 2 · Caso ambiguo. Pensá: ¿qué ve el analista si el precio de un despacho de 2 m3
    # pesa lo mismo que el de uno de 40 m3? Decidí "reportar" u "omitir", la severidad
    # (alta / media / baja, o "-" si omitís) y escribí el porqué en una o dos oraciones.
    {
        "medida": "Precio Promedio = AVERAGE(Despachos[Precio_m3])",
        "decision": "reportar",
        "severidad": "media",
        "razonamiento": "Diferentes cantidades de despacho pueden alterar el precio promedio final. " 
        "Esta formula deberia tener en cuenta ademas la cantidad despachada para el promedio final. "
        "Fix:  DIVIDE ( SUMX ( Despachos, Despachos[Precio_m3] * Despachos[m3] ), SUM ( Despachos[m3] ) )",
    },
]

# ---------------------------------------------------------------------------
# HUECO 3 · Delimitador de la entrada variable.
# Las instrucciones dicen "la medida está dentro de <...>". Elegí el nombre del tag
# (sin < >). Tiene que coincidir con el que usan las instrucciones de abajo.
# ---------------------------------------------------------------------------
TAG_MEDIDA = "medida"


def _lista(items):
    return "\n".join(f"- {i}" for i in items)


def _ejemplos():
    bloques = []
    for e in EJEMPLOS:
        bloques.append(
            "<example>\n"
            f"<{TAG_MEDIDA}>{e['medida']}</{TAG_MEDIDA}>\n"
            f"<razonamiento>{e['razonamiento']}</razonamiento>\n"
            f"<respuesta>decision: {e['decision']} | severidad: {e['severidad']}</respuesta>\n"
            "</example>"
        )
    return "<examples>\n" + "\n".join(bloques) + "\n</examples>"


def construir_prompt(medida_dax: str) -> str:
    """Arma el contenido del mensaje user para revisar UNA medida."""
    return f"""<instrucciones>
Revisá la medida DAX que está dentro de <medida>. Primero razoná dentro de <razonamiento>
y después respondé dentro de <respuesta> con: decision (reportar u omitir), severidad,
ubicación, problema y fix sugerido.
</instrucciones>

<criterios>
Reportá:
{_lista(REPORTAR)}

No reportes:
{_lista(NO_REPORTAR)}
</criterios>

<severidad>
{SEVERIDAD}
</severidad>

{_ejemplos()}

<{TAG_MEDIDA}>{medida_dax}</{TAG_MEDIDA}>"""


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    print("SYSTEM:\n" + SYSTEM + "\n")
    print("USER:\n" + construir_prompt("Ticket Promedio = [Ventas] / COUNTROWS(Despachos)"))
