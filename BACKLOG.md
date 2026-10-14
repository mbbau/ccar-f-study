# Backlog — Certificación CCAR-F

**Última actualización:** 2026-10-13 (Día 05 cerrado; plan replanificado por el examen adelantado)
**Examen:** **vie 23/10/2026** (adelantado del mar 27/10, acordado con Vane el 13/10) · meta ≥ 800/1000 (corte 720)

> Resumen del día a día: qué hicimos, qué toca hoy y qué falta. Claude lo lee al arrancar
> cada sesión y lo usa para el resumen diario del vault de Obsidian.
> Lo canónico sigue estando en otro lado: el plan en los **issues de GitHub** (uno por día),
> las notas del profe en `NOTES.md` y los errores en `errores.md`. Acá va solo el estado.
>
> Convención: `[ ]` pendiente · `[~]` en curso · `[x]` hecho · `⛔` bloqueado (decir por qué)

---

## 🔥 Hoy — mar 13/10

- [x] Calentamiento tras 5 días de pausa: 1 ✗ request con `tools`, `system` y `response` (perdió `model`, `max_tokens`, `messages`) · 2 ~ sin `role`/`content`/`type: "tool_result"`, otra vez `error_message` · 3 ✔ JSON Schema nullable con `null` literal en el enum
- [x] **Día 05** · Ventana de contexto y lost in the middle (#11): secciones 1–6, quiz 7/7, lab 17/17 en 4 corridas (pistas en el 3a), cierre 1 ✔ · 2 ~ · 3 ½ (faltó la razón del cache), learning record 0003
- [x] Dijo que el 7/10 fue "de memoria" y que no entendió la clase: le faltaba el panorama (el agente = su programa + `messages.create` en loop). Nunca hizo una llamada real a la API
- [x] Examen adelantado al vie 23/10 → plan nuevo abajo
- [ ] Repregunta pendiente para el calentamiento del 14/10: los 5 campos del request y el mensaje con dos `tool_result` (uno con `is_error`). No la contestó en el cierre
- [ ] Leer [Context windows](https://docs.claude.com/en/docs/build-with-claude/context-windows) (no venía leyendo las fuentes del final; se comprometió a leerlas)
- [ ] Decidir la API key de la Console para hacer una primera llamada real con el SDK (correr `labs/01-agentic-loop/loop.py` sin `--mock`)

> Pendientes menores: en `RESOURCES.md` quedó una entrada vieja de Prompt Caching bajo D3 (URL de
> docs.anthropic.com), duplicada con la nueva de D5.

## jue 08/10

- [x] Quiz 0001 rehecho: 5/7. Falló Q1 (`system` como mensaje, de nuevo) y Q5 (tres mensajes `user` en lugar de uno con tres `tool_result`). Errores pasados a `errores.md`
- [x] Repregunta de puntos flojos: `system` ✔, correlación por id ✔, request/mensaje/bloque ~ (describió el historial completo en vez de "1 mensaje user con N bloques tool_result")
- [x] Repaso Día 04: 2.5/5. Falló type vs. enum otra vez (`"others"` en `type`); faltó nombrar `custom_id`, el porqué de batch/sincrónico (¿alguien espera?) y el reintento con el error concreto
- [x] Repregunta `prioridad` nullable: `type: ["string","null"]` ✔ y null dentro del enum ✔, pero como `"null"` string en lugar de `null` literal
- [~] **Día 05** · Ventana de contexto y lost in the middle (#11)
  - [x] Lección `lessons/0005-ventana-de-contexto.html` y lab `labs/05-contexto/` (17 checks) armados con la skill `teach`; también `reference/contexto.html`, 6 términos nuevos en `reference/glosario.html` y fuentes D5 en `RESOURCES.md`
  - [x] Repaso inicial de la lección: esqueleto JSON 2/6 (primer nivel ✔ con `system` afuera; faltó el interior de `messages`: `role`, `tool_use`, `tool_result`, `tool_use_id`); las otras 2 preguntas ✔
  - → terminado el mar 13/10

## mié 07/10

- [ ] Rehacer el quiz final de la lección 0001 y pasar los errores del Día 01 a `errores.md` → **movido a jue 08/10**
- [x] Repregunta de arranque: formato de `tool_result` (`role: "user"` + bloque `tool_result` + `tool_use_id` = `block.id`)
- [x] Commitear los cambios del cierre del Día 02 (`NOTES.md`, `errores.md`)
- [x] **Día 03** · System prompts y few-shot (#8): lección y quizzes OK (6/6) · lab 17/17 · cierre 3/3 (falta el nombre exacto `tool_result`/`tool_use_id`) · commit hecho
- [x] **Día 04** · Salida estructurada y Message Batches (#9): quiz 5/6, lab 14/14, cierre 3/3
- [ ] **Día 05** → **movido a jue 08/10** · Ventana de contexto y lost in the middle (#11). Reforzar "¿qué ve Claude?" (falló la pregunta 3 del Día 02)

## 📅 Plan hasta el examen (vie 23/10) — propuesto el 13/10, falta confirmar

Quedan 15 días del plan (06–20) en 7 días hábiles: 2 por día y uno de 3, sin fusionar lecciones ni fines de
semana. Cada día arranca con un calentamiento corto y nunca van dos labs pesados seguidos. Ahora se prioriza
comprensión sobre cobertura: cada tema se ancla en el programa real (`messages.create` en loop o Claude Code).

| Fecha | Días del plan |
|---|---|
| mié 14/10 | 06 (multi-agente; idealmente con la primera llamada real) · 07 (MCP primitivas) |
| jue 15/10 | 08 (transportes MCP) · 09 (lab integrador MCP) |
| vie 16/10 | 10 (repaso + cuestionario ronda 1) · 11 (CLAUDE.md) |
| lun 19/10 | 12 (commands/skills/CI) · 13 (human-in-the-loop) · 14 (provenance) |
| mar 20/10 | 15 (distractores) · **mock exam** (#22, quick ~28 preg / 56 min) · 16 (bloque D1 + D2) |
| mié 21/10 | 17 (bloque D3 + D4) · 18 (bloque D5) |
| jue 22/10 | 19 (video + ficha de trade-offs) · 20 (simulacro final) |
| **vie 23/10** | **Examen** |

> **Mock exam (#22):** [claudecertificationguide.com/mock-exam](https://claudecertificationguide.com/mock-exam/start), no oficial.
> Quick mock el 20/10 como diagnóstico con toda la teoría vista; los dominios flojos definen el foco de los Días 16–18.
> La versión full (60 preg / 120 min) queda como opción para el simulacro del Día 20.

### Historial del plan de recuperación (6–9/10)

| Fecha | Días del plan |
|---|---|
| lun 06/10 | ✅ 01 · 02 |
| mié 07/10 | ✅ 03 · 04 (05 pasa al jueves) |
| jue 08/10 | ½ 05 (+ quiz 0001); 06 y 07 no se hicieron |
| vie 09/10 – lun 12/10 | sin sesión |
| mar 13/10 | ✅ 05 |

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

- Formato de `tool_result`: lo confundió con `tool_choice: any` (6/10) y con el historial (7/10). Repreguntar hasta que salga solo.
- `tool_choice`: a la mañana confundía `any`/`tool` y olvidaba `auto`; en el cierre del Día 04 dijo los cuatro bien. Repreguntar espaciado.
- JSON Schema: `type` (clase de dato) vs. valor de `enum`; no existe type fecha. Falló otra vez en el repaso del 8/10 (`"others"` en `type`). Prioridad alta.
- Dónde va `system` (parámetro de primer nivel, no un mensaje): falló el 7/10 y otra vez en el quiz 0001 del 8/10. Prioridad alta.
- Tools en paralelo: todos los `tool_result` van en **un** mensaje `user` (en el quiz 0001 del 8/10 puso uno por mensaje).
- Estructura request ⊃ mensajes ⊃ bloques: arma bien el primer nivel pero no baja al interior de `messages` (8/10).
- Ponerse en el lugar de Claude: solo sabe lo que la tool le devuelve (una falla disfrazada de "0 filas" produce una respuesta falsa).

## ✅ Hecho

- **mié 07/10** — Día 04 · Salida estructurada y Message Batches (#9): lección (repaso 2/2, quiz 5/6: falló Q11), lab 14/14 en 2 iteraciones, cierre 3/3.

- **mié 07/10** — Día 03 · System prompts y few-shot (#8): lección (quizzes 6/6 y 2/2), lab 17/17 en 4 iteraciones, cierre 3/3, learning record 0002.

- **lun 06/10** — Día 02 · Diseño de tools y `tool_choice` (#3): lección, lab y preguntas de cierre (2/3 bien).
- **lun 06/10** — Día 01 · Messages API y agentic loop (#1): lección, lab y registro de aprendizaje 0001. Repaso tras 7 días de pausa.
- **lun 28/09** — Plan reordenado por dependencias y diagnóstico inicial de fundamentos de la API.
