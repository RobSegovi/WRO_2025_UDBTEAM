#otra prueba
# pylint: disable=no-member
import cv2
import numpy as np

def lineas(frame,n):
    # Naranja
    lower_naranja = np.array([5, 100, 100])
    upper_naranja = np.array([15, 255, 255])

    # Azul
    lower_azul = np.array([80, 40, 60])
    upper_azul = np.array([140, 255, 255])

    # Seleccionar ROI en la parte baja
    h, b, _ = frame.shape
    # cv2.rectangle(frame, (140, h-40), (180, h-20), (0, 255, 0), 2)
    
    #roi = frame[80:100, 140:180]
    roi = frame[h-75:h-45, 126:193]
    roip = frame[h-75:h-45, 126:193]
    
    # Convertir a grises
    gris = cv2.cvtColor(roip, cv2.COLOR_BGR2GRAY)
    # Binarizar para detectar blanco o negro
    _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)
    # Contar pixeles blancos y negros
    blanco_pixels = cv2.countNonZero(bin)
    total_pixels = bin.size
    negro_pixels = total_pixels - blanco_pixels
    
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
 
    mask_naranja_roi = cv2.inRange(hsv_roi, lower_naranja, upper_naranja)
    mask_azul_roi = cv2.inRange(hsv_roi, lower_azul, upper_azul)

    # Contar píxeles en la ROI
    naranja_pixels = cv2.countNonZero(mask_naranja_roi)
    azul_pixels = cv2.countNonZero(mask_azul_roi)

    #solo pruebas comentar luego
    #cv2.imshow("ROI", roi)
    #cv2.imshow("Mascara Naranja", mask_naranja_roi)
    cv2.imshow("Mascara Azul", mask_azul_roi)
    #fin de codigo prueba
    
    print(f"PNEG: {negro_pixels}")
    # Retornar la linea detectada
    if naranja_pixels > 50:
        linea = 3
    elif azul_pixels > 35 and negro_pixels < azul_pixels:
        linea = 4
    else:
        return 0, naranja_pixels, azul_pixels
    
    
    if linea == 3 and n == 0 or linea == 3 and n == 1:
        return 3, naranja_pixels, azul_pixels
        #n=1
    elif linea == 4 and n == 0 or linea == 4 and n == 2:
        return 4, naranja_pixels, azul_pixels
        #n=2
    elif linea == 4 and n ==1:
        return 0, naranja_pixels, azul_pixels
    elif linea == 3 and n == 2:
        return 0, naranja_pixels, azul_pixels