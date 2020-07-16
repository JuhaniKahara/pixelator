import sys
import argparse
import cv2
from matplotlib import pyplot as plt
import logging
from PIL import Image
import numpy as np
import time
import sys

#colors = [5, 4, 3, 2, 0]
colors = [ 4, 3, 2, 0]
black = (0, 0, 0)

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


def draw(startX, startY, stopX, stopY, outfile, img):
    outfile.write('G01 X{} Y{}\n'.format(startX, startY))
    outfile.write('G00 Z0\n')
    outfile.write('G01 X{} Y{}\n'.format(stopX, stopY))
    img = cv2.line(img, (startX, startY), (stopX, stopY), black, 1)


def drawSickSack(img, n, margin, pos, size, outfile):
    if n == 0:
        outfile.write('G00 Z2.00\n')
        return None
    if n == 1:
        startX = pos[0]
        startY = pos[1] + int(size / 2)
        stopX = pos[0] + size
        stopY = pos[1] + int(size / 2)
        draw(startX, startY, stopX, stopY, outfile, img)
    elif n > 1:
        s = round(size / n)
        y_stop = pos[1] + int(size / 2)
        for i in range(n):
            if i == 0:
                # Starting y-coordinate is in the middle of the square
                startX = pos[0]
                startY = y_stop
                stopX = pos[0] + (i + 1) * s
                stopY = pos[1]
            elif i == n - 1:
                # Stopping y-coordinate is in the middle of the square
                startX = pos[0] + i * s
                startY = (n % 2) * size + pos[1]
                stopX = pos[0] + size
                stopY = y_stop
            else:
                # Y coordinate is at top or bottom of the square
                startX = pos[0] + i * s
                startY = ((i + 1) % 2) * size + pos[1]
                stopX = pos[0] + (i + 1) * s
                stopY = (i % 2) * size + pos[1]
            draw(startX, startY, stopX, stopY, outfile, img)


def testSickSack():
    finalImg = np.ones((100, 100 , 3)) * 255
    file = open('out.txt','w')

    drawSickSack(finalImg, 4, 0, (30,30), 12, file)

    plt.imshow(finalImg)
    plt.show()


def drawLines(img, n, margin, pos, size):
    # Draws n evenly spaced lines to a square starting from pos
    # Margin not supported yet
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
    size = 6
    finalImg = np.ones((width * size, height * size , 3)) * 255

    outfile = open('outTest.txt', 'w')
    for i in range(height):
        for j in range(width):
            colors = choose_color(imageThumbnail.getpixel((i, j)), get_thresholds())
            #drawLines(finalImg, colors, 0, (size*i, size*j), size)
            drawSickSack(finalImg, colors, 0, (size * i, size * j), size, outfile)

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

