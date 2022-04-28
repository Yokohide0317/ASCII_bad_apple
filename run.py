import time, os
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)

    args = parser.parse_args()
    input_path = args.input
    txt_file = os.path.join(input_path, "play.txt")
    mp4_file = os.path.join(input_path, "video.mp4")
    with open(txt_file, 'r') as f:
        frame_raw = f.read()
        frame_raw = frame_raw.replace('.', ' ')
	#f.close()
    frames = frame_raw.split('SPLIT')
	#os.system(f'mplayer -vo null -vc null ${mp4_file} &')
    init_time = time.time()
    while time.time() <= init_time + 218:
        os.system('clear')
        print(frames[int((time.time()-init_time)*10)])
        time.sleep(0.05)

