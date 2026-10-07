"""Mini validador de JSON Schema (el subconjunto que usa el lab). No lo tocás.

Hace lo mismo que jsonschema.validate para: type (o lista de types), properties,
required, enum, items y additionalProperties: false. Devuelve una lista de errores.
"""

TIPOS = {
    "string": str, "integer": int, "number": (int, float), "boolean": bool,
    "array": list, "object": dict, "null": type(None),
}


def _es_tipo(valor, t):
    if t in ("integer", "number") and isinstance(valor, bool):
        return False
    return isinstance(valor, TIPOS[t])


def validar(valor, schema, ruta="$"):
    errores = []
    tipos = schema.get("type")
    if tipos is not None:
        tipos = tipos if isinstance(tipos, list) else [tipos]
        raros = [t for t in tipos if t not in TIPOS]
        if raros:
            return [f"{ruta}: {raros} no es un type de JSON Schema (válidos: {', '.join(TIPOS)})"]
        if not any(_es_tipo(valor, t) for t in tipos):
            return [f"{ruta}: se esperaba {' o '.join(tipos)} y llegó {type(valor).__name__}"]
    if "enum" in schema and valor not in schema["enum"]:
        errores.append(f"{ruta}: {valor!r} no está en {schema['enum']}")
    if isinstance(valor, dict):
        props = schema.get("properties", {})
        for campo in schema.get("required", []):
            if campo not in valor:
                errores.append(f"{ruta}: falta el campo requerido '{campo}'")
        for campo, sub in valor.items():
            if campo in props:
                errores += validar(sub, props[campo], f"{ruta}.{campo}")
            elif schema.get("additionalProperties") is False:
                errores.append(f"{ruta}: campo no permitido '{campo}'")
    if isinstance(valor, list) and "items" in schema:
        for i, item in enumerate(valor):
            errores += validar(item, schema["items"], f"{ruta}[{i}]")
    return errores
