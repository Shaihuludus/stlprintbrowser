import os

import PySimpleGUI as sg

from stlprintbrowser.model_importer import import_model


def modal_window_import_model():
    import_window = ImportModelWindow()
    window = sg.Window('Import Model', import_window.layout, finalize=True, modal=True)
    while True:
        event, values = window.read()
        if event == ImportModelWindow.OK_BUTTON:
            import_window.import_model()
            window.close()
            del window
            break
        if event == ImportModelWindow.BROWSE_BUTTON:
            import_window.browse()
        if event == sg.WIN_CLOSED or event == ImportModelWindow.CANCEL_BUTTON:
            window.close()
            del window
            break



class ImportModelWindow:
    BROWSE_BUTTON = '-BROWSE_BUTTON-'
    OK_BUTTON = '-OK_BUTTON-'
    CANCEL_BUTTON = '-CANCEL_BUTTON-'

    def __init__(self):
        self.path_input = sg.Input(default_text='')
        self.browse_button = sg.Button('Browse', key=ImportModelWindow.BROWSE_BUTTON)
        self.multiple_checkbox = sg.Checkbox(text='Many models')
        self.author_input = sg.Input(default_text='')
        self.name_prefix_input = sg.Input(default_text='')
        self.tags_input = sg.Input(default_text='')
        self.ok_button = sg.Button('Import', key=ImportModelWindow.OK_BUTTON)
        self.cancel_button = sg.Button('Cancel', key=ImportModelWindow.CANCEL_BUTTON)
        self.layout = [[sg.Text('Select path to import', size=(20, 1)), self.path_input, self.browse_button],
                       [self.multiple_checkbox], [sg.Text('Author: ', size=(20, 1)), self.author_input],
                       [sg.Text('Name Prefix:', size=(20, 1)), self.name_prefix_input],
                       [sg.Text('Tags (; - separator)', size=(20, 1)), self.tags_input], [self.cancel_button, self.ok_button]]

    def browse(self):
        self.path_input.update(value=sg.popup_get_folder(message='Select folder with model(s)'))

    def import_model(self):
        path = self.path_input.get()
        if path is None or not os.path.isdir(path):
            sg.popup_ok('Invalid folder')
        else:
            if path[-1] != '/' and path[-1] != '\\':
                path += '/'
            if self.multiple_checkbox.get():
                for file in os.listdir(path):
                    if os.path.isdir(path + file):
                        import_model(path + file, self.author_input.get(), self.name_prefix_input.get(), self.tags_input.get())
            else:
                import_model(path, self.author_input.get(), self.name_prefix_input.get(), self.tags_input.get())
            sg.popup_ok('Model(s) imported')


