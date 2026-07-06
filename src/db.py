import sqlite3
import os
from datetime import datetime

# 🔥 Ruta correcta
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "bot.db"
)


# 🔹 Conexión DB
def get_conn():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )

    return conn


# 🔹 Crear tabla
def init_db():

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        # 🔥 WAL MODE
        cursor.execute(
            "PRAGMA journal_mode=WAL"
        )

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS descargas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT,
            archivo TEXT,
            fecha TEXT,
            estado TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            tipo TEXT,
            mensaje TEXT
        )
        """)

        conn.commit()

    except Exception as e:

        print(
            f"❌ Error init_db: {e}"
        )

    finally:

        if conn:

            conn.close()


# 🔹 Insertar descarga
def insertar_descarga(area, archivo):

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        fecha = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO descargas
            (area, archivo, fecha, estado)
            VALUES (?, ?, ?, ?)
            """,
            (
                area,
                archivo,
                fecha,
                "OK"
            )
        )

        conn.commit()

    except Exception as e:

        print(
            f"❌ Error insertar_descarga: {e}"
        )

    finally:

        if conn:

            conn.close()


# 🔹 Obtener últimas descargas
def obtener_descargas(limit=20):

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT area, archivo, fecha, estado
            FROM descargas
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print(
            f"❌ Error obtener_descargas: {e}"
        )

        return []

    finally:

        if conn:

            conn.close()


# 🔹 Contar descargas totales
def contar_descargas():

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM descargas"
        )

        total = cursor.fetchone()[0]

        return total

    except Exception as e:

        print(
            f"❌ Error contar_descargas: {e}"
        )

        return 0

    finally:

        if conn:

            conn.close()


# 🔹 Descargas hoy
def contar_descargas_hoy():

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM descargas
            WHERE date(fecha)
            =
            date('now','localtime')
            """
        )

        total = cursor.fetchone()[0]

        return total

    except Exception as e:

        print(
            f"❌ Error contar_descargas_hoy: {e}"
        )

        return 0

    finally:

        if conn:

            conn.close()


# 🔹 Estadísticas por área
def obtener_stats_areas():

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT area, COUNT(*)
            FROM descargas
            GROUP BY area
            """
        )

        rows = cursor.fetchall()

        return rows

    except Exception as e:

        print(
            f"❌ Error obtener_stats_areas: {e}"
        )

        return []

    finally:

        if conn:

            conn.close()
            
            
def registrar_evento(
        tipo,
        mensaje
):

    conn = None

    try:

        conn = get_conn()

        cursor = conn.cursor()

        fecha = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO eventos
            (
                fecha,
                tipo,
                mensaje
            )
            VALUES
            (?, ?, ?)
            """,
            (
                fecha,
                tipo,
                mensaje
            )
        )

        conn.commit()

    except Exception as e:

        print(
            f"❌ Error registrar_evento: {e}"
        )

    finally:

        if conn:

            conn.close()