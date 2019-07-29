############################################################################################################
###### Programa diseñado para Expertos Seguridad el cual lee codigos de barras de cedulas, envia informacion 
###### a un webservice y con la respuesta de este autoriza o no la salida o ingreso de usuarios.############
############################################################################################################
 
import time
from zeep import Client as clt
##import RPi.GPIO as GPIO #Se usara una Raspberry 

URL1 = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
CLIENT = clt(URL1)
TIEMPO_ESPERA = 5000

while True: #El programa corre de forma indefinida
    try:
        barcode = input('Scan Barcode: ')

        barcode = barcode.split()
        localTime = time.localtime()
        if len(barcode) > 1:
            nombreCedula = str(barcode[1] +' '+ barcode[2] +' '+ barcode[3])
            if len(barcode[4]) > 1:
                nombreCedula = nombreCedula +' '+ str(barcode[4])
        numeroCedula = barcode[0]                 
        fecha = '{}/{}/{}'.format(localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
        hora = '{}:{}:{}'.format(localTime.tm_hour, localTime.tm_min, localTime.tm_sec)

        print('La persona {} con cedula {} ingreso el {} a las {}'.format(nombreCedula,numeroCedula,fecha,hora))
        print('--------------------------------------------------')
        respuestaServidor = CLIENT.service.ControlaccesoAutomatizado(TOKEN,'{}'.format(numeroCedula),'2')
        print('La persona tiene autorizacion? \n{}'.format(respuestaServidor))

    """
        timeIn = time.time()
        timeOut = time.time()
        if respuestaServidor[0] == '1' and respuestaServidor[1] == '1':

            GPIO.output(12,GPIO.HIGH)
            while timeIn - timeOut <= TIEMPO_ESPERA:
                timeOut = time.time()
            GPIO.output(12, GPIO.LOW)

        elif respuestaServidor[0] == '1' and respuestaServidor[1] == '2':

            GPIO.output(13, GPIO.HIGH)
            while timeIn - timeOut <= TIEMPO_ESPERA:
                timeOut = time.time()
            GPIO.output(13, GPIO.LOW)

        else:
            pass
"""
    except:
        pass

    
