# !/usr/bin/env python

import os
import re
import numpy
import pytesseract
import tkinter

from PIL import Image
from scipy.misc import imsave


FOLDER = 'images'
THRESHOLDS = [30, 20, 40, 50, 70, 100, 120]
AREA = (200, 110, 300, 170)
VALUES = []


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


def run():
    with open('output.txt', 'w') as output_file:

        image_files = sorted(os.listdir(FOLDER))[0: 20]

        for image_name in image_files:
            img = Image.open(os.path.join(FOLDER, image_name))
            cropped_img = img.crop(AREA)

            value = ''
            for t in THRESHOLDS:
                cropped_img = binarize_image(cropped_img, t)
                text = pytesseract.image_to_string(cropped_img)

                floats = re.findall(r'\d+[,|\.]\d+', text)

                if len(floats) > 0:
                    value = float(floats[0].replace(',', '.'))
                    if len(VALUES) > 0:
                        #std = numpy.std(values)
                        #avg = numpy.average(values)
                        #if std == 0 or (avg + std*2 > value > avg - std*2):
                        VALUES.append(value)
                        #    break
                    else:
                        VALUES.append(value)
                        break

            output_file.write(str(value) + '\n')


if __name__ == '__main__':
    pass
    #run()

    #import wx
    #app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    #frame = wx.Frame(None, wx.ID_ANY, "Hello World")  # A Frame is a top-level window.
    #frame.Show(True)  # Show the frame.
    #app.MainLoop()


    #top = tkinter.Tk()
    #top.mainloop()
