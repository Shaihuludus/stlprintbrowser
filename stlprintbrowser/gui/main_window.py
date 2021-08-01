from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

from gui.widgets import CarouselItem
from gui.screens import ImportScreen
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
        return {}

    def filter_models(self,filters):
        self.current_model = STLModel()
        self.models = self.database.get_filtered_stl_models(filters)


class MainApp(MDApp):

    def __init__(self,main_window_controller):
        MDApp.__init__(self)
        self.main_window_controller = main_window_controller

    def build(self):
        self.root.ids.authors_filter.values = self.main_window_controller.authors
        self.root.ids.authors_filter.bind(text = self.on_authors_filter)
        self.models_table = self.prepare_table()
        self.root.ids.table_part.add_widget(self.models_table)
        self.prepare_table_menu()
        self.root.ids.rail.anim_color_active(self.root.ids.nav_table_item)
        self.root.ids.carousel_next.bind(on_press = self.root.ids.preview_image.load_next)
        self.root.ids.carousel_previous.bind(on_press = self.load_preview_previous)
        self.root.ids.import_screen.after_created()

    def load_preview_previous(self,touch):
        self.root.ids.preview_image.load_previous()

    def on_authors_filter(self,spinner, text):
        self.main_window_controller.filter_models({'author':text})
        self.models_table.row_data = self.prepare_rows()
        self.reset_carousel()

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
        for index,path in enumerate(images):
            self.root.ids.preview_image.add_widget(CarouselItem(source = path,text=str(index+1)+' from ' + str(len(images))))
        if(len(images) ==0):
            self.root.ids.preview_image.add_widget(CarouselItem())
        if(len(images) >1):
            self.root.ids.carousel_buttons.opacity=1
            self.root.ids.carousel_previous.disabled = False
            self.root.ids.carousel_next.disabled = False
        else:
            self.root.ids.carousel_buttons.opacity=0
            self.root.ids.carousel_previous.disabled = True
            self.root.ids.carousel_next.disabled = True

    def prepare_rows(self):
        data = []
        for index,model in enumerate(self.main_window_controller.models):
            single_entry = (model.name, model.directory, model.printed, model.author,index)
            data.append(single_entry)
        return data

    def prepare_table_menu(self):
        menu_items = [
            {
                "id": 'table_open',
                "viewclass": "OneLineListItem",
                "text": f"Open Selected Model Catalog",
                "height": dp(56),
                "on_release": lambda x=f"OpenModelCatalog": self.menu_callback(x),
            },{
                "id": 'table_delete',
                "viewclass": "OneLineListItem",
                "text": f"Delete Selected Model",
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

    def reset_carousel(self):
        self.root.ids.preview_image.clear_widgets()
        self.root.ids.carousel_buttons.opacity=0
        self.root.ids.carousel_previous.disabled = True
        self.root.ids.carousel_next.disabled = True