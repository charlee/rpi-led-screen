import webview
import argparse
from urllib.parse import urlparse, parse_qs


def handle_video():
    pass


def main():
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

    # create window
    window = webview.create_window('YouTube Player', html=html, width=640, height=480, resizable=False, fullscreen=False)
    webview.start(handle_video, window)


if __name__ == '__main__':
    main()