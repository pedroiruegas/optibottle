"""
OptiBottle - Pruebas Unitarias
Verifican el correcto funcionamiento del módulo de base de datos.
Ejecutar: python -m unittest tests/test_database.py -v
"""

import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from database import Database


class TestDatabase(unittest.TestCase):
    """Pruebas para la clase Database."""

    def setUp(self):
        """Se ejecuta antes de cada prueba: crea una BD temporal."""
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        self.db = Database(self.tmp.name)

    def tearDown(self):
        """Se ejecuta después de cada prueba: cierra y elimina la BD."""
        self.db.cerrar()
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    # ---------- Pruebas de materia prima ----------
    def test_agregar_material(self):
        """Debe agregar un material correctamente."""
        mat_id = self.db.agregar_material("PET", 100, 50, "kg")
        self.assertIsNotNone(mat_id)
        mats = self.db.listar_materiales()
        self.assertEqual(len(mats), 1)
        self.assertEqual(mats[0]["nombre"], "PET")

    def test_actualizar_stock(self):
        """El stock debe actualizarse correctamente."""
        mat_id = self.db.agregar_material("Tapas", 1000, 500, "piezas")
        self.db.actualizar_stock(mat_id, 750)
        mats = self.db.listar_materiales()
        self.assertEqual(mats[0]["stock_actual"], 750)

    def test_materiales_bajo_minimo(self):
        """Debe detectar materiales con stock por debajo del mínimo."""
        self.db.agregar_material("PET", 100, 50, "kg")  # OK
        self.db.agregar_material("Etiquetas", 200, 500, "piezas")  # BAJO
        bajos = self.db.materiales_bajo_minimo()
        self.assertEqual(len(bajos), 1)
        self.assertEqual(bajos[0]["nombre"], "Etiquetas")

    def test_eliminar_material(self):
        """Debe eliminar un material existente."""
        mat_id = self.db.agregar_material("Temp", 10, 5, "kg")
        self.db.eliminar_material(mat_id)
        self.assertEqual(len(self.db.listar_materiales()), 0)

    # ---------- Pruebas de órdenes ----------
    def test_crear_orden(self):
        """Debe crear una orden de producción."""
        orden_id = self.db.crear_orden(
            "ORD-TEST", "Botella 500ml", 1000, "2026-05-22", "Test User"
        )
        self.assertIsNotNone(orden_id)
        ordenes = self.db.listar_ordenes()
        self.assertEqual(len(ordenes), 1)
        self.assertEqual(ordenes[0]["estado"], "Planeada")

    def test_actualizar_estado_orden(self):
        """El estado de una orden debe poder cambiar."""
        orden_id = self.db.crear_orden("O1", "Prod", 100, "2026-05-22", "X")
        self.db.actualizar_estado_orden(orden_id, "En Proceso")
        ordenes = self.db.listar_ordenes()
        self.assertEqual(ordenes[0]["estado"], "En Proceso")

    # ---------- Pruebas de registros y métricas ----------
    def test_registrar_produccion(self):
        """Debe registrar la producción y actualizar la cantidad producida."""
        orden_id = self.db.crear_orden("O1", "Prod", 1000, "2026-05-22", "X")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Matutino", 500, 20, 15, "Sin paro")
        ordenes = self.db.listar_ordenes()
        self.assertEqual(ordenes[0]["cantidad_producida"], 500)

    def test_calcular_metricas(self):
        """Las métricas deben calcularse correctamente."""
        orden_id = self.db.crear_orden("O1", "Prod", 1000, "2026-05-22", "X")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Matutino", 900, 100, 30, "Causa A")
        m = self.db.calcular_metricas()
        self.assertEqual(m["total_buenas"], 900)
        self.assertEqual(m["total_defectuosas"], 100)
        self.assertEqual(m["total_unidades"], 1000)
        self.assertEqual(m["porcentaje_desperdicio"], 10.0)
        self.assertEqual(m["eficiencia_calidad"], 90.0)
        self.assertEqual(m["tiempo_muerto_total"], 30)

    def test_metricas_sin_datos(self):
        """Sin registros, las métricas deben dar 0 sin errores."""
        m = self.db.calcular_metricas()
        self.assertEqual(m["total_buenas"], 0)
        self.assertEqual(m["porcentaje_desperdicio"], 0)

    def test_causas_paro_frecuentes(self):
        """Debe agregar y ordenar las causas por tiempo total."""
        orden_id = self.db.crear_orden("O1", "P", 1000, "2026-05-22", "X")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Matutino", 100, 10, 30, "Mantenimiento")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Vespertino", 100, 10, 60, "Mantenimiento")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Nocturno", 100, 10, 20, "Cambio de molde")
        causas = self.db.causas_paro_frecuentes()
        self.assertEqual(len(causas), 2)
        # La más alta debe ser Mantenimiento con 90 min
        self.assertEqual(causas[0]["causa_paro"], "Mantenimiento")
        self.assertEqual(causas[0]["total_min"], 90)

    def test_eliminar_orden_borra_registros(self):
        """Al eliminar una orden, sus registros deben eliminarse también."""
        orden_id = self.db.crear_orden("O1", "P", 1000, "2026-05-22", "X")
        self.db.registrar_produccion(orden_id, "2026-05-22", "Matutino", 100, 10, 0, "Sin paro")
        self.db.eliminar_orden(orden_id)
        self.assertEqual(len(self.db.listar_ordenes()), 0)
        self.assertEqual(len(self.db.listar_registros()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
