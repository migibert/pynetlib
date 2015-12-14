import os


def read_file(filename):
    return open(os.path.join(os.path.dirname(__file__) + '/fixtures', filename), 'rb').read()
