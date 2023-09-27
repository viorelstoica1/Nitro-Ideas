import rp2
import network
import ubinascii
import machine
import time
import socket
#import servo

from servo import directie
from machine import Pin, PWM
from hbridge import hb
from led import rgbled

rgbled.setColor(40000,0,0)
rp2.country('RO')
ip = ""
ssid = "picoW"
pw = "123456789"
pico_led = machine.Pin('LED', machine.Pin.OUT)

speed_value = 0
direction = 1
isMoving = 0
unBrick = False

sunet = PWM(Pin(11))
sunet.freq(500)


def InitAP():#nonblocant
    ap = network.WLAN(network.AP_IF)
    ap.config(essid = ssid, password = pw)
    ap.active(True)
    print('Initialising access point...')
    while ap.isconnected() == False:
        time.sleep(1)
    ip_ = ap.ifconfig()[0]
    print(f'Local address is {ip_}')
    return ip_

def turn_on_led():
    pico_led.on()
    
def turn_off_led():
    pico_led.off()
    
def open_socket(ip = "0.0.0.0"):#nonblocant
    address = (ip,80)
    bindedsoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bindedsoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindedsoc.bind(address)
    print("Listening")
    return bindedsoc
    
def sendSocket(client, mesaje):
    #client.sendall((mesaje+send_termination).encode())
    #client.write((mesaje+send_termination).encode())
    client.sendto((mesaje+send_termination).encode(), ("192.168.4.16",7876))

def readSocket(client): #tentativa de optimizare
    mesajPrimit = ""
    request = client.recv(1).decode()
    if request: #daca nu e un request de incheiere de conexiune
        while request != recieve_termination:
            mesajPrimit += request
            request = client.recv(1).decode()
        print(mesajPrimit)
        return mesajPrimit 
    else: #daca am primit mesaj de inchidere
        print("Socketul a fost inchis de client")
        return " "
        
def handle_request(client):#blocant pe recieve
    request = client.recv(64)
    if request:#daca nu am primit mesaj de inchidere
        #print(request.decode())
        #response = "bau"+send_termination
        #client.sendall(response.encode())
        return request.decode()
    else:#daca am primit mesaj de inchidere, refac conexiunea
        print("Socketul a fost inchis de client")
        return " "
    
def switch(request):
        global direction
        global isMoving
        global speed_value
        global shouldRun
        if "on" in request:
            print("ON")
            turn_on_led()
        elif "off" in request:
            print("OFF")
            turn_off_led()
        elif "unbrick" in request:
            print("UNBRICKED")
            shouldRun = False
        elif "forward" in request:
            print("forward")
            direction = 1
            isMoving = 1
            hb.setDuty(float(speed_value * direction))
        elif "backward" in request:
            print("backward")
            direction = -1
            isMoving = 1
            hb.setDuty(float(speed_value * direction))
        elif "stop" in request:
            print("stop")
            isMoving = 0
            hb.setDuty(0)
        elif "speed:" in request:
            start = "/speed:"
            end = recieve_termination
            speed_value = float(request.split(start)[1].split(end)[0])/100
            print(float(speed_value * direction))
            if isMoving:
                hb.setDuty(float(speed_value * direction))
                print("Is Moving")
            else:
                hb.setDuty(0)
                print("Not Moving")
        elif "steerLeft" in request:
            print("Steering left")
            directie.steerLeft()
        elif "endSteeringLeft" in request:
            print("Stop steering left")
            directie.steerStraight()
        elif "steerRight" in request:
            print("Steering right")
            directie.steerRight()
        elif "endSteeringRight" in request:
            print("Stop steering right")
            directie.steerStraight()
        elif "hornStop" in request:
            sunet.duty_u16(0)
            print("liniste")
        elif "horn" in request:
            sunet.duty_u16(40000)
            print("claxon")


ip = InitAP()

shouldRun = True
BindedSocket = open_socket(ip)
print("Am deschis un socket")
isValidSocket = True

numarRequesturi = 0
try:
    while shouldRun:
        mesag = ""
        rgbled.setColor(0,60000,0)
        while (mesag != " ") and (shouldRun):
            numarRequesturi += 1
            print(numarRequesturi)
            mesag = handle_request(BindedSocket)
            switch(mesag)
            sendSocket(BindedSocket, "bau")
        #print("Inchid socketul")
finally:
    rgbled.setColor(40000,0,0)
#    try:
#        BindedSocket.close()
#    except:
#        pass
    BindedSocket.close()


