import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket

from Retea import AP
from servo import directie
from machine import Pin, PWM
from hbridge import hb
from led import rgbled

rgbled.setColor(40000,0,0)
rp2.country('RO')
ip = ""
ssid = "picoW"
pw = "123456789"
recv_term = ' '
send_term = ' '
speed_value = 0
direction = 1
isMoving = 0
unBrick = False

sunet = PWM(Pin(11))
sunet.freq(500)

def execWifiCommand(request):
    comenzi = [float(x) for x in request.split(recv_term) if x.strip()]
    #print(comenzi)
    #Ordine: speed steer claxon unbrick
    hb.setDuty(comenzi[0]/100.0)
    directie.steer(comenzi[1] * -1.0)
    sunet.duty_u16(40000 * int(comenzi[2]))
    if comenzi[3] == 1.0:
        shouldRun = False

rgbled.setColor(40000,0,0)
shouldRun = True
AP.open_socket()
print("Am deschis un socket")

numarRequesturi = 0
mesag = " "
try:
    rgbled.setColor(0,60000,0)
    while (shouldRun):
        numarRequesturi += 1
        #print(numarRequesturi)
        mesag = AP.recieveMsg()
        if mesag != " ":
            #print(mesag)
            execWifiCommand(mesag)
            AP.sendMsg(str(numarRequesturi/10))
        #time.sleep(0.05)
finally:
    rgbled.setColor(40000,0,0)
    AP.soc.close()

