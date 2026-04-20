from tools.SerialRead import SerialRead
from tools.Mandelbrot import Mandelbrot
from tools.Sound import Sound
from tools.Logger import Logger
from tools.AudioSaver import AudioSaver
import signal
import sys

SERIAL_PORT = "/dev/cu.usbmodem113401"
WINDOW_SIZE = 100
REAL_PART = -1.25
MAX_ITERATIONS = 100
SIGNAL_MIN, SIGNAL_MAX = 0, 54
IMAG_MIN, IMAG_MAX = -1.5, 1.5

logger = Logger("plant")
ser = SerialRead(
    serial_port=SERIAL_PORT,
    window_size=WINDOW_SIZE
)
mandelbrot = Mandelbrot(
    real_part=REAL_PART,
    max_iterations=MAX_ITERATIONS,
    signal_min=SIGNAL_MIN,
    signal_max=SIGNAL_MAX,
    imag_min=IMAG_MIN,
    imag_max=IMAG_MAX
)
sound = Sound()
for _ in range(WINDOW_SIZE):
    ser.set_line()
    ser.set_window()

sound.start_recording()
saver = AudioSaver()

running = True

def handle_exit(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handle_exit)

while running:
    ser.set_line()
    ser.set_window()
    ser.set_smoothed()
    electrical_reading = ser.get_smoothed()
    normalized = mandelbrot.transform(electrical_reading)
    sound.play_normalized(normalized)
    logger.debug(f"electrical: {electrical_reading:.2f}  normalized: {normalized:.3f}")

sound.stop()
save = input("\nSave recording? (y/n): ").strip().lower() == 'y'
if save:
    audio = sound.stop_recording()
    saver.save_from_stream(audio, sound.get_sample_rate())