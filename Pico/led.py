import time
from machine import Pin,PWM
#import machine

class LED:
    def __init__(self, pin0, pin1, pin2):
        self.pwms = [PWM(Pin(pin2, Pin.OUT)),PWM(Pin(pin1, Pin.OUT)),
                PWM(Pin(pin0, Pin.OUT))]
    # Set pwm frequency
        #self.[pwm.freq(1000) for pwm in pwms]
        self.pwms[0].freq(50)
        self.pwms[1].freq(50)
        self.pwms[2].freq(50)

    # Deinitialize PWM on all pins
    def deinit_pwm_pins(self):
        self.pwms[0].duty_u16(0)
        self.pwms[1].duty_u16(0)
        self.pwms[2].duty_u16(0)
        
    def blinkWhite(self):
        # Display WHITE
        self.pwms[0].duty_u16(40959)
        self.pwms[1].duty_u16(65535)
        self.pwms[2].duty_u16(65535)
        time.sleep(1)
        self.deinit_pwm_pins()
    
    def setColor(self, r,g,b):
        self.pwms[0].duty_u16(r)
        self.pwms[1].duty_u16(g)
        self.pwms[2].duty_u16(b)
        
    
    def testFunction(self):
            # Display 0
            self.pwms[0].duty_u16(65535)
            self.pwms[1].duty_u16(0)
            self.pwms[2].duty_u16(0)
            time.sleep(1)
            self.deinit_pwm_pins()
            
            # Display 1
            self.pwms[0].duty_u16(0)
            self.pwms[1].duty_u16(65535)
            self.pwms[2].duty_u16(0)
            time.sleep(1)
            self.deinit_pwm_pins()
            
            # Display 2
            self.pwms[0].duty_u16(0)
            self.pwms[1].duty_u16(0)
            self.pwms[2].duty_u16(65535)
            time.sleep(1)
            self.deinit_pwm_pins()

rgbled = LED(13,14,15)
#rgbled.testFunction()
