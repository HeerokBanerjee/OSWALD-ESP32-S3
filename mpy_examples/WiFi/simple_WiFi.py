import network
import time

ssid = 'BANERJEE 2.4 G'
password = '2999@3164'

sta = network.WLAN(network.STA_IF)
sta.active(True)

#Connecting to a WiFi network
sta.connect(ssid, password)
print(sta.isconnected())

print(sta.ifconfig())

''' Acting as AP
ap = network.WLAN(network.AP_IF)
ap.active(True)

#Configure your WiFi network name + pwd
ap.config(essid='MyESP32-AP', password='12345678')
print("Access Point active:", ap.active())
print("Network config:", ap.ifconfig())
'''
#Ping test
import socket

def tcp_ping(host, port=80, timeout=3):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

print("Is 192.168.1.34 up?", tcp_ping("192.168.1.34", 80))