import os
from machine import Pin, SPI

spi = SPI(2, baudrate=10000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5, Pin.OUT)

def try_mount_sd():
    try:
        sd = sdcard.SDCard(spi, cs)
        vfs = os.VfsFat(sd)
        os.mount(vfs, "/sd")
        print("Mounting berhasil. SD card terdeteksi.")
    except OSError as e:
        if e.args[0] == 19:
            print("Tidak dapat melakukan mounting. SD card tidak ditemukan.")
        else:
            print("Error:", e)

