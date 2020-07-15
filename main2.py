import sys
import argparse
import cv2
from matplotlib import pyplot as plt
import logging
from PIL import Image
import numpy as np
import time

#colors = [5, 4, 3, 2, 0]
colors = [ 4, 3, 2, 0]

def get_even_thresholds(n):
    thresholds = [0]
    step = 255 / n
    for i in range(n-1):
        thresholds.append((i + 1) * step)
    thresholds.append(255)
    return thresholds

def get_thresholds():
    #return [0, 60, 105, 155, 190, 255]
    return [0, 70, 140, 190, 255]

def drawSickSack(img, n, margin, pos, size):
    if n == 1:
        img = cv2.line(img, (pos[0], pos[1] + int(size / 2)), (pos[0] + size, pos[1] + int(size / 2)), (0, 0, 0), 1)
    elif n == 2:
        s = round(size / n)
        img = cv2.line(img, (pos[0], pos[1] + int(size / 2)), (pos[0]+s, pos[1]), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + s, pos[1]), (pos[0] + size, pos[1] + int(size / 2)) , (0, 0, 0), 1)
    elif n == 3:
        s = round(size / n)
        img = cv2.line(img, (pos[0], pos[1] + int(size / 2)), (pos[0] + s, pos[1]), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + s, pos[1]), (pos[0] + 2 * s, pos[1] + size), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + 2 * s, pos[1] + size), (pos[0] + size, pos[1] + int(size / 2)), (0, 0, 0), 1)
    elif n == 4:
        s = round(size / n)
        img = cv2.line(img, (pos[0], pos[1] + int(size / 2)), (pos[0] + s, pos[1]), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + s, pos[1]), (pos[0] + 2 * s, pos[1] + size), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + 2 * s, pos[1] + size), (pos[0] + 3 * s, pos[1]), (0, 0, 0), 1)
        img = cv2.line(img, (pos[0] + 3 * s, pos[1]), (pos[0] + size, pos[1] + int(size / 2)), (0, 0, 0), 1)



def testSickSack():
    finalImg = np.ones((100, 100 , 3)) * 255
    drawSickSack(finalImg, 4, 0, (0,0), 10)

    plt.imshow(finalImg)
    plt.show()


def drawLines(img, n, margin, pos, size):
    # Draws n evenly spaced lines to a square starting from pos
    dist = round(size / (n + 1))
    for i in range(n):
        img = cv2.line(img, (pos[0], pos[1]+(i+1)*dist), (pos[0]+size, pos[1]+(i+1)*dist),(0,0,0),1)

def choose_color(data, thresholds):
    for i in range(len(thresholds)):
        if data[0] <= thresholds[i]:
            return colors[i-1]

def handle_pixels(imageThumbnail):
    print('Size of the original greyscale thumbnail: ' + str(imageThumbnail.size))
    # Create empty image
    height = imageThumbnail.size[0]
    width = imageThumbnail.size[1]
    finalImg = np.ones((width * 10, height * 10 , 3)) * 255

    size = 10

    for i in range(height):
        for j in range(width):
            colors = choose_color(imageThumbnail.getpixel((i, j)), get_thresholds())
            #drawLines(finalImg, colors, 0, (size*i, size*j), size)
            drawSickSack(finalImg, colors, 0, (size * i, size * j), size)

    plt.imshow(finalImg)
    plt.show()

def handle_image(filename, scale):
    im = Image.open(filename)
    data = im.convert('LA').convert('RGB')
    dim = tuple(im.size)
    data.thumbnail((round(dim[0]*scale), round(dim[1]*scale)))
    handle_pixels(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--scale', dest='scale', type=float, help='Scale')
    parser.add_argument('-n', '--colors', dest='n', type=int, default=4, help='Number of colors')
    parser.add_argument('file', metavar='file', type=str, help='Source filename')

    args = parser.parse_args()
    #testSickSack()
    handle_image(args.file, args.scale)
