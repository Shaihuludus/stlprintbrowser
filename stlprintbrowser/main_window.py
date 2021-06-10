import os
from os import startfile

import PySimpleGUI as sg
from PIL import Image, ImageTk

from stlprintbrowser.import_model_window import modal_window_import_model
from stlprintbrowser.stlmodel import STLModel

headings = ['id', 'name', 'directory', 'printed',
            'author']


class MainWindow:
    MODELS_TABLE_ = '-MODELS_TABLE-'
    MODEL_IMAGE_ = '-MODEL_IMAGE-'
    NEXT_IMAGE_BUTTON_ = '-NEXT_IMAGE_BUTTON-'
    PREVIOUS_IMAGE_BUTTON_ = '-PREVIOUS_IMAGE_BUTTON-'
    OPEN_DIRECTORY_BUTTON_ = '-OPEN_DIRECTORY_BUTTON-'
    SAVE_CHANGES_BUTTON_ = '-SAVE_CHANGES_BUTTON-'
    ADD_IMAGE_BUTTON_ = '-ADD_IMAGE_BUTTON-'
    ADD_FILE_BUTTON_ = '-ADD_FILE_BUTTON-'
    ADD_TAG_BUTTON_ = '-ADD_TAG_BUTTON-'
    VALIDATE_BUTTON_ = '-VALIDATE_BUTTON-'
    DELETE_BUTTON_ = '-DELETE_BUTTON-'
    MODEL_NAME_ = '-MODEL_NAME-'
    MODEL_AUTHOR_ = '-MODEL_AUTHOR-'
    MODEL_DIRECTORY_ = '-MODEL_DIRECTORY-'
    MODEL_SUPPORTED_ = '-MODEL_SUPPORTED-'
    MODEL_PRINTED_ = '-MODEL_PRINTED-'
    MODEL_FILES_ = '-MODEL_FILES-'
    MODEL_IMAGES_ = '-MODEL_IMAGES-'
    MODEL_TAGS_ = '-MODEL_TAGS-'
    DOUBLE_CLICK_EXTENSION_ = '-DOUBLE'
    AUTHORS_FILTER = '-AUTHORS_FILTER-'
    ADD_MODEL_BUTTON = '-ADD_MODEL_BUTTON-'

    @staticmethod
    def open_file(files):
        for file in files:
            startfile(file)

    def __init__(self, models, database):
        self.models = models
        self.database = database
        self.authors = self.retrieve_authors()
        if len(self.models) > 0:
            self.selected_row = self.models[0]
            self.selected_image = 0
        self.layout = MainWindowLayout(models, self.authors,
                                       len(self.selected_row.images) < 2 or self.selected_row.images is None,
                                       self.selected_row)

    def retrieve_authors(self):
        authors = set()
        for model in self.database.get_stl_models():
            authors.add(model.author)
        return authors

    def expand_elements(self):
        self.layout.models_table.expand(True, False)
        self.layout.models_table.table_frame.pack(expand=True, fill='both')

    def next_image(self):
        self.selected_image = self.selected_image + 1
        if self.selected_image >= len(self.selected_row.images):
            self.selected_image = 0
        self.display_picture()

    def previous_image(self):
        self.selected_image = self.selected_image - 1
        if self.selected_image < 0:
            self.selected_image = len(self.selected_row.images) - 1
        self.display_picture()

    def choose_image(self):
        if len(self.layout.model_images_list.get_indexes()) > 0:
            self.selected_image = self.layout.model_images_list.get_indexes()[0]
            self.display_picture()

    def display_picture(self):
        self.layout.model_images_list.update(set_to_index=self.selected_image)
        image = Image.open(self.selected_row.images[self.selected_image])
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
            self.layout.model_tags_list.update(values=self.selected_row.tags)
            self.layout.model_tags_list.TKListbox.xview_moveto(1)
            self.layout.model_supported_checkbox.update(value=self.selected_row.supported)
            self.layout.model_printed_checkbox.update(value=self.selected_row.printed)
            self.selected_image = 0
            self.update_images_widgets()

    def update_images_widgets(self):
        self.layout.model_images_list.update(values=self.selected_row.images)
        self.layout.model_images_list.TKListbox.xview_moveto(1)
        if len(self.selected_row.images) > 0:
            self.display_picture()
            self.layout.previous_image_button.update(disabled=len(self.selected_row.images) < 2)
            self.layout.next_image_button.update(disabled=len(self.selected_row.images) < 2)
        else:
            self.layout.miniature_image.update(data=None)
            self.layout.previous_image_button.update(disabled=True)
            self.layout.next_image_button.update(disabled=True)

    def create_bindings(self):
        self.layout.model_files_list.bind('<Double-1>', MainWindow.DOUBLE_CLICK_EXTENSION_)

    def save_changes(self, values):
        self.selected_row.printed = values[MainWindow.MODEL_PRINTED_]
        self.selected_row.supported = values[MainWindow.MODEL_SUPPORTED_]
        self.selected_row.name = values[MainWindow.MODEL_NAME_]
        self.selected_row.author = values[MainWindow.MODEL_AUTHOR_]
        self.selected_row.directory = values[MainWindow.MODEL_DIRECTORY_]
        self.database.update_model(self.selected_row)
        self.refresh_models()

    def refresh_authors(self):
        self.authors = self.retrieve_authors()
        authors_update = [MainWindowLayout.ALL_AUTHORS]
        authors_update.extend(self.authors)
        self.layout.authors_combo.update(values=authors_update)

    def add_file_dialog(self, name, target, images):
        files = sg.popup_get_file(title=name, multiple_files=True, message="Select file to add",
                                  initial_folder=self.selected_row.directory)
        if files is not None:
            for file in files.split(';'):
                target.append(file)
            if images:
                self.update_images_widgets()
            else:
                self.layout.model_files_list.update(values=self.selected_row.filenames)
                self.layout.model_files_list.TKListbox.xview_moveto(1)

    def add_tags_dialog(self):
        tags = sg.popup_get_text(title='Enter New Tags', message="Tags can be separated by ';'")
        if tags is not None and tags.strip() != '':
            for tag in tags.split(';'):
                self.selected_row.tags.append(tag.strip())
            self.layout.model_tags_list.update(values=self.selected_row.tags)
            self.layout.model_tags_list.TKListbox.xview_moveto(1)

    def validate_model(self):
        if not os.path.exists(self.selected_row.directory) or not os.path.isdir(self.selected_row.directory):
            self.layout.model_directory_input.update(value='.')
        for index, file in enumerate(self.selected_row.filenames):
            if not os.path.exists(file) or not os.path.isfile(file):
                self.selected_row.filenames.pop(index)
        self.layout.model_files_list.update(values=self.selected_row.filenames)
        self.layout.model_files_list.TKListbox.xview_moveto(1)
        for index, image in enumerate(self.selected_row.images):
            if not os.path.exists(image) or not os.path.isfile(image):
                self.selected_row.images.pop(index)
        self.update_images_widgets()

    def delete_model(self):
        confirmation = sg.popup_ok_cancel('Do you want to delete this model? (It will be removed from database)',
                                          title='Delete Model')
        if confirmation == 'OK':
            self.models.remove(self.selected_row)
            self.database.delete_model(self.selected_row.id)
            if len(self.models) == 0:
                self.selected_row = STLModel()
            else:
                self.select_model([-1])
            self.layout.models_table.update(MainWindowLayout.prepare_rows(self.models))

    def filter(self, filters):
        self.models = self.database.get_filtered_stl_models(filters)
        self.layout.models_table.update(MainWindowLayout.prepare_rows(self.models), select_rows=[0])
        self.select_model([0])

    def import_model(self):
        new_model = modal_window_import_model()
        if(new_model is not None):
            self.database.add_stl_model(new_model)
            self.refresh_models()

    def refresh_models(self):
        self.models = self.database.get_stl_models()
        self.layout.models_table.update(MainWindowLayout.prepare_rows(self.models))
        self.refresh_authors()


class MainWindowLayout:
    ALL_AUTHORS = 'all'

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

    def __init__(self, models, authors, disable_buttons, selected_row):
        authors_data = [MainWindowLayout.ALL_AUTHORS]
        authors_data.extend(authors)
        self.authors_combo = sg.Combo(values=authors_data, key=MainWindow.AUTHORS_FILTER, enable_events=True)
        self.column_filters = sg.Column([[sg.Text(text='Author Filter')], [self.authors_combo]], expand_x=True,
                                        vertical_alignment='top')
        # models table and controls
        self.add_model_button = sg.Button('Import Model', key=MainWindow.ADD_MODEL_BUTTON)
        self.models_table = sg.Table(self.prepare_rows(models), headings, key=MainWindow.MODELS_TABLE_,
                                     vertical_scroll_only=False, auto_size_columns=False,
                                     col_widths=[10, 40, 100, 10, 20], num_rows=20, enable_events=True)
        self.column_models = sg.Column([[self.add_model_button], [self.models_table]], expand_x=True)

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

        self.model_files_list = sg.Listbox(values=selected_row.filenames, size=(70, 5), key=MainWindow.MODEL_FILES_)
        self.model_images_list = sg.Listbox(values=selected_row.images, size=(70, 5), key=MainWindow.MODEL_IMAGES_,
                                            enable_events=True)
        self.model_tags_list = sg.Listbox(values=selected_row.tags, size=(70, 5), key=MainWindow.MODEL_TAGS_)
        self.model_supported_checkbox = sg.Checkbox(text='', default=selected_row.supported,
                                                    key=MainWindow.MODEL_SUPPORTED_)
        self.model_printed_checkbox = sg.Checkbox(text='', default=selected_row.printed, key=MainWindow.MODEL_PRINTED_)
        self.column_information = sg.Column(
            [[sg.Text(text="Model Name:", size=(12, 1)), self.model_name_input],
             [sg.Text(text="Model Author:", size=(12, 1)), self.model_author_input],
             [sg.Text(text="Model Directory:", size=(12, 1)), self.model_directory_input, ],
             [sg.Text(text="Model Files:", size=(12, 1)), self.model_files_list],
             [sg.Text(text="Model Images:", size=(12, 1)), self.model_images_list],
             [sg.Text(text="Supported:", size=(12, 1)), self.model_supported_checkbox],
             [sg.Text(text="Printed:", size=(12, 1)), self.model_printed_checkbox],
             [sg.Text(text="Model Tags:", size=(12, 1)), self.model_tags_list], ],
            expand_x=True, expand_y=True, vertical_scroll_only=True)
        # model controls
        self.open_directory_button = sg.Button('Open Model Directory', key=MainWindow.OPEN_DIRECTORY_BUTTON_,
                                               size=(20, 1))
        self.add_image_button = sg.Button('Add Image', key=MainWindow.ADD_IMAGE_BUTTON_, size=(20, 1))
        self.add_file_button = sg.Button('Add File', key=MainWindow.ADD_FILE_BUTTON_, size=(20, 1))
        self.add_tag_button = sg.Button('Add Tags', key=MainWindow.ADD_TAG_BUTTON_, size=(20, 1))
        self.save_changes_button = sg.Button('Save Changes', key=MainWindow.SAVE_CHANGES_BUTTON_, size=(20, 1))
        self.validate_button = sg.Button('Validate Model', key=MainWindow.VALIDATE_BUTTON_, size=(20, 1))
        self.delete_button = sg.Button('Delete Model', key=MainWindow.DELETE_BUTTON_, size=(20, 1))
        self.column_controls = sg.Column(
            [[self.open_directory_button], [sg.HorizontalSeparator()], [self.add_file_button], [self.add_image_button],
             [self.add_tag_button], [sg.HorizontalSeparator()], [self.save_changes_button], [sg.HorizontalSeparator()],
             [self.validate_button], [self.delete_button]], expand_x=True, expand_y=True, size=(10, 1))
        self.layout = [[self.column_filters, self.column_models],
                       [self.column_image, self.column_information, self.column_controls]]
