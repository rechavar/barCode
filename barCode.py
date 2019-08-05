############################################################################################################
###### Programa diseñado para Expertos Seguridad el cual lee codigos de barras de cedulas, envia informacion 
###### a un webservice y con la respuesta de este autoriza o no la salida o ingreso de usuarios.############
############################################################################################################
 
import time
from zeep import Client as clt
import RPi.GPIO as GPIO #Se usara una Raspberry 

URL1 = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
CLIENT = clt(URL1)
TIEMPO_ESPERA = 5000

##GPIO config 12, 13, 6

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

GPIO.setup(13,GPIO.OUT)
GPIO.setup(6,GPIO.IN)



while True: #El programa corre de forma indefinida
    try:
        barcode = input('Scan Barcode: ')

        barcode = barcode.split()
        localTime = time.localtime()
        if len(barcode) > 1:
            apellidoCedula = str(barcode[1] +' '+ barcode[2]) 
            nombreCedula = str(barcode[3])
            if len(barcode[4]) > 1:
                nombreCedula = nombreCedula +' '+ str(barcode[4])
        numeroCedula = barcode[0]                 
        fecha = '{}/{}/{}'.format(localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
        hora = '{}:{}:{}'.format(localTime.tm_hour, localTime.tm_min, localTime.tm_sec)

        print('La persona {} con cedula {} ingreso el {} a las {}'.format(nombreCedula,numeroCedula,fecha,hora))
        print('--------------------------------------------------')
        respuestaServidor = CLIENT.service.Select_ControlaccesoAutomatizado(TOKEN,numeroCedula,'{} - {}'.format(fecha,hora))

        waitTime1 = time.time()
        waitTime2 = time.time()

        if respuestaServidor == '1':
            GPIO.output(12,GPIO.HIGH)
            while waitTime2-waitTime1 <= TIEMPO_ESPERA:
                waitTime2 = time.time()
                if waitTime2 - waitTime1 > TIEMPO_ESPERA:
                    print('Ha superado el tiempo de espera')
                    estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, '{} - {}'.format(fecha,hora), '0')

                if GPIO.input(6) == True:
                    print('El usuario a salido o ingresado')
                    estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, '{} - {}'.format(fecha,hora), '1')
                    brea
            GPIO.output(12,GPIO.LOW)   

        elif  respuestaServidor == '2': 
            GPIO.output(13,GPIO.HIGH)
            while waitTime2-waitTime1 <= TIEMPO_ESPERA:
                waitTime2 = time.time()
                if waitTime2 - waitTime1 > TIEMPO_ESPERA:
                    print('Ha superado el tiempo de espera')
                    estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, '{} - {}'.format(fecha,hora), '0')

                if GPIO.input(6) == True:
                    print('El usuario a salido o ingresado')
                    estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, '{} - {}'.format(fecha,hora), '1')
                    break 

            GPIO.output(13,GPIO.LOW)


            print(estadoUsuario)

        if respuestaServidor == '0':
            print('El usuario {} No tiene permiso para ingresar y/o salir'.format(numeroCedula))
    except:
        pass

    
