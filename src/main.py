"""
OptiBottle - Sistema de Información para Optimización de Producción
Equipo 2 - Empresa de Botellas Plásticas
Interfaz Gráfica Principal
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os
import sys

# Matplotlib para gráficas embebidas
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Permitir importar desde la misma carpeta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import Database


class OptiBottleApp:
    """Aplicación principal del sistema OptiBottle."""

    COLOR_PRIMARIO = "#1e3a8a"
    COLOR_SECUNDARIO = "#3b82f6"
    COLOR_FONDO = "#f1f5f9"
    COLOR_TEXTO = "#0f172a"
    COLOR_EXITO = "#16a34a"
    COLOR_ALERTA = "#dc2626"

    def __init__(self, root):
        self.root = root
        self.root.title("OptiBottle - Sistema de Optimización de Producción | Equipo 2")
        self.root.geometry("1100x680")
        self.root.configure(bg=self.COLOR_FONDO)

        self.db = Database()

        self._configurar_estilo()
        self._construir_header()
        self._construir_tabs()
        self._cargar_datos_iniciales()

    def _configurar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.COLOR_FONDO, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            padding=[20, 10],
            font=("Segoe UI", 10, "bold"),
            background="#e2e8f0",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.COLOR_PRIMARIO)],
            foreground=[("selected", "white")],
        )
        style.configure(
            "Treeview.Heading",
            background=self.COLOR_PRIMARIO,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
        style.configure(
            "Primary.TButton",
            background=self.COLOR_PRIMARIO,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        style.map("Primary.TButton", background=[("active", self.COLOR_SECUNDARIO)])
        style.configure(
            "Danger.TButton",
            background=self.COLOR_ALERTA,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )

    def _construir_header(self):
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARIO, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🏭  OptiBottle",
            font=("Segoe UI", 20, "bold"),
            bg=self.COLOR_PRIMARIO,
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        tk.Label(
            header,
            text="Sistema de Información para Optimización de Producción de Botellas Plásticas",
            font=("Segoe UI", 10),
            bg=self.COLOR_PRIMARIO,
            fg="#cbd5e1",
        ).pack(side="left", pady=20)

        tk.Label(
            header,
            text=f"📅 {datetime.now().strftime('%d/%m/%Y')}",
            font=("Segoe UI", 10, "bold"),
            bg=self.COLOR_PRIMARIO,
            fg="white",
        ).pack(side="right", padx=20)

    def _construir_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_dashboard = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_ordenes = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_materiales = tk.Frame(self.notebook, bg=self.COLOR_FONDO)
        self.tab_registros = tk.Frame(self.notebook, bg=self.COLOR_FONDO)

        self.notebook.add(self.tab_dashboard, text="📊  Dashboard")
        self.notebook.add(self.tab_ordenes, text="📋  Órdenes de Producción")
        self.notebook.add(self.tab_materiales, text="📦  Materia Prima")
        self.notebook.add(self.tab_registros, text="✏️  Registro de Producción")

        self._construir_dashboard()
        self._construir_tab_ordenes()
        self._construir_tab_materiales()
        self._construir_tab_registros()

        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self._refrescar_dashboard())

    # ==================== DASHBOARD ====================
    def _construir_dashboard(self):
        # Contenedor con scroll (porque ahora hay gráficas)
        canvas_dash = tk.Canvas(self.tab_dashboard, bg=self.COLOR_FONDO, highlightthickness=0)
        scrollbar_dash = ttk.Scrollbar(self.tab_dashboard, orient="vertical", command=canvas_dash.yview)
        canvas_dash.configure(yscrollcommand=scrollbar_dash.set)

        scrollbar_dash.pack(side="right", fill="y")
        canvas_dash.pack(side="left", fill="both", expand=True)

        contenedor = tk.Frame(canvas_dash, bg=self.COLOR_FONDO)
        canvas_window = canvas_dash.create_window((0, 0), window=contenedor, anchor="nw")

        def ajustar_ancho(event):
            canvas_dash.itemconfig(canvas_window, width=event.width)
        canvas_dash.bind("<Configure>", ajustar_ancho)

        def actualizar_scroll(event):
            canvas_dash.configure(scrollregion=canvas_dash.bbox("all"))
        contenedor.bind("<Configure>", actualizar_scroll)

        # Scroll con la rueda del ratón
        def _on_mousewheel(event):
            canvas_dash.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas_dash.bind_all("<MouseWheel>", _on_mousewheel)

        contenido = tk.Frame(contenedor, bg=self.COLOR_FONDO)
        contenido.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            contenido,
            text="Indicadores Clave de Producción",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
        ).pack(anchor="w", pady=(0, 15))

        # KPIs en tarjetas
        kpis_frame = tk.Frame(contenido, bg=self.COLOR_FONDO)
        kpis_frame.pack(fill="x")

        self.kpi_labels = {}
        kpis = [
            ("Unidades Buenas", "0", self.COLOR_EXITO, "✅"),
            ("Unidades Defectuosas", "0", self.COLOR_ALERTA, "❌"),
            ("% Desperdicio", "0%", "#f59e0b", "📉"),
            ("Eficiencia Calidad", "0%", self.COLOR_SECUNDARIO, "⚡"),
            ("Tiempo Muerto (min)", "0", "#6366f1", "⏱️"),
        ]

        for i, (titulo, valor, color, icono) in enumerate(kpis):
            card = tk.Frame(kpis_frame, bg="white", relief="flat", bd=0)
            card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew", ipadx=10, ipady=10)
            kpis_frame.columnconfigure(i, weight=1)

            tk.Frame(card, bg=color, height=4).pack(fill="x")

            tk.Label(card, text=icono, font=("Segoe UI", 22), bg="white").pack(pady=(10, 0))
            valor_lbl = tk.Label(card, text=valor, font=("Segoe UI", 20, "bold"), bg="white", fg=color)
            valor_lbl.pack()
            tk.Label(card, text=titulo, font=("Segoe UI", 9), bg="white", fg="#64748b").pack(pady=(0, 10))
            self.kpi_labels[titulo] = valor_lbl

        # ========== SECCIÓN DE GRÁFICAS ==========
        tk.Label(
            contenido,
            text="📈 Análisis Gráfico de la Producción",
            font=("Segoe UI", 14, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
        ).pack(anchor="w", pady=(25, 10))

        graficas_frame = tk.Frame(contenido, bg=self.COLOR_FONDO)
        graficas_frame.pack(fill="x")

        # Gráfica 1: Barras (buenas vs defectuosas por orden)
        frame_g1 = tk.Frame(graficas_frame, bg="white", bd=1, relief="solid")
        frame_g1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.fig_barras = Figure(figsize=(5, 3.2), dpi=80, facecolor="white")
        self.ax_barras = self.fig_barras.add_subplot(111)
        self.canvas_barras = FigureCanvasTkAgg(self.fig_barras, master=frame_g1)
        self.canvas_barras.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Gráfica 2: Pastel (causas de tiempo muerto)
        frame_g2 = tk.Frame(graficas_frame, bg="white", bd=1, relief="solid")
        frame_g2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.fig_pastel = Figure(figsize=(5, 3.2), dpi=80, facecolor="white")
        self.ax_pastel = self.fig_pastel.add_subplot(111)
        self.canvas_pastel = FigureCanvasTkAgg(self.fig_pastel, master=frame_g2)
        self.canvas_pastel.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Gráfica 3: Líneas (producción por día) - ancho completo
        frame_g3 = tk.Frame(graficas_frame, bg="white", bd=1, relief="solid")
        frame_g3.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.fig_lineas = Figure(figsize=(10, 3), dpi=80, facecolor="white")
        self.ax_lineas = self.fig_lineas.add_subplot(111)
        self.canvas_lineas = FigureCanvasTkAgg(self.fig_lineas, master=frame_g3)
        self.canvas_lineas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        graficas_frame.columnconfigure(0, weight=1)
        graficas_frame.columnconfigure(1, weight=1)

        # Sección causas de paro
        tk.Label(
            contenido,
            text="🔧 Principales Causas de Tiempo Muerto",
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO,
        ).pack(anchor="w", pady=(25, 10))

        frame_causas = tk.Frame(contenido, bg="white", bd=1, relief="solid")
        frame_causas.pack(fill="both", expand=True)

        cols = ("Causa", "Minutos Totales", "Ocurrencias")
        self.tree_causas = ttk.Treeview(frame_causas, columns=cols, show="headings", height=6)
        for c in cols:
            self.tree_causas.heading(c, text=c)
            self.tree_causas.column(c, anchor="center")
        self.tree_causas.pack(fill="both", expand=True, padx=5, pady=5)

        # Alertas
        self.frame_alertas = tk.Frame(contenido, bg=self.COLOR_FONDO)
        self.frame_alertas.pack(fill="x", pady=10)

    def _refrescar_dashboard(self):
        m = self.db.calcular_metricas()
        self.kpi_labels["Unidades Buenas"].config(text=f"{m['total_buenas']:,}")
        self.kpi_labels["Unidades Defectuosas"].config(text=f"{m['total_defectuosas']:,}")
        self.kpi_labels["% Desperdicio"].config(text=f"{m['porcentaje_desperdicio']}%")
        self.kpi_labels["Eficiencia Calidad"].config(text=f"{m['eficiencia_calidad']}%")
        self.kpi_labels["Tiempo Muerto (min)"].config(text=f"{m['tiempo_muerto_total']:,}")

        # Causas
        for item in self.tree_causas.get_children():
            self.tree_causas.delete(item)
        for c in self.db.causas_paro_frecuentes():
            self.tree_causas.insert(
                "", "end", values=(c["causa_paro"], c["total_min"], c["ocurrencias"])
            )

        # Alertas de inventario bajo
        for w in self.frame_alertas.winfo_children():
            w.destroy()
        bajos = self.db.materiales_bajo_minimo()
        if bajos:
            alerta = tk.Frame(self.frame_alertas, bg="#fef3c7", bd=1, relief="solid")
            alerta.pack(fill="x")
            nombres = ", ".join([b["nombre"] for b in bajos])
            tk.Label(
                alerta,
                text=f"⚠️  ALERTA: Materiales por debajo del stock mínimo: {nombres}",
                font=("Segoe UI", 10, "bold"),
                bg="#fef3c7",
                fg="#92400e",
                anchor="w",
            ).pack(fill="x", padx=10, pady=8)

        # Actualizar gráficas
        self._dibujar_graficas()

    def _dibujar_graficas(self):
        """Dibuja las 3 gráficas del dashboard con datos de la BD."""

        # ===== GRÁFICA 1: Barras (buenas vs defectuosas por orden) =====
        self.ax_barras.clear()
        datos_orden = self.db.produccion_por_orden()

        if datos_orden:
            codigos = [d["codigo"] for d in datos_orden]
            buenas = [d["buenas"] for d in datos_orden]
            defectuosas = [d["defectuosas"] for d in datos_orden]

            import numpy as np
            x = np.arange(len(codigos))
            ancho = 0.35

            self.ax_barras.bar(x - ancho/2, buenas, ancho, label="Buenas",
                               color=self.COLOR_EXITO, edgecolor="white")
            self.ax_barras.bar(x + ancho/2, defectuosas, ancho, label="Defectuosas",
                               color=self.COLOR_ALERTA, edgecolor="white")
            self.ax_barras.set_xticks(x)
            self.ax_barras.set_xticklabels(codigos, fontsize=8)
            self.ax_barras.set_ylabel("Unidades", fontsize=9)
            self.ax_barras.set_title("Producción por Orden", fontsize=11, fontweight="bold",
                                     color=self.COLOR_PRIMARIO)
            self.ax_barras.legend(fontsize=8, loc="upper right")
            self.ax_barras.grid(axis="y", alpha=0.3, linestyle="--")
            self.ax_barras.spines["top"].set_visible(False)
            self.ax_barras.spines["right"].set_visible(False)
        else:
            self.ax_barras.text(0.5, 0.5, "Sin datos para mostrar",
                                ha="center", va="center", fontsize=10, color="#94a3b8")
            self.ax_barras.set_xticks([])
            self.ax_barras.set_yticks([])

        self.fig_barras.tight_layout()
        self.canvas_barras.draw()

        # ===== GRÁFICA 2: Pastel (causas de paro) =====
        self.ax_pastel.clear()
        causas = self.db.causas_paro_frecuentes()
        # Filtrar "Sin paro" porque no aporta nada a la gráfica de causas
        causas_filtradas = [c for c in causas if c["causa_paro"] != "Sin paro" and c["total_min"] > 0]

        if causas_filtradas:
            labels = [c["causa_paro"] for c in causas_filtradas]
            sizes = [c["total_min"] for c in causas_filtradas]
            colores = ["#dc2626", "#f59e0b", "#3b82f6", "#8b5cf6", "#10b981", "#ec4899", "#6366f1"]

            wedges, texts, autotexts = self.ax_pastel.pie(
                sizes, labels=labels, autopct="%1.1f%%",
                colors=colores[:len(labels)], startangle=90,
                textprops={"fontsize": 8},
                wedgeprops={"edgecolor": "white", "linewidth": 2}
            )
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontweight("bold")
                autotext.set_fontsize(8)

            self.ax_pastel.set_title("Distribución de Causas de Paro", fontsize=11,
                                    fontweight="bold", color=self.COLOR_PRIMARIO)
        else:
            self.ax_pastel.text(0.5, 0.5, "Sin causas de paro registradas",
                               ha="center", va="center", fontsize=10, color="#94a3b8")
            self.ax_pastel.set_xticks([])
            self.ax_pastel.set_yticks([])

        self.fig_pastel.tight_layout()
        self.canvas_pastel.draw()

        # ===== GRÁFICA 3: Líneas (producción por día) =====
        self.ax_lineas.clear()
        datos_fecha = self.db.produccion_por_fecha()

        if datos_fecha:
            fechas = [d["fecha"] for d in datos_fecha]
            buenas = [d["buenas"] for d in datos_fecha]
            defectuosas = [d["defectuosas"] for d in datos_fecha]

            self.ax_lineas.plot(fechas, buenas, marker="o", linewidth=2.5,
                                color=self.COLOR_EXITO, label="Buenas", markersize=7)
            self.ax_lineas.plot(fechas, defectuosas, marker="s", linewidth=2.5,
                                color=self.COLOR_ALERTA, label="Defectuosas", markersize=7)
            self.ax_lineas.fill_between(fechas, buenas, alpha=0.1, color=self.COLOR_EXITO)
            self.ax_lineas.set_title("Tendencia de Producción Diaria", fontsize=11,
                                    fontweight="bold", color=self.COLOR_PRIMARIO)
            self.ax_lineas.set_ylabel("Unidades", fontsize=9)
            self.ax_lineas.set_xlabel("Fecha", fontsize=9)
            self.ax_lineas.legend(fontsize=9, loc="upper left")
            self.ax_lineas.grid(alpha=0.3, linestyle="--")
            self.ax_lineas.spines["top"].set_visible(False)
            self.ax_lineas.spines["right"].set_visible(False)
            self.ax_lineas.tick_params(axis="x", rotation=30, labelsize=8)
        else:
            self.ax_lineas.text(0.5, 0.5, "Sin datos para mostrar",
                               ha="center", va="center", fontsize=10, color="#94a3b8")
            self.ax_lineas.set_xticks([])
            self.ax_lineas.set_yticks([])

        self.fig_lineas.tight_layout()
        self.canvas_lineas.draw()

    # ==================== TAB ÓRDENES ====================
    def _construir_tab_ordenes(self):
        cont = tk.Frame(self.tab_ordenes, bg=self.COLOR_FONDO)
        cont.pack(fill="both", expand=True, padx=20, pady=20)

        # Formulario
        form = tk.LabelFrame(
            cont,
            text=" Nueva Orden de Producción ",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.COLOR_PRIMARIO,
            padx=15,
            pady=15,
        )
        form.pack(fill="x", pady=(0, 15))

        campos = [
            ("Código:", "codigo"),
            ("Producto:", "producto"),
            ("Cantidad Planeada:", "cantidad"),
            ("Fecha Inicio (YYYY-MM-DD):", "fecha"),
            ("Responsable:", "responsable"),
        ]
        self.entries_orden = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(form, text=label, bg="white", font=("Segoe UI", 9)).grid(
                row=i // 3, column=(i % 3) * 2, sticky="e", padx=5, pady=5
            )
            e = tk.Entry(form, font=("Segoe UI", 10), width=20)
            e.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=5, sticky="w")
            self.entries_orden[key] = e

        # Valores por defecto
        self.entries_orden["fecha"].insert(0, datetime.now().strftime("%Y-%m-%d"))

        btns = tk.Frame(form, bg="white")
        btns.grid(row=2, column=0, columnspan=6, pady=10, sticky="w")
        ttk.Button(btns, text="➕ Crear Orden", style="Primary.TButton", command=self.crear_orden).pack(side="left", padx=5)
        ttk.Button(btns, text="🔄 Limpiar", command=self.limpiar_form_orden).pack(side="left", padx=5)

        # Lista de órdenes
        tk.Label(
            cont,
            text="Órdenes Registradas",
            font=("Segoe UI", 13, "bold"),
            bg=self.COLOR_FONDO,
        ).pack(anchor="w", pady=(10, 5))

        cont_tree = tk.Frame(cont, bg="white")
        cont_tree.pack(fill="both", expand=True)

        cols = ("ID", "Código", "Producto", "Planeado", "Producido", "Inicio", "Estado", "Responsable")
        self.tree_ordenes = ttk.Treeview(cont_tree, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree_ordenes.heading(c, text=c)
            self.tree_ordenes.column(c, anchor="center", width=100)
        self.tree_ordenes.column("ID", width=40)
        self.tree_ordenes.column("Producto", width=180)
        self.tree_ordenes.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(cont_tree, orient="vertical", command=self.tree_ordenes.yview)
        sb.pack(side="right", fill="y")
        self.tree_ordenes.configure(yscrollcommand=sb.set)

        acciones = tk.Frame(cont, bg=self.COLOR_FONDO)
        acciones.pack(fill="x", pady=10)
        ttk.Button(acciones, text="▶️ En Proceso", command=lambda: self.cambiar_estado_orden("En Proceso")).pack(side="left", padx=3)
        ttk.Button(acciones, text="✅ Finalizar", command=lambda: self.cambiar_estado_orden("Finalizada")).pack(side="left", padx=3)
        ttk.Button(acciones, text="⏸️ Pausar", command=lambda: self.cambiar_estado_orden("Pausada")).pack(side="left", padx=3)
        ttk.Button(acciones, text="🗑️ Eliminar", style="Danger.TButton", command=self.eliminar_orden).pack(side="left", padx=3)
        ttk.Button(acciones, text="📤 Exportar CSV", command=self.exportar_ordenes_csv).pack(side="right", padx=3)

    def crear_orden(self):
        try:
            codigo = self.entries_orden["codigo"].get().strip()
            producto = self.entries_orden["producto"].get().strip()
            cantidad = int(self.entries_orden["cantidad"].get())
            fecha = self.entries_orden["fecha"].get().strip()
            responsable = self.entries_orden["responsable"].get().strip()

            if not codigo or not producto or cantidad <= 0:
                raise ValueError("Datos inválidos")
            datetime.strptime(fecha, "%Y-%m-%d")

            self.db.crear_orden(codigo, producto, cantidad, fecha, responsable)
            messagebox.showinfo("Éxito", f"Orden {codigo} creada correctamente.")
            self.limpiar_form_orden()
            self.refrescar_ordenes()
        except ValueError as e:
            messagebox.showerror("Error", f"Verifica los datos. {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la orden: {e}")

    def limpiar_form_orden(self):
        for k, e in self.entries_orden.items():
            e.delete(0, "end")
        self.entries_orden["fecha"].insert(0, datetime.now().strftime("%Y-%m-%d"))

    def refrescar_ordenes(self):
        for item in self.tree_ordenes.get_children():
            self.tree_ordenes.delete(item)
        for o in self.db.listar_ordenes():
            self.tree_ordenes.insert("", "end", values=(
                o["id"], o["codigo"], o["producto"], o["cantidad_planeada"],
                o["cantidad_producida"], o["fecha_inicio"], o["estado"], o["responsable"] or ""
            ))

    def cambiar_estado_orden(self, nuevo_estado):
        sel = self.tree_ordenes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una orden primero.")
            return
        orden_id = self.tree_ordenes.item(sel[0])["values"][0]
        fecha_fin = datetime.now().strftime("%Y-%m-%d") if nuevo_estado == "Finalizada" else None
        self.db.actualizar_estado_orden(orden_id, nuevo_estado, fecha_fin)
        self.refrescar_ordenes()
        messagebox.showinfo("Éxito", f"Estado actualizado a: {nuevo_estado}")

    def eliminar_orden(self):
        sel = self.tree_ordenes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una orden primero.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar la orden y todos sus registros?"):
            return
        orden_id = self.tree_ordenes.item(sel[0])["values"][0]
        self.db.eliminar_orden(orden_id)
        self.refrescar_ordenes()

    def exportar_ordenes_csv(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="ordenes_produccion.csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not ruta:
            return
        ordenes = self.db.listar_ordenes()
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ordenes[0].keys() if ordenes else [
                "id", "codigo", "producto", "cantidad_planeada", "cantidad_producida",
                "fecha_inicio", "fecha_fin", "estado", "responsable"
            ])
            writer.writeheader()
            writer.writerows(ordenes)
        messagebox.showinfo("Éxito", f"Exportado a: {ruta}")

    # ==================== TAB MATERIALES ====================
    def _construir_tab_materiales(self):
        cont = tk.Frame(self.tab_materiales, bg=self.COLOR_FONDO)
        cont.pack(fill="both", expand=True, padx=20, pady=20)

        form = tk.LabelFrame(
            cont, text=" Agregar Material ", font=("Segoe UI", 11, "bold"),
            bg="white", fg=self.COLOR_PRIMARIO, padx=15, pady=15,
        )
        form.pack(fill="x", pady=(0, 15))

        tk.Label(form, text="Nombre:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_mat_nombre = tk.Entry(form, width=25)
        self.ent_mat_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Stock Actual:", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_mat_stock = tk.Entry(form, width=15)
        self.ent_mat_stock.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Stock Mínimo:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_mat_min = tk.Entry(form, width=25)
        self.ent_mat_min.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Unidad:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_mat_unidad = ttk.Combobox(form, values=["kg", "ton", "piezas", "litros"], width=12)
        self.ent_mat_unidad.set("kg")
        self.ent_mat_unidad.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form, text="➕ Agregar Material", style="Primary.TButton", command=self.agregar_material).grid(
            row=2, column=0, columnspan=4, pady=10
        )

        cont_tree = tk.Frame(cont, bg="white")
        cont_tree.pack(fill="both", expand=True)

        cols = ("ID", "Nombre", "Stock Actual", "Stock Mínimo", "Unidad", "Estado")
        self.tree_mat = ttk.Treeview(cont_tree, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree_mat.heading(c, text=c)
            self.tree_mat.column(c, anchor="center")
        self.tree_mat.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(cont_tree, orient="vertical", command=self.tree_mat.yview)
        sb.pack(side="right", fill="y")
        self.tree_mat.configure(yscrollcommand=sb.set)

        acciones = tk.Frame(cont, bg=self.COLOR_FONDO)
        acciones.pack(fill="x", pady=10)
        ttk.Button(acciones, text="🔄 Actualizar Stock", command=self.actualizar_stock_dialog).pack(side="left", padx=3)
        ttk.Button(acciones, text="🗑️ Eliminar", style="Danger.TButton", command=self.eliminar_material).pack(side="left", padx=3)

    def agregar_material(self):
        try:
            nombre = self.ent_mat_nombre.get().strip()
            stock = float(self.ent_mat_stock.get())
            minimo = float(self.ent_mat_min.get())
            unidad = self.ent_mat_unidad.get()
            if not nombre:
                raise ValueError("Falta nombre")
            self.db.agregar_material(nombre, stock, minimo, unidad)
            messagebox.showinfo("Éxito", "Material agregado.")
            self.ent_mat_nombre.delete(0, "end")
            self.ent_mat_stock.delete(0, "end")
            self.ent_mat_min.delete(0, "end")
            self.refrescar_materiales()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def refrescar_materiales(self):
        for i in self.tree_mat.get_children():
            self.tree_mat.delete(i)
        for m in self.db.listar_materiales():
            estado = "⚠️ BAJO" if m["stock_actual"] < m["stock_minimo"] else "✅ OK"
            self.tree_mat.insert("", "end", values=(
                m["id"], m["nombre"], m["stock_actual"], m["stock_minimo"], m["unidad"], estado
            ))

    def actualizar_stock_dialog(self):
        sel = self.tree_mat.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un material.")
            return
        mat_id = self.tree_mat.item(sel[0])["values"][0]
        nombre = self.tree_mat.item(sel[0])["values"][1]

        dlg = tk.Toplevel(self.root)
        dlg.title(f"Actualizar stock - {nombre}")
        dlg.geometry("320x150")
        dlg.configure(bg="white")

        tk.Label(dlg, text=f"Nuevo stock para {nombre}:", bg="white", font=("Segoe UI", 10)).pack(pady=15)
        ent = tk.Entry(dlg, font=("Segoe UI", 11))
        ent.pack(pady=5)
        ent.focus()

        def guardar():
            try:
                nuevo = float(ent.get())
                self.db.actualizar_stock(mat_id, nuevo)
                self.refrescar_materiales()
                dlg.destroy()
                messagebox.showinfo("Éxito", "Stock actualizado.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(dlg, text="Guardar", style="Primary.TButton", command=guardar).pack(pady=10)

    def eliminar_material(self):
        sel = self.tree_mat.selection()
        if not sel:
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el material seleccionado?"):
            return
        mat_id = self.tree_mat.item(sel[0])["values"][0]
        self.db.eliminar_material(mat_id)
        self.refrescar_materiales()

    # ==================== TAB REGISTROS ====================
    def _construir_tab_registros(self):
        cont = tk.Frame(self.tab_registros, bg=self.COLOR_FONDO)
        cont.pack(fill="both", expand=True, padx=20, pady=20)

        form = tk.LabelFrame(
            cont, text=" Registrar Producción del Turno ", font=("Segoe UI", 11, "bold"),
            bg="white", fg=self.COLOR_PRIMARIO, padx=15, pady=15,
        )
        form.pack(fill="x", pady=(0, 15))

        tk.Label(form, text="Orden:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cb_orden = ttk.Combobox(form, width=30, state="readonly")
        self.cb_orden.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Fecha:", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_reg_fecha = tk.Entry(form, width=15)
        self.ent_reg_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_reg_fecha.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="Turno:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.cb_turno = ttk.Combobox(form, values=["Matutino", "Vespertino", "Nocturno"], state="readonly", width=15)
        self.cb_turno.set("Matutino")
        self.cb_turno.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Buenas:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_buenas = tk.Entry(form, width=15)
        self.ent_buenas.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form, text="Defectuosas:", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_defectuosas = tk.Entry(form, width=15)
        self.ent_defectuosas.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Tiempo muerto (min):", bg="white").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.ent_tm = tk.Entry(form, width=15)
        self.ent_tm.grid(row=2, column=3, padx=5, pady=5)

        tk.Label(form, text="Causa de paro:", bg="white").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.cb_causa = ttk.Combobox(form, values=[
            "Mantenimiento", "Falta de material", "Cambio de molde",
            "Falla eléctrica", "Calidad / rechazo", "Otro", "Sin paro"
        ], width=28)
        self.cb_causa.set("Sin paro")
        self.cb_causa.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

        ttk.Button(form, text="💾 Registrar", style="Primary.TButton", command=self.registrar_produccion).grid(
            row=4, column=0, columnspan=4, pady=10
        )

        # Tabla
        cont_tree = tk.Frame(cont, bg="white")
        cont_tree.pack(fill="both", expand=True)

        cols = ("Fecha", "Orden", "Producto", "Turno", "Buenas", "Defectuosas", "TM (min)", "Causa")
        self.tree_reg = ttk.Treeview(cont_tree, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree_reg.heading(c, text=c)
            self.tree_reg.column(c, anchor="center", width=100)
        self.tree_reg.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(cont_tree, orient="vertical", command=self.tree_reg.yview)
        sb.pack(side="right", fill="y")
        self.tree_reg.configure(yscrollcommand=sb.set)

    def refrescar_combo_ordenes(self):
        ordenes = self.db.listar_ordenes()
        valores = [f"{o['id']} - {o['codigo']} - {o['producto']}" for o in ordenes]
        self.cb_orden["values"] = valores

    def registrar_produccion(self):
        try:
            if not self.cb_orden.get():
                raise ValueError("Selecciona una orden")
            orden_id = int(self.cb_orden.get().split(" - ")[0])
            fecha = self.ent_reg_fecha.get().strip()
            datetime.strptime(fecha, "%Y-%m-%d")
            turno = self.cb_turno.get()
            buenas = int(self.ent_buenas.get() or 0)
            defectuosas = int(self.ent_defectuosas.get() or 0)
            tm = int(self.ent_tm.get() or 0)
            causa = self.cb_causa.get()

            if buenas < 0 or defectuosas < 0 or tm < 0:
                raise ValueError("No se permiten valores negativos")

            self.db.registrar_produccion(orden_id, fecha, turno, buenas, defectuosas, tm, causa)
            messagebox.showinfo("Éxito", "Registro guardado.")
            self.ent_buenas.delete(0, "end")
            self.ent_defectuosas.delete(0, "end")
            self.ent_tm.delete(0, "end")
            self.refrescar_registros()
            self.refrescar_ordenes()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def refrescar_registros(self):
        for i in self.tree_reg.get_children():
            self.tree_reg.delete(i)
        for r in self.db.listar_registros():
            self.tree_reg.insert("", "end", values=(
                r["fecha"], r["orden_codigo"], r["producto"], r["turno"],
                r["unidades_buenas"], r["unidades_defectuosas"],
                r["tiempo_muerto_min"], r["causa_paro"] or ""
            ))

    # ==================== INICIALIZACIÓN ====================
    def _cargar_datos_iniciales(self):
        self.refrescar_ordenes()
        self.refrescar_materiales()
        self.refrescar_combo_ordenes()
        self.refrescar_registros()
        self._refrescar_dashboard()


def main():
    root = tk.Tk()
    app = OptiBottleApp(root)

    def actualizar_combos(event=None):
        app.refrescar_combo_ordenes()

    app.notebook.bind("<<NotebookTabChanged>>", lambda e: (app._refrescar_dashboard(), app.refrescar_combo_ordenes()))
    root.mainloop()


if __name__ == "__main__":
    main()
