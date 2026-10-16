# Lab 07 · Primitivas MCP para el DWH de la hormigonera

**Formato:** completar huecos. No hace falta API key ni el SDK de MCP: `check.py` revisa tus decisiones, no levanta ningún servidor.

Escenario: vas a exponer el DWH del cliente en un servidor MCP para usarlo desde Claude Code. Primero hay que decidir qué es cada cosa y entender por dónde viaja cada pedido.

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `primitivas.py` | Clasificación de 10 capacidades, el flujo completo y el `tool_result`. Huecos `___`. | **Sí** |
| `check.py` | Autocorrector (23 checks). | No |

```bash
cd labs/07-mcp-primitivas
python check.py        # revisa los huecos
python primitivas.py   # muestra tools/resources/prompts, el flujo en orden y tu mensaje
```

1. **HUECO 1:** `"tool"`, `"resource"` o `"prompt"` para cada capacidad. Lección, secciones 2 y 3. La pregunta que decide: ¿quién la elige?
2. **HUECO 2:** ordenar los 6 pasos del flujo (letras entre comillas: `"C"`) y decir quién llama al servidor. Lección, sección 4.
3. **HUECO 3:** escribir el mensaje con el `tool_result`, **sin esqueleto**. Día 01 + lección, sección 4.

Objetivo: **23/23**. Guardá con `Ctrl+S` antes de cada corrida.

**Extra (opcional):** en Claude Code escribí `/mcp` para ver los servidores conectados y sus tools. Fijate cómo se llaman: `mcp__<servidor>__<tool>`.
