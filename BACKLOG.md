# Backlog — Certificación CCAR-F

**Última actualización:** 2026-10-07 (creación del backlog; Días 01–02 hechos, recuperación en curso)
**Examen:** mar 27/10/2026 · meta ≥ 800/1000 (corte 720)

> Resumen del día a día: qué hicimos, qué toca hoy y qué falta. Claude lo lee al arrancar
> cada sesión y lo usa para el resumen diario del vault de Obsidian.
> Lo canónico sigue estando en otro lado: el plan en los **issues de GitHub** (uno por día),
> las notas del profe en `NOTES.md` y los errores en `errores.md`. Acá va solo el estado.
>
> Convención: `[ ]` pendiente · `[~]` en curso · `[x]` hecho · `⛔` bloqueado (decir por qué)

---

## 🔥 Hoy — mié 07/10

- [ ] Rehacer el quiz final de la lección 0001 y pasar los errores del Día 01 a `errores.md` (quedó pendiente)
- [ ] Repregunta de arranque: formato de `tool_result` (`role: "user"` + bloque `tool_result` + `tool_use_id` = `block.id`)
- [ ] Commitear los cambios del cierre del Día 02 (`NOTES.md`, `errores.md`)
- [ ] **Día 03** · System prompts y few-shot (#8)
- [ ] **Día 04** · Salida estructurada y Message Batches (#9)
- [ ] **Día 05** · Ventana de contexto y lost in the middle (#11). Reforzar "¿qué ve Claude?" (falló la pregunta 3 del Día 02)

## 📅 Plan de recuperación (hasta el Día 10)

2–3 días de plan por día hábil, sin fusionar lecciones ni estudiar fines de semana. Repaso corto entre días
y nunca dos labs pesados seguidos.

| Fecha | Días del plan |
|---|---|
| lun 06/10 | ✅ 01 · 02 |
| mié 07/10 | 03 · 04 · 05 |
| jue 08/10 | 06 · 07 · 08 |
| vie 09/10 | 09 (lab integrador MCP) · 10 (repaso + cuestionario ronda 1) → verificar ritmo y fecha del examen |

Desde el lun 12/10 se vuelve a 1 día de plan por día hábil (Día 11 → Día 20 el vie 23/10).

## 📋 Siguiente

- [ ] Día 06 · Orquestación multi-agente y asignación de modelos (#2)
- [ ] Día 07 · Arquitectura MCP y primitivas (#4)
- [ ] Día 08 · Transportes MCP, scopes y tools nativas (#5)
- [ ] Día 09 · Lab integrador: server MCP (#14)
- [ ] Día 10 · Repaso semanas 1-2 + Cuestionario ronda 1 (#10)
- [ ] Día 11 · Jerarquía de CLAUDE.md y reglas (#6)
- [ ] Día 12 · Commands, Skills, Plan Mode y CI/CD (#7)
- [ ] Día 13 · Human-in-the-loop y propagación de errores (#12)
- [ ] Día 14 · Provenance y calibración de confianza (#13)
- [ ] Día 15 · Distractores del examen (#15)
- [ ] Día 16 · Bloque D1 + D2 (agentes + tools/MCP) (#16)
- [ ] Día 17 · Bloque D3 + D4 (Claude Code + prompts) (#17)
- [ ] Día 18 · Bloque mixto foco D5 (#18)
- [ ] Día 19 · Video Exam Prep + ficha de trade-offs (#19)
- [ ] Día 20 · Simulacro final (60 preguntas) (#20)
- [ ] Examen CCAR-F · go/no-go y día del examen (#21)

## 🎯 Puntos flojos a vigilar

- Formato de `tool_result`: lo confundió con `tool_choice: any`. Repreguntar hasta que salga solo.
- Ponerse en el lugar de Claude: solo sabe lo que la tool le devuelve (una falla disfrazada de "0 filas" produce una respuesta falsa).

## ✅ Hecho

- **lun 06/10** — Día 02 · Diseño de tools y `tool_choice` (#3): lección, lab y preguntas de cierre (2/3 bien).
- **lun 06/10** — Día 01 · Messages API y agentic loop (#1): lección, lab y registro de aprendizaje 0001. Repaso tras 7 días de pausa.
- **lun 28/09** — Plan reordenado por dependencias y diagnóstico inicial de fundamentos de la API.
