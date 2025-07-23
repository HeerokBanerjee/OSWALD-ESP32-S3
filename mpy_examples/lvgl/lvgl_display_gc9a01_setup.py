# Copyright (c) 2024 - 2025 Kevin G. Schlosser

from micropython import const
from machine import SPI, Pin
import lvgl as lv
import gc9a01
import lcd_bus  # NOQA

_WIDTH = const(240)
_HEIGHT = const(240)



### PIN CONFIGURATION - ESP32-S3-LCD-1.28
_DC_PIN = const(8)
_MOSI_PIN = const(11)
_MISO_PIN = const(0)
_SCLK_PIN = const(10)
_CS_PIN = const(9)
_RESET_PIN = const(12)
_BACKLIGHT_PIN = const(2)
_FREQ = const(40000000)

#### Create Display Interface
spi_bus = SPI.Bus(
    host=1,
    mosi=_MOSI_PIN,
    miso=_MISO_PIN,
    sck=_SCLK_PIN)

display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    dc=_DC_PIN,
    cs=_CS_PIN,
    freq=_FREQ,
)

display = gc9a01.GC9A01(
    data_bus=display_bus,
    display_width=240,
    display_height=240,
    reset_pin=_RESET_PIN,
    reset_state=gc9a01.STATE_LOW,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True
    )