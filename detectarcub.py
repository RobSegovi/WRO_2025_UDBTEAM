from ultralytics import YOLO
import cv2

model = YOLO("cubos1.pt")

# Leer una imagen de prueba 
img = cv2.imread("C:\\Users\\yesen\\OneDrive\\Escritorio\\BENJA UNIVERSIDAD\\ARCHIVOS 2025\\WRO carrito\\cubos.jpg")

results = model(img)

# Mostrar coordenadas
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        print(f"{class_name}: x={cx}, y={cy}")
        
        # Dibujar círculo
        cv2.circle(img, (cx, cy), 50, (0, 255, 0), -1)

        # Escribir el nombre
        cv2.putText(img, class_name, (cx + 15, cy), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)
img = cv2.resize(img, (800, 600))
cv2.imshow("Resultado", img)
cv2.waitKey(0)
cv2.destroyAllWindows()