from led import rgbled
rgbled.setColor(40000,0,0)#led rosu primul pt a vedea ca merge placa

import network
import time
import socket

from Retea import AP
from servo import directie
from machine import Pin, PWM
from hbridge import hb
from senzor import senzDist
#import tftbmp

shouldRun = True
distanta = 0

def execWifiCommand(request):#Ordine: speed steer claxon shouldRun
    global shouldRun, distanta
    comenzi = [float(x) for x in request.split(recv_term) if x.strip()]
    if (distanta > 20.0 or distanta < 0.0) or comenzi[0] < 0:
        hb.setDuty(comenzi[0]/100.0)
    else:
        hb.setDuty(0)
    directie.steer(comenzi[1] * -1.0)
    sunet.duty_u16(40000 * int(comenzi[2]))
    if comenzi[3] == 1.0:
        print("dead")
        shouldRun = False


sunet = PWM(Pin(11))
sunet.freq(500)

speed_value = 0
direction = 1
isMoving = 0
numarRequesturi = 0
mesag = " "
recv_term = ' '
send_term = ' '
droppedRequests = 0

AP.open_socket()
print("Am deschis un socket")
try:
    rgbled.setColor(0,60000,0)
    while (shouldRun):
        distanta = senzDist.getDistance()
        numarRequesturi += 1
        mesag = AP.recieveMsg()
        if mesag != " ":
            execWifiCommand(mesag)
            AP.sendMsg(str(distanta))
            droppedRequests = 0
            rgbled.setColor(0,60000,0)
        else:
            droppedRequests += 1
            if droppedRequests >= 5:
                hb.setDuty(0)
                rgbled.setColor(45000,60000,0)
finally:
    rgbled.setColor(40000,0,0)
    AP.soc.close()
    hb.setDuty(0)
    directie.steer(0)
