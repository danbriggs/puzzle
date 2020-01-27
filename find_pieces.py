# from skimage.metrics import structural_similarity as ssim
from PIL import Image, ImageChops


def crop(image_path, coords):
    """coords should a 4-tuple
    (left, top, right, bottom) of integers."""
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    return cropped_image

def center(topstart, botstart, leftstart, rightstart):
    center = topstart + botstart + leftstart + rightstart
    center = center/4
    return center

def matching(image, background, mask, start, array):
    """compares the image at filename image to the image at filename background.
    start should be a pair (y,x) for the upper-left corner of image in background.
    compares only those pixels where mask is false.
    mask must be the same dimensions as image.
    the percent difference is appended to array."""
    i1 = Image.open(image)
    i2 = crop(background, (start[1], start[0], start[1]+i1.width, start[0]+i1.height))
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    array.append((dif / 255.0 * 100) / ncomponents)

def rotate(image, background):
    colorImage = Image.open(image)
    array = []
    for i in range(360):
        transposed = colorImage.rotate(i)
        matching(transposed, background, array)



def rotation_piece(puzzle_piece, background, image):
    """
    Rotating the puzzle pieces pixel by pixel to find which is the best match
    for the singular puzzle piece to fit inside the puzzle itself.
    """
    diff = ImageChops.difference(background, image)
    if diff.getbbox():
        diff.show()

    topstart = puzzle_piece[0][0][1]
    leftstart = puzzle_piece[0][0][0]
    botstart = topstart
    rightstart = leftstart
    for i in range(len(puzzle_piece[0])):
        if puzzle_piece[0][i][1] > topstart:
            topstart = puzzle_piece[0][i][1]
        if puzzle_piece[0][i][1] < botstart:
            botstart = puzzle_piece[0][i][1]
    for j in range(len(puzzle_piece[0])):
        if puzzle_piece[0][j][0] <= leftstart:
            leftstart = puzzle_piece[0][j][0]
        if puzzle_piece[0][j][0] >= rightstart:
            rightstart = puzzle_piece[0][j][0]
    new_image = crop(image, leftstart[0], topstart[1], rightstart[0], botstart[0])
    centers = center(topstart, botstart, leftstart, rightstart)
    rotate(new_image, background)

def tester2():
    result_array = []
    image1 = "incomplete7_small.png"
    image2 = "incomplete6_large.png"
    matching(image1,image2,(10,1245),result_array)
    print(result_array)
    i1 = Image.open(image1)
    i2 = Image.open(image2)
    print(type(i1))
    print(type(i2))
    print(i1.size)
    print(i2.size)
    pairs = zip(i1.getdata(), i2.getdata())
    print(type(pairs))
    print(len(list(pairs)))
    transposed = i1.rotate(74)
    print("type(transposed)", type(transposed))
    print("transposed.size", transposed.size)
    transposed.show()


if __name__ == '__main__':
    tester2()
