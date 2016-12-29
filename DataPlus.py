# Load image in cv2                 | Done[x]
# Reshape width to +30%             | Done[x]
# Reshape height to +30%            | Done[x]
# Mirror to vertical axis           | Done[x]
# Create folder                     | Done[x]
# Give to each image specific 
# name, starts with barcode 
# and ends with a number 
# (can set by timer value)          | Done[x]
# Create Labels.txt, depending
# on <imagename> in new folder      | Done[x]

import cv2
import numpy as np
import os, argparse, time, re
from shutil import copyfile
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--first',
                    help = 'Write correct path to first class images with "/" in the end. \nDefault path is: /home/nik/Downloads/barcodes/')
parser.add_argument('-s', '--second',
                    help = 'Write correct path to second class images with "/" in the end.')
parser.add_argument('-d','--dir', default = '/home/nik/Documents/',
                    help = 'Write path to the folder, where you want to save images.')
args = vars(parser.parse_args())
first = args["first"]; second = args["second"]; directory = args["dir"]

print('>  Arguments are loaded.')

pool = os.listdir(first)
Images = []
for image in pool:
    Images.append(cv2.imread( str(first) + str(image) ))

def width(image_):
    sizeX, sizeY = image_.shape[1], image_.shape[0]
    return cv2.resize(image_, ( sizeX + int(sizeX*0.3), sizeY ))
def height(image_):
    sizeX, sizeY = image_.shape[1], image_.shape[0]
    return cv2.resize(image_, ( sizeX, sizeY + int(sizeY*0.3) ))
def mirror(image_):
    return cv2.flip(image_,1)

# Reshaped images
PlusImages = []
for sample in Images:
    Operations = [width(sample), height(sample), mirror(sample)]
    for changes in Operations:
        PlusImages.append(changes)

newfolder = str(directory) + 'BarcodeImages-{}i'.format(len(Images)+len(PlusImages))

print('>  PlusImages have been created.\n-  New folder created.')

def newFolder():
    os.mkdir(newfolder)
    time_ = time.ctime()
    fin = re.findall(r'(\d{2}:\d{2}):\d{2} (\d{4})', str(time_))
    ImagesA = np.asarray(Images)
    PlusImagesA = np.asarray(PlusImages)
    for fileI in range(len(Images)):
        IImN = str(str(newfolder) + '/BarcodeOrig_'+str(fin[0][0])+'_'+str(int(np.random.random()*int(np.random.randint(1000,size = 1))))+str(fin[0][1]))
        nameIOrig = str(IImN) + '.png'
        
        # Used by debugging #
        '''try:
            nameIOrig = str(IImN) + '.png'
            with open(nameIOrig, 'w') as fileIOrig:
                fileIOrig.write(ImagesA[fileI].tostring())
        except:
            i_o = Image.fromarray(ImagesA[fileI])
            i_o.save(str(nameIOrig))'''
        #                   #
        
        i_o = Image.fromarray(ImagesA[fileI])
        i_o.save(str(nameIOrig))
        
    for fileP in range(len(PlusImages)):
        PImN = str(str(newfolder) + '/BarcodePlus_'+str(fin[0][0])+'_'+str(int(np.random.random()*int(np.random.randint(1000,size = 1))))+str(fin[0][1]))
        nameIPlus = str(PImN) + '.png'
        
        i_p = Image.fromarray(PlusImagesA[fileP])
        i_p.save(str(nameIPlus))
    # It works too! 
    '''[cv2.imwrite('BarOrig{}.png'.format(numI),np.array(fileI)) for numI, fileI in enumerate(Images)]
    [cv2.imwrite('BarPlus{}.png'.format(numP),np.array(fileP)) for numP, fileP in enumerate(PlusImages)]'''
 
newFolder()
print('>  New folder name:{}.\n-  Pictures saved.'.format(str(newfolder)))

# Second class images
source = os.listdir(second)
for im in source:
    copyfile(str(second)+str(im), str(newfolder) + '/' + str(im))

names = []
for n_ in os.listdir(newfolder):
    names.append(n_)
    
All_Images = Images + PlusImages
with open(str(newfolder) + '/' + 'LoP.txt', 'w') as file:
    for lab in range(len(names)):
        pattern = 'Barcode'
        if re.findall(pattern, str(names[lab])):
            file.write('1\n')
        else:
            file.write('0\n')
##        B_Original = re.findall( r'BarcodeOri', str(lab))
##        B_Plus = re.findall( r'BarcodePlu', str(lab))
##        if B_Original != True or B_Plus != True:
##            file.write('1\n')
##        else:
##            file.write('0\n')
print('>  Labels file "LoP.txt" created.')

cv2.waitKey()
cv2.destroyAllWindows()
