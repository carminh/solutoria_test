from dosSolutoria_prueba.bd.create_table import creacion_tabla
from dosSolutoria_prueba.api.api import dataUFAPI
from dosSolutoria_prueba.bd.datalocal import UFDataLocal
from dosSolutoria_prueba.bd.commands import UF_CRUD
from dosSolutoria_prueba.views.app import show_uf_chart

import tkinter as tk  

def main():
    print("########################\n")
    print("Iniciando aplicación UF")
    print("\n########################")
    
    try:
        # config inicial
        print("Creando estructura de BD...")
        creacion_tabla()
        
        # obtener datos de la API
        print("Obteniendo datos de la API...")
        data_handler = UFDataLocal()
        
        # procesa y guarda datos
        print("Procesando datos UF...")
        resultado = data_handler.save_uf_data() 
        print(resultado)
        
        # inicializa la interfaz gráfica
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