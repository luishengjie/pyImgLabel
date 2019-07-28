from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage, QIcon
import cv2
import imutils
import os
from constants import *


class ImageObj():
    def __init__(self, image_path):
        self.image_name = image_path.split('/')[-1]
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def get_image(self):
        return self.image

    def get_name(self):
        return self.image_name

    def get_shape(self):
        h, w, _ = self.image.shape
        return h, w


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = uic.loadUi('main.ui', self)
        self.dynamic_checkbox = self.ui.sideCheckBox
        # placeholder = cv2.imread("images/grey.jpg")
        # self.update_main_screen(placeholder)
        # self.init_main_screen(imagepath='data/sample_images')
        self.image_count = -1
        self.image_path = IMAGE_PATH
        if os.path.isdir(self.image_path):
            self.images_list = os.listdir(self.image_path)
            self.images_list.sort()
            self.image_count = 0
            self.update_main_screen()
            self.update_image_text_labels()

        self.update_main_screen()
        height, width = self.curr_image.get_shape()
        self.dynamic_checkbox.initialize(self.curr_image.get_name(), width, height)


    def keyPressEvent(self, event):
        # print(event.key())
        if event.key() == KEY_RIGHT:
            self.dynamic_checkbox.update_data(self.curr_image.get_name())
            self.image_count += 1
            if self.image_count > len(self.images_list) - 1:
                self.image_count = self.images_list - 1
            # UPDATE VALUES TO CSV
            self.update_main_screen()
            height, width = self.curr_image.get_shape()
            self.dynamic_checkbox.initialize(self.curr_image.get_name(), width, height)
            
            
        elif event.key() == KEY_LEFT:
            self.dynamic_checkbox.update_data(self.curr_image.get_name())
            self.image_count -= 1
            if self.image_count < 0:
                self.image_count = 0
            self.update_main_screen()
            height, width = self.curr_image.get_shape()
            self.dynamic_checkbox.initialize(self.curr_image.get_name(), width, height)
            


        elif event.key() == ONE:
            self.dynamic_checkbox.update_checkbox(0)
            
        elif event.key() == TWO:
            self.dynamic_checkbox.update_checkbox(1)
        
        elif event.key() == THREE:
            self.dynamic_checkbox.update_checkbox(2)
        
        elif event.key() == FOUR:
            self.dynamic_checkbox.update_checkbox(3)
        
        elif event.key() == FIVE:
            self.dynamic_checkbox.update_checkbox(4)
        
        elif event.key() == SIX:
            self.dynamic_checkbox.update_checkbox(5)
        
        elif event.key() == SEVEN:
            self.dynamic_checkbox.update_checkbox(6)
        
        elif event.key() == EIGHT:
            self.dynamic_checkbox.update_checkbox(7)
        
        elif event.key() == NINE:
            self.dynamic_checkbox.update_checkbox(8)
        
        event.accept()
        # self.update_main_screen()

    def update_main_screen(self):

        if self.image_count == -1:
            image = cv2.imread(DEFAULT_IMAGE)
        else:
            image_name = self.images_list[self.image_count]
            image_name = os.path.join(self.image_path, image_name)
            self.curr_image = ImageObj(image_name)

        self.set_main_screen_image(self.curr_image.get_image())
        self.update_image_text_labels()
        
    def set_main_screen_image(self, image):
        assert(image is not None, "None Type received")
        width = self.ui.mainScreenLabel.frameGeometry().width()
        height = self.ui.mainScreenLabel.frameGeometry().height()
        image = imutils.resize(image, width=width)

        up_height, up_width, _ = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, up_width, up_width,
                         bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image)
        self.ui.mainScreenLabel.setPixmap(pixmap)

    def update_image_text_labels(self):
        self.ui.progressTextLabel.setText(str(self.image_count + 1) + ' / ' +
                                          str(len(self.images_list)))
        
        self.ui.displayImageNameLabel.setText(self.curr_image.get_name())
        height, width = self.curr_image.get_shape()
        self.ui.displayImageWidthLabel.setText(str(width))
        self.ui.displayImageHeightLabel.setText(str(height))
        
