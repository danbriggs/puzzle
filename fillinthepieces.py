import numpy as np
import pixelpath as pp
import findbackground as fb
import depthofbackground as dofb
import cv2
def fill(is_enough_edge, is_background,y,x,height,width):
    open_pixels = [[y,x]] #stack
    is_background[y,x] = True
    counter = 0
    while(len(open_pixels) > 0):
        counter+=1
        pixel = open_pixels.pop()
        y = pixel[0]
        x = pixel[1]
        is_background[y,x] = True #?
        if(y < height - 1):
            if (not is_enough_edge[y+1,x] and not is_background[y+1,x]):
                open_pixels.append([y+1,x])
            is_background[y+1,x] = True

        if(y>0):
            if (not is_enough_edge[y-1,x] and not is_background[y-1,x]):
                open_pixels.append([y-1,x])
            is_background[y-1,x] = True

        if(x<width - 1):
            if (not is_enough_edge[y,x+1] and not is_background[y,x+1]):
                open_pixels.append([y,x+1])
            is_background[y,x+1] = True

        if(x>0):
            if (not is_enough_edge[y,x-1] and not is_background[y,x-1]):
                open_pixels.append([y,x-1])
            is_background[y,x-1] = True

    print("Number of pixels reached from upper-left corner: ",counter)
    

def fill_in_pieces(image0, is_enough_edge, is_background, cutoff, sobel):
    """is_enough_edge and is_background should be 2D arrays of type bool consisting of Falses
    of the same dimensions as the image at file name image0.
    This function will fill in is_enough_edge with Trues wherever sobel is greater than cutoff.
    It will fill is_background with Trues up to and including the one-pixel boundary of a puzzle piece."""
    img = cv2.imread(image0, 0)
    img1 = cv2.imread(image0)
    height = img.shape[0]
    width = img.shape[1]
    depth = dofb.depth_of_background(image0)
    ans = fb.find_background(image0, depth)
    median_red = ans[2][:1:]
    median_green = ans[2][1:2:]
    median_blue = ans[2][2:3:]
    iqr_red = ans[3][:1:]
    iqr_green = ans[3][1:2:]
    iqr_blue = ans[3][2:3:]
    for i in range (height):
        for j in range(width):
            pic_red = img1[i,j][:1:]
            pic_green = img1[i,j][1:2:]
            pic_blue = img1[i,j][2:3:]
            #if(pic_red[0] > (median_red[0] + 0.5*iqr_red[0]) or pic_red[0] < (median_red[0] - 0.5*iqr_red[0])):
                #if(pic_green[0] > (median_green[0] + 0.5*iqr_green[0]) or pic_green[0] < (median_green[0] - 0.5*iqr_green[0])):
                    #if(pic_blue[0] > (median_blue[0] + 0.5*iqr_blue[0]) or pic_blue[0] < (median_blue[0] - 0.5*iqr_blue[0])):
            if(sobel[i,j] > cutoff ):
                is_enough_edge[i,j] = True
    fill(is_enough_edge, is_background,0,0,height,width)
    #for i in range (height):
     #   for j in range (width):
      #      if((list[i][j] == True)):
       #         k = j+1
        #        while(k < 1200 and list[i][k] == False):
         #           list[i][k] = True
          #          k += 1
    return list


