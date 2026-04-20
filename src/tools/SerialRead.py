import serial
from collections import deque

class SerialRead:

    def __init__(self, serial_port, band_rate=None, window_size=None):
        self.SERIAL_PORT = serial_port
        self.BAUD_RATE = band_rate or 9600
        self.WINDOW_SIZE = window_size or 10
        self.serial = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE)
        self.window = deque(maxlen=self.WINDOW_SIZE)
        self.line = 0
        self.smoothed = 0

    def set_line(self):
        line = self.serial.readline().decode("utf-8").strip()
        try:
            self.line = float(line)
        except ValueError:
            self.line = None

    def get_line(self):
        return self.line

    def set_window(self):
        line = self.get_line()
        if line is not None:
            self.window.append(line)

    def set_smoothed(self):
        if not self.window:
            return
        self.smoothed = sum(self.window) / len(self.window)
        
    def get_smoothed(self):
        return self.smoothed
