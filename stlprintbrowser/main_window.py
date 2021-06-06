import PySimpleGUI as sg

headings = ['id', 'name', 'directory', 'printed',
            'author']


class MainWindow:

    @staticmethod
    def prepare_rows(models):
        data = []
        for model in models:
            single_entry = [model.id, model.name,
                            model.directory,
                            model.printed, model.author]
            data.append(single_entry)
        if len(data) < 1:
            data = [['', '', '', '', '', ]]
        return data

    @staticmethod
    def format_files(filenames):
        entry = ''
        for file in filenames:
            entry += file + '\n'
        return entry

    def __init__(self, models):
        self.models = models
        if len(self.models) > 0:
            self.selected_row = self.models[0]
        self.models_table = sg.Table(self.prepare_rows(models), headings,
                              key='-MODELS_TABLE-',vertical_scroll_only=False,auto_size_columns=False,col_widths=[10,40,100,10,20],num_rows=20)
        self.column_models = sg.Column([[self.models_table]],expand_x=True)
        self.column_details = sg.Column([[sg.Image(key='-MODEL_IMAGE-')]],scrollable=True,expand_x=True,expand_y=True,vertical_scroll_only=True)
        self.layout = [[self.column_models],[self.column_details]]

    def expand_elements(self):
        self.models_table.expand(True, False)
        self.models_table.table_frame.pack(expand=True, fill='both')



