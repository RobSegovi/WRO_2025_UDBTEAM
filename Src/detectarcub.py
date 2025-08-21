# Detectar y clasificar objetos en tiempo real
# pylint: disable=no-member
import time
from ultralytics import YOLO
import cv2
import serial
import numpy as np
from detectarcolores import lineas

# Configurar Arduino
#arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
#time.sleep(2)

# Cargar modelo YOLO
model = YOLO(r"c:\Users\yesen\OneDrive\Escritorio\BENJA UNIVERSIDAD\ARCHIVOS 2025\WRO carrito\Others\cubos1.pt")

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
    if conteo % 2 ==0:
        results = model(frame)

    # Convertir a grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Seleccionar una ROI
    h, b = gris.shape
    roi = gris[int(h*0.3):int(h*0.7), 0:b] 
    # Calcular brillo
    brillo = np.mean(roi)

    maxArea = 0
    objCercano = ""
    x = 0
    y = 0
    contador = 0
    linea = 0

    # Color de la linea
    linea = lineas(frame)

    cv2.rectangle(frame, (100, h-50), (b-100, h-30), (0, 255, 0), 2)

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
    #if contador == 0 and brillo < 80:
        #indicador = "3"
    if linea == 3 and n == 0 or linea == 3 and n == 1:
        indicador = "3"
        n=1
    elif linea == 4 and n == 0 or linea == 4 and n == 2:
        indicador = "4"
        n=2
    mensaje = f"{indicador},{x},{maxArea}\n"
    #print(brillo)
    #print(linea)
    print(mensaje)
    #arduino.write(mensaje.encode())  

    # Mostrar video en ventana
    cv2.imshow("Resultado", frame)

    # Salir con tecla q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
