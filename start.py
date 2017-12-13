# !/usr/bin/env python
import os
import re
import wx
import numpy
import pytesseract

from PIL import Image
from scipy.misc import imsave


FOLDER = 'images'
THRESHOLDS = [30, 20, 40, 50, 70, 100, 120]
VALUES = []


def get_image_coordinates():
    try:
        with open('image_coordinates') as f:
            return [int(i) for i in f.read().split(',')]
    except FileNotFoundError:
        return [230, 130, 300, 170]


area = get_image_coordinates()


def set_image_coordinates(area):
    with open('image_coordinates', 'w') as f:
        f.write(', '.join([str(i) for i in area]))


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

        image_files = sorted(os.listdir(FOLDER))

        for image_name in image_files:
            img = Image.open(os.path.join(FOLDER, image_name))
            cropped_img = img.crop(area)

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


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Lectura de imagenes automática")
        panel = wx.Panel(self, wx.ID_ANY)

        self.text0 = wx.TextCtrl(panel, value=str(area[0]), pos=(20, 30))
        self.text1 = wx.TextCtrl(panel, value=str(area[1]), pos=(150, 30))
        self.text2 = wx.TextCtrl(panel, value=str(area[2]), pos=(20, 90))
        self.text3 = wx.TextCtrl(panel, value=str(area[3]), pos=(150, 90))

        self.Bind(wx.EVT_TEXT, self.on_x_coordinate0, self.text0)
        self.Bind(wx.EVT_TEXT, self.on_x_coordinate1, self.text1)
        self.Bind(wx.EVT_TEXT, self.on_x_coordinate2, self.text2)
        self.Bind(wx.EVT_TEXT, self.on_x_coordinate3, self.text3)

        read_button = wx.Button(panel, id=wx.ID_ANY, label="Leer")
        read_button.Bind(wx.EVT_BUTTON, self.onButton)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(read_button, 150, wx.ALL, 150)
        panel.SetSizer(sizer)

        self.Show(True)

    def change_area(self, coordinate_num, value):
        area[coordinate_num] = int(value)
        set_image_coordinates(area)

    def on_x_coordinate0(self, event):
        self.change_area(0, self.text0.GetValue())

    def on_x_coordinate1(self, event):
        self.change_area(1, self.text1.GetValue())

    def on_x_coordinate2(self, event):
        self.change_area(2, self.text2.GetValue())

    def on_x_coordinate3(self, event):
        self.change_area(3, self.text3.GetValue())

    def onButton(self, event):
        """
        This method is fired when its corresponding button is pressed
        """
        run()


if __name__ == '__main__':

    # With wxPython
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
