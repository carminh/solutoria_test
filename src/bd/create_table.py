
import sqlite3
from bd.conexion import conexionBD

def creacion_tabla():
    conn = conexionBD.get_bd_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uf_historica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreIndicador TEXT,
            codigoIndicador TEXT,
            unidadMedidaIndicador TEXT,
            valorIndicador REAL,
            fechaIndicador TEXT,
            fecha_actualizacion TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()