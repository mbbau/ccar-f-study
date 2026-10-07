"""Autocorrector del Lab 04. Corré: python check.py"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

from validar import validar

try:
    import extractor as x
except NameError:
    print("❌ Todavía hay ___ sin completar en REINTENTABLE (HUECO 3a). Reemplazalos por True o False.")
    sys.exit()

ok = []


def check(nombre, cond, pista):
    ok.append(bool(cond))
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


def intentar(f, *a):
    try:
        return f(*a), None
    except NameError:
        return None, "quedan ___ sin completar"


S = x.TOOL_PEDIDO["input_schema"]
P = S["properties"]

# Lo que devolvería Claude (bloque tool_use.input) para cuatro emails distintos.
EMAIL_SIN_FECHA = "Hola, para la obra Torre Sur necesitamos 30 m3 de H21 para la losa. Gracias."
SIN_FECHA = {"obra": "Torre Sur", "fecha_entrega": None, "tipo_hormigon": "H21", "tipo_hormigon_detalle": None,
             "lineas": [{"descripcion": "losa", "m3": 30}], "total_m3_declarado": None}
RARO = {"obra": "Barrio Los Álamos", "fecha_entrega": "2026-11-20", "tipo_hormigon": "otro",
        "tipo_hormigon_detalle": "autocompactante H35", "lineas": [{"descripcion": "tabiques", "m3": 18}],
        "total_m3_declarado": 18}
NO_CIERRA = {"obra": "Ruta 9 km 12", "fecha_entrega": "2026-11-03", "tipo_hormigon": "H30", "tipo_hormigon_detalle": None,
             "lineas": [{"descripcion": "base", "m3": 20}, {"descripcion": "pavimento", "m3": 15}],
             "total_m3_declarado": 40}

print("\nHUECO 1 · Schema")
tf = P["fecha_entrega"]["type"]
check("fecha_entrega acepta null", isinstance(tf, list) and set(tf) == {"string", "null"},
      'si el type es solo "string", Claude tiene que inventar una fecha para cumplir el schema → ["string", "null"]')
check("un email sin fecha valida contra el schema", not validar(SIN_FECHA, S),
      f"errores: {validar(SIN_FECHA, S)}")
enum = P["tipo_hormigon"]["enum"]
otro = "otro" if "otro" in enum else "other"
RARO["tipo_hormigon"] = otro
check("el enum tiene un valor 'otro' para lo que no está en la lista", otro in enum and "___" not in enum,
      'el patrón de la guía (4.3) es "other" + un campo de detalle; acá en castellano: "otro"')
check("tipo_hormigon_detalle es texto o null", P["tipo_hormigon_detalle"]["type"] in (["string", "null"], ["null", "string"]),
      "tiene texto solo cuando tipo_hormigon es 'otro'; si no, null")
check("un hormigón fuera de la lista valida (otro + detalle)", not validar(RARO, S), f"errores: {validar(RARO, S)}")

print("\nHUECO 2 · Validación semántica")
r, err = intentar(x.validar_semantica, NO_CIERRA)
check("detecta que 20 + 15 ≠ 40", err is None and r and "35" in r[0] and "40" in r[0],
      err or "comparé y no salió error: ¿la condición dice 'distinto'?")
check("NO_CIERRA cumple el schema igual (el schema no ve la suma)", not validar(NO_CIERRA, S),
      "esto es lo que tenés que retener: schema válido ≠ datos correctos")
r, err = intentar(x.validar_semantica, RARO)
check("un pedido que cierra no da error", err is None and r == [], err or f"devolvió {r}")
r, err = intentar(x.validar_semantica, SIN_FECHA)
check("sin total declarado no compara (no hay con qué)", err is None and r == [], err or f"devolvió {r}")

print("\nHUECO 3 · Reintentos")
check("formato: reintentable", x.REINTENTABLE["formato"] is True,
      "Claude tiene el dato en el email, solo lo escribió mal: con el error como feedback lo corrige")
check("dato ausente: NO reintentable", x.REINTENTABLE["ausente"] is False,
      "si el dato no está en el email, reintentar no lo hace aparecer (o peor: lo inventa)")
msg, err = intentar(x.armar_reintento, EMAIL_SIN_FECHA, SIN_FECHA, ["fecha: formato inválido"])
check("el reintento incluye el documento original", err is None and EMAIL_SIN_FECHA in msg, err or "falta el email")
check("el reintento incluye la extracción fallida", err is None and '"obra": "Torre Sur"' in msg,
      err or "falta la extracción anterior (extraccion_json)")
check("el reintento incluye el error específico", err is None and "- fecha: formato inválido" in msg,
      err or "falta la lista de errores (errores_txt)")

print(f"\nResultado: {sum(ok)}/{len(ok)}")
if all(ok):
    print("\n🎉 Listo. Pipeline completo: schema (forma) → validación semántica (sentido) → reintento solo si sirve.")
