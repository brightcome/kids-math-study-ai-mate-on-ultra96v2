'''
Liu Minglai
12/11/2020 4:35:30 PM
modify based on
https://github.com/AlexeyAB/darknet/blob/master/scripts/voc_label.py
change to poker card image path style
History:
v00: initial version, the py scripts should be moved to image folders.
v01: can process both train and valid
v02: simplify the train/valid folder shift, add file list gen function.
v03: solve ".jpg"/"JPG" issue
'''
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob

#image dataset definition
sets=['train','test']

#modify the class name as follow, expend to all 13 cards number
classes = ["ace", "jack", "king", "nine", "queen", "ten"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('./%s.xml'%(image_id))
    out_file = open('%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# convert the images in the "valid"&"valid" folder
for image_set in sets:
    list_file = open('%s_list.txt'%(image_set), 'w')
    for image_id in glob.glob(image_set + '/*.[jJ][pP][gG]'): #check *.jpg/*.JPG
        image_file = image_id.split('.')[0]
        print(image_file)
        convert_annotation(image_file)
        list_file.write(image_id + '\n')              #generate the image file list
    list_file.close()
    print(image_set, 'image convert done.')

print('xml to yolo format convert done.')
