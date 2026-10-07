"""Autocorrector del Lab 03. Corré: python check.py"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

import prompt as p

ok = []
VAGAS = ("cuidado", "importante", "conservador", "alta confianza", "seguro", "relevante", "grave")


def check(nombre, cond, pista):
    ok.append(cond)
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


def lleno(t):
    return isinstance(t, str) and "___" not in t and len(t.strip()) > 0


print("\nHUECO 1 · Criterios explícitos")
todos = p.REPORTAR + p.NO_REPORTAR
check("no quedan ___ en REPORTAR / NO_REPORTAR", all(lleno(c) for c in todos), "completá todas las categorías")
check("al menos 2 categorías para reportar y 2 para omitir", len(p.REPORTAR) >= 2 and len(p.NO_REPORTAR) >= 2,
      "definí qué SÍ y qué NO en categorías concretas")
vagas = [w for w in VAGAS for c in todos if w in c.lower()]
check("sin palabras vagas", not vagas,
      f"encontré {sorted(set(vagas))}: describí el TIPO de problema, no cuánto te importa")
check("cada categoría es concreta (más de 5 palabras)", all(len(c.split()) > 5 for c in todos if lleno(c)),
      "una categoría de una o dos palabras deja la frontera ambigua")
no_rep = " ".join(p.NO_REPORTAR).lower()
check("NO_REPORTAR cubre estilo o nombres", bool(re.search(r"estilo|nombre|naming|indent|formato del c[oó]digo", no_rep)),
      "el estilo (nombres, formato del código) es la fuente clásica de falsos positivos")
rep = " ".join(p.REPORTAR).lower()
check("REPORTAR cubre el caso del ejemplo 3 (resultado engañoso)", bool(re.search(r"engañ|contexto|pondera", rep)),
      "tu ejemplo 3 dice 'reportar', pero ninguna categoría de REPORTAR lo cubre: criterios y ejemplos tienen que coincidir")

print("\nHUECO 2 · Caso ambiguo")
e = p.EJEMPLOS[2]
check("ejemplo 3 completo", all(lleno(e[k]) for k in ("decision", "severidad", "razonamiento")), "completá los tres campos")
check("decisión correcta", e["decision"].strip().lower() == "reportar",
      "el promedio simple pesa igual un despacho de 2 m3 y uno de 40 m3: el número es engañoso")
check("severidad coherente con la tabla", e["severidad"].strip().lower() == "media",
      "no da error ni es siempre incorrecto; es engañoso según el contexto → mirá la definición de 'media'")
r = e["razonamiento"].lower()
check("el razonamiento explica el porqué (ponderar por volumen)",
      bool(re.search(r"pondera|m3|volumen|peso|cantidad", r)) and len(r) > 40,
      "explicá qué ve el analista y por qué (ponderado por m3)")
check("el razonamiento incluye un fix concreto en DAX", bool(re.search(r"divide|sumx|fix", r)),
      "como los ejemplos 1 y 2: terminá con 'Fix: ...' y la fórmula corregida")
check("ejemplos: entre 2 y 4 (guía 4.2)", 2 <= len(p.EJEMPLOS) <= 4, "la guía pide 2-4 ejemplos dirigidos")
check("hay ejemplos de las dos decisiones", {x["decision"] for x in p.EJEMPLOS} >= {"reportar", "omitir"},
      "sin un ejemplo de 'omitir', Claude no aprende dónde está el límite")

print("\nHUECO 3 · Delimitador")
tag = p.TAG_MEDIDA
check("TAG_MEDIDA completo y sin < >", lleno(tag) and "<" not in tag and ">" not in tag, "solo el nombre, p. ej. sin <>")
prompt = p.construir_prompt("Ticket Promedio = [Ventas] / COUNTROWS(Despachos)")
check("el tag coincide con el que nombran las instrucciones", "dentro de <medida>" in prompt and tag == "medida",
      "las instrucciones dicen <medida>: si usás otro nombre, Claude no sabe a qué se refieren")
check("la medida a revisar está delimitada", f"<{tag}>Ticket Promedio" in prompt, "envolvé la entrada variable")
check("ejemplos dentro de <examples><example>", prompt.count("<example>") == len(p.EJEMPLOS) and "<examples>" in prompt,
      "la doc pide <example> dentro de <examples>")

print(f"\nResultado: {sum(ok)}/{len(ok)}")
if all(ok):
    print("\n🎉 Listo. Así queda el prompt que recibiría Claude (python prompt.py lo imprime entero).")
