# Día 03 · Preguntas de cierre

Respondelas sin mirar la lección ni el lab. Las respuestas están al final.

## 1 · Revisor con poca adopción (D4)

Tu revisor automático de PRs reporta en 5 categorías. Los devs empezaron a ignorarlo: el 70% de los falsos positivos vienen de la categoría "comentarios desactualizados". Las otras 4 son precisas. ¿Qué hacés primero?

- A) Agregar al prompt "solo reportá comentarios cuando estés muy seguro"
- B) Desactivar temporalmente esa categoría y mejorar su prompt aparte
- C) Pedir un score de confianza y filtrar los hallazgos por debajo de 8
- D) Correr la revisión tres veces y quedarte con los hallazgos repetidos

## 2 · Recuperación libre (D1)

Claude te devolvió un `tool_use` con `id: "toolu_09"`. La tool falló porque la tabla no existe. Escribí el mensaje completo que le devolvés (role, tipo de bloque y todos sus campos).

## 3 · Recuperación libre (D1)

¿Dónde va el system prompt en un request a la Messages API? Escribí la llamada `client.messages.create(...)` con sus parámetros principales (sin los valores completos).

---

<details><summary>Respuestas</summary>

1. **B.** Skill explícito de 4.1: desactivar la categoría con muchos falsos positivos para recuperar la confianza mientras se mejora su prompt. A y C son filtros por confianza, que la guía descarta (la confianza autoinformada está mal calibrada). D, el consenso, suprime bugs reales (Q12 de la guía).
2. `{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "toolu_09", "is_error": true, "content": "[validación] La tabla X no existe. Usá dwh_listar_tablas para ver las disponibles y corregí la consulta."}]}`
3. `client.messages.create(model=..., max_tokens=..., system="...", messages=[...], tools=[...])`. `system` es un parámetro de primer nivel, no un mensaje de `messages` (no existe `role: "system"`).

</details>
