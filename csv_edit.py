import pandas as pd
import numpy as np
import re

if __name__ == '__main__':
    fontname = ["ヒラギノ明朝 ProN", "Osaka", "Klee"]
    # fontname = ["ヒラギノ明朝 ProN"]
    with open("/Users/inagakishinichiro/Desktop/py3works/FONT/kanji.txt") as f:
        characters = f.readlines()[0]
    for font in fontname:
        path_csv = "output/{}_log.csv".format(font)
        log_df = pd.read_csv(path_csv)

        output_df = pd.DataFrame()
        output_df["character"] = list(characters)
        G = np.array([np.array(re.findall(r"([0-9]*), ([0-9]*)", l)[0], dtype='int16') for l in log_df["G"]])
        output_df["M"] = log_df["M"]
        output_df["G_x"] = G[:, 0]
        output_df["G_y"] = G[:, 1]
        output_df["Euclid"] = [np.linalg.norm(v - np.array((800, 800)) // 2) for v in G]

        output_df.to_csv("output/{}_data.csv".format(font))
