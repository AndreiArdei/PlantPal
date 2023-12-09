import threading
import time

from gpiozero import Device
import serial


class SerialStream:
    def __init__(self, port, baudrate=9600):
        self._serial = serial.Serial(port, baudrate)
        self._data = {}
        self._closed = False

    @property
    def closed(self):
        return self._serial is None

    def open(self):
        def inf_read():
            while not self._closed:
                self.read()

        threading.Thread(target=inf_read, daemon=True).start()

    def close(self):
        self._serial.close()
        self._closed = True

    def read(self):
        try:
            sensor, value = self._serial.readline().strip().decode().strip().split(":")
            self._data[int(sensor)] = float(value)
        except UnicodeDecodeError:
            print("decode error")
            self._serial.readall()
        except ValueError:
            print("value error")

    def get(self, sensor: int) -> float:
        while sensor not in self._data:
            time.sleep(0.1)
        return self._data[sensor]


class SerialDevice(Device):
    def __init__(self, sensor_id: int, stream: SerialStream):
        self._sensor_id = sensor_id
        self._stream = stream
        super().__init__()

    @property
    def value(self):
        return self._stream.get(self._sensor_id)

    @property
    def closed(self):
        return self._stream.closed

    def close(self):
        self._stream.close()
