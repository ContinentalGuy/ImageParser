# Sliding window
# Coordinates X, Y      Done[x]
# Step                  Done[x]
# Show                  Done[x]
# Flag parameter        Done[]

import cv2
import numpy as np
            
image = cv2.imread('???.png')

def window(src, step, size):
    y,x,z = np.shape(src)
    xB = x + size[0]
    yB = y + size[1]
    for X in range(0, x, step[0]):
        for Y in range(0, y, step[1]):
            yield (X, Y, size)

try:
    for (x, y, size) in window(image, (50,50), (100,100)):
        copy = image.copy()
        cv2.rectangle(copy, (x, y), (x + size[1], y + size[0]), (0,100,0), 2)
        cv2.imshow('',copy)
        # Digit inside the brackets means the milliseconds
        cv2.waitKey(50)
except:
    print('Something is wrong.')

cv2.destroyAllWindows()
