"""Lab 02 · Diseño de tools. Completá los 3 huecos marcados con ___.

    python check.py      -> te corrige (sin API key)

Leé primero la sección 2 y 5 de la lección 0002.
"""
from dwh import PermisoError, TransitorioError, ValidacionError, consultar_sql, listar_tablas

# ---------------------------------------------------------------------------
# HUECO 1 · Descriptions
# Escribí la description de cada tool (mínimo 3 oraciones, en español):
#   qué hace · cuándo usarla (y cuándo NO) · qué devuelve · límites.
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "dwh_consultar_sql",
        "description": "___",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "Consulta SELECT en dialecto SQLite. Ej.: SELECT planta, SUM(m3) FROM despachos GROUP BY planta",
                }
            },
            "required": ["sql"],
        },
    },
    {
        "name": "dwh_listar_tablas",
        "description": "___",
        "input_schema": {"type": "object", "properties": {}},
    },
]

# ---------------------------------------------------------------------------
# HUECO 2 · Clasificación de errores
# Para cada tipo de error: (categoria, reintentable). Reemplazá ___ por True o False.
#   ¿Tiene sentido que Claude reintente EXACTAMENTE lo mismo?
# ---------------------------------------------------------------------------
ERRORES = {
    ValidacionError: ("validacion", ___),
    PermisoError: ("permiso", ___),
    TransitorioError: ("transitorio", ___),
}

# ---------------------------------------------------------------------------
# HUECO 3 · Qué le sugerís a Claude en cada caso (mensaje accionable, 1 oración)
# ---------------------------------------------------------------------------
SUGERENCIAS = {
    "validacion": "___",
    "permiso": "___",
    "transitorio": "___",
}


# --- Ya resuelto: usa tus huecos ---------------------------------------------
def run_tool(block) -> dict:
    funciones = {"dwh_consultar_sql": lambda i: consultar_sql(i["sql"]),
                 "dwh_listar_tablas": lambda i: listar_tablas()}
    try:
        contenido = funciones[block.name](block.input)
        return {"type": "tool_result", "tool_use_id": block.id, "content": contenido}
    except tuple(ERRORES) as e:
        categoria, reintentable = ERRORES[type(e)]
        return {
            "type": "tool_result",
            "tool_use_id": block.id,
            "is_error": True,
            "content": f"[{categoria}] {e} Reintentable: {'sí' if reintentable else 'no'}. {SUGERENCIAS[categoria]}",
        }
