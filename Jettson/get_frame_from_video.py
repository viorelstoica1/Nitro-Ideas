import numpy as np
import sysv_ipc
import cv2
import time
import math

if __name__ == '__main__':

    width = 316
    height = 208
    cropX = 0
    cropY = 100
    cropWidth = width
    cropHeight = 108
    cadre_pe_linie = 2
    video = cv2.VideoCapture('traseu_compresat.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    divizor=0



    start_frame = 2000
    end_frame = 4400
    nr_frame = start_frame
    while 1 :
        nr_frame+=1
        timp_inceput = time.time()

        video.set(cv2.CAP_PROP_POS_FRAMES, nr_frame)
        ret, image = video.read()

        #croparea imaginii
        image = image[cropY:cropY+cropHeight,cropX:cropX+cropWidth]
        width = cropWidth
        height = cropHeight
        lista_imagini = []
        text_imagini = []

        #transformare in tonuri de gri
        aux = image
        img_gri = cv2.cvtColor(aux, cv2.COLOR_BGR2GRAY)
        lista_imagini.append(img_gri)
        text_imagini.append("grayscale")

        #transformare gaus
        aux = img_gri
        img_blur = cv2.GaussianBlur(aux,(5,5),cv2.BORDER_DEFAULT)
        lista_imagini.append(img_blur)
        text_imagini.append("gaussian blur")

        #thresholding adaptiv
        aux = img_blur
        img_thresh_adapt = cv2.adaptiveThreshold(aux, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 9)#THRESH_BINARY_INV
        lista_imagini.append(img_thresh_adapt)
        text_imagini.append("threshold adaptiv")

        #thresholding fix
        #aux = img_blur
        #ret, img_thresh_fix = cv2.threshold(aux,127,255,cv2.THRESH_BINARY)
        #lista_imagini.append(img_thresh_fix)
        #text_imagini.append("threshold fix")

        # Eroziune (cu input din adaptiv)
        #kernel = np.ones((3, 3), np.uint8)# Creating kernel 
        #aux = img_thresh_adapt
        #img_erodat = cv2.erode(aux, kernel) 
        #lista_imagini.append(img_erodat)
        #text_imagini.append("eroziune din adaptiv")

        #dilatare (cu input din adaptiv)
        #aux = img_thresh_adapt
        #img_dilatat = cv2.dilate(aux, kernel, iterations=1)
        #lista_imagini.append(img_dilatat)
        #text_imagini.append("dilatare din adaptiv")

        #contururi
        aux = img_thresh_adapt
        img_contururi = np.zeros((height,width,1),np.uint8)
        lista_poligoane, hierarchy = cv2.findContours(aux, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#CHAIN_APPROX_NONE
        cv2.drawContours(img_contururi, lista_poligoane, -1, (255,255,255), 0)

        text_imagini.append("contururi din threshold")
        #lista_imagini.append(img_contururi)#mutat mai jos pt desenare pe el
        #procesare poligoane
        delim_x = [105,210,316]
        valori_zone = [0,0,0]

        for poligon_individual in lista_poligoane:
            if len(poligon_individual) > 2:
                # Get the moments of the contour

                M = cv2.moments(poligon_individual)
                # Calculate the centroid of the contour
                if (M['m10'] != 0) and (M['m00'] != 0) and (M['m01'] != 0):
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                        
                    for i in range(len(delim_x)):
                        if cx < delim_x[i]:
                            valori_zone[i] += cv2.contourArea(poligon_individual)
                            break

        if valori_zone[0] == max(valori_zone):
            directie = width
        else:
            if valori_zone[2] == max(valori_zone):
                directie = 0
            else:
                directie = width/2
        cv2.line(img_contururi,(int(width/2),height), (int(directie),0),(255,255,255), 3)
        lista_imagini.append(img_contururi)

        #sobel
        #aux = img_contururi
        #img_sobel_x5t = cv2.Sobel(aux,cv2.CV_8U,1,0,ksize=5)
        #lista_imagini.append(img_sobel_x5t)
        #text_imagini.append("sobel5 din treshold adaptiv")

        #afisare
        nr_cadre = len(lista_imagini)
        nr_linii = int(np.ceil(nr_cadre/cadre_pe_linie))
        nr_coloane = cadre_pe_linie

        randuri_poze = []
        for i in range(nr_linii):
            linie_poze = []
            for j in range(nr_coloane):
                index_lista = i*nr_coloane+j
                if index_lista < nr_cadre:
                    cv2.putText(lista_imagini[index_lista], text_imagini[index_lista], (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
                    linie_poze.append(lista_imagini[index_lista])
                else:
                    #linie_poze.append(lista_imagini[0])
                    linie_poze.append(np.zeros((height,width,1), np.uint8))
            randuri_poze.append(cv2.hconcat(linie_poze))
        final = cv2.vconcat(randuri_poze)

        cv2.imshow('video',final)

        timp_sfarsit = time.time()
        cv2.waitKey(5)
        if divizor>=5:
            #print("Puncte:"+str(contours))
            print("Zone: "+str(valori_zone[0])+" "+str(valori_zone[1])+" "+str(valori_zone[2]))
            if max(valori_zone) == valori_zone[0]:
                print("Dreapta")
            else:
                if max(valori_zone) == valori_zone[2]:
                    print("Stanga")
                else:
                    print("Fata")
            #print("T:"+str(round((timp_sfarsit-timp_inceput),3))+"s, frame:"+str(nr_frame))
            divizor=0
        divizor+=1
        if nr_frame > end_frame:
            nr_frame = start_frame
out.release()
cv2.destroyAllWindows()
