import os
import sys

from stlprintbrowser.model_importer import import_model


def importer(directory, parameters=[]):
    if directory[-1] != '/' and directory[-1] != '\\':
        directory += '/'
    if '--m' in parameters:
        print('Importing many models from: ' + directory)
        for file in os.listdir(directory):
            print(directory+file)
            if os.path.isdir(directory+file):
                import_model(directory+file)
    else:
        print('Importing single model from: ' + directory)
        import_model(import_directory)


import_directory = sys.argv.pop(-1)

if os.path.exists(import_directory) and os.path.isdir(import_directory):
    if len(sys.argv) > 1:
        importer(import_directory, sys.argv[1:])
    else:
        importer(import_directory)
else:
    print('No model to import. Stopped importer')
