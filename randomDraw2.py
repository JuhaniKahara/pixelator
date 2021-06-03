import sys
import argparse
import cv2
from matplotlib import pyplot as plt
import logging
from PIL import Image
import numpy as np
import time
import sys
from numpy import random
import math
from datetime import datetime
import configparser

black = (0, 0, 0)

def draw(x, y, outfile, k):
    x=round(k*x,2)
    y=round(k*y,2)
    outfile.write('G01 X{} Y{} F3000\n'.format(x, y))

def choose_pixels(p1, p2):
    d = round(math.hypot(p2[0] - p1[0], p2[1] - p1[1]))
    return list(zip(np.linspace(p1[0], p2[0], d),
                   np.linspace(p1[1], p2[1],d)))

def scorePoint(color, whitePenalty):
    if color == 1:
        return whitePenalty
    if 0.1 < color < 0.5:
        return 0
    return 1-color

def scoreLine(img, pixels, whitePenalty):
    score = 0
    pos = pixels[0]
    for pos in pixels:
        score = score + scorePoint(img[pos[1], pos[0], 0], whitePenalty)
    return score

def whitenPixels(img, pixels):
    #Sets pixels to white in the template image
    for pix in pixels:
        img[pix[1]][pix[0]]=1
    return img

def getNewCoords(x, y, dim, config, angle):
    while True:
        if int(config['draw']['angleMin']) < int(config['draw']['angleMax']):
            min = int(config['draw']['angleMin'])
            max = int(config['draw']['angleMax'])
        else:
            max = int(config['draw']['angleMin'])
            min = int(config['draw']['angleMax'])
        angle = angle + random.randint(min, max) * math.pi / 180
        r = random.randint(int(config['draw']['rMin']), int(config['draw']['rMax']))
        xNew = x + round(r * math.cos(angle))
        yNew = y + round(r * math.sin(angle))
        if 0<xNew<dim[1] and 0<yNew<dim[0]:
            return xNew, yNew, angle

def handle_pixels(image, config):
    # Create empty image
    height = image.shape[0]
    width = image.shape[1]
    finalImg = np.ones((height, width, 3))
    outfile = open('out_{}.txt'.format(datetime.now().strftime('%Y %m %d %H:%M:%S')), 'w')

    x = random.randint(0,width)
    y = random.randint(0,height)
    angle = 0
    draw(x, y, outfile, 1)
    outfile.write('G01 Z3.00 F3000\n')
    for j in range(int(config['draw']['nLines'])):
        scores = []
        points = []
        pixelList = []
        for i in range(int(config['draw']['nSamples'])):
            x2, y2, angle = getNewCoords(x, y, image.shape, config, angle)
            pixels = choose_pixels((x, y),(x2, y2))
            pixels = [(round(num[0]), round(num[1])) for num in pixels]
            pixelList.append(pixels)
            scores.append(scoreLine(image, pixels, int(config['draw']['whitePenalty'])))
            points.append(((x, y),(x2, y2)))
        bestPoint=np.argmax(scores)
        bestPixels = pixelList[bestPoint]
        draw(x, y, outfile, 1)
        x = points[bestPoint][1][0]
        y = points[bestPoint][1][1]
        if config.getboolean('draw', 'whitenPixels'):
            image = whitenPixels(image, bestPixels)
        finalImg = cv2.line(finalImg, points[bestPoint][0],points[bestPoint][1],(0,0,0),1)

    outfile.close()
    plt.imshow(finalImg)
    plt.show()

def handle_image(filename, config):
    im = Image.open(filename)
    data = np.asarray(im.convert('LA').convert('RGB')) / 255
    handle_pixels(data, config)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', metavar='file', type=str, help='Source filename')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')
    handle_image(args.file, config)

