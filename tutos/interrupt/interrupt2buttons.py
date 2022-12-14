from machine import Pin
from time import sleep
import time

pin1 = Pin(5,Pin.IN,Pin.PULL_DOWN)
pin2 = Pin(6,Pin.IN,Pin.PULL_DOWN)
count1 = 0
previus1 = 0
count2 = 0
previus2 = 0
debounce_time1=0
debounce_time2=0

def callback1(pin):
    global count1
    global debounce_time1 
    if ((time.ticks_ms() - debounce_time1) > 300):
        count1+=1
        debounce_time1 = time.ticks_ms()

def callback2(pin):
    global count2
    global debounce_time2 
    if ((time.ticks_ms() - debounce_time2) > 300):
        count2+=1
        debounce_time2 = time.ticks_ms()


pin1.irq(trigger=Pin.IRQ_RISING, handler=callback1)
pin2.irq(trigger=Pin.IRQ_RISING, handler=callback2)

while True:
    if (count1 > previus1):
        print("Interrupt count1 = ", count1)
        previus1 = count1
    if (count2 > previus2):
        print("Interrupt count2 = ", count2)
        previus2 = count2
    sleep(1)
