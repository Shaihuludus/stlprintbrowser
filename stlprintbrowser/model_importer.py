from os import listdir, path

from stlprintbrowser.settings import Settings
from stlprintbrowser.stlmodel import STLModel

model_types = ['stl', 'lys']
image_types = ['jpg', 'jpeg', 'png']


def prepare_tags(tags):
    tags_list = []
    for tag in tags.split(';'):
        tags_list.append(tag)
    return tags_list


def import_model(directory, author, name_prefix, tags):
    if directory[-1] != '/' and directory[-1] != '\\':
        directory += '/'
    model = STLModel()
    model.name = name_prefix + path.basename(path.realpath(directory))
    model.directory = directory if ':' in directory else path.realpath(directory)
    model.author = author
    model.tags = prepare_tags(tags)
    read_directory(directory, model)
    settings = Settings()
    exec("from stlprintbrowser.databases.%s import *" % settings.config['general']['datasource_module'])
    database = eval(settings.config['general']['datasource']+'(settings)')
    database.add_stl_model(model)


def read_directory(directory, model):
    for file in listdir(directory):
        if path.isfile(directory + file):
            file_splitted = path.basename(file).split('.')
            if len(file_splitted) > 0:
                if file_splitted[-1] in image_types:
                    model.images.append(path.abspath(directory + file).replace('\\', '/'))
                if file_splitted[-1] in model_types:
                    model.filenames.append(path.abspath(directory + file).replace('\\', '/'))
        if path.isdir(directory + file):
            read_directory(directory + file + '/', model)
