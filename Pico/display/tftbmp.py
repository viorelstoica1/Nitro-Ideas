from ST7735 import TFT,TFTColor
from machine import SPI,Pin
spi = SPI(0, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(2), mosi=Pin(3), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
#tft.rgb(True)
#tft.invertcolor(True)
tft.fill(TFT.BLACK)

f=open('guta.bmp', 'rb')
if f.read(2) == b'BM':  #header
    dummy = f.read(8) #file size(4), creator bytes(4)
    offset = int.from_bytes(f.read(4), 'little')
    print(offset)
    #offset = 1
    hdrsize = int.from_bytes(f.read(4), 'little')
    #hdrsize = 0
    print(hdrsize)
    width = int.from_bytes(f.read(4), 'little')
    print(width)
    height = int.from_bytes(f.read(4), 'little')
    print(height)
    if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
        depth = int.from_bytes(f.read(2), 'little')
        if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
            print("Image size:", width, "x", height)
            rowsize = (width * 3 + 3) & ~3
            if height < 0:
                height = -height
                flip = False
            else:
                flip = True
            w, h = width, height
            if w > 80: w = 80
            if h > 160: h = 160
            tft._setwindowloc((0,0),(w - 1,h - 1))
            for row in range(h):
                if flip:
                    pos = offset + (height - 1 - row) * rowsize
                else:
                    pos = offset + row * rowsize
                if f.tell() != pos:
                    dummy = f.seek(pos)
                for col in range(w):
                    bgr = f.read(3)
                    tft._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
spi.deinit()