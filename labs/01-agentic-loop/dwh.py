"""Mini DWH en SQLite (en memoria) para el lab. No hace falta tocarlo."""
import sqlite3

_conn = sqlite3.connect(":memory:")
_conn.executescript("""
CREATE TABLE despachos (
    fecha TEXT, planta TEXT, cliente TEXT, producto TEXT, m3 REAL, precio_m3 REAL
);
INSERT INTO despachos VALUES
 ('2026-09-01','Córdoba Norte','Constructora A','H-21',32,98000),
 ('2026-09-01','Córdoba Sur','Constructora B','H-30',18,121000),
 ('2026-09-02','Córdoba Norte','Constructora C','H-21',45,98000),
 ('2026-09-03','Córdoba Sur','Constructora A','H-25',27,109000),
 ('2026-09-03','Río Segundo','Constructora D','H-21',12,95000),
 ('2026-09-04','Córdoba Norte','Constructora B','H-30',22,121000);
""")


def query_dwh(sql: str) -> str:
    """Ejecuta SQL de solo lectura y devuelve el resultado como texto tabular.
    Lanza excepción si el SQL es inválido o no es un SELECT."""
    if not sql.strip().lower().startswith("select"):
        raise ValueError("Solo se permiten consultas SELECT.")
    cur = _conn.execute(sql)
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    lines = [" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows]
    return "\n".join(lines) if rows else "(sin filas)"


SCHEMA = "despachos(fecha TEXT, planta TEXT, cliente TEXT, producto TEXT, m3 REAL, precio_m3 REAL)"
