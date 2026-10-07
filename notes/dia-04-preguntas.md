# Día 04 · Preguntas de cierre

Respondelas sin mirar la lección ni el lab. Las respuestas están al final.

## 1 · Dos workflows y un ahorro (D4)

Tu equipo genera (a) una auditoría semanal de calidad de 4.000 medidas DAX que se revisa los lunes, y (b) un asistente que responde en el chat cuando un analista pregunta qué hace una medida. Te piden bajar costos con Message Batches. ¿Qué hacés?

- A) Batches para los dos, correlacionando las respuestas por `custom_id`
- B) Batches solo para la auditoría semanal; el asistente sigue sincrónico
- C) Los dos sincrónicos, porque Batches no garantiza el orden de resultados
- D) Batches para los dos, con fallback a sincrónico si tarda más de 1 minuto

## 2 · ¿Type o valor? (D4)

Un campo `prioridad` puede ser "alta", "media" o "baja", y a veces el email no la dice. Escribí su definición en JSON Schema (`type` y `enum`).

## 3 · Recuperación libre (D2)

Completá: con `tool_choice` en `____` Claude decide si usa una tool; en `____` tiene que usar alguna; con `____` tiene que usar una específica; y en `____` no puede usar ninguna.

---

<details><summary>Respuestas</summary>

1. **B.** Batches es para lo que nadie espera (la auditoría se lee el lunes). El asistente tiene un humano esperando: sincrónico. C es la misconception de la Q11 (el orden se resuelve con `custom_id`) y D agrega complejidad innecesaria.
2. `"prioridad": {"type": ["string", "null"], "enum": ["alta", "media", "baja", null]}`. El `type` es la clase de dato (texto o null) y el `enum` lista los valores permitidos. Si el campo es nullable y tiene enum, `null` también tiene que estar en el enum.
3. `auto` · `any` · `{"type": "tool", "name": "..."}` · `none`.

</details>
