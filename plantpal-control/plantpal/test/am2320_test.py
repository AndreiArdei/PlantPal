import time

from plantpal.input.i2c_devices import AM2320, I2CDevice

am2320 = AM2320()
time.sleep(1)

try:
    hum, temp = I2CDevice.retry(am2320.read_values, n=5)
    print(f"Hum: {hum}, Temp: {temp}")
finally:
    am2320.close()
