import os
import d3scrapier


def get_data_folder():
    return os.path.dirname(d3scrapier.__file__) + '/data'


def get_data_file(filename):
    return get_data_folder() + 'filename'
