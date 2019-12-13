import cv2
import numpy as np
from read_images import get_lines

'''
Load the data
'''

# Correction factor to correct steering angle for left and right camera image
correction_factor = 0.2

# Read in data supplied by Udacity
udacity_lines = get_lines('../../../opt/carnd_p3/data/driving_log.csv')
#images, measurements = read_full_data_set('../../../opt/carnd_p3/data/driving_log.csv',
#                                          '../../../opt/carnd_p3/data/', correction_factor)

# Read in addtionally collected data (allows the model to learn how to disengage from the borders)
add_lines = get_lines('additional_data/driving_log.csv')
#add_images, add_measurements = read_full_data_set('additional_data/driving_log.csv',
#                                                  '../../..', correction_factor)

images.extend(add_images)
measurements.extend(add_measurements)

# Read in data collected while driving counter-clockwise
counter_images, counter_measurements = read_full_data_set('counter_clockwise/driving_log.csv',
                                                          '../../..', correction_factor)

images.extend(counter_images)
measurements.extend(counter_measurements)
    
'''
Data augmentation
'''

flipped_images = []
flipped_measurements = []

# Generate additional data by flipping the image and taking the negative of the steering wheel angle
#for i in range(len(images)):
#    flipped_image = np.fliplr(images[i])
#    flipped_images.append(flipped_image)
#    flipped_measurement = - measurements[i]
#    flipped_measurements.append(flipped_measurement)

concat_images = images #+ flipped_images
concat_measurements = measurements #+ flipped_measurements

# Concatenate original and flipped data to get the complete training/validation set
X_train = np.array(concat_images)
y_train = np.array(concat_measurements)

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
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, epochs=7)

model.save('model.h5')
          