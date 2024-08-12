# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine
from led_controller import led_on


RESET_FLAG_FILE = "reset.flag"
led_on()
if RESET_FLAG_FILE not in os.listdir():
    # Create the reset flag file
    with open(RESET_FLAG_FILE, 'w') as f:
        f.write('')

    # Perform a reset
    print("Performing reset...")
    machine.reset()
else:
    # Remove the reset flag file for next run
    os.remove(RESET_FLAG_FILE)
    try:
        import main
    except ImportError:
        print("main.py not found")