"""Reordena el plan CCAR-F según dependencias (28/9/2026).

Qué hace:
  1. Renombra labels para alinearlos con la numeración de la guía oficial
     (D2 = Tools/MCP, D3 = Claude Code, D4 = Prompts).
  2. Renombra los milestones de las semanas 1-3.
  3. Actualiza título, cuerpo, milestone y labels de los issues #1-#17.
Los números de issue NO cambian, así que los "closes #N" siguen funcionando.

Uso (PowerShell, con gh logueado en tu cuenta personal):
    gh auth status
    python scripts/reordenar_issues.py --dry-run   # muestra qué haría
    python scripts/reordenar_issues.py             # aplica
"""
import json
import subprocess
import sys

REPO = "mbbau/ccar-f-study"
DRY = "--dry-run" in sys.argv
GUIA = "https://everpath-course-content.s3-accelerate.amazonaws.com/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1783542750/Claude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf"

sys.stdout.reconfigure(encoding="utf-8")


def gh(*args, capture=False):
    cmd = ["gh", *args]
    if DRY and not capture:
        print("  [dry-run]", " ".join(a if " " not in a else f'"{a}"' for a in cmd[:8]), "..." if len(cmd) > 8 else "")
        return ""
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} falló:\n{r.stderr}")
    return r.stdout


# --- 1. Labels ----------------------------------------------------------------
LABELS = {
    "D4-mcp-tools": ("D2-tools-mcp", "Dominio 2 · Diseño de tools e integración MCP (18%)"),
    "D2-claude-code": ("D3-claude-code", "Dominio 3 · Claude Code: configuración y workflows (20%)"),
    "D3-prompts-schema": ("D4-prompts-schema", "Dominio 4 · Prompt engineering y salida estructurada (20%)"),
}

# --- 2. Milestones (se busca por prefijo) ---------------------------------------
MILESTONES = {
    "Semana 1": "Semana 1 · Fundamentos (API, tools, prompts, contexto)",
    "Semana 2": "Semana 2 · Agentes + MCP",
    "Semana 3": "Semana 3 · Claude Code + confiabilidad",
}
M1, M2, M3 = MILESTONES.values()

# --- 3. Issues ----------------------------------------------------------------
RUTINA = """## Rutina (90 min)

- [ ] 10 min · Repaso activo: 5 preguntas del día anterior sin mirar notas
- [ ] 40 min · Estudio del tema (NotebookLM + doc oficial), anotando trade-offs "X cuando..., Y cuando..."
- [ ] 30 min · Lab del día
- [ ] 10 min · Escribir 3 preguntas tipo examen + actualizar `errores.md`

## Notas
"""


def body(fecha, iso, guia, tema, lab, trampa):
    return f"""**{fecha}** · {iso}

**Guía oficial:** {guia} ([PDF]({GUIA}))

## Tema

{tema}

## Lab

{lab}

## Trampa típica

{trampa}

{RUTINA}"""


def bloque(fecha, iso, actividad):
    return f"""**{fecha}** · {iso}

## Actividad

{actividad}

## Criterio de salida

≥ 75% en el bloque

## Checklist

- [ ] Hacer el bloque sin mirar notas
- [ ] Registrar cada error en `errores.md`
- [ ] Re-estudiar los 2 temas más fallados
- [ ] Anotar el resultado (%) acá abajo

## Resultado
"""


ISSUES = [
    # ---------------- Semana 1 · Fundamentos ----------------
    dict(n=1, ms=M1, title="Día 01 · Messages API y agentic loop (stop_reason)",
         body=body("Lun 28/9", "2026-09-28", "task statement 1.1 (+ fundamentos de la Messages API)",
                   "Anatomía de una llamada a la Messages API (request: `model`, `max_tokens`, `messages`, roles, `tools`; response: bloques de `content`, `stop_reason`, `usage`). Ciclo agéntico: `stop_reason` (`tool_use`, `end_turn`, `max_tokens`, `pause_turn`), manejo del historial y `tool_result` con el mismo `tool_use_id`.",
                   "Loop en Python con 1 tool (`query_dwh`) que imprime cada `stop_reason`. Autocorrector `check.py` (6 escenarios). Carpeta: `labs/01-agentic-loop/`.",
                   "Cortar el loop por el texto de la respuesta en vez de por `stop_reason`.")),
    dict(n=3, ms=M1, title="Día 02 · Diseño de tools y tool_choice",
         add=["D2-tools-mcp", "lab"], remove=["D1-agentes"],
         body=body("Mar 29/9", "2026-09-29", "task statements 2.1, 2.2 y 2.3",
                   "Definición de tools: `name`, `description` (principal mecanismo de selección del modelo), `input_schema`. Descripciones diferenciadas, separar tools genéricas en específicas. `tool_choice` (`auto`, `any`, forzar una tool, `none`). Pocas tools por agente = mejor selección. Errores estructurados con `is_error`: transitorio vs validación vs negocio vs permisos; reintentable vs no reintentable; \"sin resultados\" ≠ \"sin acceso\".",
                   "Reescribir `query_dwh` del Lab 01 en 2-3 tools específicas con descripciones diferenciadas y errores estructurados. Carpeta: `labs/02-tool-design/`.",
                   "Una tool genérica con descripción vaga (\"consulta datos\") o devolver \"sin resultados\" cuando en realidad falló el acceso.")),
    dict(n=8, ms=M1, title="Día 03 · System prompts y few-shot",
         body=body("Mié 30/9", "2026-09-30", "task statements 4.1 y 4.2",
                   "Delimitadores explícitos (XML), few-shot para casos ambiguos, criterios concretos para minimizar falsos positivos.",
                   "Prompt de revisión de medidas DAX con 3 ejemplos límite en `labs/08-prompts/`.",
                   "Instrucciones vagas (\"sé cuidadoso\") en vez de criterios concretos.")),
    dict(n=9, ms=M1, title="Día 04 · Salida estructurada y Message Batches",
         body=body("Jue 1/10", "2026-10-01", "task statements 4.3, 4.4 y 4.5",
                   "Salida garantizada con `tool_use` + JSON Schema (`tool_choice` forzado), loop validar-reintentar con el error, Message Batches API (-50%, asíncrona, hasta 24 h).",
                   "Extractor de specs de un requerimiento a JSON validado con `jsonschema` en `labs/09-structured-output/`.",
                   "Usar Batches para algo que necesita respuesta en tiempo real.")),
    dict(n=11, ms=M1, title="Día 05 · Ventana de contexto y lost in the middle",
         body=body("Vie 2/10", "2026-10-02", "task statements 5.1 y 5.4",
                   "Gestión de la ventana de contexto, \"lost in the middle\" (lo crítico al inicio o al final), resumir y descartar lo irrelevante, prompt caching. Base para entender el aislamiento de contexto de los subagentes (Día 06).",
                   "Reordenar un prompt largo con contexto TMDL y comparar respuestas.",
                   "Creer que más contexto siempre mejora la respuesta.")),
    # ---------------- Semana 2 · Agentes + MCP ----------------
    dict(n=2, ms=M2, title="Día 06 · Orquestación multi-agente y asignación de modelos",
         add=["lab"],
         body=body("Lun 5/10", "2026-10-05", "task statements 1.2, 1.3 y 1.6 (+ elección de modelos)",
                   "Patrón hub-and-spoke (coordinator-subagent), aislamiento de contexto, herramienta `Task` / subagentes con `allowedTools`, descomposición de tareas. Criterios Opus / Sonnet / Haiku para orquestador vs subagentes según latencia, costo y complejidad.",
                   "Diagramar (Mermaid en `notes/`) el agente \"analista\": orquestador + 3 subagentes con tools mínimas, y una tabla costo/latencia con 3 combinaciones de modelos en `notes/modelos.md`.",
                   "Pasarle todo el historial al subagente \"por las dudas\", o elegir el modelo más potente para todo.")),
    dict(n=4, ms=M2, title="Día 07 · Arquitectura MCP y primitivas",
         body=body("Mar 6/10", "2026-10-06", "task statement 2.4",
                   "Host, Client, Server. Primitivas: tools (las invoca el modelo), resources (contexto que elige la app), prompts (plantillas que elige el usuario).",
                   "Clasificar 10 capacidades del DWH en tool / resource / prompt en `notes/mcp-primitivas.md`.",
                   "Exponer como tool algo que es un resource de solo lectura.")),
    dict(n=5, ms=M2, title="Día 08 · Transportes MCP, scopes y tools nativas",
         body=body("Mié 7/10", "2026-10-07", "task statements 2.4 y 2.5",
                   "`stdio` (local) vs HTTP (remoto; la spec nueva usa Streamable HTTP, el material puede decir HTTP+SSE). Scope de servidores (proyecto vs usuario) y variables de entorno en la config. `isError` en MCP. Tools nativas: `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`.",
                   "Mapa mental D1 + D2 en NotebookLM y 15 preguntas de repaso.",
                   "Tirar una excepción en vez de devolver `isError: true` para que el modelo se recupere.")),
    dict(n=14, ms=M2, title="Día 09 · Lab integrador: server MCP",
         body=body("Jue 8/10", "2026-10-08", "task statements 2.2 y 2.4",
                   "Sesión completa de 90 min de práctica, con la teoría de MCP todavía fresca.",
                   "Server MCP mínimo en Python (SDK oficial, `stdio`) con 1 tool y 1 resource sobre el DWH, conectado a Claude Code. Probar un error con `isError`. Carpeta: `labs/14-mcp-server/`.",
                   "Saltear el lab \"porque ya lo leí\".")),
    dict(n=10, ms=M2, title="Día 10 · Repaso semanas 1-2 + Cuestionario ronda 1",
         body=body("Vie 9/10", "2026-10-09", "dominios 1, 2, 4 y 5.1",
                   "Repaso de la primera mitad del temario (API y loop, tools, prompts, salida estructurada, contexto, multi-agente, MCP) y 40 preguntas en \"Claude Cuestionario\".",
                   "Registrar cada error en `errores.md`.",
                   "Estudiar solo lo que salió bien.")),
    # ---------------- Semana 3 · Claude Code + confiabilidad ----------------
    dict(n=6, ms=M3, title="Día 11 · Jerarquía de CLAUDE.md y reglas",
         body=body("Lun 12/10", "2026-10-12", "task statements 3.1 y 3.3",
                   "Jerarquía de `CLAUDE.md` (usuario, proyecto, directorio) y reglas condicionales con glob en `.claude/rules/`.",
                   "`CLAUDE.md` + 2 reglas (SQL y TMDL por separado) en `labs/06-claude-md/`.",
                   "Meter todo en un solo `CLAUDE.md` gigante.")),
    dict(n=7, ms=M3, title="Día 12 · Commands, Skills, Plan Mode y CI/CD",
         body=body("Mar 13/10", "2026-10-13", "task statements 3.2, 3.4, 3.5 y 3.6",
                   "Slash commands (`.claude/commands/`), Skills (`.claude/skills/`), Plan Mode vs ejecución directa, headless con `-p` y `--output-format json`.",
                   "Comando `/review-sql` + corrida headless que devuelve JSON. Opcional: GitHub Action en este repo que corra `claude -p` sobre cada PR.",
                   "Usar Plan Mode para un cambio trivial, o no usarlo en un cambio multi-archivo.")),
    dict(n=12, ms=M3, title="Día 13 · Human-in-the-loop y propagación de errores",
         body=body("Mié 14/10", "2026-10-14", "task statements 5.2 y 5.3",
                   "Cuándo escalar a un humano (acciones irreversibles, baja confianza, ambigüedad) y cómo propagar errores entre subagentes.",
                   "Definir reglas de escalado del agente \"analista\" en `notes/hitl.md`.",
                   "Reintentar en silencio en vez de reportar el fallo al orquestador.")),
    dict(n=13, ms=M3, title="Día 14 · Provenance y calibración de confianza",
         body=body("Jue 15/10", "2026-10-15", "task statements 5.5 y 5.6",
                   "Trazabilidad de afirmaciones, mapeo afirmación-fuente, citas, calibración de confianza.",
                   "Hacer que el agente cite tabla y query de cada número que devuelve.",
                   "Aceptar una síntesis sin trazar sus fuentes.")),
    dict(n=15, ms=M3, title="Día 15 · Distractores del examen",
         body=body("Vie 16/10", "2026-10-16", "todas (técnica de examen)",
                   "Absolutos (\"siempre\", \"nunca\"), soluciones sobredimensionadas, opción correcta pero no la más simple.",
                   "Reescribir 10 preguntas falladas explicando por qué cada distractor es incorrecto.",
                   "Elegir la opción más sofisticada en vez de la que resuelve el problema planteado.")),
    # ---------------- Semana 4 · solo renumeración de dominios ----------------
    dict(n=16, ms=None, title="Día 16 · Bloque D1 + D2 (agentes + tools/MCP)",
         body=bloque("Lun 19/10", "2026-10-19", "30 escenarios de D1 + D2 en \"Claude Cuestionario\", sin mirar notas.")),
    dict(n=17, ms=None, title="Día 17 · Bloque D3 + D4 (Claude Code + prompts)",
         body=bloque("Mar 20/10", "2026-10-20", "30 escenarios de D3 + D4 en \"Claude Cuestionario\", sin mirar notas.")),
]


def main():
    who = gh("api", "user", "--jq", ".login", capture=True).strip()
    print(f"gh logueado como: {who}")
    if who != REPO.split("/")[0]:
        sys.exit(f"Esperaba {REPO.split('/')[0]}. Corré 'gh auth switch' o 'gh auth login'.")

    print("\n1) Labels")
    existing = {l["name"] for l in json.loads(gh("label", "list", "-R", REPO, "--json", "name", "--limit", "100", capture=True))}
    for old, (new, desc) in LABELS.items():
        if old in existing:
            print(f"  {old} -> {new}")
            gh("label", "edit", old, "-R", REPO, "--name", new, "--description", desc)
        else:
            print(f"  (ya estaba) {new}")

    print("\n2) Milestones")
    ms = json.loads(gh("api", f"repos/{REPO}/milestones?state=all&per_page=100", capture=True))
    for prefix, new in MILESTONES.items():
        m = next((m for m in ms if m["title"].startswith(prefix)), None)
        if not m:
            sys.exit(f"No encontré el milestone que empieza con '{prefix}'.")
        print(f"  {m['title']} -> {new}")
        if m["title"] != new:
            gh("api", "-X", "PATCH", f"repos/{REPO}/milestones/{m['number']}", "-f", f"title={new}")

    print("\n3) Issues")
    for it in ISSUES:
        print(f"  #{it['n']:>2} {it['title']}")
        args = ["issue", "edit", str(it["n"]), "-R", REPO, "--title", it["title"], "--body", it["body"]]
        if it["ms"]:
            args += ["--milestone", it["ms"]]
        for l in it.get("add", []):
            args += ["--add-label", l]
        for l in it.get("remove", []):
            args += ["--remove-label", l]
        gh(*args)

    print("\nListo." if not DRY else "\nDry-run terminado: no se cambió nada.")


if __name__ == "__main__":
    main()
