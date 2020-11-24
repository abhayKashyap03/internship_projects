from glob import glob
from PIL import Image, ImageFilter, ImageOps
import os, time
from natsort import natsorted
import numpy as np

img_paths = natsorted(glob('img/*'))

for img_path in img_paths :
    start = time.time()

    img = Image.open(img_path)
    mask_paths = natsorted(glob('masks/'+os.path.splitext(os.path.basename(img_path))[0]+"/*"))
    for mask in mask_paths :
        mask = Image.open(mask)
        mask = mask.filter(ImageFilter.FIND_EDGES)
        pixdata = mask.load()
        for y in range(mask.size[1]):
            for x in range(mask.size[0]):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (0, 0, 255, 255)
        img.paste(mask, (0, 0), mask)

    img.save(os.path.join('results', os.path.basename(img_path)))
    print('Time : {} seconds'.format(time.time() - start))
