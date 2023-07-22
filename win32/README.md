RPi LED Screen Windows Player
==============================



This is the Windows player part for the RPi LED Screen.
Specified video file will be played and mapped to the screen.

`byteorder.py`: A helper module to convert the (x, y) cooridinate to the byte index and offset used by the LED matrix.


`play.py`: The main program.

`test_image.py`: A helper program to test the LED screen. It displays a letter on each LED module to test if the byte order is correct.


## Requirements

- Python 3.10 or later
- `opencv-python`: for converting the video frames to the LED screen format
- `dxcam`: for capturing the video frames from YouTube video
- `webview`: for creating a window to play the YouTube video
- `pyserial`: for sending data to the LED screen via USB

## Usage

```
# List available COM ports
python play.py -l

# Play the video  on the LED screen (replace COM3 with correct COM port)
python play.py -u https://www.youtube.com/watch?v=FtutLA63Cp8 -p COM3

# Play the video without sending it to the LED screen. Used for testing the video player
python play.py -u https://www.youtube.com/watch?v=FtutLA63Cp8

```
