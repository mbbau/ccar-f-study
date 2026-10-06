# Hoja de errores

| Fecha | Dominio | Qué elegí | Por qué estaba mal | Regla para recordar |
| --- | --- | --- | --- | --- |
| 2026-10-06 | D1 | Repaso: devolver el resultado de una tool con `role: "any"` | `any` es un valor de `tool_choice`; el resultado de una tool vuelve como `role: "user"` | Resultado de tool = `role: "user"` + bloque `tool_result` + `tool_use_id` = `block.id` |
