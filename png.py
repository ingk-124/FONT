from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import re
from tqdm import tqdm

with open("/Users/inagakishinichiro/Desktop/py3works/FONT/joyo_kanji.txt") as f:
    characters = f.readlines()[0]


def generate_char_img(char, fontname="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc", size=(300, 300)):
    img = Image.new('L', size, 255)
    draw = ImageDraw.Draw(img)
    fontsize = int(size[0] * 0.8)
    font = ImageFont.truetype(fontname, fontsize)

    # adjust character position.
    char_displaysize = font.getsize(char)
    offset = tuple((si - sc) // 2 for si, sc in zip(size, char_displaysize))
    assert all(o >= 0 for o in offset)

    # adjust offset, half value is right size for height axis.
    draw.text((offset[0], offset[1]//2), char, font=font, fill=0)
    return img


def save_img(char, filepath, fontname="/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"):
    img = generate_char_img(char, fontname)
    img.save(filepath + ".png", 'png')


font_list = ["/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
             "/System/Library/Assets/com_apple_MobileAsset_Font5/458cb75c37483d7bcdfd68445b7246c76ecb29a6.asset/AssetData/Osaka.ttf",
             "/System/Library/Assets/com_apple_MobileAsset_Font5/1765bae07bcefebc499ababa7ecdef963e4f151e.asset/AssetData/Klee.ttc"]


def mk_png(font):
    font_name = re.findall(r'(.*/)?(.+)(\.[a-z]{3})', font)[0][-2]
    directly = "output_png/{}".format(font_name)
    os.makedirs(directly, exist_ok=True)
    for c in tqdm(characters):
        save_img(char=c, filepath="{}/{}_{}".format(directly, font_name, c), fontname=font)


if __name__ == '__main__':
    c = chr(0x5433)

    print(c)
    fontname = font_list[0]

    save_img(char=c, filepath="test1", fontname=fontname)
