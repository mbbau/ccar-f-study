# Hoja de errores

| Fecha | Dominio | Qué elegí | Por qué estaba mal | Regla para recordar |
| --- | --- | --- | --- | --- |
| 2026-10-06 | D1 | Repaso: devolver el resultado de una tool con `role: "any"` | `any` es un valor de `tool_choice`; el resultado de una tool vuelve como `role: "user"` | Resultado de tool = `role: "user"` + bloque `tool_result` + `tool_use_id` = `block.id` |
| 2026-10-06 | D2 | Timeout devuelto como `"0 filas."` sin `is_error`: elegí "Claude reintenta" | Claude no ve el timeout, solo el `tool_result`: si dice 0 filas, cree que no hubo datos y se lo dice al usuario | Claude solo sabe lo que la tool le devuelve. Una falla disfrazada de vacío produce una respuesta falsa |
