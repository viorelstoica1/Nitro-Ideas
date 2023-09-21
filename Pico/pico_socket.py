import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket
import servo

from machine import Pin, PWM
from hbridge import hb

rp2.country('RO')
ip = ""
ssid = "picoW"
pw = "123456789"
pico_led = machine.Pin('LED', machine.Pin.OUT)
recieve_termination = ' '
send_termination = ' '
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
    listeningSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listeningSoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listeningSoc.bind(address)
    listeningSoc.listen()
    print("Listening")
    return listeningSoc
    
def sendSocket(client, mesaje):
    client.sendall((mesaje+send_termination).encode())

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
    request = client.recv(128)
    if request:#daca nu am primit mesaj de inchidere
        print(request.decode())
        #response = "bau"+send_termination
        #client.sendall(response.encode())
        return True 
    else:#daca am primit mesaj de inchidere, refac conexiunea
        print("Socketul a fost inchis de client")
        return False
    
def switch(request):
        global direction
        global isMoving
        global speed_value
        global unBrick
        if "on" in request:
            print("ON")
            turn_on_led()
        elif "off" in request:
            print("OFF")
            turn_off_led()
        elif "unbrick" in request:
            print("UNBRICKED")
            unBrick = True
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
            servo.directie.steerLeft()
        elif "endSteeringLeft" in request:
            print("Stop steering left")
            servo.directie.steerStraight()
        elif "steerRight" in request:
            print("Steering right")
            servo.directie.steerRight()
        elif "endSteeringRight" in request:
            print("Stop steering right")
            servo.directie.steerStraight()
        elif "hornStop" in request:
            sunet.duty_u16(0)
            print("liniste")
        elif "horn" in request:
            sunet.duty_u16(40000)
            print("claxon")


ip = InitAP()

shouldRun = True
listeningSocket = open_socket(ip)
print("Am deschis un socket")
isValidSocket = True

numarRequesturi = 0
try:
    while shouldRun:#mentinem conexiunea cat mai mult
        print("Astept conexiune")
        connectedSocket = listeningSocket.accept()[0]
        print("Am acceptat o conexiune")
        mesag = ""
        while mesag != " ":#cat timp e deschisa conexiunea
            numarRequesturi += 1
            print(numarRequesturi)
            #isValidSocket = handle_request(connectedSocket)
            mesag = readSocket(connectedSocket)
            switch(mesag)
            sendSocket(connectedSocket, "bau")
        #print("Inchid socketul")
        connectedSocket.close()
finally:
    try:
        connectedSocket.close()
    except:
        pass
    listeningSocket.close()
    
