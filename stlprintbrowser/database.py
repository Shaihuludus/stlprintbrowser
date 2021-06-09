from tinydb import TinyDB, Query

from stlprintbrowser.stlmodel import STLModel

STL_MODELS = 'stl_models'


class STLDatabase:

    def __init__(self, settings):
        self.db = TinyDB(settings.database_path + '/stldatabase.json')

    def get_stl_models(self):
        models = []
        for model in self.db.table(STL_MODELS).all():
            models.append(STLModel.build_model(model))
        return models

    def get_filtered_stl_models(self, filters={}):
        query = self.build_query(filters)
        models = []
        if query is not None:
            data = self.db.table(STL_MODELS).search(query)
        else:
            data = self.db.table(STL_MODELS).all()
        for model in data:
            models.append(STLModel.build_model(model))
        return models

    def add_stl_model(self, model=STLModel()):
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

    def delete_model(self, id):
        self.db.table(STL_MODELS).remove(None, [id])

    def update_model(self, model):
        self.db.table(STL_MODELS).update(
            {'name': model.name,
             'filenames': model.filenames,
             'images': model.images,
             'supported': model.supported,
             'printed': model.printed,
             'author': model.author,
             'tags': model.tags,
             'directory': model.directory}, None, [model.id])

    @staticmethod
    def build_query(filters):
        query = []
        if 'author' in filters.keys() and filters['author'] != '' and filters['author'] != 'all':
            query.append(Query().author.matches(filters['author']))
        if len(query) > 0:
            return query[0]
        else:
            return None
