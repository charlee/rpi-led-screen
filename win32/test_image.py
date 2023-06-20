# Test image
# Use this script to test the LED screen
# Modify the COM port

import numpy as np
import serial
from byteorder import get_byte_index_offset

# Define the characters as binary patterns
characters = {
    '0': '0x1E2121212121211E',
    '1': '0x040C140404041F',
    '2': '0x1E2101020408101F',
    '3': '0x1E21010E0101211E',
    '4': '0x02060A121F020202',
    '5': '0x1F20201E0101211E',
    '6': '0x0608101E2121211E',
    '7': '0x1F01020408102020',
    '8': '0x1E21211E2121211E',
    '9': '0x1E21211F0101021C',
    'A': '0x1E21213F21212121',
    'B': '0x3E21213E2121213E',
    'C': '0x1E2120202020211E',
    'D': '0x3E2121212121213E',
    'E': '0x3F20203E2020203F',
    'F': '0x3F20203E20202020',
    'G': '0x1E2120202321211E',
    'H': '0x2121213F21212121',
    'I': '0x1F08080808081F',
    'J': '0x0E04040424242418',
}

LEDSCREEN_W = 40
LEDSCREEN_H = 32

# Create an empty 2D array for the image
image = np.zeros((LEDSCREEN_H, LEDSCREEN_W), dtype=int)

# Divide the image into cells
cell_width = 8
cell_height = 8

# Iterate over each cell and assign the corresponding character pattern
char_index = 0
for i in range(4):
    for j in range(5):
        cell = image[i * cell_width: (i + 1) * cell_width, j * cell_height: (j + 1) * cell_height]
        character = list(characters.keys())[char_index]
        pattern_hex = characters[character]
        pattern_bin = bin(int(pattern_hex, 16))[2:].zfill(64)
        pattern_2d = np.array([list(pattern_bin[i:i+8]) for i in range(0, 64, 8)], dtype=int)
        cell[:8, :8] = pattern_2d
        char_index += 1


# Print the resulting image, pixel by pixel
for y in range(LEDSCREEN_H):
    for x in range(LEDSCREEN_W):
        value = image[y][x]
        print(value and '.' or ' ', end='')
    print()

serial = serial.Serial('COM7', 115200, timeout=1)

size = LEDSCREEN_W * LEDSCREEN_H // 8
bytes = bytearray(size)
for y in range(LEDSCREEN_H):
    for x in range(0, LEDSCREEN_W):
        if image[y][x] == 0:
            bit = 0
        else:
            bit = 1
        index, offset = get_byte_index_offset(x, y)
        bytes[index] |= bit << offset
        
serial.write(bytes)
    