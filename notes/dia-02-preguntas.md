# Día 02 · Preguntas tipo examen

Respondelas sin mirar la lección. Las respuestas están al final.

## 1 · Devolver un error al loop

Tu agente llama a `dwh_consultar_sql` y la consulta toca una tabla restringida. ¿Cómo le devolvés el resultado a Claude?

- A) Mensaje `role: "assistant"` con bloque `text` explicando el problema
- B) Mensaje `role: "user"` con bloque `tool_result`, `tool_use_id` e `is_error: true`
- C) Mensaje `role: "user"` con bloque `text` y `tool_choice: {"type": "none"}`
- D) Mensaje `role: "user"` con bloque `tool_result` vacío y `stop_reason: "end_turn"`

## 2 · Separar o consolidar

Un agente de soporte tiene tres tools: `jira_crear_ticket`, `jira_asignar_ticket` y `jira_etiquetar_ticket`. En el 90% de los casos las llama juntas y en ese orden, y en los logs a veces saltea la segunda. ¿Qué cambio de diseño es más adecuado?

- A) Consolidarlas en una tool que crea, asigna y etiqueta el ticket
- B) Agregar una cuarta tool que verifique que el ticket quedó asignado
- C) Forzar `jira_asignar_ticket` con `tool_choice` después de cada creación
- D) Alargar las descriptions de las tres tools a seis oraciones cada una

## 3 · Vacío o falla

Un usuario pregunta "¿cuánto despachamos en Río Segundo en octubre?". La tool no pudo conectarse al DWH por un timeout, y tu código devuelve `"0 filas."` sin `is_error`. ¿Qué es lo más probable que pase?

- A) Claude reintenta la consulta porque detecta que fue un timeout
- B) Claude responde que no hubo despachos en Río Segundo en octubre
- C) La API rechaza el `tool_result` porque el contenido está vacío
- D) Claude cambia de tool y consulta `dwh_listar_tablas` para revisar

---

<details><summary>Respuestas</summary>

1. **B.** El resultado de una tool siempre vuelve como `role: "user"` con un bloque `tool_result`, cuyo `tool_use_id` es el `id` del bloque `tool_use`. El error se marca con `is_error: true` y el contenido explica qué hacer (*"No reintentes: informá al usuario que el dato está restringido"*). A es al revés: el `assistant` es Claude. C y D mezclan parámetros del request (`tool_choice`) y de la response (`stop_reason`) que no van en un mensaje.
2. **A.** Son pasos del mismo flujo sobre el mismo recurso: consolidar elimina la oportunidad de saltear uno. *Separar cuando una tool hace cosas distintas; consolidar cuando varias son pasos del mismo flujo.* C además falla en Opus 5.5 / Sonnet 5.5 (forzar una tool devuelve 400) y no escala. D no ataca la causa.
3. **B.** Claude confía en lo que dice la tool: si dice 0 filas, para Claude no hubo despachos. Esa es la trampa del día: un error que se disfraza de resultado vacío. Lo correcto: `is_error: true`, categoría transitorio, reintentable.

</details>
