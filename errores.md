# Hoja de errores

| Fecha | Dominio | Qué elegí | Por qué estaba mal | Regla para recordar |
| --- | --- | --- | --- | --- |
| 2026-10-06 | D1 | Repaso: devolver el resultado de una tool con `role: "any"` | `any` es un valor de `tool_choice`; el resultado de una tool vuelve como `role: "user"` | Resultado de tool = `role: "user"` + bloque `tool_result` + `tool_use_id` = `block.id` |
| 2026-10-06 | D2 | Timeout devuelto como `"0 filas."` sin `is_error`: elegí "Claude reintenta" | Claude no ve el timeout, solo el `tool_result`: si dice 0 filas, cree que no hubo datos y se lo dice al usuario | Claude solo sabe lo que la tool le devuelve. Una falla disfrazada de vacío produce una respuesta falsa |
| 2026-10-07 | D1 | Repaso: el `tool_result` "lleva la respuesta junto con todas las anteriores" | Confundí el bloque con el historial. El historial es la lista `messages`; el bloque es uno solo por tool | Bloque `{"type": "tool_result", "tool_use_id": <block.id>, "content": ...}` dentro de un mensaje `role: "user"` |
| 2026-10-07 | D1 | Repaso: no supe dónde va el `system` en el request | `system` es un parámetro de primer nivel del request, al lado de `model`, `messages` y `tools`; no es un mensaje | `system` va afuera de `messages` (no existe `role: "system"` como en OpenAI) |
