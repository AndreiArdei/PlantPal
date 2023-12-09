import sqlite3
import threading
import time
from contextlib import closing

from plantpal import FlowSensor, AM2320, HX711, SerialDevice, SerialStream, Pump, COM_PORT, DB_NAME

# Actuators
pump = Pump(13)

# Analog sensors
serial_stream = SerialStream(COM_PORT)
serial_stream.open()

ldr = SerialDevice(0, serial_stream)
soil_moisture_sensor = SerialDevice(1, serial_stream)

# Digital sensors
flow_sensor = FlowSensor(26, 90)
am2320 = AM2320()
hx = HX711(pd_sck_pin=24, dout_pin=23, offset=49250, scale=1 / 591000)

SENSORS = {
    # "LDR": ldr,
    # "Moisture": soil_moisture_sensor,
    "Flow": flow_sensor,
    # "Temp": am2320,
    "LoadCell": hx
}

db = None


def read_sensors_loop():
    global db
    db = sqlite3.connect(DB_NAME)

    while True:
        values = read_sensors()
        sensor_update(values)
        time.sleep(0.5)


def read_sensors():
    values = {}

    for name, sensor in SENSORS.items():
        cur = db.cursor()
        print("Measuring ", name)
        value = sensor.value
        cur.execute(
            """
            INSERT INTO 
                SensorData(MeasuredAt, PlantPalID, Data, SensorName) 
            VALUES (strftime('%s', 'now'), 1, ?, ?)
            """, (value, name))
        values[name] = value

    db.commit()
    return values


def sensor_update(values):
    print(values)


read_thread = threading.Thread(target=read_sensors_loop)
read_thread.start()
read_thread.join()
