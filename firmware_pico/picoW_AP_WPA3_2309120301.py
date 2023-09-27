import rp2
import network
import urequests as requests
import time
import socket

from machine import Pin, PWM
rp2.country('RO')
pico_led = machine.Pin('LED', machine.Pin.OUT)
#Supported AP security modes
#0x00000000 Open
#0x00200002 WPA1 TKIP
#0x00400004 WPA2 CCMP (AES)
#0x01000004 WPA3 SAE (AES)
#0xxxxxxx06 mixed WPA2 & WPA1 with CCMP & TKIP (other options are likely to default to this)

ap = network.WLAN(network.AP_IF)
ap.config(essid = "pico8", password = "123456789", security=0x01000004)
ap.active(True)
while ap.isconnected() == False:
    print('Waiting for AP setup...')
    time.sleep(1)
ip_ = ap.ifconfig()[0]
print(f'AP set up @ {ip_}')