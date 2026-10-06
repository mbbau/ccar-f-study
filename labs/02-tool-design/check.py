"""Autocorrector del Lab 02. Corré: python check.py"""
import re
import sys
from types import SimpleNamespace as NS

sys.stdout.reconfigure(encoding="utf-8")

try:
    import tools
except NameError:
    print("❌ Todavía hay ___ sin completar en ERRORES (HUECO 2). Reemplazalos por True o False.")
    sys.exit()

ok = []


def check(nombre, cond, pista):
    ok.append(cond)
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


def oraciones(t):
    return len([s for s in re.split(r"[.!?]\s", t.strip()) if len(s.strip()) > 10])


print("\nHUECO 1 · Descriptions")
for t in tools.TOOLS:
    d = t["description"]
    check(f"{t['name']}: tiene description", d != "___" and len(d) > 0, "completá la description")
    check(f"{t['name']}: al menos 3 oraciones", oraciones(d) >= 3,
          f"tiene {oraciones(d)}; la doc recomienda 3-4 como mínimo")
    check(f"{t['name']}: dice cuándo usarla", bool(re.search(r"\b(us[aá]la|usar|cuando|cuándo)\b", d, re.I)),
          "agregá cuándo conviene usarla (y cuándo no)")
d_sql = tools.TOOLS[0]["description"].lower()
check("dwh_consultar_sql: menciona que es solo lectura/SELECT", "select" in d_sql or "lectura" in d_sql,
      "aclará que solo acepta SELECT (límite importante)")
d_tab = tools.TOOLS[1]["description"].lower()
check("dwh_listar_tablas: se diferencia de la otra (esquema/tablas/columnas)",
      any(w in d_tab for w in ("esquema", "columnas", "tablas")), "explicá que devuelve tablas y columnas, no datos")

print("\nHUECO 2 · Clasificación de errores")
E = tools.ERRORES
check("ValidacionError no es reintentable", E[tools.ValidacionError][1] is False,
      "reintentar el mismo SQL inválido falla igual: hay que corregirlo")
check("PermisoError no es reintentable", E[tools.PermisoError][1] is False,
      "sin acceso sigue sin acceso: reintentar no sirve")
check("TransitorioError es reintentable", E[tools.TransitorioError][1] is True,
      "un timeout puede resolverse solo: vale reintentar")

print("\nHUECO 3 · Sugerencias accionables")
for k, v in tools.SUGERENCIAS.items():
    check(f"sugerencia '{k}' completa", v != "___" and len(v) > 15, "escribí una oración que le diga a Claude qué hacer")

print("\nComportamiento de run_tool")
def call(sql):
    return tools.run_tool(NS(type="tool_use", id="toolu_x", name="dwh_consultar_sql", input={"sql": sql}))
r = call("SELECT * FROM despachos WHERE planta = 'Mendoza'")
check("0 filas NO es un error", not r.get("is_error"), "resultado vacío ≠ falla de acceso")
r = call("SELECT * FROM costos")
check("tabla restringida -> is_error de permiso", r.get("is_error") and "[permiso]" in r["content"], "revisá ERRORES")
r = call("SELECT /*lento*/ * FROM despachos")
check("timeout -> reintentable", r.get("is_error") and "Reintentable: sí" in r["content"], "revisá ERRORES")

print(f"\n{sum(ok)}/{len(ok)} checks OK")
