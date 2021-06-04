import PySimpleGUI as sg

headings = ['id', 'name', 'filenames', 'images', 'supported', 'printed', 'author', 'tags']

class MainWindow:

    def __init__(self, models):
        self.models = models
        if len(self.models) > 0:
            self.selected_row = self.models[0]
        self.layout = [[sg.Table(self.prepare_rows(models), headings, key= '-MODELS_TABLE-')],
                       [sg.Image(key='-MODEL_IMAGE-')],]

    def prepare_rows(self, models):
        data = []
        for model in models:
            single_entry = [model.id]
            single_entry.append(model.name)
            single_entry.append(self.format_files(model.filenames))
            single_entry.append(self.format_files(model.images))
            single_entry.append(model.supported)
            single_entry.append(model.printed)
            single_entry.append(model.author)
            single_entry.append(model.tags)
            data.append(single_entry)
        if len(data) < 1:
            data = [['', '', '', '', '', '', '', '']]
        return data

    def format_files(self, filenames):
        entry = ''
        for file in filenames:
            entry += file+'\n'
        return entry


