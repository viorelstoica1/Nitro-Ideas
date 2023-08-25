import rp2
import network
import ubinascii
import machine
import urequests as requests
import time
import socket
import servo
from hbridge import hb
rp2.country('RO')
ip = ""
ssid = "picoW"
pw = "123456789"
pico_led = machine.Pin('LED', machine.Pin.OUT)
speed_value = 0
direction = 1
isMoving = 0
unBrick = False



def connect():
    #Connect to WLAN"""Stub file for the 'time' module."""
    ap = network.WLAN(network.AP_IF)
    ap.config(essid = ssid, password = pw)
    ap.active(True)
    while ap.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip_ = ap.ifconfig()[0]
    print(f'Connected on {ip_}')
    return ip_

def turn_on_led():
    pico_led.on()
    
def turn_off_led():
    pico_led.off()
    
def open_socket(ip):
    address = (ip,80)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(address)
    connection.listen(10)
    print("Connected")
    return connection

def switch(request):
        global direction
        global isMoving
        global speed_value
        global unBrick
        if "GET /on" in request:
            print("ON")
            turn_on_led()
        elif "GET /off" in request:
            print("OFF")
            turn_off_led()
        elif "GET /unbrick" in request:
            print("UNBRICKED")
            unBrick = True
        elif "GET /forward" in request:
            print("forward")
            direction = 1
            isMoving = 1
            hb.setDuty(float(speed_value * direction))
            
        elif "GET /backward" in request:
            print("backward")
            direction = -1
            isMoving = 1
            hb.setDuty(float(speed_value * direction))
            
        elif "GET /stop" in request:
            print("stop")
            isMoving = 0
            hb.setDuty(0)
            
        elif "GET /speed:" in request:
            start = "/speed:"
            end = " HTTP"
            speed_value = float(request.decode("utf-8").split(start)[1].split(end)[0])/100
            print(float(speed_value * direction))
            if isMoving:
                hb.setDuty(float(speed_value * direction))
                print("Is Moving")
            else:
                hb.setDuty(0)
                print("Not Moving")
            
        elif "GET /steerLeft" in request:
            print("Steering left")
            servo.directie.steerLeft()
        elif "GET /endSteeringLeft" in request:
            print("Stop steering left")
            servo.directie.steerStraight()
            
        elif "GET /steerRight" in request:
            print("Steering right")
            servo.directie.steerRight()
        elif "GET /endSteeringRight" in request:
            print("Stop steering right")
            servo.directie.steerStraight()
    
def handle_request(client_socket):
    global unBrick
    while unBrick != True:
        client = client_socket.accept()[0]
        request = client.recv(1024)
        print(request)
        
        switch(request)
                
        response = "HTTP/1.1 200 OK\r\n\r\nLED state changed"
        client.send(response)
        client.close()
    
try:
    ip = connect()
    connection = open_socket(ip)
    handle_request(connection)
except KeyboardInterrupt:
    machine.reset()
        
        
        

    

