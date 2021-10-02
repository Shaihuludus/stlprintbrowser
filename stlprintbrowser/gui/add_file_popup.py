import os
import sys

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivymd.uix.filemanager import MDFileManager

Builder.load_file('./stlprintbrowser/gui/add_file_popup.kv')

class AddFilePopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.new_file = ''

    def after_created(self):
        if (sys.platform == 'win32'):
            drives = [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")]
            self.disk_chooser = Spinner(values=drives, size=(10, 40), pos_hint={'center_y': 0.5}, size_hint=(0.1, None),
                                        text=drives[0])
            self.ids.file_chooser_grid.add_widget(self.disk_chooser, 1)

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

    def import_file(self,*largs, **kwargs):
        self.new_file = self.ids.import_path.text
        self.dismiss(*largs, **kwargs)