import time

from plantpal.input.flow_sensor import FlowSensor
from plantpal.output.pump import Pump

pump = Pump(14)
# sensor = FlowSensor(15, 90)

while True:
    pump.value = 1
# while True:
#     print(sensor.value)
# while True:
#     pump.value = value
#     value += 0.1
#     value %= 1
#     print(value)
#     time.sleep(0.5)
