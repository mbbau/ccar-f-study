"""Cliente falso que imita la forma de client.messages.create() del SDK de Anthropic.
Sirve para practicar el loop sin API key y para que check.py te corrija."""
import copy
from types import SimpleNamespace as NS


def text(t):
    return NS(type="text", text=t)


def tool_use(id_, sql):
    return NS(type="tool_use", id=id_, name="query_dwh", input={"sql": sql})


def resp(stop_reason, *blocks):
    return NS(stop_reason=stop_reason, content=list(blocks), role="assistant")


class FakeClient:
    """Devuelve respuestas guionadas en orden y guarda una copia de cada request."""

    def __init__(self, script):
        self._script = list(script)
        self.calls = []
        self.messages = self  # para poder llamar client.messages.create(...)

    def create(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))
        if not self._script:
            raise RuntimeError("FakeClient: el loop hizo más llamadas de las esperadas.")
        return self._script.pop(0)


# --- Guiones -----------------------------------------------------------------
def happy_path():
    return [
        resp("tool_use",
             text("Voy a consultar el DWH."),
             tool_use("toolu_01", "SELECT planta, SUM(m3) FROM despachos GROUP BY planta")),
        resp("end_turn", text("Córdoba Norte lideró con 99 m3.")),
    ]
