from ubluetooth import BLE, UUID, FLAG_READ, FLAG_WRITE, FLAG_NOTIFY
import struct
import time
import random

class BLETemp:
    def __init__(self, ble, name="ESP32-Temp"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)

        # BLE service UUID and characteristics
        SERVICE_UUID = UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        TEMP_CHAR = (UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), FLAG_READ | FLAG_NOTIFY)
        CMD_CHAR = (UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), FLAG_WRITE)

        SERVICE = (SERVICE_UUID, (TEMP_CHAR, CMD_CHAR))
        ((self._temp_handle, self._cmd_handle),) = self._ble.gatts_register_services((SERVICE,))

        self._connections = set()

        # Start advertising
        self._payload = self._advertising_payload(name=name)
        self._ble.gap_advertise(150, self._payload)
        print("Advertising as:", name)

    def _irq(self, event, data):
        if event == 1:  # connect
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Device connected:", conn_handle)
        elif event == 2:  # disconnect
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            print("Device disconnected:", conn_handle)
            self._ble.gap_advertise(100, self._payload)
        elif event == 3:  # write
            conn_handle, attr_handle = data
            if attr_handle == self._cmd_handle:
                cmd = self._ble.gatts_read(self._cmd_handle)
                print("Command received:", cmd)

    def _advertising_payload(self, name=None):
        payload = bytearray()
        payload += bytes((2, 0x01, 0x06))  # Flags
        if name:
            payload += bytes((len(name)+1, 0x09)) + name.encode()
        return payload

    def set_temperature(self, temp):
        # Write temp as 16-bit int * 100 (i.e. 25.34°C -> 2534)
        temp_value = struct.pack("<h", int(temp*100))
        self._ble.gatts_write(self._temp_handle, temp_value)
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._temp_handle, temp_value)
        print("Temperature updated to:", temp, "°C")

# Usage
ble = BLE()
ble_temp = BLETemp(ble)

while True:
    # Fake temperature data
    fake_temp = 20 + random.uniform(-2, 2)
    ble_temp.set_temperature(fake_temp)
    time.sleep(10)
