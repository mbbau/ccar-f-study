# CCAR-F Study Plan

Plan de 4 semanas (28/9 – 23/10/2026) para la certificación **Anthropic CCAR-F – Claude Certified Architect, Foundations**.

Numeración y pesos según la [guía oficial del examen](RESOURCES.md#guía-del-examen-y-preparación):

| Dominio | Peso |
| --- | --- |
| D1 · Arquitectura agéntica y orquestación | 27% |
| D2 · Diseño de tools e integración MCP | 18% |
| D3 · Claude Code: configuración y workflows | 20% |
| D4 · Prompt engineering y salida estructurada | 20% |
| D5 · Contexto, confiabilidad y escalado a humanos | 15% |

## Orden del plan

Ordenado por dependencias: cada tema usa lo del anterior (API → tools → prompts → salida estructurada → contexto → agentes → MCP → Claude Code).

| Semana | Días | Temas |
| --- | --- | --- |
| 1 · Fundamentos | 01–05 | Messages API y agentic loop · Diseño de tools · System prompts y few-shot · Salida estructurada y Batches · Ventana de contexto |
| 2 · Agentes + MCP | 06–10 | Multi-agente y modelos · Arquitectura MCP · Transportes y tools nativas · Lab server MCP · Repaso ronda 1 |
| 3 · Claude Code + confiabilidad | 11–15 | CLAUDE.md · Commands, Skills, CI/CD · Human-in-the-loop · Provenance · Distractores |
| 4 · Simulacros | 16–20 | Bloques por dominio · Ficha de trade-offs · Simulacro final |

## Cómo se sigue

- Cada día hábil es un **issue** con su checklist. Se cierra al terminar el día (idealmente desde el commit del lab: `git commit -m "lab loop agéntico, closes #1"`).
- Cada semana es un **milestone** → la pestaña *Milestones* muestra el % de avance.
- Los **labels** `D1`…`D5` permiten filtrar por dominio (misma numeración que la guía).
- Los números de issue no siguen el orden de los días (el plan se reordenó el 28/9); el título `Día NN` es el que manda.
- El **Project** tiene el tablero Todo / In progress / Done.

## Estructura

```
labs/      código de cada lab
notes/     apuntes, diagramas y la ficha final
errores.md hoja de errores de los simulacros
```
