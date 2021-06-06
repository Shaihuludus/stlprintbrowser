from tinydb import TinyDB
from stlprintbrowser.stlmodel import STLModel

STL_MODELS = 'stl_models'

class STLDatabase:

    def __init__(self, settings):
        self.db = TinyDB(settings.database_path+'/stldatabase.json')

    def get_stl_models(self):
        models = []
        for model in self.db.table(STL_MODELS).all():
            models.append(STLModel.build_model(model))
        return models

    def add_stl_model(self, model = STLModel()):
        self.db.table(STL_MODELS).insert(
            {'name': model.name,
             'filenames': model.filenames,
             'images': model.images,
             'supported': model.supported,
             'printed': model.printed,
             'author': model.author,
             'tags': model.tags,
             'directory': model.directory}
        )