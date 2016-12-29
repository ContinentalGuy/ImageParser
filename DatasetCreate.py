import numpy as np
import cv2, os, argparse, pickle, re
import csv, time
from imutils import paths
import progressbar

# Set directory                     | Done[x]
# Load images into numpy arrays     | Done[x]
# Resize images to one size         | Done[x]
# Set number of layers in ndaray    | Done[x]
# Creating dictionary               | Done[x]
# Save dictionary                   | Done[x]

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--folderFrom', required = True,
                    help = 'Folder to load images. Example: /home/nik/Documents/???-Images-?i/')
parser.add_argument('-t', '--folderTo', required = True,
                    help = 'Folder to save dataset. Example: /home/nik/Python3.5/')
parser.add_argument('-s','--size', default = (140,90),
                    help = 'Size of reshaped images. Example: 140,90')
args = vars(parser.parse_args())

# Create variables from parsed arguments
folder = args["folderFrom"]
folderTo = args["folderTo"]
sizeY,sizeX = args["size"].split(',')

#---------- Remove after testing --------
#folder = '/home/nik/Downloads/barcodes/'
#----------------------------------------

# List all files in folder.
pool = os.listdir(folder)

# Append values ro resize our pictures. Default value.
(sizeY, sizeX) = (140,90)

# Tuples for Images, Labels, Picture names, ...
Images = []
Labels = []
Names = []
failPictures = []
failPicNums = []

# Progressbar widget.
bar = progressbar.ProgressBar(widgets = [
    '>  [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',])

# Fill "Name" tuple with image names.
print('>  Append image names to pool.')
for n_ in bar(os.listdir(folder)):
    Names.append(n_)
    time.sleep(0.005)

# Print all images inside choosen folder.
print('>  Example:')
for image in range(0,len(Names), 25):#range(len(Names)):
    print('-    '+str(folder)+str(Names[image]))

# Fill "Labels" tuple with 1/0.
# Depends on image name.
for label in range(len(Names)):
    pattern = 'Barcode'
    if re.findall(pattern, str(Names[label])):
        #file.write('1\n')
        Labels.append(1)
    else:
        #file.write('0\n')
        Labels.append(0)
print('>  List "Labels" created.')

# Load arrays by image names and check their condition.
print('_'*70)
for num, image in enumerate(pool):
    try:
        im = cv2.imread((str(folder)+str(image)), 0)
        resIm = cv2.resize(im, (sizeY,sizeX)).flatten()
        Images.append(resIm)
        #Used for testing with only one type of images
        #Labels.append(1)
    except Exception as e:
        #print(e)
        failPictures.append(str(num)+':'+str(folder)+str(image))
        failPicNums.append(num)
        Labels.pop(num)
print('_'*70)

# Print picture name, that can not be loaded by some reasons.
print('>  Broken pictures:')
for fP in range(len(failPictures)):
  print('-    '+str(failPictures[fP]))

# Create "Labels.txt".
for element in Labels:
    with open(str(folderTo)+'/'+'Labels.txt','a') as file:
        file.write(str(element)+'\n')
print('>  File "Labels.txt" amended.')

Labels = np.reshape(Labels, (len(Labels),1))

print('>  Images: '+str(np.shape(Images))+' ||| Content: '+str(Images[0])+'\n'+'>  Labels: '+str(np.shape(Labels))+' ||| Content: '+str(Labels[0]))

NumberLabel, LabelRow = np.shape(Labels)
LayersImg, LengthImg = np.shape(Images)
if LayersImg == NumberLabel:
    Layers = LayersImg
    Images = np.asarray(Images)
    print('>  Number of Labels are equal to Image layers: ' + str(Layers))
    Dataset = {'Images':Images,'Labels':Labels,'Size':(sizeY,sizeX)}

    def saveCSV():
        sF = csv.writer(open((str(folderTo)+'BARCODE-dataset-{}i'.format(len(Images))),'w'))
        for key, val in Dataset.items():
            sF.writerow([key, val])
    #saveCSV()

    def loadCSV(path):
        dataDict = {}
        for key, val in csv.reader(open(path)):
            dataDict[key] = val
            return dataDict
    #dataDict = loadCSV()

    def saveNPY(dictionary):
        fileNPY = np.save((str(folderTo)+'BARCODE-dataset-{}i'.format(len(Images))), dictionary)
    saveNPY(Dataset)
    print('>  Dataset from dictionary created.\n')

    def loadNPY(path):
        fileNPY = np.load(path)
        dictionary = fileNPY.tolist()
        return dictionary
else:
    print('>  Something went wrong.\n-    Stop.\n')

cv2.waitKey()
cv2.destroyAllWindows()
