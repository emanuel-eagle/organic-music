class Mandelbrot:
    def __init__(self, real_part, max_iterations, signal_min, signal_max, imag_min, imag_max):
        self._real_part = real_part
        self._max_iterations = max_iterations
        self._signal_min = signal_min
        self._signal_max = signal_max
        self._imag_min = imag_min
        self._imag_max = imag_max

    def get_max_iterations(self):
        return self._max_iterations

    def get_real_part(self):
        return self._real_part

    def set_real_part(self, value):
        self._real_part = value

    def map_to_imaginary(self, value):
        normalized = (value - self._signal_min) / (self._signal_max - self._signal_min)
        return self._imag_min + normalized * (self._imag_max - self._imag_min)

    def iterate(self, c):
        z = 0
        for i in range(self._max_iterations):
            if abs(z) > 2:
                return i
            z = z*z + c
        return self._max_iterations

    def transform(self, electrical_reading):
        imag = self.map_to_imaginary(electrical_reading)
        c = complex(self._real_part, imag)
        iterations = self.iterate(c)
        return iterations / self._max_iterations