# pylint: disable=no-member
import cv2
import numpy as np

#Detecta cuando hay pared

def pared(frame): 

    h, b, _ = frame.shape

    # Seleccionar ROI
    roi = frame[h-90:h-75, b//3:2*b//3]  

    # Convertir a grises
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Binarizar para detectar blanco o negro
    _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)

    # Contar pixeles blancos y negros
    blanco_pixels = cv2.countNonZero(bin)
    total_pixels = bin.size
    negro_pixels = total_pixels - blanco_pixels
    
    # Decisión
    if negro_pixels > blanco_pixels * 1.8:
        return 5
    else:
        return 0
