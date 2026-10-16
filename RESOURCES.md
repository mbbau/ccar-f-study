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

### D1 (guía) · Multi-agente (Día 06)

- [Docs: Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents)
  `AgentDefinition` (`description`, `prompt`, `tools`, `model`), aislamiento de contexto (solo pasa el prompt; solo vuelve el mensaje final), paralelo. La tool se llama `Agent` en `tool_use`. **Fuente primaria del Día 06.**
- [Claude Code Docs: Create custom subagents](https://code.claude.com/docs/en/sub-agents)
  Subagentes en `.claude/agents/*.md`; `Task` renombrada `Agent` en la v2.1.63 (alias); `tools` omitido hereda todas.
- [Anthropic Engineering: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
  Orchestrator-worker real: Opus líder + Sonnet subagentes, ~15× tokens, escalar esfuerzo a la complejidad, qué necesita cada subagente, cuándo no conviene multi-agente.
- [Docs: Models overview](https://platform.claude.com/docs/en/models/overview) · [Choosing a model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model)
  Lineup actual (Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5), latencia y uso; "orchestrator that delegates bulk work to lower-cost workers".

### D2 (guía) · Diseño de tools

- [Docs: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
  Best practices de descriptions (3–4 oraciones, qué/cuándo/límites), namespacing, `input_examples` y `tool_choice`. **Fuente primaria del Día 02.**
- [Anthropic Engineering: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
  Principios: no envolver cada endpoint, consolidar, contexto significativo, eficiencia de tokens, errores accionables.

### D4 (guía) · Prompt engineering

- [Docs: Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
  Página única que reemplaza a las viejas (be clear and direct, multishot, XML tags, system prompts / role). **Fuente primaria del Día 03.**
- [Docs: Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)
  Instrucciones literales en modelos nuevos: "be conservative" reduce el recall; reportar todo y filtrar en otra pasada. (Ver también la página de Opus 4.8, sección *Code review harnesses*.)
- [Anthropic Engineering: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  System prompts "a la altura correcta"; ejemplos canónicos y diversos en vez de listas de casos borde.
- [anthropics/claude-code-security-review · prompts.py](https://github.com/anthropics/claude-code-security-review/blob/main/claudecode/prompts.py)
  Prompt real de revisión con listas explícitas de exclusiones para minimizar falsos positivos.

### D4 (guía) · Salida estructurada y Batches

- [Docs: Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  JSON outputs (`output_config.format`) y strict tool use; qué garantiza, límites del schema. **Fuente primaria del Día 04.**
- [Docs: Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
  `strict: true`: el input de la tool cumple el schema siempre.
- [Docs: Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
  Message Batches: −50%, hasta 24 h, `custom_id`, tipos de resultado, 29 días de retención.

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

- [Docs: Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)
  Qué cuenta en la ventana, cómo crece el historial, *context rot* ("more context isn't automatically better"), compaction y que el cache no libera ventana. **Fuente primaria del Día 05.**
- [Docs: Prompting best practices · Long context prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting)
  Documentos largos arriba y la pregunta al final (hasta +30% en pruebas), XML por documento, pedir citas primero. Use for: lost in the middle.
- [Anthropic Engineering: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Por qué los contextos largos degradan y cómo curarlos (compaction, notas, subagentes). Use for: 5.1, 5.4 y puente al Día 06.
- [Docs: Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
  `cache_control`, orden `tools` → `system` → `messages`, TTL 5 min / 1 h, mínimos por modelo, qué invalida el cache. Para el examen solo "saber que existe" (Out-of-Scope de la guía); útil en el trabajo.

## Gaps

- **Dominio de la doc:** la documentación se mudó de `docs.anthropic.com` / `docs.claude.com` a `platform.claude.com/docs` (los links viejos redirigen).

- **Structured outputs docs:** La URL específica de structured outputs con JSON schema no resolvió en la estructura actual de docs.anthropic.com. Los conceptos están cubiertos en la doc de tool use (el campo `input_schema`). Si Anthropic publica una página dedicada, agregarla acá.
- **Claude Code sub-pages:** Las páginas individuales de Claude Code (CLAUDE.md, skills, headless mode, sub-agents) están integradas dentro de la overview page en lugar de URLs separadas. Todo el contenido está en el link de overview de D2.

## Wisdom (Communities)

- [r/ClaudeAI (Reddit)](https://reddit.com/r/ClaudeAI)
  Comunidad activa con experiencias reales de uso de Claude, tips de certificación y troubleshooting.
- [Anthropic Discord](https://discord.gg/anthropic)
  Servidor oficial de Anthropic. Canales de Claude Code, API y certificaciones.
