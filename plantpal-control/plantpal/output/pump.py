from gpiozero import PWMOutputDevice

FREQUENCY = 100


class Pump(PWMOutputDevice):
    def __init__(self, pin: int):
        super().__init__(pin, frequency=FREQUENCY)
