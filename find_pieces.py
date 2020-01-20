from skimage.metrics import structural_similarity as ssim
from PIL import Image, ImageChops


def crop(image_path, coords):
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(coords)
    return cropped_image

def center(topstart, botstart, leftstart, rightstart):
    center = topstart + botstart + leftstart + rightstart
    center = center/4
    return center

def matching(image, background, array):
    i1 = Image.open(image)
    i2 = Image.open(background)
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
        transposed = colorImage.transpose(Image.ROTATE_i)
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
