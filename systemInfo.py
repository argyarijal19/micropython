import gc
import time
import network
import utime as times
import usocket as socket



def get_free_memory():
    return gc.mem_free()

def measure_cpu_load():
    start_time = time.ticks_ms()
    # Lakukan operasi dummy sebagai pengganti pengukuran CPU
    for i in range(1000):
        pass  # operasi sederhana untuk menghabiskan waktu
    end_time = time.ticks_ms()
    return time.ticks_diff(end_time, start_time)