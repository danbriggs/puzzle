import numpy as np
import pixelpath as pp

import cv2
#import sys
#sys.setrecursionlimit(3000)

def fill(list,y,x,height,width):
    open_pixels = [[y,x]] #stack
    list[y,x]=True
    while (len(open_pixels)>0):
        pixel=open_pixels.pop()
        y=pixel[0]
        x=pixel[1]
        if (y < height - 1 and not list[y+1,x]):
            open_pixels.append([y+1,x])
            list[y+1,x]=True
        if (y > 0 and not list[y-1,x]):
            open_pixels.append([y-1,x])
            list[y-1, x] = True
        if (x < width - 1 and not list[y,x+1]):
            open_pixels.append([y,x+1])
            list[y, x+1] = True
        if (x > 0 and not list[y,x-1]):
            open_pixels.append([y, x-1])
            list[y,x-1]=True

def fill_in_pieces(image0, list, cutoff):
    img = cv2.imread(image0,0)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize = 5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize = 5)
    sobel = (sobelx * sobelx + sobely * sobely) ** 0.5
    height = img.shape[0]
    width = img.shape[1]
    for i in range (height):
        for j in range(width):
            if(sobel[i,j] > cutoff):
                list[i,j] = True
    fill(list,0,0,height,width)
    #for i in range (height):
    #    for j in range (width):
    #        if((list[i,j] == True)):
    #            k = j+1
    #            while(k < 1200 and list[i,k] == False):
    #                list[i,k] = True
    #                k += 1
    return list


