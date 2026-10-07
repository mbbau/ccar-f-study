"""Lab 04 · Extraer un pedido de hormigón de un email a JSON validado.

Completá los 3 huecos marcados con ___ y corré: python check.py
No hace falta API key: check.py simula lo que devolvería Claude.
"""
import json

# ---------------------------------------------------------------------------
# La tool de extracción. Claude no "ejecuta" nada: su input_schema ES el formato
# de salida. Lo que vuelve en el bloque tool_use.input es el pedido extraído.
# ---------------------------------------------------------------------------
# HUECO 1 · Diseño del schema. Tres decisiones:
#   a) fecha_entrega: muchos emails no la dicen. ¿Qué "type" le das para que Claude
#      pueda devolver null en vez de inventar una fecha? (pista: puede ser una lista)
#   b) tipo_hormigon: agregá al enum el valor para lo que no está en la lista.
#   c) tipo_hormigon_detalle: el texto libre que acompaña a ese valor. ¿Qué "type"?
TOOL_PEDIDO = {
    "name": "registrar_pedido",
    "description": (
        "Registra un pedido de hormigón extraído de un email de un cliente. "
        "Usá null en cualquier campo que el email no mencione: nunca inventes valores."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "obra": {"type": "string", "description": "Nombre de la obra o dirección de entrega."},
            "fecha_entrega": {
                "type": ["string", "null"],
                "description": "Fecha de entrega en formato AAAA-MM-DD, o null si el email no la dice.",
            },
            "tipo_hormigon": {
                "type": "string",
                "enum": ["H21", "H25", "H30", "other"],
                "description": "Resistencia pedida. Si no es ninguna de la lista, usá el valor genérico y explicá en tipo_hormigon_detalle.",
            },
            "tipo_hormigon_detalle": {
                "type": ["string", "null"],
                "description": "Texto libre cuando tipo_hormigon no está en la lista; null en otro caso.",
            },
            "lineas": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "descripcion": {"type": "string"},
                        "m3": {"type": "number"},
                    },
                    "required": ["descripcion", "m3"],
                    "additionalProperties": False,
                },
            },
            "total_m3_declarado": {"type": ["number", "null"], "description": "El total que escribe el cliente, si lo escribe."},
        },
        "required": ["obra", "fecha_entrega", "tipo_hormigon", "tipo_hormigon_detalle", "lineas", "total_m3_declarado"],
        "additionalProperties": False,
    },
}

# Para el examen: forzar esta tool con tool_choice={"type": "tool", "name": "registrar_pedido"}.
# En la API actual, Opus 5.5 / Sonnet 5.5 rechazan "any" y "tool" (400): ahí se usa
# tool_choice "auto" + strict: True, o structured outputs (output_config.format).
TOOL_CHOICE_EXAMEN = {"type": "tool", "name": "registrar_pedido"}


# ---------------------------------------------------------------------------
# HUECO 2 · Validación semántica.
# El schema garantiza la FORMA (tipos, campos), no que los números cierren.
# Calculá el total de las líneas y comparalo con el declarado por el cliente.
# Si el cliente no declaró total (None), no hay nada que comparar.
# ---------------------------------------------------------------------------
def validar_semantica(pedido: dict) -> list[str]:
    errores = []
    total_calculado = sum(l["m3"] for l in pedido["lineas"])
    declarado = pedido["total_m3_declarado"]
    if declarado is not None and total_calculado != declarado:
        errores.append(
            f"suma: las líneas suman {total_calculado} m3 pero el total declarado es {declarado} m3"
        )
    return errores


# ---------------------------------------------------------------------------
# HUECO 3 · ¿Sirve reintentar?
# a) Para cada tipo de error, ¿un reintento con el error como feedback lo puede arreglar?
#    True o False.
# b) El mensaje de reintento tiene que llevar las 3 piezas que pide la guía (4.4).
#    Completá las ___ con: documento, extraccion_json, errores_txt.
# ---------------------------------------------------------------------------
REINTENTABLE = {
    "formato": True,     # la fecha vino como "15/11" en vez de "2026-11-15"
    "ausente": False,     # falta la obra y el email no la menciona en ningún lado
}


def armar_reintento(documento: str, extraccion: dict, errores: list[str]) -> str:
    extraccion_json = json.dumps(extraccion, ensure_ascii=False)
    errores_txt = "\n".join(f"- {e}" for e in errores)
    return f"""<email>{documento}</email>
<extraccion_anterior>{extraccion_json}</extraccion_anterior>
<errores>
{errores_txt}
</errores>
Corregí la extracción para resolver los errores. Si un dato no está en el email, devolvé null."""
