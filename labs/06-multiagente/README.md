# Lab 06 · El agente "analista": coordinador y tres subagentes

**Formato:** completar huecos. No hace falta API key: `check.py` revisa la configuración que armás, no llama a la API.

Escenario: el mismo cliente del lab 05. `[Ventas Netas]` de octubre no coincide con el ERP. Un coordinador delega en tres subagentes: `explorador_tmdl` (lee el modelo), `consultor_dwh` (consulta el DWH) y `redactor` (escribe el informe).

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `multiagente.py` | Definición de los subagentes, prompt del redactor y turno en paralelo. Huecos `___`. | **Sí** |
| `datos.py` | La pregunta, el historial del coordinador y lo que devuelve cada subagente. | No (pero leelo) |
| `check.py` | Autocorrector (24 checks). | No |

```bash
cd labs/06-multiagente
python check.py         # revisa los huecos
python multiagente.py   # muestra los modelos, las tools y lo ÚNICO que recibe el redactor
```

1. **HUECO 1:** `tools` y `model` de cada subagente, y las tools del coordinador. Lección, secciones 4 y 6. Los strings van entre comillas: `["Read", "Grep"]`, `"haiku"`.
2. **HUECO 2:** qué va en el prompt del redactor (`True`/`False`). Lección, sección 3.
3. **HUECO 3:** el turno del coordinador que lanza dos subagentes y el mensaje con los dos resultados. Lección, sección 4, y lección 0001.

Objetivo: **24/24**. Guardá con `Ctrl+S` antes de cada corrida.

**Extra (opcional):** abrí `.claude/agents/` en cualquier proyecto tuyo y escribí el `explorador_tmdl` como subagente de Claude Code (frontmatter `name`, `description`, `tools`, `model`). Probalo con "usá el explorador_tmdl para encontrar cómo se calcula [medida]".
