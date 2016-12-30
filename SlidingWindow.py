# Sliding window
# Coordinates X, Y      Done[x]
# Step                  Done[x]
# Show                  Done[x]
# Flag parameter        Done[x]

import cv2
import numpy as np

image = cv2.imread('/home/nik/Downloads/BarcodesProject/PHOTO.png')

def window(src, size):
    y,x,z = np.shape(src)
    stepX, stepY = (size[1]/2,size[0]/2)
    for X in range(0, x, int(stepX)):
        for Y in range(0, y, int(stepY)):
            yield (X, Y, size)

def flag(x,y,size,prediction,train,list_):
    xB = x + size[1]
    yB = y + size[0]
    location = (x,y,xB,yB)
    if np.equal(prediction,train) == True:
        list_.append(location)
        cv2.rectangle(image, (x, y), (xB, yB), (255,255,255), 2)
        cv2.waitKey(30)
    else:
        pass

def run(image,speed=100):
    try:
        for (x, y, size) in window(image, (60,60)):
            xB = x + size[1]
            yB = y + size[0]
            copy = image.copy()
            cv2.rectangle(copy, (x, y), (xB, yB), (250,25,15), 2)
            cv2.imshow('',copy)

            # Here should be flag function.
            
            # Digit inside the brackets means the milliseconds.
            # Change this parameter to increase or decrease speed.
            # It also will affect the result.
            cv2.waitKey(speed)
    except Exception as e:
        print('>  Can\'t slide through this image.')
        print('-    ' + str(e))

cv2.destroyAllWindows()
