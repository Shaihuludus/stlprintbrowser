class STLModel:

    @staticmethod
    def build_model(database_item):
        model = STLModel()
        model.id = database_item['_id']
        model.name = database_item['name']
        model.filenames = database_item['filenames']
        model.images = database_item['images']
        model.supported = database_item['supported']
        model.printed = database_item['printed']
        model.author = database_item['author']
        model.tags = database_item['tags']
        model.directory = database_item['directory']
        return model

    def __init__(self):
        self.id = 0
        self.name = ''
        self.filenames = []
        self.images = []
        self.supported = True
        self.printed = False
        self.author = ''
        self.tags = []
        self.directory = ''
