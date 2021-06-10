import PySimpleGUI as sg


def modal_window_import_model():
    import_window = sg.Window('Import Model', ImportModelWindow().layout, finalize=True, modal=True)
    while True:
        event, values = import_window.read()
        print(event)
        if event == sg.WIN_CLOSED or event == ImportModelWindow.CANCEL_BUTTON:
            import_window.close()
            del import_window
            break
    return None


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
