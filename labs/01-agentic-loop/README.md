# Lab 01 · Agentic loop y `stop_reason`

**Objetivo:** un loop en Python con 1 tool (`query_dwh`) que imprime cada `stop_reason` y decide qué hacer **solo** en base a él.

## Archivos

| Archivo | Qué es | ¿Lo tocás? |
| --- | --- | --- |
| `loop.py` | Tu loop. Tiene 2 `TODO`. | **Sí** |
| `check.py` | Autocorrector: 6 escenarios con un cliente falso. | No |
| `mock_client.py` | Cliente falso con la misma forma que `client.messages.create()`. | No |
| `dwh.py` | Mini DWH SQLite en memoria (despachos de hormigón). | No |

## Pasos (Windows / PowerShell)

```powershell
cd labs\01-agentic-loop
python check.py            # 0/6 al principio: es esperado
# ...completá TODO 1 y TODO 2 en loop.py...
python check.py            # objetivo: 6/6
python loop.py --mock      # happy path con el cliente falso
```

Opcional, contra la API real:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install anthropic
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python loop.py
```

## Regla del día

> El loop se corta por `stop_reason`, nunca por el texto de la respuesta.
