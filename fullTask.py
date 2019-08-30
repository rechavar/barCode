import time
import requests
from collections import defaultdict
import os
import json
from zeep import Client as clt 


URL = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
TIEMPO_ESPERA = 30000
estadoConexion = False
data = {}
data['visitantes'] = []
offlinetime1 = 0.0
offlinetime2 = 0.0


def offline_function(numberID,lastNameID,nameID,date,hour, action = False, entry = False):

    data['visitantes'] = {
        'name' : nameID,
        'last_name' : lastNameID,
        'number' : numberID,
        'date - time' : '{} - {}'.format(date,hour)
    }
    with open(' data.json','a') as jsonFile:
        json.dump(data,jsonFile,indent=4)
    
    jsonFile.close()

    if action:
        if entry:
            print('permitir entrada')
        else:
            print('permitir salida')

def online_function(numberID, lastNameID, nameID, date, hour, client):
    global estadoConexion
    global offlinetime1

    try:
        serverResponse = client.service.Select_ControlaccesoAutomatizado(TOKEN,numberID,'{}'.format(date))
        if serverResponse == '0':
            print('No permitir ingreso/salida')
        elif serverResponse == '1':
            print('Permitir ingreso')
        elif serverResponse == '2':
            print('Permitir salida')
    
    except requests.exceptions.ConnectionError:
        estadoConexion = False
        offlinetime1 = time.time()
        x = input('la persona esta entrando? [y/n]')
        if x == 'y':
            offline_function(numberID,lastNameID,nameID,date,hour, action= True, entry= True)
        else:
            offline_function(numberID,lastNameID,nameID,date,hour, action= True, entry= False)
        

    try:
        respuestaServidor = False
        
        print(estadoConexion)
        while respuestaServidor == False and estadoConexion == True:
            respuestaServidor = client.service.Insert_ControlaccesoAutomatizado(TOKEN, numberID, nameID, lastNameID, '{}'.format(date), serverResponse)
            print('respuesta del servidor {}'.format(serverResponse))

    except requests.exceptions.ConnectionError:
        offlinetime1 = time.time()
        estadoConexion = False
        offline_function(numberID,lastNameID,nameID,date,hour)




####  main ###
def main():
    global estadoConexion
    global offlinetime1
    global offlinetime2

    try:
        client = clt(URL)
        estadoConexion = True
    except:
        offlinetime1 = time.time()
        estadoConexion = False
    

    while True:
        
        barCode = input('acerque la cedula al lector')
        
        """
        numberID = ''
        i = 0
        while barCode[i].isdigit():
            numberID = numberID + barCode[i]
            i += 1
        
        nameID = ''
        while barCode[i].isalpha():
            nameID = nameID + barCode[i]
            i += 1
        nameID = nameID[:-1]
        lastNameID = nameID[:-1]
        """
        barCode = barCode.split()
        numberID = barCode[0]
        lastNameID = barCode[1] + '' + barCode[2]
        nameID = barCode[3]
       

        localTime = time.localtime()
        date = '{}/{}/{}'.format(localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
        hour = '{}:{}:{}'.format(localTime.tm_hour, localTime.tm_min, localTime.tm_sec)

        if estadoConexion:
            online_function(numberID, lastNameID, nameID, date, hour, client)
        else:
            x = input('la persona esta entrando? [y/n]')
            if x == 'y':
                offline_function(numberID,lastNameID,nameID,date,hour, action= True, entry= True)
            else:
                offline_function(numberID,lastNameID,nameID,date,hour, action= True, entry= False)

            offlinetime2 = time.time()

            if offlinetime2 - offlinetime1 > 10 and estadoConexion == False:
                try:
                    print('intentando conectar')
                    client = clt(URL)
                    estadoConexion = True
                except:
                    print('fallo al intentar conectar')
                    offlinetime1 = time.time()
                    pass


if __name__ == "__main__":
    main()

