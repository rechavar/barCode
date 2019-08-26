from zeep import Client as clt 
import time
import requests
URL1 = 'http://erm.expertoseguridad.com.co/wsCai/wsControlExterno.asmx?WSDL'
TOKEN = '800010866'
CLIENT = clt(URL1)
TIEMPO_ESPERA = 5000
url='http://216.58.192.142'
timeout=5
estadoConexion = False
caracteresValidos = ['+','-']

def check_internet():
    
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("no hay conexion a internet.")
    return False


while estadoConexion == False:
    estadoConexion = check_internet()

while True:
    barcode = input('Ingrese el codigo de barras')
    if barcode[-1] in caracteresValidos:
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

        respuestaServidor = CLIENT.service.Select_ControlaccesoAutomatizado(TOKEN,numeroCedula,'{} - {}'.format(fecha,hora))

        print('el servidor dio de respuesta: {} '.format(respuestaServidor))

        if respuestaServidor == '1':
            estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, fecha, '1')
            print('el servicio funciono?: {}'.format(estadoUsuario))

        if respuestaServidor == '2':
            estadoUsuario = CLIENT.service.Insert_ControlaccesoAutomatizado(TOKEN, numeroCedula, nombreCedula, apellidoCedula, fecha, '2')
            print('el servicio funciono?: {}'.format(estadoUsuario))
    else:
        print('Ingrese un documento valido')
    
