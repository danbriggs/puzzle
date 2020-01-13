import cv2
import numpy as np
from matplotlib import pyplot as plt


def color_histogram(filename, smoothing):
    """Creates a histogram of how often each color shows up in the image at filename.
    smoothing indicates how far away in color space to look from a given color.
    smoothing should be a nonnegative integer.
    answers[r,g,b] should count how many pixels in the image at filename
    have colors from a (2*smoothing+1)^3 cube in color space centered at [r,g,b].
    Try to accomplish this using numpy matrix arithmetic rather than for loops!"""
    img_pre = cv2.imread(filename)
    img = cv2.cvtColor(img_pre, cv2.COLOR_BGR2RGB)
    answers = np.zeros((256, 256, 256))
    height = img.shape[0]
    width = img.shape[1]
    for y in range(height):
        for x in range(width):
            answers[img[y, x][0], img[y, x][1], img[y, x][2]] += 1
    return answers


def main():
    filename = input('Filename of image:')
    answers = color_histogram(filename, 1)
    print(type(answers))
    print(answers.shape)
    number0 = 0
    number1 = 0
    number2 = 0
    while number0 >= 0:
        number0 = int(input('Red value:'))
        number1 = int(input('Green value:'))
        number2 = int(input('Blue value:'))
        print('Frequency:', answers[number0, number1, number2])


if __name__ == '__main__':
    main()