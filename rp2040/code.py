import usb_cdc
import time
import board
import busio
import digitalio
from adafruit_max7219.matrices import CustomMatrix

LED_SCREEN_WIDTH = 40
LED_SCREEN_HEIGHT = 32

serial = usb_cdc.data
spi = busio.SPI(board.GP2, MOSI=board.GP3)
screen = CustomMatrix(
    width=LED_SCREEN_WIDTH * LED_SCREEN_HEIGHT // 8,
    height=8,
    spi=spi,
    cs=digitalio.DigitalInOut(board.GP5),
)

def show_ready():
    screen.fill(0)
    screen.text('READY', 5, 0)
    screen.show()


data_size = LED_SCREEN_WIDTH * LED_SCREEN_HEIGHT // 8
data = bytearray([0] * data_size)
p = 0

print('Started, waiting for data')
show_ready()

frame_count = 0
ts_start = time.monotonic()
last_ts = 0

while True:
    if serial.in_waiting > 0:
        buf = serial.read(data_size)
        screen._buffer = buf
        screen.show()
        frame_count += 1
        ts = time.monotonic()
        
        # print fps every second
        if ts - last_ts >= 1:
            print(f'fps = {frame_count / (ts - ts_start)}')
            last_ts = ts
    
    else:
        time.sleep(0.01)
    

