import time
import sys
import threading
import cv2
import webview
import dxcam
import argparse
from urllib.parse import urlparse, parse_qs
import serial.tools.list_ports


UI_TITLE_HEIGHT = 32

LEDSCREEN_W = 40
LEDSCREEN_H = 32


class YouTubePlayer:

    def __init__(self):
        self.window_x = 0
        self.window_y = 0
        self.window_w = 640
        self.window_h = 480
        self.video_loaded = False
        self.window_closed = False

        self.camera = None
        self.port = None
        
        self.lock = threading.Lock()
        
    def init_serial(self):
        '''
        Initialize serial port
        '''
        if not self.port:
            raise Exception('COM port not specified')

        self.serial = serial.Serial(self.port, 115200, timeout=1)
        print(f'Serial port initialized: {self.serial.name}')
        
    def send_bytes(self, bytes: bytearray):
        '''
        Send bytes to the serial port
        '''
        if not self.serial:
            raise Exception('Serial port not initialized')
        
        self.serial.write(bytes)


    def process_frame(self, frame):
        # gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # resize to the best w, h
        frame = cv2.resize(frame, (LEDSCREEN_W, LEDSCREEN_H))

        # threshold
        _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        
        return frame
    
    def send_frame_to_ledscreen(self, frame):
        '''
        Send frame to LED screen
        '''
        # convert to bytes
        bytes = bytearray()
        for y in range(LEDSCREEN_H):
            for x in range(0, LEDSCREEN_W, 8):
                byte = 0
                for i in range(8):
                    if frame[y][x + i] > 0:
                        byte |= 1 << i
                bytes.append(byte)
        
        self.send_bytes(bytes)

    
    def restart_capturing(self):
        '''
        Restarts capturing with the new window region.
        '''
        if not self.camera:
            return
        
        # since this func may be called in the event, need to use lock to prevent camera being read
        self.lock.acquire()

        if self.camera.is_capturing:
            self.camera.stop()

        region = (self.window_x, self.window_y + UI_TITLE_HEIGHT, self.window_x + self.window_w, self.window_y + self.window_h + UI_TITLE_HEIGHT)
        self.camera.start(region=region, target_fps=30)

        self.lock.release()


    def handle_video(self, window):
        
        self.init_serial()
        self.camera = dxcam.create(output_color="BGR")
        
        # wait for window to be moved
        while not self.video_loaded:
            time.sleep(0.1)
        
        
        # start a cv2 window to show the captured preview
        cv2.namedWindow('preview', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('preview', self.window_w, self.window_h)
        
        # start capturing
        # acquire lock to prevent camera being restarted
        self.restart_capturing()
        while not self.window_closed:

            # capture one frame
            self.lock.acquire()
            frame = self.camera.get_latest_frame()
            if frame is None:
                continue
            self.lock.release()
            
            # process frame
            frame = self.process_frame(frame)
            
            # send to screen
            self.send_frame_to_ledscreen(frame)

            # show preview
            cv2.imshow('preview', frame)
            cv2.waitKey(1)
            
        self.camera.stop()
        del self.camera

        cv2.destroyAllWindows()
        
        if self.serial:
            self.serial.close()


    def play(self):
        # parse video url. Specify -p for com ports, specify -l to list available com ports
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', help='YouTube video URL', required=False)
        parser.add_argument('-p', '--port', help='COM port', required=False)
        parser.add_argument('-l', '--list', action='store_true', help='List available COM ports', required=False)
        args = parser.parse_args()
        
        if args.list:
            ports = serial.tools.list_ports.comports()
            for port in ports:
                print(f'{port.device}: {port.description}')
            exit(0)
            
        if not args.url or not args.port:
            # show error message to STDERR
            print('Please specify YouTube video URL and COM port', file=sys.stderr)
            parser.print_help()
            exit(0)
            
        # verify port name
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports]
        if args.port not in port_names:
            print(f'Invalid COM port: {args.port}', file=sys.stderr)
            exit(0)

        url = args.url
        self.port = args.port
        
        # parse video id using urlparse
        url_data = urlparse(url)
        query = parse_qs(url_data.query)
        video_id = query["v"][0]

        # generate embed url
        url = 'https://www.youtube.com/embed/{}?autoplay=1&rel=0'.format(video_id)
        
        # generate a webpage that contains the above url
        html = '''
<html>
<body style="margin:0px;padding:0px;overflow:hidden">
  <iframe src="{}" frameborder="0" allowfullscreen style="overflow:hidden;height:100%;width:100%" height="100%" width="100%"></iframe>
  </div>
</body>
</html>
'''.format(url)

        # event callbacks
        def on_loaded():
            self.video_loaded = True

        def on_moved(x, y):
            self.window_x = x
            self.window_y = y
            self.restart_capturing()
            
        def on_closed():
            self.window_closed = True
            print('Window closed')
            
        def handle_play(window):
            self.handle_video(window)

        # create window
        window = webview.create_window('YouTube Player', html=html, width=640, height=480 + UI_TITLE_HEIGHT, resizable=False, fullscreen=False)
        window.events.loaded += on_loaded
        window.events.moved += on_moved
        window.events.closed += on_closed
        webview.start(handle_play, window)


if __name__ == '__main__':
    player = YouTubePlayer()
    player.play()