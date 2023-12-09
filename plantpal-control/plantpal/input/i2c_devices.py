import time

from gpiozero import Device
from smbus import SMBus

I2C_MESSAGE_OFFSET = 4


class I2CDevice(Device):

    def __init__(self, bus, address):
        self._bus = SMBus(bus)
        self._address = address
        super(I2CDevice, self).__init__()

    def close(self):
        if self._bus is not None:
            self._bus.close()
            # Are you stupid PyCharm?
            # noinspection PyAttributeOutsideInit
            self._bus = None

        super(I2CDevice, self).close()

    @property
    def closed(self):
        return self._bus is None

    @property
    def value(self):
        raise RuntimeError("Cannot read I2C value")

    def _read(self, register: int, length: int) -> list[int]:
        data = self._bus.read_i2c_block_data(self._address, register, length + I2C_MESSAGE_OFFSET)
        crc_1 = self._crc16(data[0:-2])
        crc_2 = (data[-1] << 8) | data[-2]

        if crc_1 != crc_2:
            raise RuntimeError(f"CRC failure 0x{crc_1:04X} vs 0x{crc_2:04X}")

        return data[2:-2]

    def _write(self, register: int, data: list[int]):
        self._bus.write_i2c_block_data(self._address, register, data)

    def _wake_up(self):
        try:
            self._write(0, [0])
        except OSError:
            pass

    @staticmethod
    def _crc16(data):
        crc = 0xFFFF
        for x in data:
            crc ^= x
            for i in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xa001
                else:
                    crc >>= 1
        return crc

    @staticmethod
    def retry(func, n=3, delay=0.1):
        cause = None
        for _ in range(n):
            try:
                return func()
            except OSError as e:
                if e is not None:
                    cause = e
            except RuntimeError as e:
                cause = e

            time.sleep(delay)

        if cause is None:
            raise RuntimeError("Unexpected")

        print("Failed after retry")
        raise cause




AM2320_ADDRESS = 0x5C
AM2320_REG_READ = 0x03
AM2320_REG_TEMP_H = 0x04
AM2320_REG_HUM_H = 0x00


class AM2320(I2CDevice):

    def __init__(self, bus=1, address=AM2320_ADDRESS):
        super().__init__(bus, address)

    def read_values(self) -> (float, float):
        self._wake_up()
        time.sleep(0.01)

        # Request data
        self._write(AM2320_REG_READ, [AM2320_REG_HUM_H, AM2320_REG_TEMP_H])
        time.sleep(0.002)

        # Read data
        data = self._read(0, 4)
        time.sleep(0.1)

        humidity = ((data[0] << 8) | data[1]) / 10.0
        temperature = ((data[2] << 8) | data[3]) / 10.0

        return humidity, temperature

    @property
    def humidity(self) -> float:
        """The measured relative humidity in percent."""
        return self.read_values()[0]

    @property
    def temperature(self) -> float:
        """The measured temperature in Celsius."""
        return self.read_values()[1]
