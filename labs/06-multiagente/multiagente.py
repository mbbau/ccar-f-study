"""Lab 06 · El agente "analista": un coordinador y tres subagentes.

Completá los huecos marcados con ___ y corré: python check.py
No hace falta API key: check.py revisa lo que configurás, no llama a la API.
Para ver qué recibe cada agente: python multiagente.py

Mapa:
                       ┌─ explorador_tmdl  (lee el modelo TMDL)
  cliente → coordinador┼─ consultor_dwh    (consulta el DWH con SQL)
                       └─ redactor         (escribe el informe final)

El coordinador es un programa con su loop (Día 01). Para delegar, llama a la tool "Agent"
(en la guía del examen se llama "Task": es la misma, la renombraron). Cada llamada arranca
un subagente con SU PROPIA ventana de contexto: no ve el historial del coordinador.
"""
from datos import (HISTORIAL_COORDINADOR, PREGUNTA_DEL_CLIENTE, RESUMEN_CONSULTOR,
                   RESUMEN_EXPLORADOR)

___ = "___"  # marca de hueco: no la borres

# Tools que existen en este sistema:
#   "Read", "Grep", "Glob"  → leer y buscar en archivos (solo lectura)
#   "Write", "Edit"         → crear y modificar archivos
#   "Bash"                  → ejecutar cualquier comando en la terminal
#   "query_sql"             → consultar el DWH (solo SELECT)
#   "Agent"                 → lanzar un subagente (alias viejo: "Task")
#
# Modelos (alias): "haiku" (el más rápido y barato) · "sonnet" · "opus" · "fable" (el más capaz y lento)


# ---------------------------------------------------------------------------
# HUECO 1 · Definir los subagentes (guía 1.3: AgentDefinition = description + prompt + tools).
# Para cada subagente completá:
#   "tools": la lista MÍNIMA que necesita para su trabajo. Ojo: si omitís "tools",
#            el subagente hereda TODAS las tools.
#   "model": el alias del modelo. Pensá en costo y latencia: ¿cuánto razonamiento pide la tarea?
# Y completá las tools del coordinador: ¿qué necesita para poder delegar?
# ---------------------------------------------------------------------------
SUBAGENTES = {
    "explorador_tmdl": {
        "description": "Busca medidas, columnas y filtros en los archivos TMDL del modelo. "
                       "Usalo para saber cómo se calcula algo en Power BI.",
        "prompt": "Sos un explorador de modelos TMDL. Buscá lo pedido y devolvé el hallazgo "
                  "con archivo y línea. No modifiques nada.",
        "tools": ["Read", "Grep", "Glob"],
        "model": "haiku",
    },
    "consultor_dwh": {
        "description": "Consulta el DWH con SQL de solo lectura. Usalo para contar o sumar datos reales.",
        "prompt": "Sos un analista SQL. Escribí la consulta mínima y devolvé el resultado con la consulta usada.",
        "tools": ["query_sql"],
        "model": "opus",
    },
    "redactor": {
        "description": "Escribe el informe final para el cliente a partir de hallazgos ya verificados.",
        "prompt": "Sos un redactor técnico. Escribí informes claros de una página; cada afirmación con su fuente.",
        "tools": ["Write", "Edit"],
        "model": "sonnet",
    },
}

COORDINADOR_ALLOWED_TOOLS = ["Agent", "Bash"]


# ---------------------------------------------------------------------------
# HUECO 2 · El prompt para el redactor (guía 1.3: el contexto se pasa EXPLÍCITO en el prompt).
# El redactor arranca con la ventana vacía: solo va a leer este string. Marcá True lo que
# tiene que ir en el prompt y False lo que no.
# ---------------------------------------------------------------------------
VA_EN_EL_PROMPT = {
    "objetivo": True,              # qué tiene que lograr y para quién
    "hallazgo_explorador": True,   # el resumen completo del explorador, con su fuente
    "hallazgo_consultor": True,    # el resultado SQL, con la consulta que lo produjo
    "formato_de_salida": True,     # qué forma tiene que tener el informe
    "historial_completo": False,    # toda la conversación del coordinador, "por las dudas"
    "acordate_de_antes": False,     # "usá lo que encontraste la vez anterior"
}

PIEZAS = {
    "objetivo": "<objetivo>Explicarle al cliente por qué [Ventas Netas] de octubre da $1.250.430 "
                "y el ERP $1.310.000.</objetivo>",
    "hallazgo_explorador": f"<hallazgo fuente=\"explorador_tmdl\">{RESUMEN_EXPLORADOR}</hallazgo>",
    "hallazgo_consultor": f"<hallazgo fuente=\"consultor_dwh\">{RESUMEN_CONSULTOR}</hallazgo>",
    "formato_de_salida": "<formato>Una página. Primero la causa en una oración; después la evidencia, "
                         "cada afirmación con su fuente entre corchetes.</formato>",
    "historial_completo": "<historial>" + "\n".join(str(m) for m in HISTORIAL_COORDINADOR) + "</historial>",
    "acordate_de_antes": "Usá lo que encontraste la vez anterior sobre este cliente.",
}


def prompt_para_redactor() -> str:
    return "\n\n".join(PIEZAS[k] for k, va in VA_EN_EL_PROMPT.items() if va is True)


# ---------------------------------------------------------------------------
# HUECO 3 · Lanzar dos subagentes en paralelo (guía 1.3) y devolverle los resultados.
# El explorador y el consultor no dependen uno del otro: el coordinador los lanza a la vez.
# Desde la API, una llamada a "Agent" es un tool_use como cualquier otro (Día 01).
#
# 3a · El turno del coordinador. ¿Qué role tiene y qué type tienen los dos bloques?
# 3b · Lo que tu programa agrega a messages cuando terminan los dos subagentes:
#      ¿qué role?, ¿qué type tiene cada bloque?, ¿con qué campo se correlaciona cada
#      resultado con su pedido? Escribí el id que corresponde (string).
# ---------------------------------------------------------------------------
def turno_coordinador() -> dict:
    return {
        "role": "assistant",
        "content": [
            {"type": "tool_use", "id": "toolu_01", "name": "Agent",
             "input": {"subagent_type": "explorador_tmdl",
                       "prompt": "Buscá cómo se calcula [Ventas Netas] y qué filtros aplica. "
                                 "Devolvé la expresión DAX con archivo y línea."}},
            {"type": "tool_use", "id": "toolu_02", "name": "Agent",
             "input": {"subagent_type": "consultor_dwh",
                       "prompt": "Sumá el importe de octubre 2026 en dwh.ventas agrupado por estado. "
                                 "Devolvé el resultado y la consulta usada."}},
        ],
    }


def mensajes_con_resultados() -> list:
    """Lista de mensajes que se agregan a messages después del turno del coordinador."""
    return [
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "toolu_01", "content": RESUMEN_EXPLORADOR},
            {"type": "tool_result", "tool_use_id": "toolu_02", "content": RESUMEN_CONSULTOR},
        ]},
    ]


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    largo_historial = sum(len(str(m)) for m in HISTORIAL_COORDINADOR)
    print(f"Ventana del coordinador: {len(HISTORIAL_COORDINADOR)} mensajes, ~{largo_historial} caracteres\n")
    for nombre, d in SUBAGENTES.items():
        print(f"{nombre:16} model={d['model']!s:7} tools={d['tools']}")
    p = prompt_para_redactor()
    print(f"\nLo ÚNICO que recibe el redactor (además de su system prompt): {len(p)} caracteres")
    print("-" * 70)
    print(p[:1500] + (" […]" if len(p) > 1500 else ""))
    print("-" * 70)
    print("\nTurno del coordinador:", [(b["type"], b["input"]["subagent_type"]) for b in turno_coordinador()["content"]])
    print("Mensajes que agregás después:", [(m["role"], [(b["type"], b["tool_use_id"]) for b in m["content"]])
                                          for m in mensajes_con_resultados()])
