from dosSolutoria_prueba.bd.conexion import conexionBD

import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pandas as pd


class UFChartApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Datos UF")
        self.root.geometry("900x600")
        

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        
        self.create_widgets()
        
        self.load_data()
        
    def create_widgets(self):

        # Fr principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Fr de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # titulo
        title_label = ttk.Label(control_frame, text="Datos Históricos de UF", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=4, pady=5)
        
        # labels y controles de fecha
        ttk.Label(control_frame, text="Fecha Inicio:").grid(row=1, column=0, padx=5, sticky=tk.E)
        self.start_date_entry = ttk.Entry(control_frame)
        self.start_date_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(control_frame, text="Fecha Fin:").grid(row=1, column=2, padx=5, sticky=tk.E)
        self.end_date_entry = ttk.Entry(control_frame)
        self.end_date_entry.grid(row=1, column=3, padx=5)
        
        # bttn filtrado
        filter_button = ttk.Button(control_frame, text="Filtrar", command=self.filter_data)
        filter_button.grid(row=1, column=4, padx=10)
        
        # bttn mostrar datos
        all_data_button = ttk.Button(control_frame, text="Mostrar Todo", command=self.load_data)
        all_data_button.grid(row=1, column=5, padx=5)
        
        #fr de gráfico
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # creación de figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 6), facecolor='#f5f5f5')
        self.ax.set_title('Evolución de la UF', pad=20, fontsize=14)
        self.ax.set_xlabel('Fecha', fontsize=10)
        self.ax.set_ylabel('Valor (CLP)', fontsize=10)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # añade figura a tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Fr de configuración
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.info_label = ttk.Label(info_frame, text="Cargando datos...")
        self.info_label.pack()
    
    def load_data(self):
        # cargar todos los datos sin filtros
        conn = conexionBD.get_bd_connection()
        query = "SELECT fechaIndicador, valorIndicador FROM uf_historica WHERE codigoIndicador='UF' ORDER BY fechaIndicador"
        self.df = pd.read_sql(query, conn, parse_dates=['fechaIndicador'])
        conn.close()
        
        # actualizar campos de fecha
        if not self.df.empty:

            min_date = self.df['fechaIndicador'].min().strftime('%Y-%m-%d')
            max_date = self.df['fechaIndicador'].max().strftime('%Y-%m-%d')
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, min_date)
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, max_date)
        
        self.update_chart()
    
    def filter_data(self):

        # filtrar por el rango de fechas
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        try:
            # validación de fechas

            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            if start_date > end_date:
                raise ValueError("La fecha de inicio no puede ser mayor a la fecha fin")
            
            conn = conexionBD.get_bd_connection()
            query = """
                SELECT fechaIndicador, valorIndicador 
                FROM uf_historica 
                WHERE codigoIndicador='UF' 
                AND fechaIndicador BETWEEN ? AND ?
                ORDER BY fechaIndicador
            """
            self.df = pd.read_sql(query, conn, params=[start_date, end_date], parse_dates=['fechaIndicador'])
            conn.close()
            
            self.update_chart()
            
        except ValueError as e:
            self.info_label.config(text=f"Error en formato de fecha: {e}. Use YYYY-MM-DD")
    
    def update_chart(self):

        # actualizar el gráfico con los datos actuales
        self.ax.clear()
        
        if self.df.empty:
            self.ax.text(0.5, 0.5, 'No hay datos para mostrar', 
                        ha='center', va='center', fontsize=12)
            self.info_label.config(text="No se encontraron datos para el rango seleccionado")
        else:

            # grafica datos con colores
            self.ax.plot(self.df['fechaIndicador'], self.df['valorIndicador'], 
                        marker='o', markersize=4, linestyle='-', 
                        color='#2c7bb6', linewidth=2, alpha=0.8)
            

            # formateo de ejes
            self.ax.set_title('Evolución de la UF', pad=20, fontsize=14)
            self.ax.set_xlabel('Fecha', fontsize=10)
            self.ax.set_ylabel('Valor (CLP)', fontsize=10)
            self.ax.grid(True, linestyle='--', alpha=0.6)
            

            # rota labels de fechas para mejor legibilidad
            plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
            
            
            # actualiza información
            min_val = self.df['valorIndicador'].min()
            max_val = self.df['valorIndicador'].max()
            info_text = (f"Datos mostrados: {len(self.df)} registros | "
                         f"Valor mínimo: {min_val:.2f} | Valor máximo: {max_val:.2f}")
            self.info_label.config(text=info_text)
        
        self.fig.tight_layout()
        self.canvas.draw()

def show_uf_chart():
    root = tk.Tk()
    app = UFChartApp(root)
    root.mainloop()

