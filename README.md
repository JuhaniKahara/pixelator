# pixelator

This project turns images in to G-code coordinates. The scripts were used in an art project in summer 2020 to produce drawing coordinates for a CNC-drawing robot.
Two different types of approaches were used: Zigzag and RandomDraw.

## Method 1 - Zigzag

How it works?

1. Turns image to a greyscale image
2. Scales it with scale parameter to get the desired amount of pixels
3. For each pixel in the original image:
   - Determine how many lines should be drawn using the greyscale image and color thresholds
   - Draw the zigzag pattern with given number of lines to the pixel
  
Example of original photo (left) and the end result (right). The real life size of the end result is approx. 26cmx26cm.
  
![Image of President](https://github.com/JuhaniKahara/pixelator/blob/master/images/kekko_both.png)

## Method 2 - RandomDraw

This method iteratively generates random candidate lines and draws the best one based on the original image and scoring function.

The score for a line:

1. Determine the pixels that the line would overlap
2. Each pixel gets a score based on the color (scorePoint-function)
2. Sum the score of individual pixels

When the best line has been chosen, set the corresponding pixels in the original image to white (=no score / minus score from these pixels from now on)
