from character import Character
from tqdm import tqdm
import re
import csv

with open("kanji.txt") as f:
    characters = f.readlines()[0]

font_list = ["/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",
             "/System/Library/Assets/com_apple_MobileAsset_Font5/458cb75c37483d7bcdfd68445b7246c76ecb29a6.asset"
             "/AssetData/Osaka.ttf",
             "/System/Library/Assets/com_apple_MobileAsset_Font5/1765bae07bcefebc499ababa7ecdef963e4f151e.asset"
             "/AssetData/Klee.ttc"]

if __name__ == '__main__':
    for font in font_list:
        with open("output/{}_log.csv".format(re.findall(r'(.*/)?(.+)(\.[a-z]{3})', font)[0][-2]), 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(("character", "G", "M"))
            for char in tqdm(characters):
                c = Character(char=char, font=font, size=(800, 800))
                c.main()
                writer.writerow((c, c.G, c.M))
