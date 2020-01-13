import os
import sys
import statistics
import time
import random
import cv2
from scipy.stats import iqr
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import averager as av

UPPER_LIMIT = 900 #max length of path

def average_sobel(y, x, cutoff, keep_track,border, sobely,sobelx, sobel):
    returnlist = []
    yint = int(y)
    xint = int(x)
    ypart = (0.25)*(sobely[yint+1, xint] + sobely[yint, xint+1] + \
                sobely[yint+1, xint+1] + sobely[yint, xint])
    returnlist.append(ypart)
    xpart = (0.25)*(sobelx[yint+1, xint] + sobelx[yint, xint+1] + \
                sobelx[yint+1, xint+1] + sobelx[yint, xint])
    returnlist.append(xpart)
    avg_sobel = (0.25)*(sobel[yint+1, xint] + sobel[yint, xint+1] + \
                sobel[yint+1, xint+1] + sobel[yint, xint])
    returnlist.append(avg_sobel)
    return returnlist


def pixel_path(y, x, cutoff, keep_track, border, sobely, sobelx, sobel,sobelcopy):
    # Takes the y and x coordinates of a pixel in the image
    # If the sobel at that location is less than cutoff, return []
    # Otherwise, return a sequence of pixel positions drawing a path following
    # the edge.
    # NOTE: important to stop when you come back somewhere "near enough"
    # Use theta and sobel
    # keep_track is a boolean stating whether to keep track of pixels that have been checked.
    # border is an integer denoting the radius of an extra region around each pixel
    # to denote as True in hasbeenchecked.
    if (sobel[y, x] < cutoff):
        return []
    ycoord = y
    xcoord = x
    returnlist = []
    # NOTE: consider taking the average sobel of the four nearest neighbors
    # weigh each one depending on how close it is to the original coordinate
    for i in range(250):
        yint = int(round(ycoord))
        xint = int(round(xcoord))
        ypart = av.averager(sobely)(yint,xint)
        xpart = av.averager(sobelx)(yint,xint)
        size = sobel[yint, xint]
        ycoord = ycoord - xpart / size
        xcoord = xcoord + ypart / size
        sobelcopy[yint, xint] = 0
        returnlist.append([ycoord, xcoord, av.averager(sobel)(yint,xint)])
        if (i > 10):
            if ((ycoord - y) * (ycoord - y) + (xcoord - x) * (xcoord - x) < 1):
                break
    return returnlist


def pixel_path_recurse(originaly, originalx, y, x, cutoff, iteration, keep_track,
                       border, sobely, sobelx, sobel, sobelcopycopy, height, width):
    ycoord = y
    xcoord = x
    yint = int(round(ycoord))
    xint = int(round(xcoord))
    returnlist = []
    if (sobel[yint, xint] < cutoff and iteration == 0):
        return []
    elif (yint == originaly and xint == originalx and iteration > 100):
        return []
    elif ((ycoord - originaly) * (ycoord - originaly) + (xcoord - originalx) * (xcoord - originalx) < 16 and iteration > 100):
        return []
    else:
        if (y>=height-2 or y<=2 or x>= width-2 or x<=2):
            return []
        ypart = av.averager(sobely)(yint,xint)
        xpart = av.averager(sobelx)(yint,xint)
        size = av.averager(sobel)(yint, xint)
        ycoord = ycoord - xpart / (size+1)
        xcoord = xcoord + ypart / (size+1)
        sobelcopycopy[yint, xint] = 0
        returnlist.append([ycoord, xcoord, av.averager(sobel)(yint,xint)])
        iteration += 1
        if (iteration>=UPPER_LIMIT):
            return []
        return returnlist + pixel_path_recurse(originaly, originalx, ycoord,
                                               xcoord, cutoff, iteration,
                                               keep_track, border,sobely,
                                               sobelx,sobel,sobelcopycopy, height, width)
