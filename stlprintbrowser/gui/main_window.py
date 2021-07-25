from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu

class MainWindowController():

    def __init__(self,database):
        self.database = database
        self.authors = self.retrieve_authors()
        self.models = self.database.get_stl_models()

    def retrieve_authors(self):
        authors = set()
        for model in self.database.get_stl_models():
            authors.add(model.author)
        authors.add('All')
        return authors

class MainApp(MDApp):

    def __init__(self,mainWindowController):
        MDApp.__init__(self)
        self.mainWindowController = mainWindowController

    def build(self):
        self.root.ids.authors_filter.values = self.mainWindowController.authors
        self.root.ids.table_part.add_widget(self.prepare_table())
        self.prepare_table_menu()
        self.root.ids.rail.anim_color_active(self.root.ids.nav_table_item)


    def prepare_table(self):
        return MDDataTable(
            size_hint=(1,1),
            pos_hint={'center_x': .5,'center_y': .5},
            check=True,
            use_pagination=True,
            rows_num =15,
            column_data=[
                ("Name", dp(70)),
                ("Directory", dp(110)),
                ("Printed", dp(20)),
                ("Author", dp(50))
            ],
            row_data = self.prepare_rows()
        )

    def prepare_rows(self):
        data = []
        for model in self.mainWindowController.models:
            single_entry = (model.name, model.directory, model.printed, model.author)
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