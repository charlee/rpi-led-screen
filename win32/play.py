import argparse



def main():
    
    # parse arguments
    # the program should take only one positional argument: the video file
    parser = argparse.ArgumentParser(description='Play a video file.')
    parser.add_argument('video_file', metavar='video_file', type=str, help='the video file to play')
    args = parser.parse_args()

    print(args.video_file)
    

if __name__ == '__main__':
    main()