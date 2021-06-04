from stlprintbrowser.settings import Settings
from stlprintbrowser.database import STLDatabase
from os import listdir, path

from stlprintbrowser.stlmodel import STLModel

model_types = ['stl', 'lys']
image_types = ['jpg', 'jpeg', 'png']

def import_model(directory):
    model = STLModel()
    model.name = path.basename(directory)
    for file in listdir(directory):
        file_splitted = path.basename(file).split('.')
        if len(file_splitted) > 0:
            if(file_splitted[1] in image_types):
                model.images.append(path.abspath(file).replace('\\','/'))
            if(file_splitted[1] in model_types):
                model.filenames.append(path.abspath(file).replace('\\','/'))
    database = STLDatabase(Settings())
    database.add_stl_model(model)