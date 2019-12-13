
'''
helper functions to read in images
'''

import csv
from scipy import ndimage

def get_lines(csv_path):
    
    lines = []
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        for ind, line in enumerate(reader):
            if ind!=0:
                lines.append(line)
    
    return lines

def load_images(lines, images_path, col, correction_factor):
    
    images = []
    measurements = []
    
    for line in lines:
        # Load images
        source_path = images_path + line[col].strip()
        image = ndimage.imread(source_path)
        images.append(image)
        measurement = float(line[3])
        measurements.append(measurement + correction_factor)

    return images, measurements

def read_full_data_set(lines_path, images_path, correction_factor):
    
    lines = get_lines(lines_path)

    images, measurements = load_images(lines, images_path, 0, 0)
    left_images, left_measurements = load_images(lines, images_path, 1, correction_factor)
    right_images, right_measurements = load_images(lines, images_path, 2, -correction_factor)

    # Adding left and right images to the training data set
    images.extend(left_images)
    images.extend(right_images)
    measurements.extend(left_measurements)
    measurements.extend(right_measurements)
    
    return images, measurements