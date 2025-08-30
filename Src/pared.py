# pylint: disable=no-member
import cv2
import numpy as np

#Detecta cuando hay pared

def pared(frame,lado): 
    
    h, b, _ = frame.shape
    # Seleccionar ROI
    roi = frame[h-90:h, b//3:2*b//3]
    # Convertir a grises
    gris = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Binarizar para detectar blanco o negro
    _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)
    
    # Contar pixeles blancos y negros
    blanco_pixels = cv2.countNonZero(bin)
    total_pixels = bin.size
    negro_pixels = total_pixels - blanco_pixels
    
    if lado == 1: #LADO DERECHO
        # Seleccionar ROI
        roi1 = frame[h-60:h, 0:20]
        cv2.rectangle(frame, (0, h-60), (20, h), (0, 255, 0), 2)
        # Convertir a grises
        gris1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
        # Binarizar para detectar blanco o negro
        _, bin = cv2.threshold(gris1, 100, 255, cv2.THRESH_BINARY)
        
        # Contar pixeles blancos y negros
        blanco_pixels1 = cv2.countNonZero(bin)
        total_pixels1 = bin.size
        negro_pixels1 = total_pixels1 - blanco_pixels1
        # Decisión
        if negro_pixels1 > blanco_pixels1 * 0.8 or negro_pixels > blanco_pixels * 0.8:
            return 5
        else:
            return 0

    if lado == 2: #LADO IZQUIERDO
        # Seleccionar ROI
        print("LADO2")
        roi2 = frame[h-60:h, b-20:b]
        cv2.rectangle(frame, (b-20, h-60), (b, h), (0, 255, 0), 2)
        # Convertir a grises
        gris2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2GRAY)
        # Binarizar para detectar blanco o negro
        _, bin = cv2.threshold(gris2, 100, 255, cv2.THRESH_BINARY)
        
        # Contar pixeles blancos y negros
        blanco_pixels2 = cv2.countNonZero(bin)
        total_pixels2 = bin.size
        negro_pixels2 = total_pixels2 - blanco_pixels2
        # Decisión
        if negro_pixels2 > blanco_pixels2 * 0.8 or negro_pixels > blanco_pixels * 0.8:
            return 5
        else:
            return 0