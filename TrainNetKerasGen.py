from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense


# dimensions of our images.
sizeX, sizeY = 150, 150

trainDirectory = 'data/train'
validationDirectory = 'data/validation'
trainData = 100
validationData = 40
epochs = 5

# ConvNet Model.
model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, sizeX, sizeY)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',
              metrics=['accuracy'])

# Generate images for training
trainDataGenerated = ImageDataGenerator(rescale=1./255,
        shear_range=0.2,zoom_range=0.2,
        horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
testDataGenerated = ImageDataGenerator(rescale=1./255)

trainGenerator = trainDataGenerated.flow_from_directory(
        trainDirectory,target_size=(sizeX, sizeY),
        batch_size=32,class_mode='binary')

validationGenerator = testDataGenerated.flow_from_directory(
        validationDirectory,target_size=(sizeX, sizeY),
        batch_size=32,class_mode='binary')

model.fit_generator(trainGenerator,samples_per_epoch=trainData,
        nb_epoch=epochs,validation_data=validationGenerator,
        nb_val_samples=validationData)

model.load_weights('convnet_weights.h5')
