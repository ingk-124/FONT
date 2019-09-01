from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import re
import gravity


def generate_char_img(char, fontname, size=(300, 300)):
    img = Image.new('L', size, 255)
    draw = ImageDraw.Draw(img)
    fontsize = int(size[0] * 0.8)
    font = ImageFont.truetype(fontname, fontsize)

    # adjust character position.
    char_displaysize = font.getsize(char)
    offset = tuple((si - sc) // 2 for si, sc in zip(size, char_displaysize))
    assert all(o >= 0 for o in offset)

    # adjust offset, half value is right size for height axis.
    draw.text((offset[0], offset[1] // 2), char, font=font, fill=0)
    return img


class Character:
    def __init__(self, char, font, size=(200, 200)):
        self.char = char
        self.font = font
        self.size = size
        self.font_name = re.findall(r'(.*/)?(.+)(\.[a-z]{3})', font)[0][-2]
        self.image_raw = None
        self.image_G = None
        self.G = None
        self.M = 0

    def search_g(self):
        im = generate_char_img(char=self.char, fontname=self.font, size=self.size)
        edited = gravity.edit_image(im)
        self.image_G, self.image_raw, self.G, self.M = edited

    def save_images(self):
        raw_directly = "output_png/{}".format(self.font_name)
        if not os.path.exists(raw_directly):
            os.makedirs(raw_directly, exist_ok=True)
        self.image_raw.save("{}/{}_{}.png".format(raw_directly, self.font_name, self.char), 'png')

        edit_directly = "output_G/{}".format(self.font_name)
        if not os.path.exists(edit_directly):
            os.makedirs(edit_directly, exist_ok=True)
        self.image_G.save("{}/{}_{}_G.png".format(edit_directly, self.font_name, self.char), 'png')

    def main(self):
        self.search_g()
        self.save_images()
