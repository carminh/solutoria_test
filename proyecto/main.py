from dosSolutoria_prueba.bd.create_table import creacion_tabla
from dosSolutoria_prueba.api.api import dataUFAPI
from dosSolutoria_prueba.bd.datalocal import UFDataLocal
from dosSolutoria_prueba.bd.commands import UF_CRUD
from dosSolutoria_prueba.views.app import show_uf_chart # Importa la nueva función
import tkinter as tk  # Necesario para la interfaz gráfica

def main():
    print("Iniciando aplicación UF")
    
    try:
        # 1. Configuración inicial
        print("Creando estructura de BD...")
        creacion_tabla()
        
        # 2. Obtener datos de la API
        print("Obteniendo datos de la API...")
        api = dataUFAPI()
        data_handler = UFDataLocal()
        data_handler.initialize()
        
        # 3. Procesar y guardar datos UF
        print("Procesando datos UF...")
        resultado = data_handler.save_uf_data() 
        print(resultado)
        
        # 4. Mostrar la interfaz gráfica
        print("Iniciando interfaz gráfica...")
        root = tk.Tk()
        show_uf_chart()  
        root.mainloop()
        
        print("Proceso completado exitosamente")
        
    except Exception as e:
        print(f"Error en el proceso: {e}")
        raise e

if __name__ == "__main__":
    main()