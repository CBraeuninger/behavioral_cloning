'''
Generator to load and preprocess the training and validation data
'''

from read_images import read_images_lcr
import numpy as np
from sklearn.utils import shuffle

def generator(samples, batch_size=32):

    num_samples = len(samples)

    while 1: # Loop forever so the generator never terminates

        shuffle(samples)

        for offset in range(0, num_samples, batch_size):

            batch_samples = samples[offset:offset+batch_size]
            
            images = []
            measurements = []
            
            for batch_sample in batch_samples:
                im, meas, l_im, l_meas, r_im, r_meas = read_images_lcr(batch_sample.get_line(),
                                                                       batch_sample.get_images_path(),
                                                                       batch_sample.get_correction_factor())
                images.append(im)
                measurements.append(meas)
                images.append(l_im)
                measurements.append(l_meas)
                images.append(r_im)
                measurements.append(r_meas)
                                 
            # Data augmentation

            flipped_images = []
            flipped_measurements = []

            # Generate additional data by flipping the image and taking the negative of the steering wheel angle
            for i in range(len(images)):
                flipped_image = np.fliplr(images[i])
                flipped_images.append(flipped_image)
                flipped_measurement = - measurements[i]
                flipped_measurements.append(flipped_measurement)

            # Concatenate original and flipped data to get the complete training/validation set
            concat_images = images + flipped_images
            concat_measurements = measurements + flipped_measurements

            X_train = np.array(concat_images)
            y_train = np.array(concat_measurements)

            yield shuffle(X_train, y_train)



