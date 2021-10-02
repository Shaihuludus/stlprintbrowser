import multiprocessing
import os
import subprocess
import sys

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.filemanager import MDFileManager

from stlprintbrowser.gui.add_file_popup import AddFilePopup
from stlprintbrowser.gui.widgets import CarouselItem
from stlprintbrowser.model_importer import import_model

Builder.load_file('./stlprintbrowser/gui/screens.kv')

STL_EXTENSIONS = {'.stl'}
MODEL_EXTENSIONS = {'.stl','.lys'}
IMAGE_EXTENSIONS = {'.jpg','.jpeg','.png'}

class ImportScreen(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bind_main_window(self, main_window):
        self.main_window = main_window

    def after_created(self):
        if (sys.platform == 'win32'):
            drives = [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")]
            self.disk_chooser = Spinner(values=drives, size=(10, 40), pos_hint={'center_y': 0.5}, size_hint=(0.1, None),
                                        text=drives[0])
            self.ids.file_chooser_grid.add_widget(self.disk_chooser, 1)
            self.ids.import_button.bind(on_press = self.import_model)

    def import_model(self,touch):
        path = self.ids.import_path.text
        if path is None or not os.path.isdir(path):
            Popup(title='Error', content=Label(text='Please select directory'),size_hint=(None, None), size=(400, 400)).open()
        else:
            if path[-1] != '/' and path[-1] != '\\':
                path += '/'
            if self.ids.import_many_models.active:
                for file in os.listdir(path):
                    if os.path.isdir(path + file):
                        import_model(path + file, self.ids.import_author.text, self.ids.import_name.text, self.ids.import_tags.text)
            else:
                import_model(path, self.ids.import_author.text, self.ids.import_name.text, self.ids.import_tags.text)
            self.main_window.refresh_models()
            self.ids.import_path.text = ''
            Popup(title='Success', content=Label(text='Models imported'),size_hint=(None, None), size=(400, 400)).open()

    def open_file_manager(self):
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        path = '/'
        if (sys.platform == 'win32'):
            path = self.disk_chooser.text + path
        self.file_manager.show(path)

    def select_path(self, path):
        self.ids.import_path.text = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

class DetailsScreen(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bind_main_window(self, main_window):
        self.main_window = main_window

    def reset_model(self):
        self.ids.details_preview_image.clear_widgets()
        self.ids.details_carousel_buttons.opacity=0
        self.ids.details_carousel_previous.disabled = True
        self.ids.details_carousel_next.disabled = True
        self.ids.files_list.clear_widgets()

    def set_model(self, model):
        self.reset_model()
        self.model = model
        self.ids.details_author.text = model.author
        self.ids.details_name.text = model.name
        self.ids.details_tags.text = '; '.join(model.tags)
        self.ids.details_printed.active = model.printed
        self.ids.details_supported.active = model.supported
        images = model.images
        self.models_table = self.prepare_files_table(model.filenames)
        self.ids.files_list.add_widget(self.models_table)
        for index,path in enumerate(images):
            self.ids.details_preview_image.add_widget(CarouselItem(source = path,text=str(index+1)+' from ' + str(len(images))))
        if(len(images) ==0):
            self.ids.details_preview_image.add_widget(CarouselItem())
        if(len(images) >1):
            self.ids.details_carousel_buttons.opacity=1
            self.ids.details_carousel_previous.disabled = False
            self.ids.details_carousel_next.disabled = False
        else:
            self.ids.details_carousel_buttons.opacity=0
            self.ids.details_carousel_previous.disabled = True
            self.ids.details_carousel_next.disabled = True

    def prepare_files_table(self,files):
        data = []
        for index,file in enumerate(files):
            data_entry = (index+1,file)
            data.append(data_entry)
        models_table =  MDDataTable(
            size_hint=(1,1),
            pos_hint={'center_x': .5,'center_y': .5},
            check=True,
            use_pagination=True,
            rows_num =15,
            column_data=[
                ("Nr", dp(20)),
                ("File Name", dp(200))
            ],
            row_data = data
        )
        return models_table

    def display_stl_file(self, touch):
        if(len(self.models_table.get_row_checks())>1 or len(self.models_table.get_row_checks())==0):
            Popup(title='Error', content=Label(text='Please select only one file'),size_hint=(None, None), size=(400, 400)).open()
        else:
            filename, file_extension = os.path.splitext(self.models_table.get_row_checks()[0][1])
            if(file_extension in STL_EXTENSIONS):
                os.system('python ./stlprintbrowser/stlrender/render_stl.py "'+self.models_table.get_row_checks()[0][1]+'"')
            else:
                Popup(title='Error', content=Label(text='Please select stl file'),size_hint=(None, None), size=(400, 400)).open()

    def open_directory(self, touch):
        os.startfile(self.model.directory)

    def open_files(self, touch):
        for selected_rows in self.models_table.get_row_checks():
            os.startfile(selected_rows[1])

    def add_files(self,instance):
        if(instance.new_file != ''):
            filename, file_extension = os.path.splitext(instance.new_file)
            print(file_extension)

    def add_files_open(self,touch):
        popup = AddFilePopup(title='Add files',size_hint=(None, None), size=(600, 300))
        popup.bind(on_dismiss=self.add_files)
        popup.after_created()
        popup.open()