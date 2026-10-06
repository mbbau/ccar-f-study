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
        "description": "Ejecuta una consulta de SQL de solo lectura (SELECT) sobre el data warehouse. La tabla de costos está resitrngida: consultarla devuelve un error de permiso. Usala cuando necesites devolver métricas relacionadas ventas o producción. No la uses para descubrir qué tablas o columnas existen; para eso está dwh_listar_tablas. Si no hay coincidencias devuelve 0 filas, lo cual no es un error",
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
        "description": "Devuelve todas las tablas que tenemos disponibles para utilizar en el DWH junto con sus columnas. Usala antes de escribir SQL para conocer las tablas a consultar. No la uses cuando necesitas ejecutar queries de SQL para obtener métricas del DWH.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

# ---------------------------------------------------------------------------
# HUECO 2 · Clasificación de errores
# Para cada tipo de error: (categoria, reintentable). Reemplazá ___ por True o False.
#   ¿Tiene sentido que Claude reintente EXACTAMENTE lo mismo?
# ---------------------------------------------------------------------------
ERRORES = {
    ValidacionError: ("validacion", False),
    PermisoError: ("permiso", False),
    TransitorioError: ("transitorio", True),
}

# ---------------------------------------------------------------------------
# HUECO 3 · Qué le sugerís a Claude en cada caso (mensaje accionable, 1 oración)
# ---------------------------------------------------------------------------
SUGERENCIAS = {
    "validacion": "Revisar el input schema y corregir el input antes de reintentar.",
    "permiso": "No reintentes: informá al usuario que ese dato está restringido.",
    "transitorio": "Esperar unos segundos, y volver a intentarlo.",
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
