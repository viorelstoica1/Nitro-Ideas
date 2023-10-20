import numpy as np
import sysv_ipc
import cv2
import time
import math

if __name__ == '__main__':

    width = 316
    height = 208
    cropX = 0
    cropY = 150
    cropWidth = width
    cropHeight = 120
    cadre_pe_linie = 2
    video = cv2.VideoCapture('traseu_compresat.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    divizor=0

    start_frame = 1800
    end_frame = 4400
    nr_frame = start_frame
    while 1 :
        nr_frame+=1
        timp_inceput = time.time()

        video.set(cv2.CAP_PROP_POS_FRAMES, nr_frame)
        ret, image = video.read()

        #croparea imaginii
        #image = image[cropY:cropY+cropHeight,cropX:cropX+cropWidth]
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
        img_thresh_adapt = cv2.adaptiveThreshold(aux, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 15)#THRESH_BINARY_INV
        lista_imagini.append(img_thresh_adapt)
        text_imagini.append("threshold adaptiv")

        #thresholding fix
        aux = img_blur
        ret, img_thresh_fix = cv2.threshold(aux,127,255,cv2.THRESH_BINARY)
        #lista_imagini.append(img_thresh_fix)
        #text_imagini.append("threshold fix")

        # Eroziune (cu input din adaptiv)
        kernel = np.ones((3, 3), np.uint8)# Creating kernel 
        aux = img_thresh_adapt
        img_erodat = cv2.erode(aux, kernel) 
        #lista_imagini.append(img_erodat)
        #text_imagini.append("eroziune din adaptiv")

        #dilatare (cu input din adaptiv)
        aux = img_thresh_adapt
        img_dilatat = cv2.dilate(aux, kernel, iterations=1)
        #lista_imagini.append(img_dilatat)
        #text_imagini.append("dilatare din adaptiv")

        #sobel
        aux = img_thresh_adapt
        img_sobel_x5 = cv2.Sobel(aux,cv2.CV_8U,1,0,ksize=5)
        lista_imagini.append(img_sobel_x5)
        text_imagini.append("sobel din adaptiv 5")

        # Eroziune (cu input din sobel)
        kernel = np.ones((3, 3), np.uint8)# Creating kernel 
        aux = img_sobel_x5
        img_erodat_sobel = cv2.erode(aux, kernel) 
        lista_imagini.append(img_erodat_sobel)
        text_imagini.append("eroziune de 3 din sobel 5")

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
            print("T:"+str(round((timp_sfarsit-timp_inceput),3))+"s, frame:"+str(nr_frame))
            divizor=0
        divizor+=1
        if nr_frame > end_frame:
            nr_frame = start_frame
out.release()
cv2.destroyAllWindows()
