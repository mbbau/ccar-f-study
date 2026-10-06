"""Mini DWH del Lab 02. Ahora con errores tipados, como un DWH real. No hace falta tocarlo."""
import sqlite3


class ValidacionError(Exception):
    """El SQL es inválido o no es un SELECT. Reintentar igual no sirve: hay que corregir la consulta."""


class PermisoError(Exception):
    """La consulta toca una tabla a la que este agente no tiene acceso."""


class TransitorioError(Exception):
    """Falla temporal (timeout, conexión). Reintentar en unos segundos puede funcionar."""


_conn = sqlite3.connect(":memory:")
_conn.executescript("""
CREATE TABLE despachos (fecha TEXT, planta TEXT, cliente TEXT, producto TEXT, m3 REAL, precio_m3 REAL);
INSERT INTO despachos VALUES
 ('2026-09-01','Córdoba Norte','Constructora A','H-21',32,98000),
 ('2026-09-01','Córdoba Sur','Constructora B','H-30',18,121000),
 ('2026-09-02','Córdoba Norte','Constructora C','H-21',45,98000),
 ('2026-09-03','Córdoba Sur','Constructora A','H-25',27,109000),
 ('2026-09-03','Río Segundo','Constructora D','H-21',12,95000),
 ('2026-09-04','Córdoba Norte','Constructora B','H-30',22,121000);
CREATE TABLE costos (planta TEXT, costo_m3 REAL);
INSERT INTO costos VALUES ('Córdoba Norte',71000),('Córdoba Sur',76000),('Río Segundo',69000);
""")

TABLAS_PERMITIDAS = {"despachos"}
ESQUEMA = {"despachos": "fecha TEXT, planta TEXT, cliente TEXT, producto TEXT, m3 REAL, precio_m3 REAL"}


def consultar_sql(sql: str) -> str:
    s = sql.strip().lower()
    if not s.startswith("select"):
        raise ValidacionError("Solo se permiten consultas SELECT.")
    if "costos" in s:
        raise PermisoError("Sin acceso a la tabla 'costos' (datos financieros restringidos).")
    if "/*lento*/" in s:
        raise TransitorioError("Timeout: el DWH no respondió en 30 s.")
    try:
        cur = _conn.execute(sql)
    except sqlite3.Error as e:
        raise ValidacionError(f"SQL inválido: {e}")
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    if not rows:
        return "0 filas."
    return "\n".join([" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows])


def listar_tablas() -> str:
    return "\n".join(f"{t}({cols})" for t, cols in ESQUEMA.items())
