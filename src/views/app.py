from solutoria_test.src.bd.conexion import conexionBD
from solutoria_test.src.bd.commands import UF_CRUD


import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pandas as pd


class UFChartApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Datos UF")
        self.root.geometry("900x600")
        self.crud = UF_CRUD() 
        

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

        # bttns CRUD

        crud_frame = ttk.Frame(main_frame)
        crud_frame.pack(fill=tk.X, pady=(5, 10))

        create_button = ttk.Button(crud_frame, text="Crear", command=self.create_record)
        create_button.pack(side=tk.LEFT, padx=5)

        read_button = ttk.Button(crud_frame, text="Leer", command=self.read_record)
        read_button.pack(side=tk.LEFT, padx=5)

        update_button = ttk.Button(crud_frame, text="Actualizar", command=self.update_record)
        update_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(crud_frame, text="Eliminar", command=self.delete_record)
        delete_button.pack(side=tk.LEFT, padx=5)
    
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


            # obtener la fecha máxima de la base de datos para manejo de errores
            conn = conexionBD.get_bd_connection()
            #fecha maxima
            max_date_query = "SELECT MAX(fechaIndicador) as max_fecha FROM uf_historica WHERE codigoIndicador='UF'"
            max_date_df = pd.read_sql(max_date_query, conn, parse_dates=['max_fecha'])
            #fecha minima
            min_date_query = "SELECT MIN(fechaIndicador) as min_fecha FROM uf_historica WHERE codigoIndicador='UF'"
            min_date_df = pd.read_sql(min_date_query, conn, parse_dates=['min_fecha'])

            conn.close()
            max_db_date = max_date_df['max_fecha'][0].date()
            min_db_date = min_date_df['min_fecha'][0].date()

            # validaciones de rango
            if end_date > max_db_date:
                messagebox.showerror("Error", f"La fecha fin no puede ser mayor que la última fecha disponible en la bd ({max_db_date.strftime('%Y-%m-%d')})")
                return
            if start_date < min_db_date:
                messagebox.showerror("Error", f"La fecha inicio no puede ser menor que la primera fecha disponible en la bd ({min_db_date.strftime('%Y-%m-%d')})")
                return
            if start_date > end_date:
                messagebox.showerror("Error", "La fecha de inicio no puede ser mayor a la fecha fin")
                return

            conn()
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
            messagebox.showerror("Error de Formato", f"Error en formato de fecha: {e}. Use YYYY-MM-DD")
        
    
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

    #MANEJO DE OPERACIONES CRUD
    def create_record(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Crear Registro UF")
        create_window.geometry("300x200")

        ttk.Label(create_window, text="Fecha (YYYY-MM-DD):").pack(pady=5)
        date_entry = ttk.Entry(create_window)
        date_entry.pack(pady=5)

        ttk.Label(create_window, text="Valor UF:").pack(pady=5)
        value_entry = ttk.Entry(create_window)
        value_entry.pack(pady=5)

        def save_record():
            date_str = date_entry.get()
            value_str = value_entry.get()
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                value = float(value_str)
                uf_data = {
                    'nombreIndicador': 'UF',
                    'codigoIndicador': 'UF',
                    'unidadMedidaIndicador': 'CLP',
                    'valorIndicador': value,
                    'fechaIndicador': date.strftime('%Y-%m-%d')
                }
                self.crud.create_datos(uf_data)
                messagebox.showinfo("Éxito", "Registro creado exitosamente")
                create_window.destroy()
                self.load_data()
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        save_button = ttk.Button(create_window, text="Guardar", command=save_record)
        save_button.pack(pady=10)

    def read_record(self):
        read_window = tk.Toplevel(self.root)
        read_window.title("Leer Registros UF")
        read_window.geometry("400x300")

        self.tree = ttk.Treeview(read_window, columns=('Fecha', 'Valor'), show='headings')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Valor', text='Valor UF')
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # uso metodo read_datos para obtener los datos
        df = self.crud.read_datos()
        for index, row in df.iterrows():
            self.tree.insert('', 'end', values=(row['fechaIndicador'], row['valorIndicador']))

        close_button = ttk.Button(read_window, text="Cerrar", command=read_window.destroy)
        close_button.pack(pady=5)

    def update_record(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Registro UF")
        update_window.geometry("300x200")

        ttk.Label(update_window, text="ID del Registro:").pack(pady=5)
        id_entry = ttk.Entry(update_window)
        id_entry.pack(pady=5)

        ttk.Label(update_window, text="Nuevo Valor UF:").pack(pady=5)
        value_entry = ttk.Entry(update_window)
        value_entry.pack(pady=5)

        ttk.Label(update_window, text="Nueva Fecha (YYYY-MM-DD):").pack(pady=5)
        date_entry = ttk.Entry(update_window)
        date_entry.pack(pady=5)

        def save_update():
            record_id = id_entry.get()
            new_value_str = value_entry.get()
            new_date_str = date_entry.get()
            try:
                record_id = int(record_id)
                new_value = float(new_value_str)
                new_date = datetime.strptime(new_date_str, '%Y-%m-%d').date()
                new_data = {
                    'nombreIndicador': 'UF',
                    'codigoIndicador': 'UF',
                    'unidadMedidaIndicador': 'CLP',
                    'valorIndicador': new_value,
                    'fechaIndicador': new_date.strftime('%Y-%m-%d')
                }
                success = self.crud.update_datos(record_id, new_data)
                if success:
                    messagebox.showinfo("Éxito", f"Registro actualizado exitosamente. ID: {record_id}")
                    update_window.destroy()
                    self.load_data()
                else:
                    messagebox.showerror("Error", "No se encontró el registro para actualizar")
            except ValueError as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        save_button = ttk.Button(update_window, text="Guardar", command=save_update)
        save_button.pack(pady=10)

    def delete_record(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Eliminar Registro UF")
        delete_window.geometry("300x200")

        ttk.Label(delete_window, text="ID del Registro:").pack(pady=5)
        id_entry = ttk.Entry(delete_window)
        id_entry.pack(pady=5)

        def confirm_delete():
            record_id = id_entry.get()
            try:
                record_id = int(record_id)
                success = self.crud.delete_datos(record_id)
                if success:
                    messagebox.showinfo("Éxito", f"Registro eliminado exitosamente. Id: {record_id}")
                    delete_window.destroy()
                    self.load_data()
                else:
                    messagebox.showerror("Error", "No se encontró el registro para eliminar")
            except ValueError as e:
                messagebox.showerror("Error", f"ID inválido: {e}")

        delete_button = ttk.Button(delete_window, text="Eliminar", command=confirm_delete)
        delete_button.pack(pady=10)


def show_uf_chart():
    root = tk.Tk()
    app = UFChartApp(root)
    root.mainloop()

