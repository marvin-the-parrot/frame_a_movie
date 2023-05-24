import ffmpeg
import numpy as np
from PIL import Image


def extract_frames(video_path, interval):
    frames = []

    # Open the video file
    probe = ffmpeg.probe(video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        raise ValueError("No video stream found in the input file.")

    # Extract frames
    out, _ = (
        ffmpeg.input(video_path)
            # .filter("select", "not(mod(n,120))")
            .filter("fps", "0.1")
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True)
    )

    # Convert the output to a numpy array
    width = video_stream['width']
    height = video_stream['height']
    frames = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])

    return frames


def calculate_average_color(image):
    # Convert image to PIL format if using OpenCV
    # image_pil = Image.fromarray(image)

    # Calculate average color
    average_color = np.mean(image, axis=(0, 1)).astype(int)

    return average_color


def main():
    video_path = 'files/the_matrix.mp4'
    frames = extract_frames(video_path, 10)

    average_colors = []
    for frame in frames:
        average_color = calculate_average_color(frame)
        average_colors.append(average_color)

    # create an image that has the average colors along the width
    width = len(average_colors)
    height = 100
    image = Image.new('RGB', (width, height))
    for x in range(width):
        for y in range(height):
            image.putpixel((x, y), tuple(average_colors[x]))

    image.save('files/average_colors.png',interpolation='None')
    print('Image saved to files/average_colors.png')


if __name__ == '__main__':
    main()
