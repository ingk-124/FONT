import os
import re
import gravity


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
        im = gravity.generate_char_img(char=self.char, fontname=self.font, size=self.size)
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
