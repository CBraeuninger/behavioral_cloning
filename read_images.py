
'''
helper functions to read in images
'''

from scipy import ndimage

def read_image(line, images_path, col, correction_factor):
    
    # Load image
    source_path = images_path + line[col].strip()
    image = ndimage.imread(source_path)
    measurement = float(line[3]) + correction_factor

    return image, measurement

def read_images_lcr(line, images_path, correction_factor):
    
    image, measurement = read_image(line, images_path, 0, 0)
    left_image, left_measurement = read_image(line, images_path, 1, correction_factor)
    right_image, right_measurement = read_image(line, images_path, 2, -correction_factor)
    
    return image, measurement, left_image, left_measurement, right_image, right_measurement