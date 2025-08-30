# Detectar y clasificar objetos en tiempo real
# pylint: disable=no-member
import time
from ultralytics import YOLO
import cv2
import serial
import numpy as np
from color import lineas
from pared import pared
from roi import interior

# Configurar Arduino y el puerto

def abrir_puerto():
    while True:
        try:
            s = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=9600,
                timeout=1,
                rtscts=False,
                dsrdtr=False
            )
            # evitar reset
            s.dtr = False
            s.rts = False
            time.sleep(2)  # darle tiempo al arduino
            s.reset_input_buffer()
            s.reset_output_buffer()
            print("? Puerto serie abierto correctamente")
            return s
        except serial.SerialException as e:
            print("No pude abrir el puerto, reintentando:", e)
            time.sleep(1)
            
# abrir puerto
arduino = abrir_puerto()
 
# Cargar modelo YOLO
model = YOLO("cubos1.pt")

# Abrir la camara
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # ancho
cap.set(4, 240)  # alto

n = 0
results = []
conteo=0
giro = 0
lado = 0
time.sleep(3)
prim = 0
x = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer la camara")
        break
    conteo += 1
    # Solo analizar cada 2 frames
    if conteo % 2 == 0:
        results = model(frame)

    h, b, _ = frame.shape
    maxArea = 0
    objCercano = ""
    #x = 0
    y = 0
    contador = 0
    linea = 0
    p = 0
    
    indicador = 0
    

    # Color de la linea
    linea, pixnaranja, pixazul = lineas(frame,  n)

    # Detectar pared
    p = pared(frame,lado)
    
    a = interior(frame,linea,giro,lado)
    if a == 4:
        giro = 1
    elif a == 6 or a == 7:
        giro = 0
    elif a == 13:
        lado = 1 # Lado derecho
        x=2
    elif a == 14:
        lado = 2 # Lado izquierdo
        x=1

                                              #h-75
    cv2.rectangle(frame, (b//3, h-90), (2*b//3, h), (0, 255, 0), 2) #rectangulo detecta pared
    cv2.rectangle(frame, (126, h-75), (193, h-45), (0, 255, 0), 2) #rectangulo detecta lineas 

    # Preparar mensaje para Arduino
 
    if lado == 0:
        indicador = "1" #AVANZAR
    elif a == 1:
        indicador = "1" #AVANZAR
    elif a == 2:
        indicador = "2" #CORREGIR A LA DERECHA
    elif a == 3:
        indicador = "3" #CORREGIR A LA IZQUIERDA
    elif a == 4:
        indicador = "1" #AVANZAR
        if lado == 2:
            x = 1
        if lado == 1:
            x = 2
    elif a == 5:
        indicador = "1" #AVANZAR
    elif a == 6:
        indicador = "4" #GIRO A LA IZQUIERDA CON DELAY
        mensaje = f"{indicador},{x},{maxArea}\n"
        for _ in range(10):
                arduino.write(mensaje.encode())
                print("4444")
                time.sleep(0.1)
        
    elif a == 7:  
        indicador = "5" #GIRO A LA DERECHA CON DELAY
        mensaje = f"{indicador},{x},{maxArea}\n"
        for _ in range(10):
                arduino.write(mensaje.encode())
                print("5555")
                time.sleep(0.1)
 
    if p == 5:
        indicador = "6" #DETENER Y RETROCEDER
    
    mensaje = f"{indicador},{x},{maxArea}\n"

    #impresion de valores en cmdp
    print(f"{mensaje} n:{n} linea:{linea} pN:{pixnaranja} pB:{pixazul} a:{a}")
    
    
    # enviar mensaje al arduino
    try:
        arduino.write(mensaje.encode())
    except serial.SerialException as e:
        print("?? Error de escritura, reabriendo puerto:", e)
        try:
            arduino.close()
        except:
            pass
        time.sleep(0.5)
        arduino = abrir_puerto()
        
        
    # Mostrar video en ventana
    cv2.imshow("Resultado", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


if arduino.is_open:
    arduino.close()
    print("? se cerro el puerto")