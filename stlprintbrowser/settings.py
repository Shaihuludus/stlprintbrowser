import configparser


class Settings:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.database_path = config['database']['database_path']
        self.theme = config['view']['theme']