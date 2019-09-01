from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image, ImageDraw, ImageMath
import numpy as np
import re
import png


def open_as_gray(path):
    im = Image.open(path).convert("L")
    return im


def im_to_np(im):
    im_array = np.asarray(im)
    return np.array([[[0 if x else 1] for x in y] for y in im_array]).reshape(im_array.shape)


def adjust_array(mat):
    Y, X = mat.shape
    top, left = mat.shape
    bottom = 0
    right = 0
    for i, x in enumerate(mat):
        if any(x):
            top = i if top > i else top
            bottom = i if bottom < i else bottom

    for i, y in enumerate(mat.T):
        if any(y):
            left = i if left > i else left
            right = i if right < i else right

    char_area = mat[top:bottom, left:right]

    height, width = char_area.shape

    margin = ((Y - height) // 2, (X - width) // 2)

    matrix = np.full(mat.shape, 0)

    matrix[margin[0]:margin[0] + height, margin[1]:margin[1] + width] = char_area

    return matrix


def edit_image(im):
    mat = adjust_array(im_to_np(im))
    x = np.array([np.full(mat.shape[1], i) for i in range(mat.shape[0])])
    y = np.array([range(mat.shape[1]) for i in range(mat.shape[0])])

    M = {}
    for n, m in [(0, 0), (1, 0), (0, 1)]:
        M_nm = np.sum(np.power(x, n) * np.power(y, m) * mat)
        M[str(n) + str(m)] = M_nm

    G = (int(round(M["10"] / M["00"])), int(round(M["01"] / M["00"])))

    im_adjusted = Image.fromarray(np.uint8(210 - mat * 210)).convert("RGB")
    im_G = Image.fromarray(np.uint8(210 - mat * 210)).convert("RGB")

    draw = ImageDraw.Draw(im_G)
    r = im_G.size[0] / 25
    draw.ellipse(((G[1] - r, G[0] - r), (G[1] + r, G[0] + r)), fill=(210, 50, 50))

    return im_G, im_adjusted, G, M["00"]


def save_image(path, directly):
    image = edit_image(open_as_gray(path))
    image[0].save(directly + "/" + re.findall(r'(.*/)?(.+)\.png', path)[0][1] + "_G.png", 'png')
