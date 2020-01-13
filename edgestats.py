from PIL import Image
import statistics
from scipy.stats import iqr

def border_color_statistics(image0):
    """Gets s.d., mean, median, and iqr of the colors
        in the boundary 1 pixel of image0, and returns them as a list."""
    color_boundary_red = []
    color_boundary_green = []
    color_boundary_blue = []
    im = Image.open(image0)
    pixel_color = im.load()
    width0=im.size[0]
    height0=im.size[1]
    #print('height0',height0)
    #print('width0',width0)
    for i in range(width0):
        color_boundary_red.append(pixel_color[i, 0][0])
        color_boundary_red.append(pixel_color[i, height0-1][0])
        color_boundary_green.append(pixel_color[i, 0][1])
        color_boundary_green.append(pixel_color[i, height0-1][1])
        color_boundary_blue.append(pixel_color[i, 0][2])
        color_boundary_blue.append(pixel_color[i, height0-1][2])
    for j in range(height0):
        color_boundary_red.append(pixel_color[0, j][0])
        color_boundary_red.append(pixel_color[width0-1, j][0])
        color_boundary_green.append(pixel_color[0, j][1])
        color_boundary_green.append(pixel_color[width0-1, j][1])
        color_boundary_blue.append(pixel_color[0, j][2])
        color_boundary_blue.append(pixel_color[width0-1, j][2])
    standard_deviation = []
    standard_deviation.append(statistics.stdev(color_boundary_red))
    standard_deviation.append(statistics.stdev(color_boundary_green))
    standard_deviation.append(statistics.stdev(color_boundary_blue))
    mean = []
    mean.append(statistics.mean(color_boundary_red))
    mean.append(statistics.mean(color_boundary_green))
    mean.append(statistics.mean(color_boundary_blue))
    median = []
    median.append(statistics.median(color_boundary_red))
    median.append(statistics.median(color_boundary_green))
    median.append(statistics.median(color_boundary_blue))
    iqrr = []
    iqrr.append(iqr(color_boundary_red))
    iqrr.append(iqr(color_boundary_green))
    iqrr.append(iqr(color_boundary_blue))
    returnlist = []
    returnlist.append(standard_deviation)
    returnlist.append(mean)
    returnlist.append(median)
    returnlist.append(iqrr)
    return returnlist
