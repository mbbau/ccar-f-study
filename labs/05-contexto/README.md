# Lab 05 · Contexto para preguntar sobre un modelo TMDL

**Formato:** completar huecos. No hace falta API key: `check.py` revisa el request que armás, no lo manda.

Escenario: sesión larga con un cliente de una hormigonera. `[Ventas Netas]` de octubre no coincide con el ERP y le preguntás a Claude por qué, pasándole el modelo TMDL entero.

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `contexto.py` | Hechos del caso, recorte del `tool_result` y armado del request. 3 huecos `___`. | **Sí** |
| `datos.py` | El TMDL, el resultado completo de `get_medida` y la pregunta. | No (pero leelo) |
| `check.py` | Autocorrector (17 checks). | No |

```bash
cd labs/05-contexto
python check.py      # revisa los huecos
python contexto.py   # muestra cómo queda el request: claves, orden de bloques y dónde está el cache
```

1. **HUECO 1:** qué datos van al bloque de *hechos del caso* (no se resumen) y cuáles se pueden resumir. Lección, sección 3.
2. **HUECO 2:** qué campos del `tool_result` necesita Claude para la pregunta. Lección, sección 2.
3. **HUECO 3:** dónde va el `system`, en qué orden van los bloques y cuál lleva `cache_control`. Lección, secciones 1, 4 y 5.

> El check arranca pidiendo el HUECO 1: Python no puede importar el archivo con `___` sueltos en un diccionario. Completá esos `True`/`False` primero.

Objetivo: **17/17**. Guardá con `Ctrl+S` antes de cada corrida.

**Extra (opcional, si tenés API key):** mandá el request con el SDK y comparalo con una versión con la pregunta arriba del TMDL. Pista: hay una razón en el TMDL para la diferencia de montos que no es el filtro de `Estado`. ¿La encuentra Claude en las dos versiones?
