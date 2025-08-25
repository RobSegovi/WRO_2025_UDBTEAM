# Detectar y clasificar objetos en tiempo real
# pylint: disable=no-member
import time
from ultralytics import YOLO
import cv2
import serial
import numpy as np
from detectarcolores import lineas
from detectarpared import pared

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
    x = 0
    y = 0
    contador = 0
    linea = 0
    p = 0

    # Color de la linea
    linea = lineas(frame)

    # Detectar pared
    p = pared(frame)

    cv2.rectangle(frame, (100, h-40), (b-100, h-20), (0, 255, 0), 2)
    cv2.rectangle(frame, (b//3, h-90), (2*b//3, h-75), (0, 255, 0), 2)

    # Procesar detecciones
    for r in results:
        for box in r.boxes:
            contador += 1
            x1, y1, x2, y2 = box.xyxy[0]
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            area = (x2 - x1) * (y2 - y1)
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            #print(f"{class_name}: x={cx}, y={cy}, Area={area}")

            if area > maxArea:
                maxArea = area
                objCercano = class_name
                x = cx
                y = cy
            # Dibujar circulo
            # cv2.circle(frame, (cx, cy), 15, (0, 255, 0), -1)
            # Escribir nombre
            # cv2.putText(frame, class_name, (cx + 15, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            # Dibujar rectangulo

    # Preparar mensaje para Arduino
    if contador == 0:
        indicador = "0"
    else:
        if objCercano == "Cubo verde":
            indicador = "1"
        elif objCercano == "Cubo rojo":
            indicador = "2"
        else:
            indicador = "0"
    
    if p == 5:
        indicador = "5"

    if linea == 3 and n == 0 or linea == 3 and n == 1:
        indicador = "3"
        n=1
    elif linea == 4 and n == 0 or linea == 4 and n == 2:
        indicador = "4"
        n=2
    
    mensaje = f"{indicador},{x},{maxArea}\n"

    #print(linea)
    print(mensaje)
    
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