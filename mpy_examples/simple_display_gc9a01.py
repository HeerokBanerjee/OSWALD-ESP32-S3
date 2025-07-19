from machine import Pin, SPI
import time
import gc9a01
tft = gc9a01.GC9A01(
        SPI(2, baudrate=1152000,polarity=0, sck=Pin(10), mosi=Pin(11)),
        240,
        240,
        reset=Pin(12, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(2, Pin.OUT),
        rotation=0)
tft.init()
tft.fill(gc9a01.GREEN)

# Play with it