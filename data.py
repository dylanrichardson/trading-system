from utility import *
import traceback
import os


class Data:

    def __init__(self):
        self.path = None
        self.data = None
        self.path = self.get_path()
        self.data = self.get_data()

    def data_error_msg(self):
        return 'Failed to get data for ' + str(self.get_params())

    def get_data(self):
        try:
            if not self.data:
                self.make_path()
                self.data = self.read_data()
                if not self.data:
                    self.data = self.get_new_data()
                    self.write_data()
                if not self.data:
                    raise Exception(self.data_error_msg())
            return self.data
        except Exception:
            raise Exception(traceback.format_exc() + '\n' + self.data_error_msg())

    def get_path(self):
        if not self.path:
            file_name = shorten_path(encrypt_dict(self.get_params()))
            cwd = os.getcwd()
            self.path = os.path.join(cwd, PARAMS['data_folder'], self.get_folder(),
                                     file_name + '.' + self.get_extension())
        return self.path

    def make_path(self):
        make_path(self.get_path())

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
