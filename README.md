# pixelator

This project turns images in to G-code coordinates. The scripts were used in an art project in summer 2020 to produce drawing coordinates for a CNC-drawing robot.
Two different types of approaches were used: Zigzag and RandomDraw.

## Run with Python 3.6.8 (other Python 3 versions most likely work too)
Install required python packages to your environment:

`pip install -r requirements.txt`

## Method 1 - Zigzag

Try: `python zigzag.py -s 0.1 images/man.jpeg`

### How it works?

1. Turns image to a greyscale image
2. Scales it with scale parameter to get the desired amount of pixels
3. For each pixel in the original image:
   - Determine how many lines should be drawn using the greyscale image and color thresholds
   - Draw the zigzag pattern with given number of lines to the pixel
  
Example of original photo (left) and the end result (right). Original photo is from UKK-arkisto. The real life size of the end result is approx. 26cmx26cm.
  
![Image of President](https://github.com/JuhaniKahara/pixelator/blob/master/images/kekko_both.png)

## Method 2 - RandomDraw

Try: `python randomDraw2.py images/man.jpeg` (The end result is highly dependent on the image, configs and chance)

This method iteratively generates random candidate lines and draws the best one based on the original image and scoring function.

The score for a line:

1. Determine the pixels that the line would overlap
2. Each pixel gets a score based on the color (scorePoint-function)
2. Sum the score of individual pixels

When the best line has been chosen, set the corresponding pixels in the original image to white (=no score / minus score from these pixels from now on) before generating the next line.

## Art robot in action (RandomDraw mode)

The robot was built by Jaakko Mäntylä, designer and software developer from Tampere, Finland.

https://user-images.githubusercontent.com/28629173/120377966-7d1a9600-c326-11eb-933a-3322ed33346e.mp4



