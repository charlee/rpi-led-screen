LED Screen controller on Raspberry Pi Pico
==========================================


This is a program running on Raspberry Pi Pico to control the LED Matrix screen.

## Prerequisites

- [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) 8.1.0 or later (tested only on 8.1.0)
- [CircuitPython libraries](https://circuitpython.org/libraries).

This program requires the `adafruit_max7219` library.


`boot.py`

Enables the USB data port and disables the USB storage and USB midi.


`code.py`

The main program.

This program simply reads data from USB data port and sends it to the LED Matrix screen. All the data is sent as is, without any processing.
The Python script running on a computer (see `win32` folder) is responsible for sending the data in the correct format.
