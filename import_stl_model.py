import os
import sys

from stlprintbrowser.model_importer import import_model

valid_parameters = ['--m', '--a']


def importer(directory, parameters=[]):
    author = ''
    name_prefix = ''
    tags = ''
    if '--a' in parameters:
        index = parameters.index('--a')
        if (index + 1) == len(parameters) or parameters[index + 1] in valid_parameters:
            print('No author in parameters')
            return
        else:
            author = parameters[index + 1]
    if '--n' in parameters:
        index = parameters.index('--n')
        if (index + 1) == len(parameters) or parameters[index + 1] in valid_parameters:
            print('No name prefix in parameters')
            return
        else:
            name_prefix = parameters[index + 1]
    if '--t' in parameters:
        index = parameters.index('--t')
        if (index + 1) == len(parameters) or parameters[index + 1] in valid_parameters:
            print('No tags parameters')
            return
        else:
            tags = parameters[index + 1]
    if '--m' in parameters:
        print('Importing many models from: ' + directory)
        for file in os.listdir(directory):
            print(directory + file)
            if os.path.isdir(directory + file):
                import_model(directory + file, author, name_prefix, tags)
    else:
        print('Importing single model from: ' + directory)
        import_model(import_directory, author, name_prefix, tags)


import_directory = sys.argv.pop(-1)

if os.path.exists(import_directory) and os.path.isdir(import_directory):
    if import_directory[-1] != '/' and import_directory[-1] != '\\':
        import_directory += '/'
    if len(sys.argv) > 1:
        importer(import_directory, sys.argv[1:])
    else:
        importer(import_directory)
else:
    print('No model to import. Stopped importer')
