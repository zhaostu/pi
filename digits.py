import time

from RPi import GPIO

import pin

# Pin order is from top segment, running clockwise, then the center last.
segment_channels = (
    pin.GPIO20,
    pin.GPIO21,
    pin.GPIO19,
    pin.GPIO13,
    pin.GPIO06,
    pin.GPIO16,
    pin.GPIO7,
)

dp_channel = pin.GPIO26
btn_channel = pin.GPIO12

digits = (
    0x3f, 0x06, 0x5b, 0x4f,
    0x66, 0x6d, 0x7d, 0x07,
    0x7f, 0x6f, 0x77, 0x7c,
    0x39, 0x5e, 0x79, 0x71,
)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(segment_channels, GPIO.OUT)
GPIO.setup(dp_channel, GPIO.OUT)
GPIO.setup(btn_channel, GPIO.IN)

def display(n):
    d = digits[n]
    for i in range(7):
        GPIO.output(segment_channels[i], GPIO.LOW if d & 1 else GPIO.HIGH)
        d >>= 1
    GPIO.output(dp_channel, GPIO.LOW if n % 3 == 0 else GPIO.HIGH)

def wait_for_btn():
    while GPIO.input(btn_channel) == 1:
        time.sleep(0.01)
    while GPIO.input(btn_channel) == 0:
        time.sleep(0.01)

def main():
    try:
        number = 0
        while True:
            display(number)
            wait_for_btn()
            number = (number + 1) % 16
            print('Button clicked, increasing number to {}.'.format(number))
    except:
        GPIO.cleanup(segment_channels)
        GPIO.cleanup(dp_channel)
        GPIO.cleanup(btn_channel)
    
if __name__ == '__main__':
    main()
