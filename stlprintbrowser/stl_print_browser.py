from stlprintbrowser.gui.main_window import MainWindowController, MainApp
from stlprintbrowser.settings import Settings

settings = Settings()
exec("from stlprintbrowser.databases.%s import *" % settings.config['general']['datasource_module'])
database = eval(settings.config['general']['datasource']+'(settings)')

MainApp(MainWindowController(database)).run()
