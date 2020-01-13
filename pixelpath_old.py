def pixel_path(y,x,cutoff, keep_track, border, sobely, sobelx, sobel, sobelcopy):
    #takes the x and y coordinates of the pixel the images
    #If the sobel at that label is less than cutoff, return []
    #Otherwise, return a sequence of pixel position drawing a path following
    #the edge
    #NOTE: important to stop when you come back somewhere "near enough"
    #Use theta and sobel
    #Try using the weighted average of the sobels(sobelx, sobely)
    #the four nearest coordinates a floating-point coordinate pair instead of just the nearest lattice point.
    #keep track is a boolean stating whether to keep track of pixels that have been checked.
    #border is an integer denoting the radius of an extra region around each pixel.
    #to denote as True in hasbeenchecked
    if(sobel[y,x] < cutoff):
        return[]
    ycoord = y
    xcoord = x
    returnlist = []
    for i in range(2000):
        yint = int(round(ycoord))
        xint = int(round(xcoord))
        ypart = sobely[yint,xint]
        xpart = sobelx[yint,xint]
        size = sobel[yint,xint]
        ycoord=ycoord-xpart/size
        xcoord=xcoord+ypart/size
        sobelcopy[yint, xint] = 0
        returnlist.append([ycoord,xcoord,sobel[int(ycoord), int(xcoord)]])
        if(i>10):
            if(ycoord-y)**2+(xcoord-x)**2 < 25:
                break
    return returnlist

def pixel_path_average(y, x, cutoff, keep_track, border, sobely, sobelx, sobel):
    ycoord = y
    xcoord = x
    returnlist = []
    yint = int(ycoord)
    xint = int(xcoord)
    ypart = (y - yint)*(xint+1 - x)*sobely[yint+1, xint] + (x - xint)*(yint+1-y)*sobely[yint, xint+1] + \
                (y-yint)*(x-xint)*sobely[yint+1, xint+1] + (yint - y)*(xint - x)*sobely[yint, xint]
    returnlist.append(ypart)
    xpart = (y - yint)*(xint+1 - x)*sobelx[yint+1, xint] + (x - xint)*(yint+1-y)*sobelx[yint, xint+1] + \
                (y-yint)*(x-xint)*sobelx[yint+1, xint+1] + (yint - y)*(xint - x)*sobelx[yint, xint]
    returnlist.append(xpart)
    avg_sobel = (y - yint)*(xint+1 - x)*sobel[yint+1, xint] + (x - xint)*(yint+1-y)*sobel[yint, xint+1] + \
               (y-yint)*(x-xint)*sobel[yint+1, xint+1] + (yint - y)*(xint - x)*sobel[yint, xint]
    returnlist.append(avg_sobel)
    return returnlist

def pixel_path_recurse(originaly, originalx, y, x, cutoff, iteration, keep_track, border, sobely, sobelx, sobel, sobelcopycopy):
    ycoord = y
    xcoord = x
    yint = int(round(ycoord))
    xint = int(round(xcoord))
    returnlist = []
    if(sobel[yint, xint] < cutoff and iteration == 0):
        return []
    elif(((ycoord- originaly)*(ycoord-originaly) + (xcoord - originalx)*(xcoord - originalx) < 5) and iteration > 200):
        return []
    else:
        ypart = pixel_path_average(yint, xint,2000,0,0,sobely,sobelx,sobel)[0]
        xpart = pixel_path_average(yint, xint,2000,0,0,sobely,sobelx,sobel)[1]
        size = sobel[yint, xint]
        ycoord = ycoord - xpart/size
        xcoord = xcoord + ypart/size
        sobelcopycopy[yint, xint] = 0
        returnlist.append([ycoord, xcoord, pixel_path_average(int(ycoord), int(xcoord),2000,0,0,sobely,sobelx,sobel)[2]])
        iteration += 1
    return returnlist + pixel_path_recurse(originaly, originalx, ycoord, xcoord, cutoff, iteration, keep_track, border,sobely,sobelx,sobel,sobelcopycopy)

def average_sobel(y, x):
    returnlist = []
    yint_down = int(y)
    xint_down = int(x)
    yint_up = yint_down + 1
    xint_up = yint_up + 1
    avg_sobely = (0.25)*(sobely[yint_down, xint_down] + sobely[yint_down, xint_up] + sobely[yint_up, xint_down] + sobely[yint_up, xint_up])
    returnlist.append(avg_sobely)
    avg_sobelx = (0.25)*(sobelx[yint_down, xint_down] + sobelx[yint_down, xint_up] + sobelx[yint_up, xint_down] + sobelx[yint_up, xint_up])
    returnlist.append(avg_sobelx)
    avg_sobel = (0.25) * (sobel[yint_down, xint_down] + sobel[yint_down, xint_up] + sobel[yint_up, xint_down] + sobel[yint_up, xint_up])
    returnlist.append(avg_sobel)
    return returnlist
