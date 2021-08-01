from pymongo import MongoClient

from stlprintbrowser.stlmodel import STLModel

STL_MODELS = 'stl_models'


class STLMongoDatabase:

    def __init__(self, settings):
        self.client = MongoClient(settings.config['mongo']['address'])
        self.db = self.client[settings.config['mongo']['database']]

    def get_stl_models(self):
        models = []
        for model in self.db[STL_MODELS].find():
            models.append(STLModel.build_model(model))
        return models

    def get_filtered_stl_models(self, filters={}):
        query = self.build_query(filters)
        models = []
        if query is not None:
            data = self.db[STL_MODELS].find(query)
        else:
            data = self.db[STL_MODELS].find()
        for model in data:
            models.append(STLModel.build_model(model))
        return models

    def add_stl_model(self, model=STLModel()):
        self.db[STL_MODELS].insert_one(
            {'name': model.name,
             'filenames': model.filenames,
             'images': model.images,
             'supported': model.supported,
             'printed': model.printed,
             'author': model.author,
             'tags': model.tags,
             'directory': model.directory}
        )

    def delete_model(self, id):
        self.db[STL_MODELS].delete_one({'_id':id})

    def update_model(self, model):
        self.db[STL_MODELS].update(
            {'_id': model.id},
            {'name': model.name,
             'filenames': model.filenames,
             'images': model.images,
             'supported': model.supported,
             'printed': model.printed,
             'author': model.author,
             'tags': model.tags,
             'directory': model.directory})

    @staticmethod
    def build_query(filters):
        if 'author' in filters.keys() and filters['author'] != '' and filters['author'] != 'All':
            return {'author': filters['author']}
        else:
            return None
