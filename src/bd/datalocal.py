import dosSolutoria_prueba.api.api as api
from dosSolutoria_prueba.bd.conexion import conexionBD
import sqlite3

class UFDataLocal:

    def __init__(self):
        self.api = api.dataUFAPI()
        self.data = []

    
    def only_uf_data(self):
        
        raw_data = self.api.fetchData()
        self.data = []

        for item in raw_data:
            if item is None or not item:
                continue
            if item.get('codigoIndicador') != 'UF':
                continue
            self.data.append(item)


    def save_uf_data(self):
        self.only_uf_data()

        if not self.data:
            return "No hay datos de UF para guardar"

        self.insert_datos_into_bd(self.data)

        print(f"Se guardaron {len(self.data)} registros de UF en la base de datos")



    def insert_datos_into_bd(self, datos):
        conn = conexionBD.get_bd_connection()
        cursor = conn.cursor()
        
        for item in datos:
            if item.get("codigoIndicador") == "UF":
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO uf_historica (
                            nombreIndicador, codigoIndicador, 
                            unidadMedidaIndicador, valorIndicador, fechaIndicador
                        ) VALUES (?, ?, ?, ?, ?)
                    """, (
                        item.get('nombreIndicador'),
                        item.get('codigoIndicador'),
                        item.get('unidadMedidaIndicador'),
                        item.get('valorIndicador'),
                        item.get('fechaIndicador')
                    ))
                except sqlite3.Error as e:
                    print(f"Error al insertar registro: {e}")
        
        conn.commit()
        conn.close()    




