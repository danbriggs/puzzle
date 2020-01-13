import numpy as np
import cv2
from matplotlib import pyplot as plt

def get_sobels(im0):
    """im0 should be a 2D numpy array of numbers
    (i.e., a grayscale image).
    returns the sobel y, sobel x, and sobel of im0."""
    sobelx = cv2.Sobel(im0,cv2.CV_64F,1,0,ksize=5)
    sobely = cv2.Sobel(im0,cv2.CV_64F,0,1,ksize=5)
    sobel = (sobelx*sobelx + sobely*sobely)**.5
    return sobely, sobelx, sobel

def make_color_sobels(filename,whether_to_display):
    """Computes the result of a 3-channel Sobel filter for the image at filename.
    Returns scaled_color_sobel_y, scaled_color_sobel_x, and scaled_color_sobel.
    Displays it if whether_to_display is True."""
    image = cv2.imread(filename)
    image_grayscale = cv2.imread(filename,0)
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print('image[0,0].shape: ',image[0,0].shape)
    print('image[0,0]: ',image[0,0])
    red_channel = image[:,:,0]
    green_channel = image[:,:,1]
    blue_channel = image[:,:,2]
    print('red_channel[0,0]: ',red_channel[0,0])

    red_sobels = get_sobels(red_channel)
    green_sobels = get_sobels(green_channel)
    blue_sobels = get_sobels(blue_channel)
    red_sobel_y = red_sobels[0]
    green_sobel_y = green_sobels[0]
    blue_sobel_y = blue_sobels[0]
    red_sobel_x = red_sobels[1]
    green_sobel_x = green_sobels[1]
    blue_sobel_x = blue_sobels[1]
    red_sobel = red_sobels[2]
    green_sobel = green_sobels[2]
    blue_sobel = blue_sobels[2]
    red_max_y = np.amax(red_sobel_y)
    green_max_y = np.amax(green_sobel_y)
    blue_max_y = np.amax(blue_sobel_y)
    red_max_x = np.amax(red_sobel_x)
    green_max_x = np.amax(green_sobel_x)
    blue_max_x = np.amax(blue_sobel_x)
    red_max = np.amax(red_sobel)
    green_max = np.amax(green_sobel)
    blue_max = np.amax(blue_sobel)
    print('red_max: ',red_max)
    print('green_max: ', green_max)
    print('blue_max: ', blue_max)
    max_max_y = np.amax([red_max_y,green_max_y,blue_max_y])
    max_max_x = np.amax([red_max_x,green_max_x,blue_max_x])
    max_max = np.amax([red_max,green_max,blue_max])
    color_sobel_y = np.stack([red_sobel_y,green_sobel_y,blue_sobel_y],axis=2)
    color_sobel_x = np.stack([red_sobel_x,green_sobel_x,blue_sobel_x],axis=2)
    color_sobel = np.stack([red_sobel,green_sobel,blue_sobel],axis=2)
    print('color_sobel.shape: ',color_sobel.shape)
    height = color_sobel.shape[0]
    width = color_sobel.shape[1]
    scaled_color_sobel_y = color_sobel_y/max_max_y
    scaled_color_sobel_x = color_sobel_x/max_max_x
    scaled_color_sobel = color_sobel/max_max

    if (whether_to_display):
        plt.subplot(2,2,1),plt.imshow(image[:,:,])
        plt.title('Image'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,2),plt.imshow(scaled_color_sobel[:,:,])
        plt.title('Scaled Color Sobel'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,3),plt.imshow(scaled_color_sobel_y[:,:,])
        plt.title('Scaled Color Sobel Y'), plt.xticks([]), plt.yticks([])
        plt.subplot(2,2,4),plt.imshow(scaled_color_sobel_x[:,:,])
        plt.title('Scaled Color Sobel X'), plt.xticks([]), plt.yticks([])

        plt.show()

    return scaled_color_sobel_y, scaled_color_sobel_x, scaled_color_sobel
