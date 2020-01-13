# pip install opencv-python

import cv2
import numpy as np
import time
import random
from matplotlib import pyplot as plt

img = cv2.imread('dave.jpg',0)
print('shape of img',img.shape)
print('type of img[500,1000]',type(img[500,1000]))

imgcolor = cv2.imread('incomplete2.png')
print('shape of imgcolor',imgcolor.shape)

def border_color_statistics(image0, depth):
    """Gets mean color, median color, and standard deviation of the color
    in the boundary n pixels, where n=depth."""

laplacian = cv2.Laplacian(img,cv2.CV_64F)
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
sobel = (sobelx*sobelx+sobely*sobely)**.5
sobelcopy = np.copy(sobel)
sobelcopycopy = np.copy(sobel)
theta = np.arctan(sobelx/sobely)
highs = sobel[sobel>6000]
print(np.multiply(False,1)) 
print('shape of sobel',sobel.shape)
print('size of sobel',sobel.shape[0]*sobel.shape[1])
print('shape of highs',highs.shape)
indicators=np.multiply(sobel>6000,1)
print('shape of indicators',indicators.shape)
restricted_theta = indicators*(np.pi)+theta*indicators
print('shape of restricted theta',restricted_theta.shape)

print('max of sobel:',np.max(sobel))
print('min of sobel:',np.min(sobel))

def average_sobel(y,x):
    returnlist = []
    yint_down = int(y)
    xint_down = int(x)
    yint_up = yint_down + 1
    xint_up = xint_down + 1
    avg_sobely = (0.25)*(sobely[yint_down, xint_down] + sobely[yint_down, xint_up]
                         + sobely[yint_up, xint_down] + sobely[yint_up, xint_up])
    returnlist.append(avg_sobely)
    avg_sobelx = (0.25)*(sobelx[yint_down, xint_down] + sobelx[yint_down, xint_up]
                         + sobelx[yint_up, xint_down] + sobelx[yint_up, xint_up])
    returnlist.append(avg_sobelx)
    avg_sobel = (0.25)*(sobel[yint_down, xint_down] + sobel[yint_down, xint_up]
                         + sobel[yint_up, xint_down] + sobel[yint_up, xint_up])
    returnlist.append(avg_sobel)
    return returnlist
    
def pixel_path(y,x,cutoff,keep_track,border):
    #Takes the y and x coordinates of a pixel in the image
    #If the sobel at that location is less than cutoff, return []
    #Otherwise, return a sequence of pixel positions drawing a path following
    #the edge.
    #NOTE: important to stop when you come back somewhere "near enough"
    #Use theta and sobel
    #keep_track is a boolean stating whether to keep track of pixels that have been checked.
    #border is an integer denoting the radius of an extra region around each pixel
    #to denote as True in hasbeenchecked.
    if(sobel[y,x]<cutoff):
        return []
    ycoord = y
    xcoord = x
    returnlist = []
    #NOTE: consider taking the average sobel of the four nearest neighbors
    #weigh each one depending on how close it is to the original coordinate
    for i in range(250):
        yint = int(round(ycoord))
        xint = int(round(xcoord))
        ypart = average_sobel(yint,xint)[0]
        xpart = average_sobel(yint,xint)[1]
        size = sobel[yint, xint]
        ycoord = ycoord - xpart/size
        xcoord = xcoord + ypart/size
        sobelcopy[yint, xint] = 0
        returnlist.append([ycoord, xcoord, average_sobel(int(ycoord), int(xcoord))[2]])
        if(i>10):
            if((ycoord-y)*(ycoord-y) + (xcoord-x)*(xcoord-x) < 1):
                break
    return returnlist

def pixel_path_recurse(originaly, originalx, y,x, iteration,keep_track,border):
    ycoord = y
    xcoord = x
    yint = int(round(ycoord))
    xint = int(round(xcoord))
    returnlist = []
    if(((ycoord - originaly)*(ycoord-originaly) +
        (xcoord - originalx)*(xcoord-originalx))<2 and
       iteration > 20):
       return []
    else:
        ypart = average_sobel(yint,xint)[0]
        xpart = average_sobel(yint,xint)[1]
        size = sobel[yint, xint]
        ycoord = ycoord - xpart/size
        xcoord = xcoord + ypart/size
        sobelcopycopy[yint, xint] = 0
        returnlist.append([ycoord, xcoord, average_sobel(int(ycoord), int(xcoord))[2]])
        iteration += 1
        return returnlist + pixel_path_recurse(originaly, originalx, ycoord,xcoord,iteration,keep_track,border)

def determine_if_above_cutoff(y,x,cutoff):
    if (sobel[y,x]<cutoff):
        return False
    return True

height=sobel.shape[0]
width=sobel.shape[1]
#ycord=[random.randint(0,height-1) for i in range(1000000)]
#xcord=[random.randint(0,width-1) for i in range(1000000)]
#start0=time.time()
#for i in range(1000000):
#    determine_if_above_cutoff(ycord[i],xcord[i],2000)
#end0=time.time()
#print("Time to determine a million: ",end0-start0)

hasbeenchecked = np.zeros((height,width), dtype=bool)
print("hasbeenchecked[500,1000]: ",hasbeenchecked[500,1000])

start1=time.time()
print("pixel path 1", pixel_path(42,36,2000,False,0))
end1=time.time()
print("pixel path 2", pixel_path(54,32,2000,False,0))
start2=time.time()
print("pixel path recurse 1", pixel_path_recurse(42,36,42,36,0,False,0))
end2=time.time()
print("iterative: ",end1-start1)
print("recursive: ",end2-start2)

#plt.subplot(2,2,1),plt.imshow(restricted_theta[:100,:100],cmap = 'gray')
#plt.title('Restricted Theta'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,1),plt.imshow(sobelcopy[:100,:100],cmap = 'gray')
plt.title('Sobel Copy'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(sobel[:100,:100],cmap = 'gray')
plt.title('Sobel'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,3),plt.imshow(sobelx[:100,:100],cmap = 'gray')
#plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely[:100,:100],cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelcopycopy[:100,:100],cmap = 'gray')
plt.title('Sobel Recurse'), plt.xticks([]), plt.yticks([])



plt.show()
