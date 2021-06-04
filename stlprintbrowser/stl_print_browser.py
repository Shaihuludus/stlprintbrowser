import PySimpleGUI as sg
from stlprintbrowser.settings import Settings
from stlprintbrowser.database import STLDatabase
from stlprintbrowser.main_window import MainWindow

settings = Settings()
database = STLDatabase(settings)

sg.theme(settings.theme)

# Create the Window
window = sg.Window('STL PRINT BROWSER', MainWindow(database.get_stl_models()).layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()