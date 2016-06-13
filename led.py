import time

from RPi import GPIO

import pin

LED_CHANNEL = pin.GPIO19

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_CHANNEL, GPIO.OUT)

while True:
    GPIO.output(LED_CHANNEL, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_CHANNEL, GPIO.LOW)
    time.sleep(0.5)
