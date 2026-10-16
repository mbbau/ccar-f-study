"""Lab 07 · Un servidor MCP para el DWH de la hormigonera: primitivas y flujo.

Completá los huecos marcados con ___ y corré: python check.py
No hace falta API key ni el SDK de MCP: check.py revisa lo que decidís, no levanta el servidor.
Para ver el resultado: python primitivas.py
"""
___ = "___"  # marca de hueco: no la borres


# ---------------------------------------------------------------------------
# HUECO 1 · ¿Tool, resource o prompt? (lección, secciones 2 y 3)
# Vas a exponer estas capacidades del DWH en un servidor MCP. Para cada una escribí
# "tool", "resource" o "prompt". La pregunta que decide: ¿QUIÉN la elige?
#   - el modelo, en medio del loop, para hacer algo o calcular algo  → "tool"
#   - la aplicación, para darle contexto de solo lectura (tiene URI)  → "resource"
#   - el usuario, que elige una plantilla (por ejemplo, con /)          → "prompt"
# ---------------------------------------------------------------------------
CLASIFICACION = {
    "Catálogo de tablas y columnas del DWH (esquema)": "resource",
    "Ejecutar una consulta SELECT y devolver las filas": "tool",
    "Refrescar la partición fVentas-2026-10 del modelo": "tool",
    "Plantilla 'Revisá esta medida DAX' que el analista elige con /": "prompt",
    "Diccionario de negocio: la definición de cada KPI": "resource",
    "Crear un ticket en Jira con el error de carga": "tool",
    "Archivo con el último log de refresh del modelo": "resource",
    "Plantilla 'Informe mensual de calidad de datos' con el mes como argumento": "prompt",
    "Enviarle al cliente el informe por mail": "tool",
    "Lista fija de los reportes que dependen de cada modelo (lineage)": "resource",
}


# ---------------------------------------------------------------------------
# HUECO 2 · El flujo completo (lección, sección 4)
# Estos pasos están desordenados. Escribí las letras en el orden en que pasan,
# desde que arranca Claude Code hasta que Claude recibe el resultado de la tool.
# ---------------------------------------------------------------------------
PASOS = {
    "A": "Claude responde con stop_reason \"tool_use\" y un bloque tool_use con name e input",
    "B": "El host agrega a messages un mensaje user con el bloque tool_result",
    "C": "El client se conecta al servidor y averigua qué capabilities tiene (tools, resources, prompts)",
    "D": "El client llama tools/call al servidor con el nombre de la tool y sus argumentos",
    "E": "El client pide tools/list y recibe name, description e inputSchema de cada tool",
    "F": "El host pone esas tools en el parámetro tools del request a la Messages API",
}
ORDEN = ["C", "E", "F", "A", "D", "B"]

# 2b · ¿Quién le manda el tools/call al servidor? Escribí "claude", "client" o "usuario".
QUIEN_LLAMA_AL_SERVIDOR = "client"


# ---------------------------------------------------------------------------
# HUECO 3 · Del resultado MCP al tool_result (Día 01 + lección, sección 4)
# El servidor contestó el tools/call con un resultado MCP como este:
#     {"content": [{"type": "text", "text": "37 remitos Pendiente, $59.570"}], "isError": False}
# Escribí el MENSAJE que el host agrega a messages para devolvérselo a Claude.
# Sin esqueleto esta vez: es lo que escribiste en el calentamiento.
#   - Usá tool_use_id (el id del bloque tool_use que mandó Claude).
#   - El texto va en el content del bloque: resultado_mcp["content"][0]["text"].
#   - Ojo: MCP lo llama "isError"; la Messages API lo llama "is_error".
# ---------------------------------------------------------------------------
def mensaje_resultado(tool_use_id: str, resultado_mcp: dict) -> dict:
    texto = resultado_mcp["content"][0]["text"]
    fallo = resultado_mcp["isError"]
    return {
            "role": "user", 
            "content":
                [{"type":"tool_result", 
                  "tool_use_id":tool_use_id, 
                  "content":texto,
                  "is_error": fallo}
                ]
            }


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    for tipo in ("tool", "resource", "prompt"):
        print(f"\n{tipo.upper()}S")
        for cap, t in CLASIFICACION.items():
            if t == tipo:
                print(f"  - {cap}")
    print("\nFlujo:")
    for i, letra in enumerate(ORDEN, 1):
        print(f"  {i}. {PASOS.get(letra, '___')}")
    ok = {"content": [{"type": "text", "text": "37 remitos Pendiente, $59.570"}], "isError": False}
    print("\nMensaje que agregás a messages:\n ", mensaje_resultado("toolu_01", ok))
