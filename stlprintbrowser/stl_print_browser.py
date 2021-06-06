import PySimpleGUI as sg
from stlprintbrowser.settings import Settings
from stlprintbrowser.database import STLDatabase
from stlprintbrowser.main_window import MainWindow
from PIL import Image, ImageTk

settings = Settings()
database = STLDatabase(settings)

sg.theme(settings.theme)
main_window = MainWindow(database.get_stl_models())


def start_window():
    start = sg.Window('STL PRINT BROWSER', main_window.layout, finalize=True)
    if len(main_window.models) > 0:
        start['-MODELS_TABLE-'].update(select_rows=[0])
        if len(main_window.selected_row.images) > 0:
            start['-MODEL_IMAGE-'].update(data=ImageTk.PhotoImage(
                Image.open(main_window.selected_row.images[0])))
    return start


window = start_window()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()