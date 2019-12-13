import cv2
import math
import numpy as np
from data_set import DataSet
from sample import Sample
from data_generator import generator
from sklearn.model_selection import train_test_split

'''
Load the data
'''

# Correction factor to correct steering angle for left and right camera image
correction_factor = 0.2

# Read in data supplied by Udacity
udacity_data = DataSet('../../../opt/carnd_p3/data/driving_log.csv')
                        
# Read in addtionally collected data (allows the model to learn how to disengage from the borders)
add_data = DataSet('additional_data/driving_log.csv')

# Read in data collected while driving counter-clockwise
counter_data = DataSet('counter_clockwise/driving_log.csv')

samples = []

for line in udacity_data.get_lines():
    samples.append(Sample(line, '../../../opt/carnd_p3/data/', correction_factor))

for line in add_data.get_lines():
    samples.append(Sample(line, '../../..', correction_factor))

for line in counter_data.get_lines():
    samples.append(Sample(line, '../../..', correction_factor))
                   
train_samples, validation_samples = train_test_split(samples, test_size=0.2)

batch_size = 32

train_generator = generator(train_samples, batch_size=batch_size)
validation_generator = generator(validation_samples, batch_size=batch_size)

'''
Define and train the model
'''

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Conv2D, Cropping2D

model = Sequential()

model.add(Cropping2D(cropping=((60, 25),(0, 0)), input_shape=(160, 320, 3)))
model.add(Lambda(lambda x: x / 255.0 - 0.5))
model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2)))
model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2)))
model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2)))
model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1)))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
model.fit_generator(train_generator, steps_per_epoch=math.ceil(len(train_samples)/batch_size),
            validation_data=validation_generator,
            validation_steps=math.ceil(len(validation_samples)/batch_size),
            epochs=7, verbose=1)

model.save('model.h5')
          