#from keras.layers.convolutional import Convolution1D, Convolution2D, MaxPooling2D
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
import numpy as np
import cv2, argparse


parser = argparse.ArgumentParser()
parser.add_argument('-d','--dataset',
                    help = 'Load dataset from path.')
parser.add_argument('-e','--epochs',type = int, default = 5,
                    help = 'Number of epochs. Default = 5.')
parser.add_argument('-p', '--percntg', type = int, default = 50,
                    help = 'Percentage of training and testing datas. Default = 50%.')
parser.add_argument('-c','--classes', default = 1,
                    help = 'Number of class images. Default = 1.')
args = vars(parser.parse_args())

dataset = args["dataset"]
epochs = int(args["epochs"])
percntg = int(args["percntg"])
classes = int(args["classes"])

def load_dataset(path):
        fileNPY = np.load(path)
        dictionary = fileNPY.tolist()
        Images = np.asarray(dictionary['Images'])
        Labels = np.asarray(dictionary['Labels'])
        sizeY,sizeX = dictionary['Size']
        depth = np.shape(Images)[0]
        return Images, Labels, sizeY, sizeX, depth

D_Images, D_Labels, sizeY, sizeX, depth = load_dataset(dataset)

##print('D_Images, D_Labels, sizeY, sizeX, depth'+'\n'+str(D_Images)+'\n'+str(D_Labels)+'\n'+str(sizeY)+'\n'+str(sizeX)+'\n'+str(depth)+'\n')

# Prepare data to correct form.
D_Images = np.reshape(D_Images, (depth, sizeX, sizeY))
D_Images = D_Images[np.newaxis, :, :, :]
##D_Labels = np_utils.to_categorical(D_Labels,2)

# Slice function.
def slice_(Data, Labels, percentage):
    d_size = Data.shape
    l_size = Labels.shape
    if d_size[0] == l_size[0]:
        Full = d_size[0]
        Divid = int(Full * percentage/100)
        print('>  Slicing by {}%. ||| Index: '.format(percentage)+str(Divid))
        return Divid

Value = slice_(D_Images, D_Labels, percntg)

# Slice data to train set...
Image_train = D_Images[:Value]
Labels_train = D_Labels[:Value]

# ...and test set.
Image_test = D_Images[Value:]
Labels_test = D_Labels[Value:]

# Add CNN model.

'''
# First model. Work's fast and gives 50% accuracy.
model = Sequential()
model.add(Convolution2D(64,5,5, border_mode = 'same', input_shape = (depth, sizeY, sizeX)))
model.add(Convolution2D(32,5,5, border_mode = 'same'))
model.add(Activation("softmax"))
'''

#'''
# Second model. Work's well on correct dataset, created with keras library.
model = Sequential()
model.add(Convolution2D(32,3,3, input_shape=(depth,sizeX,sizeY)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten(input_shape = Image_train.shape[1:]))
model.add(Dense(256, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation = 'sigmoid'))
#'''

'''
# Third model.
model = Sequential()
# First layer.
model.add(Convolution2D(20,5,5, input_shape = (depth, sizeY, sizeX)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2), strides = (2,2), dim_ordering = "th"))
# Second layer.
model.add(Dense(32, input_dim = Image_train.shape[1]))
model.add(Activation("softmax"))
'''

# Compile model.
model.compile(loss = 'binary_crossentropy', optimizer = 'sgd',
              metrics = ["accuracy"])

# Fit training images and labels.
print('>  Number of epochs: {}'.format(epochs))
model.fit(Image_train, Labels_train, nb_epoch = epochs, batch_size = 10, shuffle = 'batch')

# Evaluating model.
parameters = model.evaluate(Image_test, Labels_test, batch_size = 30)

model.save_weights('cnn_weights.hdf5')
