import numpy as np
import sysv_ipc
import cv2


if __name__ == '__main__':

    fifo_path1 = '/home/ursachi/pixy2/src/host/libpixyusb2_examples/get_raw_frame/pipe1'  # Path to the named pipe
    fifo_path2 = '/home/ursachi/pixy2/src/host/libpixyusb2_examples/get_raw_frame/pipe2'

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
                print(f"Python script received message: {message}")

        except FileNotFoundError:
            print("Named pipe not found. Make sure the C++ program is running.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        key = 1000
        size = 1000000

        memory = sysv_ipc.SharedMemory(key)
        memory_value = memory.read(size)

        cv2.namedWindow("IMAGES",cv2.WINDOW_NORMAL)

        image_array = np.frombuffer(memory_value,dtype=np.uint8)

        image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
        cv2.imshow("IMAGES",image)
        cv2.waitKey(1)

        memory.detach()