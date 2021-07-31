from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

from stlmodel import STLModel


class MainWindowController():

    def __init__(self,database):
        self.database = database
        self.authors = self.retrieve_authors()
        self.models = self.database.get_stl_models()
        self.current_model = STLModel()

    def retrieve_authors(self):
        authors = set()
        for model in self.database.get_stl_models():
            authors.add(model.author)
        authors.add('All')
        return authors

    def loadImages(self, id):
        self.current_model = self.models[id]
        if(len(self.current_model.images)>0):
            return self.current_model.images
        return {'no_image_available.png'}

class MainApp(MDApp):

    def __init__(self,main_window_controller):
        MDApp.__init__(self)
        self.main_window_controller = main_window_controller

    def build(self):
        self.root.ids.authors_filter.values = self.main_window_controller.authors
        self.models_table = self.prepare_table()
        self.root.ids.table_part.add_widget(self.models_table)
        self.prepare_table_menu()
        self.root.ids.rail.anim_color_active(self.root.ids.nav_table_item)


    def prepare_table(self):
        models_table =  MDDataTable(
            size_hint=(1,1),
            pos_hint={'center_x': .5,'center_y': .5},
            check=True,
            use_pagination=True,
            rows_num =15,
            column_data=[
                ("Name", dp(70)),
                ("Directory", dp(110)),
                ("Printed", dp(20)),
                ("Author", dp(50)),
                ("", dp(0))
            ],
            row_data = self.prepare_rows()
        )
        models_table.bind(on_row_press = self.on_row_press)
        return models_table

    def on_row_press(self, instance_table, instance_row):
        index = int(instance_row.table.data_model.data[(instance_row.index - instance_row.index%len(instance_table.column_data))+len(instance_table.column_data)-1]['text'])
        images = self.main_window_controller.loadImages(index)
        self.root.ids.preview_image.clear_widgets()
        for path in images:
            self.root.ids.preview_image.add_widget(Image(source = path))

    def prepare_rows(self):
        data = []
        for index,model in enumerate(self.main_window_controller.models):
            single_entry = (model.name, model.directory, model.printed, model.author,index)
            data.append(single_entry)
        return data

    def prepare_table_menu(self):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Open Model Catalog",
                "height": dp(56),
                "on_release": lambda x=f"OpenModelCatalog": self.menu_callback(x),
            },{
                "viewclass": "OneLineListItem",
                "text": f"Delete Model",
                "height": dp(56),
                "on_release": lambda x=f"DeleteModel": self.menu_callback(x),
            }
        ]
        self.tableMenu = MDDropdownMenu(
            items=menu_items,
            width_mult=4)

    def table_menu(self,button):
        self.tableMenu.caller = button
        self.tableMenu.open()

    def menu_callback(self, x):
        pass