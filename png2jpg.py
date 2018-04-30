from glob import glob  
import argparse                                                         
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--folder', required=True,
                help='path to the input image')
    
args = vars(ap.parse_args())

pngs = glob(args['folder'] + '*.png')

for j in pngs:
    img = cv2.imread(j)
    cv2.imwrite(j[:-3] + 'jpg', img)
    os.remove(j)

# pngs = glob(args['folder'] + '*.png')

# for j in pngs:
#     im = Image.open(j)
#     bg = im.convert("RGB")
#     bg.save(j[:-3] + 'jpg')
#     #os.remove(j)