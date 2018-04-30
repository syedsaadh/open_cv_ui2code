#!/usr/bin/env python
'''Crop the ui elments from the Mockup Ui Image.

Usage:

    python detect_components.py --image=PathToIMAGE

This will place the cropped components in predicted/imagename/.

Script created by Saad, Ujjwal, Manan
'''
import argparse
import os
import shutil
import cv2
import imutils
import json

from scripts.label_image import LabelImage
components = []
labelImage = LabelImage()
# Returns new_image resized Image.
def downscale_image(img, width=300):
    try:
        img = imutils.resize(img, width)
    except AttributeError:
        print('Shape Not Found for ' + str(img))
    return img

def apply_filters(img):
    edges = cv2.Canny(img,100,200)
    save_img(edges, 'image-detected.canny.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_img(gray, 'image-detected.gray.jpg')
    gray2 = cv2.bitwise_not(gray)
    save_img(gray2, 'image-detected.inverted.jpg')
    blurred = cv2.GaussianBlur(gray2, (5, 5), 0)
    save_img(blurred, 'image-detected.blurred.jpg')
    otsuThresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    save_img(otsuThresh, 'image-detected.otsu.jpg')
    thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)[1]
    save_img(thresh, 'image-detected.thresh.jpg')
    return thresh

def pad_and_crop(img, contour, pad=10):
    x, y, w, h = cv2.boundingRect(contour)
    x1 = x-pad
    x2 = x+w+(2*pad)
    y1 = y-pad
    y2 = y+h+(2*pad)

    height, width, channels = img.shape
    #print(str(height) + " " + str(width))
    if(x1 < 0):
        x1 = 0
    if(y1 < 0):
        y1 = 0
    if(x2 > width):
        x2 = width
    if(y2 > height):
        y2 = height
    crop_img = img[y1:y2, x1:x2]
    return crop_img

def save_img(img, name):
    cv2.imwrite(name, img)
    return

def visualize_and_label(img, text, ymin, xmin, ymax, xmax, color=(0, 0, 0), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness)
    cv2.putText(img, text, (xmin, ymin), font, 0.5, color, 2, cv2.LINE_AA)
    return img

# For Sorting Contours
def get_contour_precedence(contour, cols):
    tolerance_factor = 10
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

def find_components(img, originalImage, ratio):
    _, cnts, hierarchy = cv2.findContours(img.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cnts.sort(key=lambda x:get_contour_precedence(x, img.shape[1]))
    
    imageAllContours = originalImage.copy()
    for idx, c in enumerate(cnts):
        #print(str(idx) + ' - ' + str(cv2.contourArea(c)))
        c = c.astype('float')
        c *= ratio
        c = c.astype('int')

        # compute the center of the contour
        M = cv2.moments(c)
        
        x, y, w, h = cv2.boundingRect(c)
        #cv2.drawContours(imageAllContours, [c], -1, (0, 0, 0), 2)
        if cv2.contourArea(c) > 30:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #print(str(cv2.boundingRect(c)))
            #print('x1 = ' + str(x) + ' x2 = ' + str(x+w) + ' y1 = ' + str(y) + ' y2 =' + str(y+h))
            cropped = pad_and_crop(originalImage, c)
            filename = 'rect' + str(idx) + '.jpg'
            save_img(cropped, filename)
            res = labelImage.predict('rect' + str(idx) + '.jpg')
            label, accuracy = res	        
            cv2.putText(imageAllContours, label, (x, y), 0, 0.5, (0, 255, 0), cv2.FONT_HERSHEY_PLAIN, cv2.LINE_AA)
            cv2.rectangle(imageAllContours, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            components.append([x, y, x+w, y+h, cX, cY, label, accuracy, filename])
    save_img(imageAllContours, 'image-detected.allcontours.jpg')

def components_to_json(img):
    json_data = {}
    image_info = {}
    im_height, im_width = img.shape[:2]
    image_info['height'] = im_height
    image_info['width'] = im_width
    json_data['image_info'] = image_info
    data = []
    for idx, item in enumerate(components):
        x1, y1, x2, y2, cX, cY, label, accuracy, filename = item
        comp = {}
        comp['x1'] = x1
        comp['y1'] = y1
        comp['x2'] = x2
        comp['y2'] = y2
        comp['cx'] = cX
        comp['cy'] = cY
        comp['left'] = (x1 * 100) / im_width 
        comp['top'] = (y1 * 100) / im_height 
        comp['right'] = ((im_width - x2) * 100) / im_width 
        comp['bottom'] = ((im_height - y2) * 100) / im_height 
        comp['label'] = label
        comp['accuracy'] = str(accuracy)
        comp['filename'] = filename
        if(accuracy > 0.8):
            comp['trulyPredicted'] = 'true'
        else:
            comp['trulyPredicted'] = 'false' 
        data.append(comp)
    
    
    json_data['components'] = data
    with open('../../compoenents_map.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)
    with open('compoenents_map.json', 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True,
                help='path to the input image')
    
    args = vars(ap.parse_args())
    imageName = os.path.splitext(os.path.basename(args['image']))[0].replace(" ", "")
    image = cv2.imread(args['image'])
    imageOld = cv2.imread('predict/card.jpg')
    #Change Current Working Directory
    
    os.chdir('predicted')    
    if(os.path.exists(imageName) == False):
        os.mkdir(imageName)
    else: 
        shutil.rmtree(imageName)
        os.mkdir(imageName)
    os.chdir(imageName)

    resized = downscale_image(image)
    ratio = image.shape[0] / float(resized.shape[0])
    filtered = apply_filters(resized)
    
    try:
        find_components(filtered, image, ratio)
        print(components)
        components_to_json(image)
    except Exception as e:
        print('%s %s' % (imageName, e))