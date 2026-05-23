# 🏭 OptiBottle

> Sistema de información para la **optimización del área de producción** en una empresa mediana de fabricación de botellas plásticas.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/tests-11%2F11%20passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-Academic-yellow?style=flat-square)

**Proyecto Integrador de Aprendizaje (PIA)** | Sistemas de Información | Equipo 2

🌐 **[Ver sitio web del proyecto →](https://TU_USUARIO.github.io/optibottle/)**

---

## 📋 Tabla de contenidos

- [Sobre el proyecto](#-sobre-el-proyecto)
- [Funcionalidades](#-funcionalidades)
- [Stack tecnológico](#-stack-tecnológico)
- [Instalación](#-instalación)
- [Capturas](#-capturas)
- [Documentación](#-documentación)
- [Pruebas](#-pruebas)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Equipo](#-equipo)

---

## 🎯 Sobre el proyecto

En una planta mediana de producción de botellas plásticas, cada turno genera cientos de eventos productivos: piezas buenas, defectuosas, paros por mantenimiento, falta de material o cambios de molde. Sin un sistema, toda esa información se pierde o se anota en papel.

**OptiBottle** digitaliza la captura, calcula indicadores automáticamente y muestra alertas para apoyar la toma de decisiones, ayudando a la empresa a:

- 📉 Reducir desperdicios
- ⏱️ Disminuir tiempos muertos
- 🎯 Identificar causas de paro
- 📊 Tomar decisiones basadas en datos

---

## ✨ Funcionalidades

| Módulo | Descripción |
|--------|-------------|
| 📊 **Dashboard** | KPIs en vivo: unidades buenas/defectuosas, % desperdicio, eficiencia, tiempo muerto, causas de paro y alertas |
| 📋 **Órdenes de Producción** | Alta, gestión de estados (Planeada/En Proceso/Pausada/Finalizada), exportación a CSV |
| 📦 **Materia Prima** | Inventario con alertas automáticas de stock mínimo |
| ✏️ **Registro de Producción** | Captura por turno con causas de paro |

---

## 🛠️ Stack tecnológico

- **Python 3.8+** — Lenguaje principal
- **Tkinter/ttk** — Interfaz gráfica de escritorio (incluida en Python)
- **SQLite** — Base de datos embebida (incluida en Python)
- **unittest** — Pruebas unitarias (incluida en Python)

> ✅ **Cero dependencias externas.** Todo viene incluido con Python.

---

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior

### Pasos
```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/optibottle.git
cd optibottle

# 2. (Opcional) Cargar datos de ejemplo
python cargar_datos_ejemplo.py

# 3. Ejecutar la aplicación
python src/main.py
```

---

## 📸 Capturas

> Las capturas aparecerán al ejecutar el sistema. El dashboard muestra los KPIs en tiempo real con tarjetas a color y una tabla de causas de paro.

---

## 📚 Documentación

Toda la documentación está disponible en **[el sitio web del proyecto](https://TU_USUARIO.github.io/optibottle/)** o descarga los PDFs directamente:

- 📘 [**Manual Técnico**](docs/manuales/optibottle_Manual_Tecnico.pdf) — Arquitectura, modelo de datos, módulos, fórmulas y pruebas
- 📗 [**Manual de Usuario**](docs/manuales/optibottle_Manual_Usuario.pdf) — Guía paso a paso para operadores y supervisores
- 🎬 [**Guion del Video**](docs/manuales/optibottle_Guion_Video.pdf) — Script completo para grabar la demo

---

## 🧪 Pruebas

El proyecto incluye **11 pruebas unitarias** que verifican el correcto funcionamiento de la capa de datos.

```bash
python -m unittest tests/test_database.py -v
```

**Resultado esperado:**
```
Ran 11 tests in 0.22s
OK
```

Las pruebas cubren:
- ✅ Alta, actualización y eliminación de materiales
- ✅ Detección de stock bajo mínimo
- ✅ Creación y cambio de estado de órdenes
- ✅ Registro de producción y actualización de cantidades
- ✅ Cálculo de KPIs y métricas
- ✅ Integridad referencial al eliminar órdenes

---

## 📁 Estructura del proyecto

```
optibottle/
├── src/
│   ├── main.py              # Interfaz gráfica (Tkinter)
│   └── database.py          # Capa de datos (SQLite)
├── tests/
│   ├── test_database.py     # Pruebas unitarias
│   └── resultado_pruebas.txt
├── docs/                    # Sitio web (GitHub Pages)
│   ├── index.html
│   ├── manual-tecnico.html
│   ├── manual-usuario.html
│   ├── guion-video.html
│   └── manuales/            # PDFs de los manuales
├── data/                    # Base de datos (auto-generada)
├── cargar_datos_ejemplo.py  # Script con datos demo
├── .gitignore
└── README.md
```

---

## 👥 Equipo

**Equipo 2** — Sistemas de Información

---

## 📄 Licencia

Proyecto académico desarrollado para la unidad de aprendizaje de Sistemas de Información. Uso educativo.
