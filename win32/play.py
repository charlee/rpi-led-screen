import time
import threading
import cv2
import webview
import dxcam
import argparse
from urllib.parse import urlparse, parse_qs


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
        
        self.lock = threading.Lock()

    def process_frame(self, frame):
        # gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # resize to the best w, h
        frame = cv2.resize(frame, (LEDSCREEN_W, LEDSCREEN_H))

        # threshold
        _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
        
        return frame
    
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

            # show preview
            cv2.imshow('preview', frame)
            cv2.waitKey(1)
            
        self.camera.stop()
        del self.camera

        cv2.destroyAllWindows()
      


    def play(self):
        # parse video url
        parser = argparse.ArgumentParser()
        parser.add_argument('url', help='YouTube video URL')
        args = parser.parse_args()
        
        # parse video id using urlparse
        url_data = urlparse(args.url)
        query = parse_qs(url_data.query)
        video_id = query["v"][0]

        # generate embed url
        url = 'https://www.youtube.com/embed/{}?autoplay=1&controls=0&rel=0'.format(video_id)
        
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