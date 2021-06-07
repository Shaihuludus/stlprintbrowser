import PySimpleGUI as sg

from stlprintbrowser.database import STLDatabase
from stlprintbrowser.main_window import MainWindow
from stlprintbrowser.settings import Settings
from os import startfile

settings = Settings()
database = STLDatabase(settings)

sg.theme(settings.theme)
main_window = MainWindow(database.get_stl_models(), database)


def start_window():
    start = sg.Window('STL PRINT BROWSER', main_window.layout.layout, finalize=True, resizable=True)
    main_window.create_bindings()
    if len(main_window.models) > 0:
        start['-MODELS_TABLE-'].update(select_rows=[0])
        if len(main_window.selected_row.images) > 0:
            main_window.display_picture()

    start.maximize()
    main_window.expand_elements()
    return start


window = start_window()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == MainWindow.NEXT_IMAGE_BUTTON_:
        main_window.next_image()
    if event == MainWindow.PREVIOUS_IMAGE_BUTTON_:
        main_window.previous_image()
    if event == MainWindow.MODELS_TABLE_:
        main_window.select_model(values[MainWindow.MODELS_TABLE_])
    if event == MainWindow.MODEL_FILES_+MainWindow.DOUBLE_CLICK_EXTENSION_:
        main_window.open_file(values[MainWindow.MODEL_FILES_])
    if event == MainWindow.OPEN_DIRECTORY_BUTTON_:
        startfile(values[MainWindow.MODEL_DIRECTORY_])
    if event == MainWindow.SAVE_CHANGES_BUTTON_:
        main_window.save_changes(values)
window.close()
