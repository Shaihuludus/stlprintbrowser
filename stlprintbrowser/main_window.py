import PySimpleGUI as sg
from PIL import Image, ImageTk

headings = ['id', 'name', 'directory', 'printed',
            'author']


class MainWindow:
    MODELS_TABLE_ = '-MODELS_TABLE-'
    MODEL_IMAGE_ = '-MODEL_IMAGE-'
    NEXT_IMAGE_BUTTON_ = '-NEXT_IMAGE_BUTTON-'
    PREVIOUS_IMAGE_BUTTON_ = '-PREVIOUS_IMAGE_BUTTON-'

    def __init__(self, models):
        self.models = models
        if len(self.models) > 0:
            self.selected_row = self.models[0]
            self.selected_image = 0
        self.layout = MainWindowLayout(models,
                                       len(self.selected_row.images) < 2)

    def expand_elements(self):
        self.layout.models_table.expand(True, False)
        self.layout.models_table.table_frame.pack(expand=True, fill='both')

    def next_image(self):
        self.selected_image = self.selected_image + 1
        if self.selected_image >= len(self.selected_row.images):
            self.selected_image = 0
        self.display_picture(self.selected_image)

    def previous_image(self):
        self.selected_image = self.selected_image - 1
        if self.selected_image < 0:
            self.selected_image = len(self.selected_row.images) - 1
        self.display_picture(self.selected_image)

    def display_picture(self, image_number=0):
        image = Image.open(self.selected_row.images[image_number])
        image.thumbnail((500, 500))
        self.layout.miniature_image.update(data=ImageTk.PhotoImage(image))

    def select_model(self, selected_models):
        if len(selected_models) == 1:
            self.selected_row = self.models[selected_models[0]]
            if len(self.selected_row.images) > 0:
                self.display_picture()
                self.layout.previous_image_button.update(disabled=len(
                    self.selected_row.images) < 2)
                self.layout.next_image_button.update(disabled=len(
                    self.selected_row.images) < 2)
            else:
                self.layout.miniature_image.update(data=None)


class MainWindowLayout:

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

    def __init__(self, models, disable_buttons):
        self.models_table = sg.Table(self.prepare_rows(models), headings,
                                     key=MainWindow.MODELS_TABLE_,
                                     vertical_scroll_only=False,
                                     auto_size_columns=False,
                                     col_widths=[10, 40, 100, 10, 20],
                                     num_rows=20, enable_events=True)
        self.column_models = sg.Column([[self.models_table]], expand_x=True)
        self.previous_image_button = sg.Button('Previous Image',
                                               key=MainWindow.PREVIOUS_IMAGE_BUTTON_,
                                               disabled=disable_buttons)
        self.next_image_button = sg.Button('Next Image',
                                           key=MainWindow.NEXT_IMAGE_BUTTON_,
                                           disabled=disable_buttons)
        self.miniature_image = sg.Image(key=MainWindow.MODEL_IMAGE_, )
        self.column_details = sg.Column(
            [[self.previous_image_button, self.next_image_button],
             [self.miniature_image], ], scrollable=True,
            expand_x=True, expand_y=True, vertical_scroll_only=True)
        self.layout = [[self.column_models], [self.column_details]]
