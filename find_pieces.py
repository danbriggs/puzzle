from PIL import Image, ImageChops
import cv2

def cropping(image, coords):
    cropped_image = image.crop(coords)
    return cropped_image

def center(topstart, botstart, leftstart, rightstart):
    return [(topstart + botstart)/2,  (leftstart + rightstart)/2]

def matching(image, background, mask, start, array):
    """
    compares the image at filename image to the image as filename background.
    start should be a pair (y, x) for the upper-left corner of image in background.
    compares only those pixels where mask is true.
    mask must be the same dimensions as image.
    the percent difference is appendid by a array.
    """
    i1 = image
    i2 = background.crop((int(start[0]), int(start[1]), int(start[0] +  i1.width), int(start[1]+  i1.height)))
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))
    ncomponents = i1.size[0] * i1.size[1] * 3
    array.append((dif / 255.0 * 100) / ncomponents)
    return array

def rotate(image, background, start):
    array = []
    for i in range(360):
        rotated = image.rotate(i)
        rotated.show()
        matching(rotated, background, 0, start, array)
    return array

if __name__ == '__main__':
    ip1 = Image.open('incomplete2.jpg')
    ip2 = Image.open('incomplete2_piece.png')
    rotate(ip2, ip1, (100, 100))

def rotation_piece(puzzle_pieces, background, image):
    """
    Rotating the puzzle pieces pixel by pixel to find which is the best match
    for the singular puzzle piece to fit inside the puzzle itself.
    puzzle pieces should be a list of list of (y, x) pairs corresponding to the
    boundaries of the edges of the pieces.
    """
    background_image = Image.open(background)
    image_image = Image.open(image)
    topstart = puzzle_pieces[0][0][0]
    leftstart = puzzle_pieces[0][0][1]
    botstart = topstart
    rightstart = leftstart
    for i in range(len(puzzle_pieces[0])):
        if puzzle_pieces[0][i][0] < topstart:
            topstart = puzzle_pieces[0][i][0]
        if puzzle_pieces[0][i][0] > botstart:
            botstart = puzzle_pieces[0][i][0]
        if puzzle_pieces[0][i][1] <= leftstart:
            leftstart = puzzle_pieces[0][i][1]
        if puzzle_pieces[0][i][1] >= rightstart:
            rightstart = puzzle_pieces[0][i][1]
    new_image = image_image.crop((leftstart, topstart, rightstart, botstart))
    new_stats = rotate(new_image, background_image, (center(topstart, botstart, leftstart, rightstart)))
    return new_stats
