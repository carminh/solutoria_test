

import json
import requests

class dataUFAPI:
    USERNAME = "clasica05@gmail.com"
    FLAG_JSON = True
    token = ""
    url_base = "https://postulaciones.solutoria.cl"
    token = ""

    @staticmethod
    def getToken():
        url = f"{dataUFAPI.url_base}/api/acceso"
        params = {
            "userName": dataUFAPI.USERNAME,
            "flagJson": dataUFAPI.FLAG_JSON
        }

        response = requests.post(url, json=params)

        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                dataUFAPI.token = data.get("token")
                return dataUFAPI.token
            else:
                print("Token no obtenido")
                print(response.text)
                return None
        
    @staticmethod
    def fetchData():
        if not dataUFAPI.token:
            token = dataUFAPI.getToken()
            if not token:
                print("No se pudo obtener un token")
                return None

        url = f"{dataUFAPI.url_base}/api/indicadores"
        headers = {
            "Authorization": f"Bearer {dataUFAPI.token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("**Error:", response.status_code)
            print(response.text)
            return None