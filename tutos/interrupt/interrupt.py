from machine import Pin
from time import sleep

pin = Pin(5,Pin.IN,Pin.PULL_DOWN)
count = 0
previus = 0

def callback(pin):
    global count
    count+=1

pin.irq(trigger=Pin.IRQ_RISING, handler=callback)
while True:
    if (count > previus):
        print("Interrupt count = ", count)
        previus = count
        sleep(1)
