import numpy as np
import sysv_ipc
import cv2
import time
import math

if __name__ == '__main__':

    width = 316
    height = 208
    cropX = 0
    cropY = 120
    cropWidth = width
    cropHeight = 208-cropY
    cadre_pe_linie = 2
    video = cv2.VideoCapture('Traseu_NXP_mijloc.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    divizor=0

    deadzone_x_start = width/16
    deadzone_x_finish = width*15/16

    start_frame = (3*60+50)*30
    end_frame = start_frame +5*30
    nr_frame = start_frame
    dir_filt = 0
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
        #aux = img_blur
        #img_thresh_adapt = cv2.adaptiveThreshold(aux, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 9)#THRESH_BINARY_INV
        #lista_imagini.append(img_thresh_adapt)
        #text_imagini.append("threshold adaptiv")

        #thresholding fix
        aux = img_blur
        ret, img_thresh_fix = cv2.threshold(aux,127,255,cv2.THRESH_BINARY)
        cv2.rectangle(img_thresh_fix, (int(deadzone_x_start),int(0)), (int(deadzone_x_finish),int(height)), 0, -1)
        lista_imagini.append(img_thresh_fix)
        text_imagini.append("threshold fix")

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

        #sobel
        #aux = img_thresh_adapt
        #img_sobel_x5t = cv2.Sobel(aux,cv2.CV_8U,1,0,ksize=5)
        #lista_imagini.append(img_sobel_x5t)
        #text_imagini.append("sobel5 din treshold adaptiv")

        # Eroziune (cu input din adaptiv)
        #kernel = np.ones((3, 3), np.uint8)# Creating kernel 
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        #aux = img_sobel_x5t
        #img_erodat = cv2.erode(aux, kernel) 
        #lista_imagini.append(img_erodat)
        #text_imagini.append("eroziune din adaptiv")

        #contururi
        aux = img_thresh_fix
        img_contururi = np.zeros((height,width,1),np.uint8)
        lista_poligoane, hierarchy = cv2.findContours(aux, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#CHAIN_APPROX_NONE
        cv2.drawContours(img_contururi, lista_poligoane, -1, (255,255,255), 0)

        text_imagini.append("contururi din threshold")
        #lista_imagini.append(img_contururi)#mutat mai jos pt desenare pe el
        #procesare poligoane
        delim_x = [105,210,316]
        valori_zone = [0,0,0]

        #parcurg poligoanele extrase mai sus
        lista_mijlocuri = []
        has_left = False
        has_right = False
        has_middle = False
        lista_stanga = []
        lista_dreapta = []
        lista_mijloc = []
        for poligon_individual in lista_poligoane:
            if len(poligon_individual) > 2:
                # Get the moments of the contour
                
                min_x = width
                max_x = 0
                #print(poligon_individual)
                for punct in poligon_individual:
                    if punct[0][0] > max_x:
                        max_x = punct[0][0]
                    else:
                        if punct[0][0] < min_x:
                            min_x = punct[0][0]
                latime = max_x - min_x
                mijloc = (max_x + min_x)/2
                if min_x > deadzone_x_start and max_x < deadzone_x_finish and latime > width/15:
                    has_middle = True
                    lista_mijloc.append(mijloc)
                else:
                    if mijloc < deadzone_x_start:
                        has_left = True
                        lista_stanga.append(mijloc)
                    else:
                        has_right = True
                        lista_dreapta.append(mijloc)
#                M = cv2.moments(poligon_individual)
                # Calculate the centroid of the contour
#                if (M['m10'] != 0) and (M['m00'] != 0) and (M['m01'] != 0):
#                    cx = int(M['m10']/M['m00'])
#                    cy = int(M['m01']/M['m00'])#probabil inutil
#                    lista_mijlocuri.append(cx)
                    #if cx < width/2:
#                    if cx < deadzone_x_start:
#                        has_left = True
#                        lista_stanga.append(cx)
#                    else:
#                        if cx > deadzone_x_finish:
#                            has_right = True
#                            lista_dreapta.append(cx)
#                        else:
#                            lista_mijloc.append(cx)
#                            has_middle = True
    #                    for i in range(len(delim_x)):
    #                        if cx < delim_x[i]:
    #                            valori_zone[i] += cv2.contourArea(poligon_individual)
    #                            break

#        if valori_zone[0] == max(valori_zone):
#            directie = width
#        else:
#            if valori_zone[2] == max(valori_zone):
#                directie = 0
#            else:
#                directie = width/2
        
        if has_middle == True:
            #print(lista_mijloc)
            directie = np.mean(lista_mijloc)
            dir_filt += 0.05*(directie - dir_filt)
            #print(directie)
        else:
            if has_left == False:
                #directie = directie-width/2
                lista_stanga.append(0)
            if has_right == False:
                #directie = directie+width/2
                lista_dreapta.append(width)
            directie = (np.mean(lista_stanga) + np.mean(lista_dreapta))/2
            dir_filt += 0.4*(directie - dir_filt)
        cv2.rectangle(img_contururi,(int(deadzone_x_start),int(0)), (int(deadzone_x_finish), int(width)), 0, -1)
        cv2.line(img_contururi,(int(width/2),height), (int(dir_filt),0),(255,255,255), 3)
        lista_imagini.append(img_contururi)
        #r = ((deadzone_x_start,0),(deadzone_x_finish,height))


            
            




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
        cv2.waitKey(40)
        if divizor>=5:
            #print("Zone: "+str(valori_zone[0])+" "+str(valori_zone[1])+" "+str(valori_zone[2]))
            #print("T:"+str(round((timp_sfarsit-timp_inceput),3))+"s, frame:"+str(nr_frame))
            divizor=0
        else:
            divizor+=1
        if nr_frame > end_frame:
            nr_frame = start_frame
out.release()
cv2.destroyAllWindows()
