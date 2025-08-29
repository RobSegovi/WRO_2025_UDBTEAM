# pylint: disable=no-member
import cv2
import numpy as np

#Detecta cuando hay pared

def pared(frame): 

    h, b, _ = frame.shape

    # Seleccionar ROI
                    # h-75
    roi = frame[h-90:h, b//3:2*b//3]
    #roi = frame[70:90, 140:180] 

    # Convertir a grises
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Binarizar para detectar blanco o negro
    _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)

    # Contar pixeles blancos y negros
    blanco_pixels = cv2.countNonZero(bin)
    total_pixels = bin.size
    negro_pixels = total_pixels - blanco_pixels
    
    # Decisión
    if negro_pixels > blanco_pixels * 0.8:
        return 5
    else:
        return 0