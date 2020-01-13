import statistics
from PIL import Image
from scipy.stats import iqr

# Minjune changed this slightly

def border_color_statistics(image0, depth):
    """Gets mean color and standard deviation of the color
        in the boundary n pixels, where n-depth"""
    color_boundary_red = []
    color_boundary_green = []
    color_boundary_blue = []
    standard_deviation = []
    mean = []
    median = []
    im = Image.open(image0)
    pixel_color = im.load()
    height0 = im.size[1]
    width0 = im.size[0]
    for i in range(width0):
        for k in range(depth):
            color_boundary_red.append(pixel_color[i, k][0])
            color_boundary_red.append(pixel_color[i, height0-k-1][0])
            color_boundary_green.append(pixel_color[i, k][1])
            color_boundary_green.append(pixel_color[i, height0-k-1][1])
            color_boundary_blue.append(pixel_color[i, k][2])
            color_boundary_blue.append(pixel_color[i, height0-k-1][2])
    for j in range(height0):
        for h in range(depth):
            color_boundary_red.append(pixel_color[h, j][0])
            color_boundary_red.append(pixel_color[width0-1-h, j][0])
            color_boundary_green.append(pixel_color[h, j][1])
            color_boundary_green.append(pixel_color[width0-h-1, j][1])
            color_boundary_blue.append(pixel_color[h, j][2])
            color_boundary_blue.append(pixel_color[width0-h-1, j][2])
    standard_deviation.append(statistics.stdev(color_boundary_red))
    standard_deviation.append(statistics.stdev(color_boundary_green))
    standard_deviation.append(statistics.stdev(color_boundary_blue))
    mean.append(statistics.mean(color_boundary_red))
    mean.append(statistics.mean(color_boundary_green))
    mean.append(statistics.mean(color_boundary_blue))
    median.append(statistics.median(color_boundary_red))
    median.append(statistics.median(color_boundary_green))
    median.append(statistics.median(color_boundary_blue))
    iqr1 = []
    iqr1.append(iqr(color_boundary_red))
    iqr1.append(iqr(color_boundary_green))
    iqr1.append(iqr(color_boundary_blue))
    returnlist = []
    returnlist.append(standard_deviation)
    returnlist.append(mean)
    returnlist.append(median)
    returnlist.append(iqr1)
    return returnlist
