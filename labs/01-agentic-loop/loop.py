"""Lab 01 · Agentic loop con stop_reason.

Completá los TODO. Corré:
    python check.py          -> te corrige contra 6 escenarios (sin API key)
    python loop.py --mock    -> corre el happy path con el cliente falso
    python loop.py           -> corre contra la API real (necesita ANTHROPIC_API_KEY)
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")  # emojis/acentos en la consola de Windows

from dwh import SCHEMA, query_dwh

MODEL = "claude-opus-5-5"  # cambialo por el modelo que tengas disponible

TOOLS = [
    {
        "name": "query_dwh",
        "description": (
            "Ejecuta una consulta SQL SELECT de solo lectura contra el DWH de despachos de hormigón "
            f"y devuelve las filas como texto. Esquema: {SCHEMA}. "
            "Usala cuando necesites datos numéricos de despachos; no inventes cifras."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"sql": {"type": "string", "description": "Consulta SQL SELECT (dialecto SQLite)."}},
            "required": ["sql"],
        },
    }
]


def run_tool(block) -> dict:
    """Recibe un bloque tool_use y devuelve UN bloque tool_result (dict).

    TODO 1:
      - Si block.name == "query_dwh", ejecutá query_dwh(block.input["sql"]).
      - Devolvé {"type": "tool_result", "tool_use_id": ..., "content": ...}.
      - Si la tool lanza una excepción, NO cortes el loop: devolvé el mensaje de error
        con "is_error": True para que Claude pueda corregirse.
    """
    if block.name == "query_dwh":
        try:
            result = query_dwh(block.input["sql"])
            return {
                "type": "tool_result",
                "tool_use_id": block.tool_use_id,
                "content": {"result": result, "is_error": False},
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": block.tool_use_id,
                "content": {"result": str(e), "is_error": True},
            }

    raise NotImplementedError("TODO 1")


def run_agent(client, question: str, max_iterations: int = 10) -> str:
    """Loop agéntico. Devuelve el texto final de Claude.

    TODO 2: implementá el while/for que:
      a) llama client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
      b) imprime response.stop_reason en cada vuelta
      c) decide QUÉ HACER según stop_reason (no según el texto):
           - "tool_use"   -> agregá la respuesta como mensaje assistant, ejecutá TODAS las tools
                             y mandá TODOS los tool_result en UN solo mensaje user. Seguí el loop.
           - "end_turn"   -> devolvé el texto final.
           - "max_tokens" -> no ejecutes tools a medias; devolvé el texto con un aviso de truncado.
           - otro valor   -> devolvé el texto que haya (o un aviso).
      d) no supera max_iterations llamadas (guardrail contra loops infinitos);
         si se alcanza, devolvé un aviso (no lances excepción).
    """
    messages = [{"role": "user", "content": question}]
    iteration = 0
    while iteration < max_iterations:
        response = client.messages.create(model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages)
        print(response.stop_reason)
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            results = [run_tool(b) for b in response.content if b.type == "tool_use"]
            messages.append({"role": "user", "content": results})
        elif response.stop_reason == "end_turn":
            return final_text(response)
        elif response.stop_reason == "max_tokens":
            return final_text(response) + "\n\n[AVISO: Respuesta truncada por límite de tokens.]"
        else:
            return final_text(response) + f"\n\n[AVISO: Detenido por stop_reason={response.stop_reason}]"
        iteration += 1
        messages.append({"role": "user", "content": {"type": "text", "text": "Continuá, por favor."}})
##    raise NotImplementedError("TODO 2")
    return "[AVISO: Se alcanzó el máximo de iteraciones sin obtener una respuesta final.]"
    


def final_text(response) -> str:
    return "".join(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    q = "¿Qué planta despachó más m3 en septiembre y cuánto facturó?"
    if "--mock" in sys.argv:
        from mock_client import FakeClient, happy_path
        client = FakeClient(happy_path())
    else:
        import anthropic
        client = anthropic.Anthropic()
    print("\nRespuesta final:\n", run_agent(client, q))
