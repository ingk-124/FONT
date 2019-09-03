from character import Character
from tqdm import tqdm
import re
import csv

with open("kanji.txt") as f:
    characters = f.readlines()[0]

font_list = ["/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
             "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
             "/System/Library/Assets/com_apple_MobileAsset_Font5/1765bae07bcefebc499ababa7ecdef963e4f151e.asset"
             "/AssetData/Klee.ttc"]

if __name__ == '__main__':
    for font in font_list[1:2]:
        with open("output/{}.csv".format(re.findall(r'(.*/)?(.+)(\.[a-z]{3})', font)[0][-2]), 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(("character", "G_x", "G_y", "M", "Euclid"))
            with tqdm(characters) as pbar:
                for i, char in enumerate(pbar):
                    pbar.set_description("[{}:{}]" .format(i, char))
                    c = Character(char=char, font=font, size=(500, 500))
                    c.main()
                    writer.writerow((char, c.G[0], c.G[1], c.M, c.euclid))
