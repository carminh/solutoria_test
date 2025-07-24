

import sqlite3


class conexionBD:

    @staticmethod
    def get_bd_connection():
        conn = sqlite3.connect("datos.db")

        if conn is None:
            raise Exception("Error al conectar a la bd")
        return conn
    