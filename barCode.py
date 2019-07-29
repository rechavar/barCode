############################################################################################################
###### Programa diseñado para Expertos Seguridad el cual lee codigos de barras de cedulas, envia informacion 
###### a un webservice y con la respuesta de este autoriza o no la salida o ingreso de usuarios.############
############################################################################################################


import requests as rq 
import time
#import RPi.GPIO as GPIO #Se usara una Raspberry 

URL =  'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?op=ControlaccesoAutomatizado'
TIEMPO_ESPERA = 10000

while True: #El programa corre de forma indefinida

    barcode = input('Scan Barcode: ')
    text = []
    for i in barcode:
        text.append(i)
    i = 0 
    char = text[i]
    numeroCedula = ''
    while not char.isalpha():
        try:
            numeroCedula = numeroCedula + '{}'.format(char)
            i += 1
            char = text[i]
        except:
            break
        

    PARAMS = {'Token': '800010866',
              'Identificacion': numeroCedula,
              'lector': '2'}

    respuestaServidor = rq.get(url = URL, params= PARAMS)
    print(respuestaServidor.text)

"""
    timeIn = time.time()
    timeOut = time.time()
    if respuestaServidor[0] == '1' and respuestaServidor[1] == '1':

        GPIO.output(12,GPIO.HIGH)
        while timeIn - timeOut <= TIEMPO_ESPERA:
            timeOut = time.time()
        GPIO.output(12, GPIO.LOW)

    elif respuestaServidor[0] = '1' and respuestaServidor[1] = '2':

        GPIO.output(13, GPIO.HIGH)
        while timeIn - timeOut <= TIEMPO_ESPERA:
            timeOut = time.time()
        GPIO.output(13, GPIO.LOW)

    else:
        pass

"""

    
