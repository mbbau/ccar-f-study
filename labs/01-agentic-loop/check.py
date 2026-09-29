"""Autocorrector del Lab 01. Corré: python check.py"""
import traceback
import sys

sys.stdout.reconfigure(encoding="utf-8")  # emojis/acentos en la consola de Windows

from mock_client import FakeClient, happy_path, resp, text, tool_use
from loop import run_agent

results = []


def scenario(name):
    def deco(fn):
        def wrapper():
            try:
                fn()
                results.append((name, True, ""))
            except AssertionError as e:
                results.append((name, False, str(e)))
            except Exception:
                results.append((name, False, traceback.format_exc(limit=1).strip().splitlines()[-1]))
        return wrapper
    return deco


def last_user(call):
    return call["messages"][-1]


@scenario("1 · Happy path: tool_use -> end_turn")
def s1():
    c = FakeClient(happy_path())
    out = run_agent(c, "q")
    assert len(c.calls) == 2, f"se esperaban 2 llamadas, hubo {len(c.calls)}"
    msgs = c.calls[1]["messages"]
    assert msgs[-2]["role"] == "assistant", "antes del tool_result debe ir el mensaje assistant con el tool_use"
    u = last_user(c.calls[1])
    assert u["role"] == "user", "el tool_result va en un mensaje con role user"
    tr = u["content"][0]
    assert tr["type"] == "tool_result", "el primer bloque del mensaje user debe ser tool_result"
    assert tr["tool_use_id"] == "toolu_01", "tool_use_id debe ser el id del bloque tool_use"
    assert "Córdoba Norte" in tr["content"], "el content debe traer el resultado de query_dwh"
    assert "99 m3" in out, "debe devolver el texto final de end_turn"


@scenario("2 · Trampa: el texto dice 'listo' pero stop_reason es tool_use")
def s2():
    c = FakeClient([
        resp("tool_use", text("Listo, ya tengo la respuesta."), tool_use("toolu_07", "SELECT COUNT(*) FROM despachos")),
        resp("end_turn", text("Hay 6 despachos.")),
    ])
    out = run_agent(c, "q")
    assert len(c.calls) == 2, "cortaste por el texto: stop_reason era tool_use, había que seguir"
    assert "6 despachos" in out


@scenario("3 · Tools en paralelo: 2 tool_use en una misma respuesta")
def s3():
    c = FakeClient([
        resp("tool_use",
             tool_use("toolu_a", "SELECT SUM(m3) FROM despachos"),
             tool_use("toolu_b", "SELECT COUNT(DISTINCT cliente) FROM despachos")),
        resp("end_turn", text("156 m3 y 4 clientes.")),
    ])
    run_agent(c, "q")
    u = last_user(c.calls[1])
    ids = [b["tool_use_id"] for b in u["content"] if b.get("type") == "tool_result"]
    assert ids == ["toolu_a", "toolu_b"], f"todos los tool_result van en UN mensaje user, en orden; recibí {ids}"
    assert c.calls[1]["messages"][-2]["role"] == "assistant", "no metas mensajes entre tool_use y tool_result"


@scenario("4 · Error de tool: SQL inválido -> is_error y el loop sigue")
def s4():
    c = FakeClient([
        resp("tool_use", tool_use("toolu_x", "DROP TABLE despachos")),
        resp("tool_use", tool_use("toolu_y", "SELECT COUNT(*) FROM despachos")),
        resp("end_turn", text("Son 6.")),
    ])
    out = run_agent(c, "q")
    tr = last_user(c.calls[1])["content"][0]
    assert tr.get("is_error") is True, "si la tool falla, devolvé el error con is_error=True (no lances excepción)"
    assert len(c.calls) == 3 and "6" in out, "después del error Claude debe poder reintentar"


@scenario("5 · max_tokens con un tool_use cortado")
def s5():
    c = FakeClient([resp("max_tokens", text("Voy a consultar"), tool_use("toolu_cut", "SELECT"))])
    out = run_agent(c, "q")
    assert len(c.calls) == 1, "con max_tokens no ejecutes el tool_use (puede estar incompleto) ni sigas como si nada"
    assert isinstance(out, str) and out, "devolvé el texto parcial con un aviso de truncado"


@scenario("6 · Guardrail: max_iterations")
def s6():
    script = [resp("tool_use", tool_use(f"toolu_{i}", "SELECT 1")) for i in range(50)]
    c = FakeClient(script)
    run_agent(c, "q", max_iterations=3)
    assert len(c.calls) <= 3, f"hiciste {len(c.calls)} llamadas con max_iterations=3"


for fn in (s1, s2, s3, s4, s5, s6):
    fn()

print()
for name, ok, msg in results:
    print(("✅" if ok else "❌"), name, ("" if ok else f"\n     → {msg}"))
print(f"\n{sum(ok for _, ok, _ in results)}/{len(results)} escenarios OK")
