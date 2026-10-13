"""Autocorrector del Lab 05. Corré: python check.py"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

try:
    import contexto as c
except NameError:
    print("❌ Todavía hay ___ sin completar en ES_HECHO_DEL_CASO (HUECO 1). Reemplazalos por True o False.")
    sys.exit()

from datos import PREGUNTA, RESULTADO_GET_MEDIDA, TMDL_MODELO

ok = []


def check(nombre, cond, pista):
    ok.append(bool(cond))
    print(("✅" if cond else "❌"), nombre, "" if cond else f"\n     → {pista}")


def intentar(f, *a):
    try:
        return f(*a), None
    except NameError as e:
        if "'___'" in str(e):
            return None, "quedan ___ sin completar"
        return None, f"{e}: ¿le faltan comillas a un string, o escribiste mal el nombre de una variable?"
    except Exception as e:  # p. ej. KeyError por un campo mal escrito
        return None, f"{type(e).__name__}: {e}"


print("\nHUECO 1 · Hechos del caso")
H = list(c.ES_HECHO_DEL_CASO.values())
check("la fecha que espera el cliente es un hecho", H[0] is True,
      "un resumen la convierte en 'lo necesita pronto': lo que el cliente dijo que espera va literal")
check("los dos montos son hechos", H[1] is True,
      "un resumen la convierte en 'hay una diferencia en ventas': se pierden $1.250.430 y $1.310.000")
check("la partición afectada es un hecho", H[2] is True,
      "es el id que vas a necesitar para investigar: si se borronea, Claude lo tiene que volver a buscar")
check("la explicación de Claude NO es un hecho", H[3] is False,
      "es razonamiento ya hecho, no un dato del caso: se puede resumir (o descartar)")
check("el saludo NO es un hecho", H[4] is False, "no cambia ninguna respuesta futura")
hechos = c.armar_hechos()
check("los montos llegan textuales al bloque de hechos", "$1.250.430" in hechos and "$1.310.000" in hechos,
      "el bloque de hechos copia el dato tal cual, nunca un resumen")

print("\nHUECO 2 · Recortar el tool_result")
r, err = intentar(c.recortar_resultado, RESULTADO_GET_MEDIDA)
check("se queda con la expresión DAX", err is None and "expresion" in r,
      err or "sin la expresión, Claude no puede explicar qué calcula la medida")
check("se queda con las dependencias", err is None and "dependencias" in r,
      err or "la pregunta pide de qué columnas depende")
ruido = ("lineageTag", "annotations", "modifiedTime", "structureModifiedTime", "changedProperties",
         "extendedProperties", "kpi", "detailRowsDefinition", "formatStringDefinition", "errorMessage")
sobran = [k for k in ruido if r and k in r]
check("tira los metadatos que no responden la pregunta", err is None and not sobran,
      err or f"sobran {sobran}: ocupan tokens en cada request y no aportan a la respuesta")
check("5 campos o menos", err is None and len(r) <= 5, err or f"te quedaste con {len(r)} campos")
if err is None:
    antes, despues = len(json.dumps(RESULTADO_GET_MEDIDA)), len(json.dumps(r))
    check("el resultado se achica a menos de un tercio", despues < antes / 3,
          f"{antes} → {despues} caracteres")
else:
    check("el resultado se achica a menos de un tercio", False, err)

print("\nHUECO 3 · Armar el request")
req, err = intentar(c.armar_request, TMDL_MODELO, hechos, PREGUNTA)
NOMBRES_3 = ("system es un parámetro de primer nivel", "no hay ningún mensaje con role system",
             "el TMDL (documento largo) va primero", "la pregunta va al final",
             "los hechos van entre el TMDL y la pregunta", "cache_control solo en el bloque del TMDL")
if err:
    for nombre in NOMBRES_3:
        check(nombre, False, err)
else:
    check("system es un parámetro de primer nivel", req.get("system") == c.SYSTEM,
          f"claves de primer nivel: {list(req)}. El system prompt va con la clave \"system\", al lado de model y messages")
    roles = [m.get("role") for m in req["messages"]]
    check("no hay ningún mensaje con role system", "system" not in roles,
          "en la API de Claude el system prompt no es un mensaje")
    bloques = req["messages"][0]["content"]
    textos = [b.get("text", "") for b in bloques]
    check("el TMDL (documento largo) va primero", textos and textos[0].startswith("<modelo_tmdl>"),
          "long context prompting: los documentos largos arriba, la pregunta abajo")
    check("la pregunta va al final", textos and textos[-1] == PREGUNTA,
          "la pregunta al final mejora la respuesta con documentos largos (hasta 30% en las pruebas de Anthropic)")
    check("los hechos van entre el TMDL y la pregunta", len(textos) == 3 and textos[1].startswith("<hechos_del_caso>"),
          "cambian en cada turno: si van antes del TMDL, rompen el cache del TMDL en cada request")
    con_cache = [i for i, b in enumerate(bloques) if "cache_control" in b]
    check("cache_control solo en el bloque del TMDL", con_cache == [0],
          f"está en los bloques {con_cache}. El breakpoint va al final de lo que no cambia: el TMDL. "
          "Si lo ponés en la pregunta, cada request escribe un cache nuevo que nunca se lee")

print(f"\nResultado: {sum(ok)}/{len(ok)}")
if all(ok):
    print("\n🎉 Listo. Contexto curado: hechos textuales, resultados recortados, documento arriba, "
          "pregunta abajo y el prefijo estable cacheado.\n   Corré python contexto.py para ver el request.")
