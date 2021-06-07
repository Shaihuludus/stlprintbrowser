from os import startfile

import PySimpleGUI as sg
from PIL import Image, ImageTk

headings = ['id', 'name', 'directory', 'printed',
            'author']


class MainWindow:
    MODELS_TABLE_ = '-MODELS_TABLE-'
    MODEL_IMAGE_ = '-MODEL_IMAGE-'
    NEXT_IMAGE_BUTTON_ = '-NEXT_IMAGE_BUTTON-'
    PREVIOUS_IMAGE_BUTTON_ = '-PREVIOUS_IMAGE_BUTTON-'
    OPEN_DIRECTORY_BUTTON_ = '-OPEN_DIRECTORY_BUTTON-'
    MODEL_NAME_ = '-MODEL_NAME-'
    MODEL_AUTHOR_ = '-MODEL_AUTHOR-'
    MODEL_DIRECTORY_ = '-MODEL_DIRECTORY-'
    MODEL_SUPPORTED_ = '-MODEL_SUPPORTED-'
    MODEL_PRINTED_ = '-MODEL_PRINTED-'
    MODEL_FILES_ = '-MODEL_FILES-'
    MODEL_IMAGES_ = '-MODEL_IMAGES-'
    MODEL_TAGS_ = '-MODEL_TAGS-'
    DOUBLE_CLICK_EXTENSION_ = '-DOUBLE'

    def __init__(self, models):
        self.models = models
        if len(self.models) > 0:
            self.selected_row = self.models[0]
            self.selected_image = 0
        self.layout = MainWindowLayout(models, len(self.selected_row.images) < 2, self.selected_row)

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
            self.layout.model_name_input.update(value=self.selected_row.name)
            self.layout.model_author_input.update(value=self.selected_row.author)
            self.layout.model_directory_input.update(value=self.selected_row.directory)
            self.layout.model_files_list.update(values=self.selected_row.filenames)
            self.layout.model_files_list.TKListbox.xview_moveto(1)
            self.layout.model_images_list.update(values=self.selected_row.images)
            self.layout.model_images_list.TKListbox.xview_moveto(1)
            self.layout.model_tags_list.update(values=self.selected_row.tags)
            self.layout.model_tags_list.TKListbox.xview_moveto(1)
            self.layout.model_supported_checkbox.update(value=self.selected_row.supported)
            self.layout.model_printed_checkbox.update(value=self.selected_row.printed)
            if len(self.selected_row.images) > 0:
                self.display_picture()
                self.layout.previous_image_button.update(disabled=len(self.selected_row.images) < 2)
                self.layout.next_image_button.update(disabled=len(self.selected_row.images) < 2)
            else:
                self.layout.miniature_image.update(data=None)

    def create_bindings(self):
        self.layout.model_files_list.bind('<Double-1>', MainWindow.DOUBLE_CLICK_EXTENSION_)

    @staticmethod
    def open_file(files):
        for file in files:
            startfile(file)


class MainWindowLayout:

    @staticmethod
    def prepare_rows(models):
        data = []
        for model in models:
            single_entry = [model.id, model.name, model.directory, model.printed, model.author]
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

    def __init__(self, models, disable_buttons, selected_row):

        # models table
        self.models_table = sg.Table(self.prepare_rows(models), headings, key=MainWindow.MODELS_TABLE_,
                                     vertical_scroll_only=False, auto_size_columns=False,
                                     col_widths=[10, 40, 100, 10, 20], num_rows=20, enable_events=True)
        self.column_models = sg.Column([[self.models_table]], expand_x=True)

        # image and image controls
        self.previous_image_button = sg.Button('Previous Image', key=MainWindow.PREVIOUS_IMAGE_BUTTON_,
                                               disabled=disable_buttons)
        self.next_image_button = sg.Button('Next Image', key=MainWindow.NEXT_IMAGE_BUTTON_, disabled=disable_buttons)
        self.miniature_image = sg.Image(key=MainWindow.MODEL_IMAGE_, )
        self.column_image = sg.Column([[self.previous_image_button, self.next_image_button], [self.miniature_image], ],
                                      scrollable=True, expand_x=True, expand_y=True, vertical_scroll_only=True,
                                      element_justification='center')
        # model details
        self.model_name_input = sg.Input(default_text=selected_row.name, key=MainWindow.MODEL_NAME_)
        self.model_author_input = sg.Input(default_text=selected_row.author, key=MainWindow.MODEL_AUTHOR_)
        self.model_directory_input = sg.Input(default_text=selected_row.directory, key=MainWindow.MODEL_DIRECTORY_)
        self.open_directory_button = sg.Button('Open', key=MainWindow.OPEN_DIRECTORY_BUTTON_)

        self.model_files_list = sg.Listbox(values=selected_row.filenames, size=(70, 5), key=MainWindow.MODEL_FILES_)
        self.model_images_list = sg.Listbox(values=selected_row.images, size=(70, 5), key=MainWindow.MODEL_IMAGES_)
        self.model_tags_list = sg.Listbox(values=selected_row.tags, size=(70, 5), key=MainWindow.MODEL_TAGS_)
        self.model_supported_checkbox = sg.Checkbox(text='', default=selected_row.supported)
        self.model_printed_checkbox = sg.Checkbox(text='', default=selected_row.printed)
        self.column_information = sg.Column(
            [[sg.Text(text="Model Name:", size=(12, 1)), self.model_name_input],
             [sg.Text(text="Model Author:", size=(12, 1)), self.model_author_input],
             [sg.Text(text="Model Directory:", size=(12, 1)), self.model_directory_input, self.open_directory_button],
             [sg.Text(text="Model Files:", size=(12, 1)), self.model_files_list],
             [sg.Text(text="Model Images:", size=(12, 1)), self.model_images_list],
             [sg.Text(text="Supported:", size=(12, 1)), self.model_supported_checkbox],
             [sg.Text(text="Printed:", size=(12, 1)), self.model_printed_checkbox],
             [sg.Text(text="Model Tags:", size=(12, 1)), self.model_tags_list],], scrollable=True,
            expand_x=True, expand_y=True, vertical_scroll_only=True)

        self.layout = [[self.column_models], [self.column_image, self.column_information]]
