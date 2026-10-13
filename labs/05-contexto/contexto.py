"""Lab 05 · Armar el contexto para preguntarle a Claude sobre un modelo TMDL.

Completá los 3 huecos marcados con ___ y corré: python check.py
No hace falta API key: check.py revisa el request que armás, no llama a la API.
Para ver cómo queda el request: python contexto.py
"""
import json

from datos import PREGUNTA, RESULTADO_GET_MEDIDA, TMDL_MODELO

MODELO = "claude-sonnet-5-5"
SYSTEM = (
    "Sos un analista que revisa modelos semánticos de Power BI. "
    "Respondé solo con lo que está en el TMDL y en los hechos del caso; si algo no está, decilo."
)


# ---------------------------------------------------------------------------
# HUECO 1 · Hechos del caso (guía 5.1).
# Es una sesión larga con un cliente. Para no llenar el contexto, el historial viejo
# se va a RESUMIR. Lo que marques True se copia tal cual, en cada request, en un bloque
# <hechos_del_caso> que el resumen no toca.
#   True  = dato transaccional que un resumen puede volver vago (montos, fechas, ids, lo que
#           el cliente dijo que espera).
#   False = se puede resumir o perder sin que cambie la respuesta.
# ---------------------------------------------------------------------------
ES_HECHO_DEL_CASO = {
    "El cliente necesita el reporte de ventas validado antes del 2026-11-13": True,
    "[Ventas Netas] de octubre da $1.250.430 y el ERP dice $1.310.000": True,
    "La diferencia aparece en la partición fVentas-2026-10": True,
    "Claude explicó en tres párrafos qué es un modelo estrella": False,
    "El cliente saludó y agradeció la ayuda del equipo": False,
}


def armar_hechos() -> str:
    return "\n".join(f"- {hecho}" for hecho, va in ES_HECHO_DEL_CASO.items() if va)


# ---------------------------------------------------------------------------
# HUECO 2 · Recortar el resultado de una tool (guía 5.1).
# get_medida devuelve 20 campos (mirá RESULTADO_GET_MEDIDA en datos.py). Cada resultado
# queda en el historial y se reenvía en todos los requests que siguen.
# Leé la PREGUNTA (en datos.py) y quedate solo con los campos que Claude necesita para
# contestarla. Escribilos como una tupla de strings: ("campo1", "campo2", ...).
# ---------------------------------------------------------------------------
def recortar_resultado(resultado: dict) -> dict:
    campos = (
    "nombre",
    "tabla",
    "expresion",
    "dependencias",
    "dataType"
    )
    return {campo: resultado[campo] for campo in campos}


# ---------------------------------------------------------------------------
# HUECO 3 · Armar el request (guía 5.1 + long context prompting + prompt caching).
# Tres bloques de texto para el mensaje del usuario:
#   - bloque_tmdl:     el modelo entero. LARGO y no cambia entre preguntas.
#   - bloque_hechos:   los hechos del caso. CORTO y cambia en cada turno.
#   - bloque_pregunta: la pregunta de este turno. CORTA y cambia siempre.
# ---------------------------------------------------------------------------
def armar_request(tmdl: str, hechos: str, pregunta: str) -> dict:
    bloque_tmdl = {"type": "text", "text": f"<modelo_tmdl>\n{tmdl}\n</modelo_tmdl>"}
    bloque_hechos = {"type": "text", "text": f"<hechos_del_caso>\n{hechos}\n</hechos_del_caso>"}
    bloque_pregunta = {"type": "text", "text": pregunta}

    # 3a · Prompt caching: el breakpoint va al final de lo que NO cambia entre requests.
    #      ¿Qué bloque? (escribí el nombre de la variable)
    bloque_tmdl["cache_control"] = {"type": "ephemeral"}

    return {
        "model": MODELO,
        "max_tokens": 2048,
        # 3b · ¿Con qué clave (string) va el system prompt, y a qué nivel? (Día 01)
        "system": SYSTEM,
        "messages": [
            # 3c · Ordená los tres bloques (nombres de variable, separados por coma).
            #      Pista: documentos largos arriba, la pregunta al final.
            {"role": "user", "content": [bloque_tmdl, bloque_hechos, bloque_pregunta]},
        ],
    }


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    recortado = recortar_resultado(RESULTADO_GET_MEDIDA)
    antes, despues = len(json.dumps(RESULTADO_GET_MEDIDA)), len(json.dumps(recortado))
    print(f"tool_result: {antes} → {despues} caracteres\n")
    req = armar_request(TMDL_MODELO, armar_hechos(), PREGUNTA)
    print("Claves de primer nivel:", list(req))
    print("Bloques del mensaje user, en orden:")
    for i, b in enumerate(req["messages"][0]["content"]):
        cache = "  ← cache_control" if "cache_control" in b else ""
        print(f"  [{i}] {len(b['text']):>5} caracteres · {b['text'][:45]!r}{cache}")
