import pandas as pd
import os
import sys


class DataClass():
    def __init__(self, image_name, image_width, image_height, labelslist):
        self.data_dict = {}
        self.data_dict['image'] = image_name
        self.data_dict['width'] = image_width
        self.data_dict['height'] = image_height
        for label in labelslist:
            self.data_dict[label] = 0

    def add_class(self, class_label):
        if class_label in self.data_dict:
            self.data_dict[class_label] = 1
        else:
            print('[ERROR], label:{} does not exist'.format(class_label))
    
    def remove_class(self, class_label):
        if class_label in self.data_dict:
            self.data_dict[class_label] = 0

    def get_dict(self):
        return self.data_dict

    def set_value(self, key, value):
        self.data_dict[key] = value


class LabelData():
    def __init__(self, label_path, labelslist):
        self.labelslist = labelslist
        self.label_path = label_path
        self.initialize()

    def update_data(self, data_row):
        # self.dataframe = self.dataframe.append({'User_ID': 40, 'UserName': 'Riti', 'Action': 'Login'}, ignore_index=True)
        self.dataframe = self.dataframe.append(data_row, ignore_index=True)
        self.dataframe.to_csv(self.label_path, index=False)

    def initialize(self):
        # Check if file path exists
        if os.path.isfile(self.label_path):
            self.dataframe = pd.read_csv(self.label_path)
            new_columns = []
            for label in self.labelslist:
                if label not in self.dataframe.columns.values:
                    new_columns.append(label)

            for label in new_columns:
                self.dataframe[label] = [0 for i in range(self.dataframe.shape[0])]

            # Rearrange the columns
            static_columns = self.dataframe.columns.tolist()[:3]
            label_columns = self.dataframe.columns.tolist()[3:]
            label_columns.sort()
            cols = static_columns + label_columns
            self.dataframe = self.dataframe[cols]

        else:
            # Init a new dataframe
            columns = ['image', 'width', 'height'] + self.labelslist
            self.dataframe = pd.DataFrame(columns=columns)

    def show_data(self):
        print(self.dataframe)

    def get_data(self):
        return self.dataframe

    def get_values(self, image_name):
        data_values = self.dataframe.loc[self.dataframe['image'] == image_name]
        cols = self.dataframe.columns.tolist()
        name = str(data_values[cols[0]].values[0])
        width = int(data_values[cols[1]].values[0])
        height = int(data_values[cols[2]].values[0])
        data = DataClass(name, width, height, self.labelslist)

        for d_value in cols[3:]:
            data.set_value(d_value, int(data_values[d_value].values[0]))

        return data.get_dict()

    def get_label_values(self, image_name):
        data_values = self.dataframe.loc[self.dataframe['image'] == image_name]
        cols = self.dataframe.columns.tolist()
        name = str(data_values[cols[0]].values[0])
        width = int(data_values[cols[1]].values[0])
        height = int(data_values[cols[2]].values[0])
        print('name:', name)
        print('width:', width)
        print('height:', height)
        data = DataClass(name, width, height, self.labelslist)

        for d_value in cols[3:]:
            data.set_value(d_value, int(data_values[d_value].values[0]))

        return data.get_dict()
