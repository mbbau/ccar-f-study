# Notas del profe

- Idioma: explicaciones en español, términos técnicos en inglés (como en el examen).
- Cada día hábil = 1 issue de GitHub con su rutina de 90 min (10 repaso · 40 estudio · 30 lab · 10 cierre). Las lecciones siguen el issue del día.
- Stack del lab: Python + SQL (SQLite local como stand-in del DWH). Labs con autocorrector (`check.py`) y cliente falso para no depender de API key.
- Matías trabaja en Windows (PowerShell); los scripts fuerzan UTF-8 en stdout.
- Repo personal (portafolio): los commits y el push los hace él desde su máquina.
- Regla: antes de un dominio nuevo, mini diagnóstico (5 preguntas) para calibrar la zona de desarrollo próximo. No asumir fundamentos de la API por experiencia con otros SDKs (el OpenAI Agents SDK le escondía el loop).
- 28/9: el plan se reordenó por dependencias (`scripts/reordenar_issues.py`). Cada issue cita los task statements de la guía oficial.
- Diagnóstico 28/9 (fundamentos API): no sabía dónde va `system` ni que la API es stateless; creía que `content` era un JSON con `choices` (modelo mental de OpenAI). Sí sabía que las tools las ejecuta su código. → incorporado en la lección 0001 (fundamentos + loop, una sola lección para el Día 01). Las comparaciones con OpenAI le sirven como puente.
- Matías es especialista en datos, no desarrollador: lidera el proyecto del chatbot (lo construyó Rodo). Quiere aprender y crecer; está leyendo *Machine Learning Engineering with Python* (Packt).
- Labs: el autocompletado de VS Code le terminaba el código. Preferir ejercicios de leer/predecir y completar huecos, y revisar juntos el código generado (bug por bug, conectado a la teoría).
- 6/10: retomó después de una semana sin estudiar (venía 6 días atrasado). Plan de recuperación: 2–3 días de plan por día hábil hasta el Día 10 (vie 9/10), sin fusionar lecciones ni estudiar fines de semana.
- Repaso Día 01 (6/10, con 7 días de pausa): stateless ✔; `stop_reason` ✔ pero no recordaba `tool_use`/`end_turn`; no recordaba el formato del `tool_result` (role `user`, `tool_use_id` = `block.id`). → Volver a preguntar ambos al cierre del Día 02 y al inicio del Día 03.
- Cierre Día 02 (6/10): `stop_reason` ya lo recuerda (`tool_use`/`end_turn`). Formato de `tool_result`: sigue sin fijarse y lo confundió con `tool_choice: any` (interferencia con lo del día). → Pregunta 1 de `notes/dia-02-preguntas.md` + repreguntar al arrancar el Día 03. Pidió que yo escribiera las preguntas del cierre: se las doy para responder (recuperación) en vez de generar.
- Preguntas cierre Día 02: 1 ✔ (B, aunque no mencionó `role: "user"` en el porqué), 2 ✔, 3 ✘: creyó que Claude "sabe" del timeout aunque la tool devuelva "0 filas". Le cuesta ponerse en el lugar de Claude (solo ve lo que le devolvés) → reforzar con escenarios "¿qué ve Claude?" en el Día 03 y en el Día 05 (contexto).
- Los errores del Día 01 nunca se registraron en `errores.md`. Matías va a rehacer el quiz final de la lección 0001 en la próxima sesión y pasar los errores: anotarlos antes de arrancar el Día 03.
- Push: lo puedo hacer yo con su cuenta personal `mbbau` (gh ya autenticado), cuando él lo pide.
- 7/10: se creó `BACKLOG.md` (estado diario: hoy, plan de recuperación, siguiente, hecho). Leerlo al arrancar cada sesión y actualizarlo al cierre; lo usa el resumen diario del vault de Obsidian.
