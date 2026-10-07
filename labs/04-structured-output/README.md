# Lab 04 · Pedido de hormigón → JSON validado

**Formato:** completar huecos. No hace falta API key ni instalar nada: `check.py` simula lo que devolvería Claude, y `validar.py` es un mini `jsonschema` (mismo comportamiento para lo que usa el lab).

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `extractor.py` | Tool de extracción (schema), validación semántica y reintentos. 3 huecos `___`. | **Sí** |
| `check.py` | Autocorrector (14 checks) con 3 pedidos simulados. | No |
| `validar.py` | Validador de JSON Schema. | No |

```bash
cd labs/04-structured-output
python check.py
```

1. **HUECO 1:** schema: campo nullable, valor `"otro"` en el enum y su campo de detalle.
2. **HUECO 2:** validación semántica: ¿las líneas suman el total declarado?
3. **HUECO 3:** ¿qué errores vale la pena reintentar?, y las 3 piezas del mensaje de reintento.

> El check arranca pidiendo el HUECO 3a: Python no puede importar el archivo con `___` sueltos en un diccionario. Completá esos dos `True`/`False` primero y después seguí en orden.

Objetivo: **14/14**.
