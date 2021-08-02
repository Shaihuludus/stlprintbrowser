import os
import sys

from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager

from model_importer import import_model

Builder.load_file('./stlprintbrowser/gui/screens.kv')


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
                import_model(path, self.ids.import_author.text, self.ids.import_name.text, self.ids.import_tags.txt)
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
