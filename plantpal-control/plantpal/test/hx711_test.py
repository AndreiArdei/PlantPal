import time

from RPi import GPIO

from plantpal.input.spi_devices import HX711

GPIO.setmode(GPIO.BCM)
hx = HX711(pd_sck_pin=24, dout_pin=23)

time.sleep(1)

offset = 49250
scale = 1 / (2 * 295500)

avg = []

# initial = 0
# for _ in range(5):
#     initial = max(initial, hx.read())
#     print("initial: ", initial)
#     time.sleep(1)

while True:
    res = (hx.read() - offset) * scale
    avg.append(res)
    # print(sum(avg) / len(avg))
    print(res)