import time

from gpiozero import DigitalInputDevice, HoldMixin


class FlowSensor(HoldMixin, DigitalInputDevice):
    def __init__(self, pin, liter=5880.0):
        self._liter = liter
        self._pulse = 0
        self.when_activated = self._on_pulse
        self._count_pulse = False
        super(FlowSensor, self).__init__(pin)

    def _on_pulse(self):
        if not self._count_pulse:
            return

        self._pulse += 1

    @property
    def value(self):
        return self.read()

    def read(self, delay=1):
        self._pulse = 0
        self._count_pulse = True
        time.sleep(delay)
        self._count_pulse = False

        flow_rate = self._pulse / 5880  # L/s
        flow_rate *= 1000  # mL/min
        flow_rate *= 60  # mL/min

        # flow_rate = self._pulse * 2.25
        # flow_rate /= 10  # divide by 10 for reasons
        # flow_rate *= 60  # mL/min

        return flow_rate
