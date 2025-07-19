import cst816
from machine import Pin, I2C, SPI
import time
import gc9a01
tft = gc9a01.GC9A01(
        SPI(2, baudrate=2000000,polarity=0, sck=Pin(10), mosi=Pin(11)),
        240,
        240,
        reset=Pin(12, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        dc=Pin(8, Pin.OUT),
        backlight=Pin(2, Pin.OUT),
        rotation=0,
        buffer_size=16*32*2)
tft.fill(gc9a01.WHITE)

# Initialize I2C
# i2c_device = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
touch = cst816.CST816()

# Check if the touch controller is detected
if touch.who_am_i():
    print("CST816 detected.")
else:
    print("CST816 not detected.")

# Read touch data continuously
while True:
    point = touch.get_point()
    gesture = touch.get_gesture()
    press = touch.get_touch()
    distance = touch.get_distance()
    print("Position: {0},{1} - Gesture: {2} - Pressed? {3} - Distance: {4},{5}".format(point.x_point, point.y_point, gesture, press, distance.x_dist, distance.y_dist))
    time.sleep(0.05)
    
    # GESTURES
    if gesture == 1: #SWIPE UP
        tft.fill(gc9a01.BLACK)
    elif gesture == 2: #SWIPE DOWN
        tft.fill(gc9a01.WHITE)
    elif gesture == 3: #SWIPE LEFT
        tft.fill(gc9a01.GREEN) 
    elif gesture == 4: #SWIPE RIGHT
        tft.fill(gc9a01.YELLOW) 
    elif gesture == 5: #DOUBLE TAP
        tft.fill(gc9a01.BLUE)
    elif gesture == 12: # LONG PRESS
        tft.fill(gc9a01.RED)


