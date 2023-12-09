from plantpal.input.serial_devices import SerialDevice, SerialStream

COM_PORT = "/dev/ttyUSB0"

serial_stream = SerialStream(COM_PORT)
serial_stream.open()

ldr = SerialDevice(0, serial_stream)
soil_moisture_sensor = SerialDevice(1, serial_stream)

while True:
    print(f"moisture: {soil_moisture_sensor.value}, ldr: {ldr.value}")
