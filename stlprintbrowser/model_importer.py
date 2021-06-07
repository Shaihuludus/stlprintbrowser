from os import listdir, path

from stlprintbrowser.database import STLDatabase
from stlprintbrowser.settings import Settings
from stlprintbrowser.stlmodel import STLModel

model_types = ['stl', 'lys']
image_types = ['jpg', 'jpeg', 'png']


def import_model(directory):
    if directory[-1] != '/' and directory[-1] != '\\':
        directory += '/'
    model = STLModel()
    model.name = path.basename(path.realpath(directory))
    model.directory = directory if ':' in directory else path.realpath(directory)
    for file in listdir(directory):
        file_splitted = path.basename(file).split('.')
        if len(file_splitted) > 0:
            if file_splitted[1] in image_types:
                model.images.append(path.abspath(directory + file).replace('\\', '/'))
            if file_splitted[1] in model_types:
                model.filenames.append(path.abspath(directory + file).replace('\\', '/'))
    database = STLDatabase(Settings())
    database.add_stl_model(model)
