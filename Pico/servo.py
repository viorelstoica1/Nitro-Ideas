from machine import Pin, PWM

class Servo:
    def __init__(self,pin):
        self._PinServo = Pin(21, Pin.OUT)
        self._PWMServo = PWM(self._PinServo)
        self._PWMServo.freq(50)
        self._PWMServo.duty_u16(5000)
        # 5900 max stanga
        # 5000 mijloc
        # 4100 max dreapta
    def steerLeft(self):
        self._PWMServo.duty_u16(5900)
    def steerRight(self):
        self._PWMServo.duty_u16(4100)
    def steerStraight(self):
        self._PWMServo.duty_u16(5000)
    def setFrequency(self, newFrequency):
        if newFrequency > 300:
            print("Frecventa e prea mare pentru servo, max 300hZ")
        else:
            self._PWMServo.freq(newFrequency)
        
directie = Servo(21)
directie.steerStraight()
