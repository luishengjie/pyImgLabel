from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGridLayout
from utils import labeldata as ld
from constants import LABELS_PATH, ANNOTATE_DATA_PATH


class DynamicCheckBox(QWidget):
    def __init__(self, parent=None):
        super(DynamicCheckBox, self).__init__(parent)
        layout = QGridLayout()
        self.check_dict = {}
        self.checks = []
        self.labelslist = [line.rstrip('\n') for line in open(LABELS_PATH)]
        self.labelslist.sort()
        length = len(self.labelslist)
        split_val = int(length / 2)
        for i, label in enumerate(self.labelslist):
            c = QCheckBox("{}. {}".format(i+1, label))
            # c = QCheckBox(str(label))
            c.setStyleSheet("QCheckBox {text-align: left top; padding: 5 px;}")
            c.setContentsMargins(0, 0, 0, 0)

            # c.setChecked(True)
            if i > split_val:
                i = i - split_val - 1
                pos = 1
            else:
                pos = 0
            layout.addWidget(c, i, pos)
            self.checks.append(c)
            self.check_dict[label] = c
        layout.setSpacing(0)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.label_data = ld.LabelData(ANNOTATE_DATA_PATH, self.labelslist)

    def update_checkbox(self, checkbox_id):
        if checkbox_id < len(self.labelslist):
            status = self.checks[checkbox_id].isChecked()
            # Toggle the status
            status = not status
            self.checks[checkbox_id].setChecked(status)
            self.check_dict[self.labelslist[checkbox_id]].setChecked(status)

    def set_checkbox(self, key, value):
        if key in self.check_dict:
            status = bool(value)
            self.check_dict[key].setChecked(status)

    def initialize(self, image_id, width, height):
        # Read CSV, if csv contains image data
        data_values = self.label_data.dataframe.loc[self.label_data.dataframe['image'] == image_id]
        if data_values.empty:
            data = ld.DataClass(image_id, width, height, self.labelslist)
            self.label_data.update_data(data.get_dict())

        # print(self.label_data.get_values(image_id))
        for key, value in self.label_data.get_values(image_id).items():
            self.set_checkbox(key, value)

    def update_data(self, image_id):
        data_values = self.label_data.dataframe.loc[self.label_data.dataframe['image'] == image_id]
        cols_values = data_values.columns.values
        for i, header in enumerate(cols_values[3:]):
            if self.check_dict[header].isChecked():
                value = 1
            else:
                value = 0
            # print(header,self.check_dict[header].isChecked())
            self.label_data.dataframe.ix[self.label_data.dataframe['image'] == image_id, header] = value
            # print(self.label_data.dataframe.ix[self.label_data.dataframe['image'] == image_id, header])

        self.label_data.dataframe.to_csv(ANNOTATE_DATA_PATH, index=False)

    def delete_row(self, key):
        print(key)
        self.label_data.dataframe = self.label_data.dataframe[self.label_data.dataframe.image != key]
        self.label_data.dataframe.to_csv(ANNOTATE_DATA_PATH, index=False)
        
