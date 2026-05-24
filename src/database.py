"""
OptiBottle - Módulo de Base de Datos
Equipo 2 - Sistemas de Información
Maneja la conexión y operaciones con SQLite
"""

import sqlite3
import os
from datetime import datetime


class Database:
    """Clase para manejar la base de datos del sistema OptiBottle."""

    def __init__(self, db_path="data/optibottle.db"):
        # Asegurar que exista la carpeta data
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.crear_tablas()

    def crear_tablas(self):
        """Crea las tablas necesarias si no existen."""
        cursor = self.conn.cursor()

        # Tabla de materia prima
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materia_prima (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                stock_actual REAL NOT NULL DEFAULT 0,
                stock_minimo REAL NOT NULL DEFAULT 0,
                unidad TEXT NOT NULL DEFAULT 'kg'
            )
        """)

        # Tabla de órdenes de producción
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ordenes_produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                producto TEXT NOT NULL,
                cantidad_planeada INTEGER NOT NULL,
                cantidad_producida INTEGER DEFAULT 0,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT,
                estado TEXT NOT NULL DEFAULT 'Planeada',
                responsable TEXT
            )
        """)

        # Tabla de registros de producción (eventos diarios)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orden_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                turno TEXT NOT NULL,
                unidades_buenas INTEGER NOT NULL DEFAULT 0,
                unidades_defectuosas INTEGER NOT NULL DEFAULT 0,
                tiempo_muerto_min INTEGER NOT NULL DEFAULT 0,
                causa_paro TEXT,
                FOREIGN KEY (orden_id) REFERENCES ordenes_produccion(id)
            )
        """)

        self.conn.commit()

    # ---------- MATERIA PRIMA ----------
    def agregar_material(self, nombre, stock_actual, stock_minimo, unidad):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO materia_prima (nombre, stock_actual, stock_minimo, unidad) VALUES (?, ?, ?, ?)",
            (nombre, stock_actual, stock_minimo, unidad),
        )
        self.conn.commit()
        return cursor.lastrowid

    def listar_materiales(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM materia_prima ORDER BY nombre")
        return [dict(row) for row in cursor.fetchall()]

    def actualizar_stock(self, material_id, nuevo_stock):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE materia_prima SET stock_actual = ? WHERE id = ?",
            (nuevo_stock, material_id),
        )
        self.conn.commit()

    def eliminar_material(self, material_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM materia_prima WHERE id = ?", (material_id,))
        self.conn.commit()

    def materiales_bajo_minimo(self):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM materia_prima WHERE stock_actual < stock_minimo"
        )
        return [dict(row) for row in cursor.fetchall()]

    # ---------- ÓRDENES DE PRODUCCIÓN ----------
    def crear_orden(self, codigo, producto, cantidad_planeada, fecha_inicio, responsable):
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO ordenes_produccion
               (codigo, producto, cantidad_planeada, fecha_inicio, responsable)
               VALUES (?, ?, ?, ?, ?)""",
            (codigo, producto, cantidad_planeada, fecha_inicio, responsable),
        )
        self.conn.commit()
        return cursor.lastrowid

    def listar_ordenes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM ordenes_produccion ORDER BY fecha_inicio DESC")
        return [dict(row) for row in cursor.fetchall()]

    def actualizar_estado_orden(self, orden_id, estado, fecha_fin=None):
        cursor = self.conn.cursor()
        if fecha_fin:
            cursor.execute(
                "UPDATE ordenes_produccion SET estado = ?, fecha_fin = ? WHERE id = ?",
                (estado, fecha_fin, orden_id),
            )
        else:
            cursor.execute(
                "UPDATE ordenes_produccion SET estado = ? WHERE id = ?",
                (estado, orden_id),
            )
        self.conn.commit()

    def eliminar_orden(self, orden_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM registros_produccion WHERE orden_id = ?", (orden_id,))
        cursor.execute("DELETE FROM ordenes_produccion WHERE id = ?", (orden_id,))
        self.conn.commit()

    # ---------- REGISTROS DE PRODUCCIÓN ----------
    def registrar_produccion(self, orden_id, fecha, turno, buenas, defectuosas, tiempo_muerto, causa):
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO registros_produccion
               (orden_id, fecha, turno, unidades_buenas, unidades_defectuosas, tiempo_muerto_min, causa_paro)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (orden_id, fecha, turno, buenas, defectuosas, tiempo_muerto, causa),
        )
        # Actualizar la cantidad producida en la orden
        cursor.execute(
            """UPDATE ordenes_produccion
               SET cantidad_producida = cantidad_producida + ?
               WHERE id = ?""",
            (buenas, orden_id),
        )
        self.conn.commit()
        return cursor.lastrowid

    def listar_registros(self, orden_id=None):
        cursor = self.conn.cursor()
        if orden_id:
            cursor.execute(
                """SELECT r.*, o.codigo as orden_codigo, o.producto
                   FROM registros_produccion r
                   JOIN ordenes_produccion o ON r.orden_id = o.id
                   WHERE r.orden_id = ?
                   ORDER BY r.fecha DESC""",
                (orden_id,),
            )
        else:
            cursor.execute(
                """SELECT r.*, o.codigo as orden_codigo, o.producto
                   FROM registros_produccion r
                   JOIN ordenes_produccion o ON r.orden_id = o.id
                   ORDER BY r.fecha DESC"""
            )
        return [dict(row) for row in cursor.fetchall()]

    # ---------- MÉTRICAS / KPIs ----------
    def calcular_metricas(self):
        """Calcula KPIs globales del sistema."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                COALESCE(SUM(unidades_buenas), 0) as total_buenas,
                COALESCE(SUM(unidades_defectuosas), 0) as total_defectuosas,
                COALESCE(SUM(tiempo_muerto_min), 0) as total_tiempo_muerto
            FROM registros_produccion
        """)
        row = cursor.fetchone()
        total_buenas = row["total_buenas"]
        total_defectuosas = row["total_defectuosas"]
        total_tm = row["total_tiempo_muerto"]
        total_unidades = total_buenas + total_defectuosas

        porcentaje_desperdicio = (
            (total_defectuosas / total_unidades * 100) if total_unidades > 0 else 0
        )
        eficiencia_calidad = (
            (total_buenas / total_unidades * 100) if total_unidades > 0 else 0
        )

        return {
            "total_buenas": total_buenas,
            "total_defectuosas": total_defectuosas,
            "total_unidades": total_unidades,
            "tiempo_muerto_total": total_tm,
            "porcentaje_desperdicio": round(porcentaje_desperdicio, 2),
            "eficiencia_calidad": round(eficiencia_calidad, 2),
        }

    def causas_paro_frecuentes(self):
        """Devuelve las causas de paro más frecuentes."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT causa_paro, SUM(tiempo_muerto_min) as total_min, COUNT(*) as ocurrencias
            FROM registros_produccion
            WHERE causa_paro IS NOT NULL AND causa_paro != ''
            GROUP BY causa_paro
            ORDER BY total_min DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def produccion_por_orden(self):
        """Devuelve buenas y defectuosas agrupadas por orden."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT o.codigo,
                   COALESCE(SUM(r.unidades_buenas), 0) as buenas,
                   COALESCE(SUM(r.unidades_defectuosas), 0) as defectuosas
            FROM ordenes_produccion o
            LEFT JOIN registros_produccion r ON o.id = r.orden_id
            GROUP BY o.id, o.codigo
            HAVING (buenas + defectuosas) > 0
            ORDER BY o.codigo
        """)
        return [dict(row) for row in cursor.fetchall()]

    def produccion_por_fecha(self):
        """Devuelve totales de producción agrupados por fecha."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT fecha,
                   SUM(unidades_buenas) as buenas,
                   SUM(unidades_defectuosas) as defectuosas
            FROM registros_produccion
            GROUP BY fecha
            ORDER BY fecha
        """)
        return [dict(row) for row in cursor.fetchall()]

    def cerrar(self):
        self.conn.close()
