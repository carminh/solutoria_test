


import sqlite3
import pandas as pd
from dosSolutoria_prueba.bd.conexion import conexionBD
from dosSolutoria_prueba.bd.datalocal import UFDataLocal



class UF_CRUD:
    
    def create_datos(self, uf_data):
        conn = conexionBD.get_bd_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO uf_historica (
            nombreIndicador, codigoIndicador, 
            unidadMedidaIndicador, valorIndicador, fechaIndicador
        ) VALUES (?, ?, ?, ?, ?)
        ''', (
            uf_data['nombreIndicador'],
            uf_data['codigoIndicador'],
            uf_data['unidadMedidaIndicador'],
            uf_data['valorIndicador'],
            uf_data['fechaIndicador']
        ))
        
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    

    def read_datos(self, fechaInicio=None, fechaFin=None, limite=None):
        conn = conexionBD.get_bd_connection() 
        query = "SELECT * FROM uf_historica WHERE codigoIndicador='UF'"
        params = []
        
        if fechaInicio and fechaFin:
            query += " AND fechaIndicador BETWEEN ? AND ?"
            params.extend([fechaInicio, fechaFin])
        elif fechaInicio:
            query += " AND fechaIndicador >= ?"
            params.append(fechaInicio)
        elif fechaFin:
            query += " AND fechaIndicador <= ?"
            params.append(fechaFin)
            
        query += " ORDER BY fechaIndicador DESC"
        
        if limite:
            query += " LIMIT ?"
            params.append(limite)
            
        df = pd.read_sql(query, conn, params)
        conn.close()
        return df



    def update_datos(self, uf_id, new_data):
        conn = conexionBD.get_bd_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE uf_historica 
            SET nombreIndicador=?, codigoIndicador=?, 
            unidadMedidaIndicador=?, valorIndicador=?, fechaIndicador=?
            WHERE id=?""", (
            new_data['nombreIndicador'],
            new_data['codigoIndicador'],
            new_data['unidadMedidaIndicador'],
            new_data['valorIndicador'],
            new_data['fechaIndicador'],
            uf_id
        ))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0


    def delete_datos(self, uf_id):
        conn =conexionBD.get_bd_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM uf_historica WHERE id=?", (uf_id,))
        
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0