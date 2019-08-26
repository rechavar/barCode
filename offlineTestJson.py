import time
import requests
from collections import defaultdict
import os
import json

URL1 = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
TIEMPO_ESPERA = 5000
url='http://216.58.192.142'
timeout=5
estadoConexion = False
caracteresValidos = ['+','-']
data = {}
data['visitantes'] = []

while True:
    barcode = input('acerque el codigo al lector de barras')
    localTime = time.localtime()
    hora = '{}:{}:{}'.format(localTime.tm_hour, localTime.tm_min, localTime.tm_sec)
    date = '{}/{}/{}'.format(localTime.tm_mday, localTime.tm_mon, localTime.tm_year)
    if barcode[-2] in caracteresValidos:
        barcode = barcode.split()
        numeroCedula = barcode[0]
        apellidoCedula = barcode[1] + ' ' + barcode[2]
        nombreCedula = barcode[3]

        data['visitantes'].append({
            'name' : nombreCedula,
            'lastName' :  apellidoCedula,
            'numberID' : numeroCedula,
            'date-time' : '{}-{}'.format(hora,date)  
        })

        with open('data.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

        jsonFile.close()
    
