from machine import Pin, PWM, mem32;
from time import sleep;
led = Pin('LED', Pin.OUT)

class PWMComp:
    def __init__(self, PinH, PinL, deadfrac=0.005, minlow=0.005, freq=40000):
        self.deadticks = int(deadfrac * 65535)
        self.maxhighticks = 65535 - self.deadticks - int(minlow*65535)
        if 1 & ~(PinH ^ PinL):
            raise Exception("Pins " + str(PinH) + " and " + str(PinL) + " are on the same channel of the same slice!")
        self.PinH = Pin(PinH, Pin.OUT)
        self.PinL = Pin(PinL, Pin.OUT)
        self.PWMH = PWM(self.PinH)
        self.PWML = PWM(self.PinL)
        self.PWML.freq(freq)
        self.PWMH.freq(freq)
        
        #https://forums.raspberrypi.com/viewtopic.php?t=332255
        self.slice = (PinH>>1)&0x7
        if self.slice != (0x7&(PinL>>1)):
            raise Exception("Pins " + str(PinL) + " " + str(PinH) + " used in PWMComp are not from same slice!")    
        mem32[0x40050000 +0x14*self.slice] = (mem32[0x40050000 +0x14*self.slice]&~0xc) | (0x8 if PinH<PinL else 0x4) | 0x2
        
    def setDuty(self, f): # f in [0, 1)
        if f>0:
            f *= 65535
            f = min(int(f), self.maxhighticks)
            self.PWMH.duty_u16(f)
            self.PWML.duty_u16(f+self.deadticks)
        else:
            self.PWMH.duty_u16(0)
            self.PWML.duty_u16(0)
            print("here")
    def setFree(self): # free wheeling
        self.PWMH.duty_u16(0)
        self.PWML.duty_u16(0)
            
        
class HBridge:
    def __init__(self, H0, L0, H1, L1, df=0.005, ml=0.005):
        self.PWMC0 = PWMComp(H0, L0, df, ml)
        self.PWMC1 = PWMComp(H1, L1, df, ml)
    def setDuty(self, f): # f in (-1, 1)
        if f<0:
            self.PWMC0.setDuty(-f)
            self.PWMC1.setDuty(0)
        else:
            self.PWMC0.setDuty(0)
            self.PWMC1.setDuty(f)

hb=HBridge(18, 19, 7, 6)
# if 1:
#     for i in range(30):
#         hb.setDuty(-i/10.0/7.4)
#         sleep(0.1)
#     for i in range(30,-1,-1):
#         hb.setDuty(-i/10.0/7.4)
#         sleep(0.1)
hb.setDuty(0)
# led=Pin('LED', Pin.OUT)
# ledpwm = PWM(led)
# ledpwm.freq(8)
# ledpwm.duty_u16(65535>>1)