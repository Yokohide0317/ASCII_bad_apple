from PIL import Image
import argparse
import os
import time
import cv2
from tqdm import tqdm


ASCII_CHARS = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

def scale_image(image, new_width, new_height):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    if new_height == 0:
        new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=3.69):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_height_width):
    new_height = new_height_width[1]
    new_width = new_height_width[0]
    image = scale_image(image, new_width, new_height)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(_image_filepath, _new_height_width):
    image = None
    try:
        image = Image.open(_image_filepath)
    except:
        print("Unable to open image file {image_filepath}.".format(image_filepath=image_filepath))
        return
    image_ascii = convert_image_to_ascii(image, _new_height_width)
    return image_ascii

def get_video_prop(_mp4_file):
    vidcap = cv2.VideoCapture(_mp4_file)
    video_frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT) # Get Num of Frame
    video_fps = vidcap.get(cv2.CAP_PROP_FPS)                 # Get Frame Rate
    video_length = video_frame_count / video_fps # Get Length of Video

    return vidcap, video_length

def set_frame_size(size):
    size_dict = {
        "small": [50, 15],
        "medium": [100, 30],
        "large": [150, 45],
        "xlarge": [200, 60]
    }
    height_width = size_dict[size]
    return height_width

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-s', '--size', default="medium", choices=["small", "medium", "large", "xlarge"])

    args = parser.parse_args()
    input_path = args.input
    txt_file = os.path.join(input_path, "play.txt")
    mp4_file = os.path.join(input_path, "video.mp4")
    jpg_file = os.path.join(input_path, "output.jpg")

    time_count = 0
    frames = []
    vidcap, video_length, = get_video_prop(mp4_file)
    total = int(video_length*1000)

    new_height_width = set_frame_size(args.size)

    pbar = tqdm(total=total)
    while time_count <= total:
        vidcap.set(0, time_count)
        success, image = vidcap.read()
        if success:
            cv2.imwrite(jpg_file, image)
        frames.append(handle_image_conversion(jpg_file, new_height_width))
        time_count = time_count + 100
        pbar.update(100)
    pbar.close()

    f = open(txt_file, 'w')
    f.write('SPLIT'.join(frames))
    f.close()

