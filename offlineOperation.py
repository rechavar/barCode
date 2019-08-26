import time
import requests
from collections import defaultdict
import os
import pandas as pd
import csv

URL1 = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
TIEMPO_ESPERA = 5000
url='http://216.58.192.142'
timeout=5
estadoConexion = False
caracteresValidos = ['+','-']
columnName = ['name', 'lastName','numberID','hour','date']

if not os.path.exists('data.csv'):
    dataFrame = pd.DataFrame(columns= columnName)
    dataFrame.to_csv('data.csv', index = False)

while True:
    barcode = input('acerque el codigo al lector de barras')
    localTime = time.localtime()
    if barcode[-2] in caracteresValidos:
        barcode = barcode.split()
        numeroCedula = barcode[0]
        apellidoCedula = barcode[1] + ' ' + barcode[2]
        nombreCedula = barcode[3]
        row = [nombreCedula,apellidoCedula,numeroCedula,'{}:{}:{}'.format(localTime.tm_hour, localTime.tm_min, localTime.tm_sec),
                '{}/{}/{}'.format(localTime.tm_year, localTime.tm_mon, localTime.tm_mday)]

        with open('data.csv','a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        csvFile.close()
        
    else:
        print('ingrese un documento valido')
        pass
    
