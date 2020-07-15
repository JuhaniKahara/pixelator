import sys
import argparse
import logging
from PIL import Image
import time

outfile = 'out.txt'

def get_even_thresholds(n):
    thresholds = [0]
    step = 255 / n
    for i in range(n-1):
        thresholds.append((i + 1) * step)
    thresholds.append(255)
    return thresholds

def get_thresholds(n):
    return [0, 60, 105, 155, 190, 255]

def choose_color(data, thresholds):
    for i in range(len(thresholds)):
        if data[0] <= thresholds[i]:
            return i-1

def print_pixels(data , thresholds):
    file = open(outfile, 'w')
    for j in range(data.size[1]):
        for i in range(data.size[0]):
            color = choose_color(data.getpixel((i, j)), thresholds)
            #previewColor
            p = round((thresholds[color] + thresholds[color+1]) / 2)
            data.putpixel((i,j), (p, p, p))
            file.write((str(color) if color > 9 else ' ' + str(color)) + ' ,')
        file.write('\n\n')
    file.close()
    #data.show()
    print(data.size)
    data.save("outcustom3.png")
    print("OK")

def handle_image(filename, scale, n):
    im = Image.open(filename)
    data = im.convert('LA').convert('RGB')
    dim = tuple(im.size)
    print(dim)
    data.thumbnail((round(dim[0]*scale), round(dim[1]*scale)))
    print_pixels(data, get_thresholds(n))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--scale', dest='scale', type=float, help='Scale')
    parser.add_argument('-n', '--colors', dest='n', type=int, default=4, help='Number of colors')
    parser.add_argument('file', metavar='file', type=str, help='Source filename')

    args = parser.parse_args()
    handle_image(args.file, args.scale, args.n)
