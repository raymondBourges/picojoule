from machine import Pin, ADC
from time import sleep

potar = ADC(27)
u2v = 3.3 / 65535
while True:
    print("%1.2f" % (potar.read_u16() * u2v), " volts")
    sleep(1)