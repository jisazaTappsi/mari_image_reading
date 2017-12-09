import os
import re
import numpy
import pytesseract
from PIL import Image
from scipy.misc import imsave


def binarize_image(image, threshold):
    """Binarize an image."""
    image = image.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    arrays = binarize_array(image, threshold)
    imsave('tmp_img.jpg', arrays)
    return Image.open('tmp_img.jpg')


def binarize_array(numpy_array, threshold=100):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array


folder = 'images'
thresholds = [30, 20, 40, 50, 70, 100, 120]
area = (200, 110, 300, 170)
values = []

with open('output.txt', 'w') as output_file:

    image_files = sorted(os.listdir(folder))[0: 20]

    for image_name in image_files:
        img = Image.open(os.path.join(folder, image_name))
        cropped_img = img.crop(area)

        value = ''
        for t in thresholds:
            cropped_img = binarize_image(cropped_img, t)
            text = pytesseract.image_to_string(cropped_img)

            floats = re.findall(r'\d+[,|\.]\d+', text)

            if len(floats) > 0:
                value = float(floats[0].replace(',', '.'))
                if len(values) > 0:
                    #std = numpy.std(values)
                    #avg = numpy.average(values)
                    #if std == 0 or (avg + std*2 > value > avg - std*2):
                    values.append(value)
                    #    break
                else:
                    values.append(value)
                    break

        output_file.write(str(value) + '\n')
