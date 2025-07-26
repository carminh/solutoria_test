from bd.create_table import creacion_tabla
from api.api import dataUFAPI
from bd.datalocal import UFDataLocal
from bd.commands import UF_CRUD
from views.app import show_uf_chart

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