# CCAR-F Resources

Fuentes oficiales y verificables para preparar la certificación Claude Certified Architect – Foundations.

## Knowledge

### Guía del examen y preparación

- [Claude Certified Architect – Foundations Exam Guide (PDF oficial, v1.0, jul-2026)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1783542750/Claude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf)
  Blueprint oficial: 5 dominios con sus *task statements* (Knowledge of / Skills in), 6 escenarios, formato (60 ítems, 120 min, corte 720) y 12 preguntas de ejemplo. **La fuente que define qué entra en el examen.**

- [Anthropic Partner Academy (Skilljar)](https://anthropic.skilljar.com)
  Portal oficial con cursos preparatorios para las certificaciones Anthropic. Use for: prerequisitos del examen, cursos oficiales.

### D1 · Arquitectura agéntica y orquestación (27%)

- [Blog: "Building Effective Agents" – Anthropic Research](https://www.anthropic.com/research/building-effective-agents)
  Guía oficial de Anthropic con los 5 agentic patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) y cuándo usar workflows vs. agents. **Lectura esencial para D1.**
- [Docs: Tool Use Overview (agents-and-tools)](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview)
  Referencia de la API de tool use: definición de herramientas con `input_schema`, manejo de `tool_use` / `tool_result`, y el agentic loop (while + stop_reason). Use for: implementar el loop agéntico.
- [Docs: Tool Use Overview (build-with-claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
  Documentación complementaria de tool use desde la perspectiva de building con Claude. Use for: ejemplos prácticos y best practices.
- [Docs: Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)
  Todos los valores de `stop_reason`, cómo manejar cada uno y trampas (respuestas vacías, `tool_use` truncado, `pause_turn`). **Fuente primaria del Día 01.**
- [Docs: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
  Formato de `tool_result`, reglas de orden, parallel tool use e `is_error`. Use for: lab del agentic loop.
- [Anthropic Cookbook (GitHub)](https://github.com/anthropics/anthropic-cookbook)
  Notebooks con ejemplos oficiales: agentes, tool use, sub-agents, RAG, multi-model. Use for: labs prácticos y patrones de referencia.

### D2 (guía) · Diseño de tools

- [Docs: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  Best practices de descriptions (3–4 oraciones, qué/cuándo/límites), namespacing, `input_examples` y `tool_choice`. **Fuente primaria del Día 02.**
- [Anthropic Engineering: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
  Principios: no envolver cada endpoint, consolidar, contexto significativo, eficiencia de tokens, errores accionables.

### D2 · Claude Code: configuración y workflows (20%)

- [Claude Code Docs: Overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
  Documentación oficial de Claude Code: instalación, comandos, CLAUDE.md, settings.json, skills, hooks, headless mode (`-p`/`--print`), sub-agents. **Hub principal para D2.**

### D3 · Prompt engineering y salida estructurada (20%)

- [Docs: Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
  Cómo funciona prompt caching: breakpoints, cache_control, costos reducidos. Use for: optimización de costos y latencia en llamadas repetitivas.
- [Docs: Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/message-batches)
  API de procesamiento por lotes: crear batches, polling de resultados, límites. Use for: escenarios de alto volumen (evaluaciones masivas, procesamiento offline).

### D4 · Diseño de herramientas e integración MCP (18%)

- [MCP Specification (modelcontextprotocol.io)](https://modelcontextprotocol.io/specification)
  Especificación completa del Model Context Protocol: transports (stdio, SSE), resources, tools, prompts, sampling. **Lectura esencial para D4.**
- [MCP Introduction](https://modelcontextprotocol.io/introduction)
  Introducción oficial al protocolo MCP: qué problema resuelve, arquitectura client-server, conceptos clave.
- [MCP Python SDK (GitHub)](https://github.com/modelcontextprotocol/python-sdk)
  SDK oficial en Python para construir servidores y clientes MCP. Use for: labs de construcción de servidores MCP.

### D5 · Contexto, confiabilidad y escalado a humanos (15%)

- [Docs: Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
  (También relevante para D5.) Estrategias de manejo de contexto largo y reducción de costos.

## Gaps

- **Dominio de la doc:** la documentación se mudó de `docs.anthropic.com` / `docs.claude.com` a `platform.claude.com/docs` (los links viejos redirigen).

- **Structured outputs docs:** La URL específica de structured outputs con JSON schema no resolvió en la estructura actual de docs.anthropic.com. Los conceptos están cubiertos en la doc de tool use (el campo `input_schema`). Si Anthropic publica una página dedicada, agregarla acá.
- **Claude Code sub-pages:** Las páginas individuales de Claude Code (CLAUDE.md, skills, headless mode, sub-agents) están integradas dentro de la overview page en lugar de URLs separadas. Todo el contenido está en el link de overview de D2.

## Wisdom (Communities)

- [r/ClaudeAI (Reddit)](https://reddit.com/r/ClaudeAI)
  Comunidad activa con experiencias reales de uso de Claude, tips de certificación y troubleshooting.
- [Anthropic Discord](https://discord.gg/anthropic)
  Servidor oficial de Anthropic. Canales de Claude Code, API y certificaciones.
