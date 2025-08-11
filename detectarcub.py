""" Detectar y clasificar objetos"""
# pylint: disable=no-member
from ultralytics import YOLO
import cv2

model = YOLO("cubos1.pt")

# Leer una imagen de prueba
img = cv2.imread("cubov.jpg")

#if img is None:
    #print("Error: No se pudo leer la imagen. Revisa el nombre, la ruta o que esté descargada localmente.")
    #exit()

results = model(img)

maxArea = 0
objCercano = ""
contador = 0
x = 0
y = 0

# Mostrar coordenadas
for r in results:
    for box in r.boxes:
        contador += 1
        x1, y1, x2, y2 = box.xyxy[0]
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        area = (x2 - x1) * (y2 - y1)
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        print(f"{class_name}: x={cx}, y={cy}, Area={area}")
        if area > maxArea:
            maxArea = area
            objCercano = class_name
            x = cx
            y = cy

        # Dibujar círculo
        cv2.circle(img, (cx, cy), 15, (0, 255, 0), -1)

        # Escribir el nombre
        cv2.putText(img, class_name, (cx + 15, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

print(f"Objeto más cercano: {objCercano}, Area={maxArea}")
if contador == 0:
    mensaje = "0,x,y\n"
else:
    if objCercano == "Cubo verde":
        indicador = "1"
    elif objCercano == "Cubo rojo":
        indicador = "2"
    else:
        indicador = "0"
    mensaje = f"{indicador},{x},{y}\n"

print(mensaje)
img = cv2.resize(img, (800, 600))
cv2.imshow("Resultado", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
