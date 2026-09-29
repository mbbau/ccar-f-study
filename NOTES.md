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
