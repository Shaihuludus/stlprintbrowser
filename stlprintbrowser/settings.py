import configparser


class Settings:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')