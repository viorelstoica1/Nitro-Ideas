import network
import socket
import time


class Retea:
    def __init__(self, ssid = "picoW", pw = "123456789", recieve_termination = ' ', send_termination = ' '):
        print('Initialising access point...')
        self.ap = network.WLAN(network.AP_IF)
        self.recieve_termination = recieve_termination
        self.send_termination = send_termination
        self.ap.config(essid = ssid, password = pw)
        self.ap.active(True)
        while self.ap.isconnected() == False:
            time.sleep(0.5)
        self.ip_ = self.ap.ifconfig()[0]
        
    def open_socket(self, ip = "0.0.0.0"):
        address = (ip,80)
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.bind(address)
        self.soc.settimeout(0.005)

    def sendMsg(self, mesaje):
        self.soc.sendto((mesaje+self.send_termination).encode(), ("192.168.4.16",7876))
        
    def recieveMsg(self):#blocant pe recieve in functie de timeout
        try:
            request = self.soc.recv(64)
            return request.decode()
        except OSError as probabilTimeout:
            #print(probabilTimeout)
            return " "


AP = Retea()
# shouldRun = True
# AP.open_socket()
# print("Am deschis un socket")
# 
# numarRequesturi = 0
# mesag = " "
# try:
#     while (shouldRun):#cat timp e deschisa conexiunea
#         numarRequesturi += 1
#         print(numarRequesturi)
#         mesag = AP.recieveMsg()
#         if mesag != " ":
#             print(mesag)
#             AP.sendMsg(str(numarRequesturi/10))
#         time.sleep(0.05)
# finally:
#     AP.soc.close()
