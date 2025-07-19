from ubluetooth import BLE
ble = BLE()
ble.active(True)
# Start advertising
ble.gap_advertise(150, b'\x02\x01\x06' + b'\x05\x08ESP32BLE')
print("Started Advertising")
# Check in nRFConnect