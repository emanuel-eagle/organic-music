# organic-music

A plant talks. This listens.

`organic-music` is a live audio instrument that reads weak bioelectrical signals from a houseplant, passes them through a Mandelbrot set transformation, and generates a continuous tone in real time. The pitch drifts slowly as the plant's electrical state changes — part generative music, part science experiment, part something harder to name.

Recordings are saved as `.wav` files to `./samples` and can be shared anywhere audio files work.

---

## How it works

A pair of electrodes (alligator clips) sit in the soil and on a leaf of a houseplant. The voltage difference between them — tiny, on the order of millivolts — is picked up by an INA128PA instrumentation amplifier and passed to an Arduino Uno, which reads it on an analog pin and streams values over USB to a Mac.

A Python script reads that stream, smooths it with a rolling average, and maps it into the Mandelbrot set: the voltage controls the imaginary part of the complex number C, while the real part is fixed at a point on the boundary of the set. The number of iterations before the sequence escapes determines a normalized 0–1 value, which maps to a frequency between 200 and 2000 Hz.

That frequency feeds a continuous audio stream playing through whatever output device you have connected. The tone never stops — it just slowly shifts.

---

## Hardware

- Arduino Uno
- INA128PA instrumentation amplifier (DIP-8)
- Breadboard
- 2x alligator clip leads
- Jumper wires
- A resistor between ~50–500 ohms (for amplifier gain — see below)
- A houseplant

### Wiring

The INA128PA sits straddled across the center of the breadboard. With pin 1 at e11:

```
Pin 1 (RG)   → e11   — one leg of gain resistor
Pin 2 (IN−)  → e12   — black alligator clip (soil)
Pin 3 (IN+)  → e13   — red alligator clip (leaf)
Pin 4 (V−)   → e14   — jumper to negative rail (GND)
Pin 5 (REF)  → f14   — jumper to negative rail (GND)
Pin 6 (OUT)  → f13   — jumper to Arduino A0
Pin 7 (V+)   → f12   — jumper to positive rail (5V)
Pin 8 (RG)   → f11   — other leg of gain resistor
```

Positive rail → Arduino 5V  
Negative rail → Arduino GND

### Setting the gain

The resistor between pins 1 and 8 sets how much the amp multiplifies the plant signal. The formula is:

**Gain = 1 + (50,000 / resistor in ohms)**

A 470 ohm resistor gives about 100x gain, which is a good starting point. Too little gain and the signal is too weak to be interesting. Too much and it clips or saturates. Swap resistors and watch the Serial Plotter to tune it.

### Electrodes

- Red clip → somewhere on a leaf
- Black clip → into the soil near the roots

Keep the wires short. Move the breadboard away from your computer if you pick up a strong 60 Hz sawtooth pattern — that's mains electrical noise from the wall outlets, not the plant.

---

## Software setup

You'll need Python (via Homebrew works fine) and the Arduino IDE or VSCode with the Arduino extension.

### Arduino sketch

Upload this to the Uno:

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  int signal = analogRead(A0);
  Serial.println(signal);
  delay(10);
}
```

Note the port name shown in the Serial Plotter title bar — you'll need it below (something like `/dev/cu.usbmodem113401`).

### Python dependencies

```
pyserial
numpy
sounddevice
soundfile
```

Install with:

```bash
pip install -r requirements.txt
```

### Configuration

Open `src/main.py` and set your serial port:

```python
SERIAL_PORT = "/dev/cu.usbmodem113401"  # replace with your port
```

You can also tune these to taste:

```python
WINDOW_SIZE = 50       # higher = slower, smoother frequency changes
REAL_PART = -1.25      # fixed real part of C in the Mandelbrot set
SIGNAL_MIN = 0         # expected minimum analog reading
SIGNAL_MAX = 54        # expected maximum analog reading
```

---

## Running it

```bash
python3 src/main.py
```

The script will warm up silently for a moment while it fills the signal window, then the tone will begin. Let it run as long as you like — the plant will do what it does.

Press `Ctrl+C` to stop. You'll be asked if you want to save the session as a `.wav` file. If you say yes, it gets written to `./samples/plant_TIMESTAMP.wav`.

---

## Project structure

```
organic-music/
├── src/
│   ├── main.py
│   └── tools/
│       ├── SerialRead.py     # reads and smooths Arduino serial data
│       ├── Mandelbrot.py     # maps signal to iteration count
│       ├── Sound.py          # continuous audio stream
│       ├── AudioSaver.py     # saves stream to .wav
│       └── Logger.py         # logging wrapper
├── samples/                  # saved recordings land here
└── requirements.txt
```

---

## Notes

The signal you're reading is real but noisy. Environmental electrical interference from nearby computers and power cables will show up — a perfectly regular sawtooth wave at 60 Hz is mains noise, not the plant. The rolling average in `SerialRead` smooths most of this out, but moving the setup away from other electronics helps.

The Mandelbrot boundary at `REAL_PART = -1.25` produces wildly varying iteration counts for small changes in the imaginary axis, which is what makes the mapping interesting. Points deep inside the set always return the maximum iteration count (no variation), and points far outside escape immediately (also no variation). The interesting music lives on the edge.

Recordings sound best when the window size is high enough that the frequency drifts slowly — somewhere between 50 and 200 readings. Sessions of 10+ minutes start to develop an almost meditative quality as the plant settles.