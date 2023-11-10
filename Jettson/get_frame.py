import numpy as np
import sysv_ipc
import cv2
import time
import serial

def procesare(image, height, width):
    global dir_filt
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
            if mijloc > deadzone_x_start and mijloc < deadzone_x_finish and latime > width/10:
                has_middle = True
                lista_mijloc.append(mijloc)
            else:
            if mijloc < deadzone_x_start:
                has_left = True
                lista_stanga.append(cv2.contourArea(poligon_individual))
            else:
                has_right = True
                lista_dreapta.append(cv2.contourArea(poligon_individual))
                M = cv2.moments(poligon_individual)
                # Calculate the centroid of the contour
                if (M['m10'] != 0) and (M['m00'] != 0) and (M['m01'] != 0):
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])#probabil inutil
                    lista_mijlocuri.append(cx)
                    #if cx < width/2:
                    if cx < deadzone_x_start:
                        has_left = True
                        lista_stanga.append(cx)
                    else:
                        if cx > deadzone_x_finish:
                            has_right = True
                            lista_dreapta.append(cx)
                        else:
                            lista_mijloc.append(cx)
                            has_middle = True
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
    

#    if has_middle == True:
        #print(lista_mijloc)
#        directie = np.mean(lista_mijloc)
#        dir_filt += 0.05*(directie - dir_filt)
#        #print(directie)
#    else:
#    if has_left == False:
        #directie = directie-width/2
#        lista_stanga.append(0)
#    if has_right == False:
        #directie = directie+width/2
#        lista_dreapta.append(width)

    if has_left == False:
        suma_stanga = 0
    else:
        suma_stanga = np.mean(lista_stanga)
    if has_right == False:
        suma_dreapta = 0
    else:
        suma_dreapta = np.mean(lista_dreapta)
    #directie = (np.mean(lista_stanga) + np.mean(lista_dreapta))/2
    directie = (suma_dreapta - suma_stanga)/30
    print(directie)
    dir_filt += 0.4*(directie - dir_filt)
    #cv2.rectangle(img_contururi,(int(deadzone_x_start),int(0)), (int(deadzone_x_finish), int(width)), 0, -1)
    cv2.line(img_contururi,(int(width/2),height), (int(dir_filt),0),(255,255,255), 3)
    lista_imagini.append(img_contururi)

    directie = (dir_filt/(width/2)-1)
    
    transmit = str(viteza)+" "+str(directie)+" 0.0 0.0"
    s.write((transmit + "\n").encode())
    transmit = ""
    if 0:
        recieve = s.read_until().strip()
        if(recieve):
            print("Mesaj:"+recieve.decode())
        else:
            print("Timeout!")

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
    return final

if __name__ == '__main__':
    s = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    s.flush()
    recieve = ""
    transmit = "Init USB"

    width = 316
    height = 208
    cropX = 0
    cropY = 120
    cropWidth = width
    cropHeight = 208-cropY
    cadre_pe_linie = 2
    video = cv2.VideoCapture('traseu_compresat.mp4')
    fps = video.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    divizor=0
    dir_filt = 0
    
    deadzone_x_start = width*1.5/16
    deadzone_x_finish = width*14.5/16
    
    viteza = 10
    directie = -1.0
    start_frame = 2000
    end_frame = 4400
    nr_frame = start_frame
    fifo_path1 = '/home/nitro/pixy2/build/get_raw_frame/pipe1'  # Path to the named pipe
    fifo_path2 = '/home/nitro/pixy2/build/get_raw_frame/pipe2'

    # Define the codec and create VideoWriter object
    #width = 316
    #height = 208
    #cropX = 0
    #cropY = 150
    #cropWidth = width
    #cropHeight = 50
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter('Traseu_NXP.mp4', fourcc, 30, (width, height))
    #print(cv2.getBuildInformation())
    #divizor=0
    while 1 :
    # Open the named pipe for writing
        try:
            with open(fifo_path1, 'w') as fifo1:
                # Read the message from the named pipe
                message = "STORE IMAGE IN SHARED MEMORY!"
                fifo1.write(message)

        except FileNotFoundError:
            print("Named pipe not found. Make sure the C++ program is running.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


        # Open the named pipe for reading
        try:
            with open(fifo_path2, 'r') as fifo2:
                # Read the message from the named pipe
                message = fifo2.read()
                #print(f"Python script received message: {message}")

        except FileNotFoundError:
            print("Named pipe not found. Make sure the C++ program is running.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        key = 1000
        size = 1000000
        timp_inceput = time.time()
        memory = sysv_ipc.SharedMemory(key)
        memory_value = memory.read(size)

        #cv2.namedWindow("IMAGES",cv2.WINDOW_NORMAL)

        image_array = np.frombuffer(memory_value,dtype=np.uint8)

        image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
        out.write(image) # Write out frame to video
        final = procesare(image, height, width)

        cv2.imshow('video',final)
        cv2.waitKey(1)
        memory.detach()
        timp_sfarsit = time.time()
        if divizor>=5:
            print("T:"+str(round((timp_sfarsit-timp_inceput),6)))
            divizor=0
        divizor+=1
out.release()
cv2.destroyAllWindows()
