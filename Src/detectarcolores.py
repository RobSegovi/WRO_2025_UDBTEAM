# pylint: disable=no-member
import cv2
import numpy as np

def lineas(frame):
    # Naranja
    lower_naranja = np.array([5, 100, 100])
    upper_naranja = np.array([15, 255, 255])

    # Azul
    lower_azul = np.array([100, 100, 100])
    upper_azul = np.array([130, 255, 255])

    # --- ROI: rectángulo en la parte baja ---
    h, b= frame.shape
    roi = frame[h-50:h-30, 100:b-100]  # zona baja centrada
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    mask_naranja_roi = cv2.inRange(hsv_roi, lower_naranja, upper_naranja)
    mask_azul_roi = cv2.inRange(hsv_roi, lower_azul, upper_azul)

    # Contar píxeles en la ROI
    naranja_pixels = cv2.countNonZero(mask_naranja_roi)
    azul_pixels = cv2.countNonZero(mask_azul_roi)

    # Retornar la linea detectada
    if naranja_pixels > 200:  # umbral ajustable
        return 3
    elif azul_pixels > 200:
        return 4
    else:
        return 0
