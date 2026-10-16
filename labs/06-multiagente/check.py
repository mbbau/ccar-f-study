"""Autocorrector del Lab 06. Corré: python check.py"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

try:
    import multiagente as m
except SyntaxError as e:
    print(f"❌ Error de sintaxis en multiagente.py, línea {e.lineno}: ¿faltan comillas o una coma?")
    sys.exit()
except NameError as e:
    print(f"❌ {e}: ¿le faltan comillas a un string? Los nombres de tools y modelos van entre comillas.")
    sys.exit()

from datos import HISTORIAL_COORDINADOR, RESUMEN_CONSULTOR, RESUMEN_EXPLORADOR

ok = []
H = m.___


def check(nombre, cond, pista):
    ok.append(bool(cond))
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


def tiene_hueco(x):
    if isinstance(x, (list, tuple)):
        return any(tiene_hueco(i) for i in x)
    if isinstance(x, dict):
        return any(tiene_hueco(v) for v in x.values())
    return x == H


print("\nHUECO 1 · Definir los subagentes")
S = m.SUBAGENTES
exp, con, red = S["explorador_tmdl"], S["consultor_dwh"], S["redactor"]
LECTURA = {"Read", "Grep", "Glob"}
PELIGROSAS = {"Write", "Edit", "Bash"}
check("explorador: solo tools de lectura", exp["tools"] and not tiene_hueco(exp["tools"]) and set(exp["tools"]) <= LECTURA,
      f"tiene {exp['tools']}. Solo busca y lee TMDL: Read, Grep, Glob. Write/Edit/Bash le darían poder para "
      "romper el modelo sin necesitarlo (mínimo privilegio)")
check("explorador: puede buscar (Grep o Glob)", set(exp["tools"]) & {"Grep", "Glob"},
      "para encontrar una medida entre muchos archivos necesita buscar, no solo leer")
check("consultor: solo query_sql", con["tools"] == ["query_sql"],
      f"tiene {con['tools']}. Su trabajo es consultar el DWH; Bash le daría acceso a la terminal entera")
check("redactor: puede escribir el informe", "Write" in red["tools"],
      f"tiene {red['tools']}. Tiene que crear el archivo del informe")
check("redactor: no consulta datos por su cuenta", not ({"query_sql", "Bash"} & set(red["tools"])),
      "trabaja con los hallazgos que le pasa el coordinador; si consulta por su cuenta, se salta el hub")
MODELOS = {"haiku", "sonnet", "opus", "fable", "inherit"}
modelos = [d["model"] for d in S.values()]
check("los tres modelos son alias válidos", all(x in MODELOS for x in modelos),
      f"pusiste {modelos}. Alias: \"haiku\", \"sonnet\", \"opus\", \"fable\" (o \"inherit\")")
check("el explorador no usa el modelo más caro", exp["model"] not in ("opus", "fable"),
      "buscar en archivos es trabajo voluminoso y simple: la doc recomienda Haiku para tareas de subagente "
      "de baja latencia y bajo costo")
check("no todo con el mismo modelo grande", not all(x in ("opus", "fable") for x in modelos),
      "trampa del día: elegir el modelo más potente para todo. Multi-agente ya gasta ~15× los tokens de un chat")
check("el coordinador puede delegar (Agent o Task)", {"Agent", "Task"} & set(m.COORDINADOR_ALLOWED_TOOLS),
      f"tiene {m.COORDINADOR_ALLOWED_TOOLS}. Para lanzar subagentes, allowedTools tiene que incluir la tool "
      "Agent (en la guía: \"Task\")")

print("\nHUECO 2 · El prompt para el redactor")
V = m.VA_EN_EL_PROMPT
if tiene_hueco(V):
    print("   (quedan ___ en VA_EN_EL_PROMPT: completalos con True o False)")
check("lleva el objetivo", V["objetivo"] is True, "sin objetivo el redactor no sabe qué informe escribir ni para quién")
check("lleva el hallazgo del explorador", V["hallazgo_explorador"] is True,
      "el redactor NO hereda nada del coordinador: si no está en el prompt, no existe para él")
check("lleva el hallazgo del consultor", V["hallazgo_consultor"] is True,
      "ídem: los resultados de otros agentes se pasan completos en el prompt (guía 1.3)")
check("lleva el formato de salida", V["formato_de_salida"] is True,
      "cada subagente necesita objetivo, formato de salida, tools y límites claros (Anthropic, multi-agent research)")
check("NO lleva el historial completo", V["historial_completo"] is False,
      "trampa del día: pasar todo 'por las dudas'. Es ruido (logs de refresh, saludos) y anula el aislamiento de contexto")
check("NO dice 'acordate de antes'", V["acordate_de_antes"] is False,
      "los subagentes no comparten memoria entre invocaciones: 'la vez anterior' no existe para él")
p = m.prompt_para_redactor()
check("las fuentes llegan textuales al prompt", "fVentas.tmdl, línea 41" in p and "SELECT SUM(importe)" in p,
      "con el contenido viaja la fuente (archivo, consulta): así el informe conserva la atribución")
largo_hist = sum(len(str(x)) for x in HISTORIAL_COORDINADOR)
check("el prompt es mucho más chico que el historial", len(p) < largo_hist / 5,
      f"prompt {len(p)} caracteres vs. historial {largo_hist}")

print("\nHUECO 3 · Dos subagentes en paralelo")
t = m.turno_coordinador()
check("3a · el turno del coordinador es role assistant", t["role"] == "assistant",
      f"pusiste {t['role']!r}. Lo que genera el modelo (el coordinador) es siempre un mensaje assistant")
check("3a · los dos pedidos son bloques tool_use", [b["type"] for b in t["content"]] == ["tool_use", "tool_use"],
      f"pusiste {[b['type'] for b in t['content']]}. Llamar a Agent es una tool como cualquier otra: Claude la pide con tool_use")
check("3a · en paralelo = dos tool_use en UNA respuesta", len(t["content"]) == 2,
      "guía 1.3: varios Agent/Task en una misma respuesta, no uno por turno")
msgs = m.mensajes_con_resultados()
check("3b · es UN solo mensaje", len(msgs) == 1,
      "todos los resultados de un turno van juntos, en un único mensaje")
r = msgs[0]
check("3b · role user", r["role"] == "user",
      f"pusiste {r['role']!r}. Los resultados de tools los manda tu programa: role \"user\"")
tipos = [b["type"] for b in r["content"]]
check("3b · dos bloques tool_result", tipos == ["tool_result", "tool_result"],
      f"pusiste {tipos}. Claude pide con tool_use, vos respondés con tool_result")
ids = [b["tool_use_id"] for b in r["content"]]
check("3b · cada tool_use_id apunta a su pedido", ids == ["toolu_01", "toolu_02"],
      f"pusiste {ids}. El resultado del explorador responde al tool_use \"toolu_01\"; el del consultor, a \"toolu_02\"")

print(f"\nResultado: {sum(ok)}/{len(ok)}")
if all(ok):
    print("\n🎉 Listo: tools mínimas, modelos según la tarea, contexto explícito y paralelo en un turno."
          "\n   Corré python multiagente.py para ver qué recibe cada agente.")
