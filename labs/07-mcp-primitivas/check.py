"""Autocorrector del Lab 07. Corré: python check.py"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

try:
    import primitivas as p
except SyntaxError as e:
    print(f"❌ Error de sintaxis en primitivas.py, línea {e.lineno}: ¿faltan comillas, una coma o una llave?")
    sys.exit()
except NameError as e:
    print(f"❌ {e}: ¿le faltan comillas a un string? \"tool\", \"C\", \"client\" van entre comillas.")
    sys.exit()

ok = []


def check(nombre, cond, pista):
    ok.append(bool(cond))
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


print("\nHUECO 1 · ¿Tool, resource o prompt?")
ESPERADO = {
    "Catálogo de tablas y columnas del DWH (esquema)": ("resource",
        "es un catálogo de solo lectura: la guía (2.4) lo pone como ejemplo de resource. "
        "Así el agente ve qué hay sin gastar tool calls explorando"),
    "Ejecutar una consulta SELECT y devolver las filas": ("tool",
        "aunque no modifica nada, la elige el modelo en medio del loop con argumentos que él arma (la consulta)"),
    "Refrescar la partición fVentas-2026-10 del modelo": ("tool", "es una acción con efecto: la invoca el modelo"),
    "Plantilla 'Revisá esta medida DAX' que el analista elige con /": ("prompt",
        "una plantilla que elige el usuario es un prompt (en Claude Code aparece como comando /)"),
    "Diccionario de negocio: la definición de cada KPI": ("resource", "contenido de referencia, de solo lectura"),
    "Crear un ticket en Jira con el error de carga": ("tool",
        "acción con efecto. Y para Jira, la guía (2.4) prefiere un servidor de la comunidad antes que uno propio"),
    "Archivo con el último log de refresh del modelo": ("resource", "un archivo para leer: contexto, no acción"),
    "Plantilla 'Informe mensual de calidad de datos' con el mes como argumento": ("prompt",
        "los prompts pueden tener argumentos; lo que importa es que lo elige el usuario"),
    "Enviarle al cliente el informe por mail": ("tool", "acción con efecto hacia afuera"),
    "Lista fija de los reportes que dependen de cada modelo (lineage)": ("resource",
        "catálogo fijo de solo lectura. Exponerlo como tool es la trampa del día"),
}
C = p.CLASIFICACION
for cap, (tipo, pista) in ESPERADO.items():
    check(f"{cap[:55]}", C.get(cap) == tipo, f"pusiste {C.get(cap)!r}. Es \"{tipo}\": {pista}")

print("\nHUECO 2 · El flujo completo")
O = p.ORDEN
check("2 · el orden completo es correcto", O == ["C", "E", "F", "A", "D", "B"],
      f"pusiste {O}. Pistas abajo")
check("arranca con la conexión (C)", O[:1] == ["C"], "antes de cualquier otra cosa, el client se conecta y averigua qué ofrece el servidor")
check("tools/list (E) antes del request (F)", "E" in O and "F" in O and O.index("E") < O.index("F"),
      "el host no puede pasarle a la API tools que todavía no conoce")
check("el request con tools (F) antes del tool_use (A)", "F" in O and "A" in O and O.index("F") < O.index("A"),
      "Claude solo puede pedir tools que están en el parámetro tools del request (Día 05: lo que no está, no existe)")
check("tools/call (D) después del tool_use (A) y antes del tool_result (B)",
      all(x in O for x in "ADB") and O.index("A") < O.index("D") < O.index("B"),
      "Claude pide, el client ejecuta en el servidor, y recién ahí hay resultado para devolver")
check("2b · el que llama al servidor es el client", p.QUIEN_LLAMA_AL_SERVIDOR == "client",
      f"pusiste {p.QUIEN_LLAMA_AL_SERVIDOR!r}. Claude nunca habla con el servidor: solo emite tool_use. "
      "El client (dentro del host) hace el tools/call")

print("\nHUECO 3 · Del resultado MCP al tool_result")


def probar(resultado):
    try:
        return p.mensaje_resultado("toolu_01", resultado), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


bien = {"content": [{"type": "text", "text": "37 remitos Pendiente, $59.570"}], "isError": False}
mal = {"content": [{"type": "text", "text": "Timeout: el DWH no respondió en 30 s"}], "isError": True}
m, err = probar(bien)
es_dict = err is None and isinstance(m, dict)
if not es_dict:
    err = err or f"devolviste {m!r}: tiene que ser un diccionario {{\"role\": ..., \"content\": [...]}}"
check("devuelve un mensaje (dict)", es_dict, err)
m = m if es_dict else {}
check("role user", m.get("role") == "user",
      f"pusiste {m.get('role')!r}. El resultado lo manda tu programa: role \"user\" (no assistant, no system)")
cont = m.get("content")
check("content es una lista de bloques", isinstance(cont, list) and len(cont) == 1 and isinstance(cont[0], dict),
      f"content del mensaje = {cont!r}. Es una LISTA con un bloque (un dict) adentro: [ {{...}} ]")
b = cont[0] if isinstance(cont, list) and cont and isinstance(cont[0], dict) else {}
check("el bloque es type tool_result", b.get("type") == "tool_result",
      f"type = {b.get('type')!r}. Claude pide con tool_use; vos contestás con tool_result")
check("tool_use_id correcto", b.get("tool_use_id") == "toolu_01",
      f"tool_use_id = {b.get('tool_use_id')!r}. Usá el parámetro tool_use_id (el campo se llama así, no tool_id)")
check("el texto va en el content del bloque", b.get("content") == "37 remitos Pendiente, $59.570",
      f"content del bloque = {b.get('content')!r}. Usá la variable texto")
m2, err2 = probar(mal)
b2 = (m2 or {}).get("content", [{}])[0] if isinstance(m2, dict) and isinstance(m2.get("content"), list) and m2["content"] else {}
check("si el servidor falló, is_error True", isinstance(b2, dict) and b2.get("is_error") is True,
      err2 or "con isError True en MCP, el bloque lleva \"is_error\": True (con guion bajo). Usá la variable fallo")

print(f"\nResultado: {sum(ok)}/{len(ok)}")
if all(ok):
    print("\n🎉 Listo: primitivas por quién las controla, el flujo host → client → server → Claude, "
          "y el tool_result escrito sin esqueleto.\n   Corré python primitivas.py para verlo junto.")
