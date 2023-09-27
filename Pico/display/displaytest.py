from ST7735 import TFT
from machine import SPI,Pin
from sysfont import sysfont
import time
spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=None)
tft=TFT(spi,1,0,4)
tft.setGraphic()
tft.initr()
tft.rgb(True)
tft.rotation(1)


def test_main():
    tft.fill(TFT.BLACK)
    for j in range (0,1000):
        i = str(j)
        tft.text((0, 0), i, TFT.WHITE, sysfont, 1) #merge cu font 3 daca decomentezi linia 21 (fillrect)
        #time.sleep_ms(1000)
        #tft.fill(TFT.BLACK)
        #tft.fillrect((0, 0), tft._size, TFT.BLACK)
        
    tft.text((0, 0), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)
    #tft.text((0, 0), str(time.time()), TFT.PURPLE, sysfont)

test_main()