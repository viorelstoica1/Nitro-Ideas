import numpy as np
import sysv_ipc
import cv2


if __name__ == '__main__':

    fifo_path1 = '/home/nitro/pixy2/build/get_raw_frame/pipe1'  # Path to the named pipe
    fifo_path2 = '/home/nitro/pixy2/build/get_raw_frame/pipe2'

    # Define the codec and create VideoWriter object
    width = 316
    height = 208
    cropX = 0
    cropY = 150
    cropWidth = width
    cropHeight = 50
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter('Semne.mp4', fourcc, 30, (width, height))
    #print(cv2.getBuildInformation())
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

        memory = sysv_ipc.SharedMemory(key)
        memory_value = memory.read(size)

        #cv2.namedWindow("IMAGES",cv2.WINDOW_NORMAL)

        image_array = np.frombuffer(memory_value,dtype=np.uint8)

        image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
        #image = image[cropY:cropY+cropHeight,cropX:cropX+cropWidth]
        #croparea imaginii
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #transformare in tonuri de gri
        #image = cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
        #transformare gaus
        #ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
        # Creating kernel 
        #kernel = np.ones((5, 5), np.uint8) 
        # Eroding
        #image = cv2.erode(image, kernel) 
        #dilatare
        #image = cv2.dilate(image, kernel, iterations=1)
        cv2.imshow('video',image)
        #out.write(image) # Write out frame to video
        cv2.waitKey(1)

        memory.detach()

out.release()
cv2.destroyAllWindows()
