from machine import Pin
import time

# Onboard-LED Pin
led = Pin(25, Pin.OUT)

while True:
    led.toggle()        # LED umschalten
    time.sleep(0.5)     # 0,5 Sekunden warten
