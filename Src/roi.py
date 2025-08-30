# pylint: disable=no-member
import cv2
import numpy as np

def interior(frame,l,giro, lado):
    #DETECTAR DE QUE LADO ESTAMOS
    if lado == 0:
        if l == 3:
            return 13
            #algo
        if l == 4:
            return 14
            #algo
        return 1
    
    #ESTA PARTE ES PARA SENTIDO IZQUIERDA
    
    if lado == 2:
        h, b, _ = frame.shape
    
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)

    
        roi1 = bin[h-135:h-75, 0:20]   # ROI izquierda
        roi2 = bin[h-165:h-105, 85:105]  # ROI central izquierda
        roip = bin[5:25, 140:180]  # ROI de pared de giro
        #roi3 = frame[h-90:h-75, b-70:b-20]    # roi derecha

        cv2.rectangle(frame, (0, h-135), (20, h-75), (0, 255, 0), 2)
        cv2.rectangle(frame, (85, h-165), (105, h-105), (0, 255, 0), 2)
        cv2.rectangle(frame, (140, 5), (180, 25), (0, 255, 0), 2)
    
        def analizar_zonai(roi):
            blanco_pixels = cv2.countNonZero(roi)
            total_pixels = roi.size
            negro_pixels = total_pixels - blanco_pixels
            if negro_pixels > blanco_pixels*0.35:
                return 1
            else:
                return 0

        a = analizar_zonai(roi1)   # izquierda
        b = analizar_zonai(roi2)   # centro izquierda
        c = analizar_zonai(roip)
        #print (f"c: {c}")
        
        if giro == 0:
            if a == 1 and b == 0 and l == 0 :
                return 1   # IR RECTO
            elif a == 1 and b == 1 and l == 0:
                return 2   # CORREGIR A LA DERECHA
            elif a == 0 and b == 0 and l == 0:
                return 3   # CORREGIR A LA IZQUIERDA
            elif l==4 :#a == 0 and b == 0 and c == 0 and l == 4:
                #giro = 1
                return 4   # AVANZAR HASTA DETECTAR NEGRO DE GIRO
            else:
                return 5
    
        c = analizar_zonai(roip)
        #Cuando ya detecto linea pero tiene que girar a la izquierda    
        if giro == 1:
            print("giro es 1")
            #print (f"cb: {c}")
            if c == 1:
                print("DETECTE PARED")
                return 6
            return 1
        
    # ESTA PARTE ES PARA SENTIDO DERECHA
    if lado == 1:
        h, b, _ = frame.shape
    
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, bin = cv2.threshold(gris, 100, 255, cv2.THRESH_BINARY)

        roi1 = bin[h-135:h-75, b-20:b]   # ROI derecha
        roi2 = bin[h-165:h-105, b-105:b-85]  # ROI central derecha
        roip = bin[5:25, 140:180]  # ROI de pared de giro

        cv2.rectangle(frame, (b-20, h-135), (b, h-75), (0, 255, 0), 2)
        cv2.rectangle(frame, (b-105, h-165), (b-85, h-105), (0, 255, 0), 2)
        cv2.rectangle(frame, (140, 5), (180, 25), (0, 255, 0), 2)
    
        def analizar_zonad(roi):
            blanco_pixels = cv2.countNonZero(roi)
            total_pixels = roi.size
            negro_pixels = total_pixels - blanco_pixels
            if negro_pixels > blanco_pixels*0.35:
                return 1
            else:
                return 0
            
        a = analizar_zonad(roi1)   # derecha
        b = analizar_zonad(roi2)   # centro derecha
        c = analizar_zonad(roip)
        
        if giro == 0:
            if a == 1 and b == 0 and l == 0 :
                return 1   # IR RECTO
            elif a == 1 and b == 1 and l == 0:
                return 3   # CORREGIR A LA IZQUIERDA
            elif a == 0 and b == 0 and l == 0:
                return 2   # CORREGIR A LA DERECHA
            elif l==3 :#a == 0 and b == 0 and c == 0 and l == 4:
                #giro = 1
                return 4   # AVANZAR HASTA DETECTAR NEGRO DE GIRO
            else:
                return 5
    
        c = analizar_zonad(roip)
        #Cuando ya detecto linea pero tiene que girar a la derecha    
        if giro == 1:
            print("giro es 1")
            #print (f"cb: {c}")
            if c == 1:
                print("DETECTE PARED")
                return 7
            return 1