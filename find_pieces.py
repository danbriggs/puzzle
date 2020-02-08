from PIL import Image, ImageChops
import cv2

def cropping(image_path, coords):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    return cropped_image

def center(topstart, botstart, leftstart, rightstart):
    center = topstart + botstart + leftstart + rightstart
    center = center/4
    return center

def matching(image, background, mask, start, array):
    """
    compares the image at filename image to the image as filename background.
    start should be a pair (x, y) for the upper-left corner of image in background.
    compares only those pixels where mask is true.
    mask must be the same dimensions as image.
    the percent difference is appended by a array.
    """
    i1 = image
    i2 = cropping(background, (start[1], start[0], start[1] + i1.width, start[0] + i1.height))
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
        if(i == 72):
            image.show()
            image.save('rotated_image_76.jpg')
        if(i == 216):
            image.show()
            image.save('rotated_image_216.jpg')
        matching(rotated, background, 0, start, array)
    return array

def rotation_piece(puzzle_piece, background, image):
    """
    Rotating the puzzle pieces pixel by pixel to find which is the best match
    for the singular puzzle piece to fit inside the puzzle itself.
    puzzle_pieces should be a list of lists of (x,y) ports corresponding to the boundaries of puzzle pieces.
    """
    topstart = puzzle_piece[0][0][1]
    leftstart = puzzle_piece[0][0][0]
    botstart = topstart
    rightstart = leftstart
    for i in range(len(puzzle_piece[0])):
        if puzzle_piece[0][i][1] < topstart:
            topstart = puzzle_piece[0][i][1]
        if puzzle_piece[0][i][1] < botstart:
            botstart = puzzle_piece[0][i][1]
    for j in range(len(puzzle_piece[0])):
        if puzzle_piece[0][j][0] <= leftstart:
            leftstart = puzzle_piece[0][j][0]
        if puzzle_piece[0][j][0] >= rightstart:
            rightstart = puzzle_piece[0][j][0]
    new_image = cropping(image, (leftstart, botstart, rightstart, topstart))
    new_stats = rotate(new_image, background)
    return new_stats

