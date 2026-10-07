# Lab 03 · Prompt de revisión de medidas DAX

**Formato:** completar huecos (no escribís código desde cero). No hace falta API key.

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `prompt.py` | System prompt + criterios + few-shot + armado del prompt. Tiene 3 huecos `___`. | **Sí** |
| `check.py` | Autocorrector (17 checks). | No |

```bash
cd labs/03-prompts
python check.py     # revisa los huecos
python prompt.py    # imprime el prompt completo que recibiría Claude
```

1. **HUECO 1:** criterios explícitos: qué categorías reportar y cuáles no (sin "cuidado", "importante"…).
2. **HUECO 2:** el tercer ejemplo few-shot, un caso ambiguo: decisión, severidad y razonamiento.
3. **HUECO 3:** el nombre del tag XML que delimita la medida a revisar.

Objetivo: **17/17**. Después, `python prompt.py` y leé el prompt entero de arriba abajo como si fueras Claude.
