from machine import ADC, Pin

adc = ADC(Pin(33))
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def battery_log():
    adc.width(ADC.WIDTH_12BIT)
    adc.atten(ADC.ATTN_11DB)
    anlog_value = adc.read()
    return map_value(anlog_value, 0.0, 4095.0, 0, 100)

    
    