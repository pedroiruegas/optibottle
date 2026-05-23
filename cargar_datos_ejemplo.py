"""
OptiBottle - Cargar datos de ejemplo
Útil para demostraciones y para el video del PIA.
Ejecutar: python cargar_datos_ejemplo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from database import Database


def cargar():
    # Eliminar BD previa si existe
    db_path = "data/optibottle.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"BD anterior eliminada: {db_path}")

    db = Database(db_path)

    print("Cargando materiales...")
    db.agregar_material("PET (resina)", 850, 500, "kg")
    db.agregar_material("Tapas plásticas", 12000, 5000, "piezas")
    db.agregar_material("Etiquetas", 8500, 10000, "piezas")  # Bajo mínimo
    db.agregar_material("Colorante azul", 45, 30, "kg")
    db.agregar_material("Pegamento", 18, 25, "litros")  # Bajo mínimo

    print("Cargando órdenes...")
    o1 = db.crear_orden("ORD-001", "Botella PET 500ml", 50000, "2026-05-15", "Juan Pérez")
    o2 = db.crear_orden("ORD-002", "Botella PET 1L", 25000, "2026-05-18", "María López")
    o3 = db.crear_orden("ORD-003", "Botella PET 600ml", 30000, "2026-05-20", "Carlos Ruiz")

    db.actualizar_estado_orden(o1, "En Proceso")
    db.actualizar_estado_orden(o2, "En Proceso")

    print("Cargando registros de producción...")
    # Orden 1
    db.registrar_produccion(o1, "2026-05-15", "Matutino", 8500, 320, 45, "Mantenimiento")
    db.registrar_produccion(o1, "2026-05-15", "Vespertino", 9200, 180, 20, "Sin paro")
    db.registrar_produccion(o1, "2026-05-16", "Matutino", 9100, 250, 30, "Cambio de molde")
    db.registrar_produccion(o1, "2026-05-16", "Vespertino", 8800, 410, 60, "Falla eléctrica")
    db.registrar_produccion(o1, "2026-05-17", "Matutino", 9400, 200, 15, "Sin paro")

    # Orden 2
    db.registrar_produccion(o2, "2026-05-18", "Matutino", 4200, 180, 25, "Falta de material")
    db.registrar_produccion(o2, "2026-05-18", "Vespertino", 4500, 95, 10, "Sin paro")
    db.registrar_produccion(o2, "2026-05-19", "Matutino", 4300, 220, 35, "Mantenimiento")

    # Orden 3
    db.registrar_produccion(o3, "2026-05-20", "Matutino", 5100, 290, 40, "Calidad / rechazo")

    print("\n✅ Datos de ejemplo cargados con éxito!")
    print("\nResumen:")
    m = db.calcular_metricas()
    print(f"  Total unidades buenas: {m['total_buenas']:,}")
    print(f"  Total unidades defectuosas: {m['total_defectuosas']:,}")
    print(f"  % de desperdicio: {m['porcentaje_desperdicio']}%")
    print(f"  Eficiencia de calidad: {m['eficiencia_calidad']}%")
    print(f"  Tiempo muerto total: {m['tiempo_muerto_total']} min")

    db.cerrar()


if __name__ == "__main__":
    cargar()
