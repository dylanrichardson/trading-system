import os
from utility import *

class Data:

    def __init__(self):
        self.path = self.get_path()
        self.data = self.get_data()


    def get_data(self):
        if not hasattr(self, 'data'):
            self.make_path()
            self.data = self.read_data()
            if not self.data:
                self.data = self.get_new_data()
                self.write_data()
        return self.data


    def get_path(self):
        if not hasattr(self, 'path'):
            file_name = shorten_path(encrypt_dict(self.get_params()))
            cwd = os.getcwd()
            self.path = os.path.join(cwd, PARAMS['data_folder'], self.get_folder(), file_name + '.' + self.get_extension())
        return self.path


    def make_path(self):
        dir_name = os.path.dirname(self.get_path())
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)


    def get_params(self):
        raise NotImplementedError()


    def get_new_data(self):
        raise NotImplementedError()


    def get_folder(self):
        raise NotImplementedError()


    def get_extension(self):
        raise NotImplementedError()


    def read_data(self):
        raise NotImplementedError()


    def write_data(self):
        raise NotImplementedError()
