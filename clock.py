import time
import datetime
import threading
import queue

from RPi import GPIO

import pin

# Pin order is from top segment, running clockwise, then the center last.
segment_channels = (
    pin.GPIO18,
    pin.GPIO24,
    pin.GPIO27,
    pin.GPIO17,
    pin.GPIO4,
    pin.GPIO23,
    pin.GPIO5,
)

digit_channels = (
    pin.GPIO12,
    pin.GPIO16,
    pin.GPIO20,
    pin.GPIO26,
)

digits = (
    0x3f, 0x06, 0x5b, 0x4f,
    0x66, 0x6d, 0x7d, 0x07,
    0x7f, 0x6f, 0x77, 0x7c,
    0x39, 0x5e, 0x79, 0x71,
)

time_queue = queue.Queue()

def display(dig, n):
    prev_dig = (dig - 1) % 4
    GPIO.output(digit_channels[prev_dig], GPIO.LOW)

    d = digits[n]
    for i in range(7):
        GPIO.output(segment_channels[i], GPIO.LOW if d & 1 else GPIO.HIGH)
        d >>= 1

    GPIO.output(digit_channels[dig], GPIO.HIGH)

def get_time_digits():
    now = datetime.datetime.now()
    hour = now.hour % 12
    minute = now.minute
    return (hour // 10, hour % 10, minute // 10, minute % 10)

def update_time():
    prev_time_digits = None
    while True:
        time_digits = get_time_digits()
        if time_digits != prev_time_digits:
            time_queue.put(time_digits)
            prev_time_digits = time_digits
        time.sleep(0.5)

def main():
    digit = 0
    timer_thread = threading.Thread(target=update_time, daemon=True)
    timer_thread.start()
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(segment_channels, GPIO.OUT)
        GPIO.setup(digit_channels, GPIO.OUT)

        numbers = time_queue.get()

        while True:
            if digit == 0 and not time_queue.empty():
                # Check whether time changed.
                numbers = time_queue.get()
            display(digit, numbers[digit])
            digit = (digit + 1) % 4
            time.sleep(0.005)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup(segment_channels)
        GPIO.cleanup(digit_channels)
    
if __name__ == '__main__':
    main()
