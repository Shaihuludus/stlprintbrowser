import PySimpleGUI as sg
from settings import Settings
from database import STL_Database

settings = Settings()
database = STL_Database(settings)

sg.theme(settings.theme)   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('This is placeholder for more complex layout')]]

# Create the Window
window = sg.Window('STL PRINT BROWSER', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()