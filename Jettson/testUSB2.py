import serial


def main():
    s = serial.Serial(port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    s.flush()
    recieve = ""
    transmit = "Init USB"
    usbWorking = 1
    while(usbWorking):
        transmit = input("Mesaj:")
        if(transmit):
            s.write((transmit + "\r").encode())
            transmit = ""
            recieve = s.read_until().strip()
            if(recieve):
                print(recieve.decode())
            else:
                print("Timeout!")
        else:
            usbWorking = 0

        

if __name__ == "__main__":
    main()
