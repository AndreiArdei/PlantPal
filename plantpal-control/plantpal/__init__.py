import os
import sqlite3
from contextlib import closing

from plantpal.input.flow_sensor import FlowSensor
from plantpal.input.i2c_devices import AM2320
from plantpal.input.serial_devices import SerialStream, SerialDevice
from plantpal.input.spi_devices import HX711
from plantpal.output.pump import Pump

DB_NAME = os.getenv("PLANTPAL_DB", "../identifier.sqlite")
if not os.path.isfile(DB_NAME):
    exit("Cannot find DB")
COM_PORT = "/dev/ttyUSB0"
