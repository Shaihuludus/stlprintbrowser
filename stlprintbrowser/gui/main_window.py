import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from stlprintbrowser.gui.widgets import CarouselItem
from stlprintbrowser.gui.screens import ImportScreen, DetailsScreen
from stlprintbrowser.stlmodel import STLModel


Builder.load_file('./stlprintbrowser/gui/widgets.kv')

class MainWindowController():

    def __init__(self,database):
        self.database = database
        self.retrieve_authors()
        self.models = self.database.get_stl_models()
        self.current_model = STLModel()

    def retrieve_authors(self):
        self.authors = set()
        for model in self.database.get_stl_models():
            self.authors.add(model.author)
        self.authors.add('All')
        return self.authors

    def load_model_details(self, id):
        self.current_model = self.models[id]
        if(len(self.current_model.images)>0):
            return self.current_model.images
        return {}

    def filter_models(self,filters):
        self.current_model = STLModel()
        self.models = self.database.get_filtered_stl_models(filters)

    def delete_models(self,models):
        for model in models:
            self.database.delete_model(self.models[int(model[4])].id)
        self.current_model = STLModel()
        self.models = self.database.get_stl_models()


class MainApp(MDApp):

    confirm_delete_dialog = None

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
        self.root.ids.import_screen.bind_main_window(self)
        self.root.ids.details_screen.bind_main_window(self)
        self.root.ids.details_screen.set_model(self.main_window_controller.current_model)

    def load_preview_previous(self,touch):
        self.root.ids.preview_image.load_previous()

    def on_authors_filter(self,spinner, text):
        self.main_window_controller.filter_models({'author':text})
        self.models_table.row_data = self.prepare_rows()
        self.reset_carousel()

    def refresh_models(self):
        self.main_window_controller.filter_models({})
        self.main_window_controller.retrieve_authors()
        self.models_table.row_data = self.prepare_rows()
        self.root.ids.authors_filter.values = self.main_window_controller.authors
        self.root.ids.authors_filter.text = 'All'
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
                ("Tags", dp(110)),
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
        images = self.main_window_controller.load_model_details(index)
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
        self.root.ids.details_screen.set_model(self.main_window_controller.current_model)

    def prepare_rows(self):
        data = []
        for index,model in enumerate(self.main_window_controller.models):
            single_entry = (model.name, '; '.join(model.tags), model.printed, model.author,index)
            data.append(single_entry)
        return data

    def prepare_table_menu(self):
        menu_items = [
            {
                "id": 'table_open',
                "viewclass": "OneLineListItem",
                "text": f"Open Selected Model Catalog",
                "height": dp(56),
                "on_release": lambda x=f"OpenModelCatalog": self.open_directories(x),
            },{
                "id": 'table_delete',
                "viewclass": "OneLineListItem",
                "text": f"Delete Selected Model",
                "height": dp(56),
                "on_release": lambda x=f"DeleteModel": self.delete_models_dialog(x),
            }
        ]
        self.tableMenu = MDDropdownMenu(
            items=menu_items,
            width_mult=4)

    def table_menu(self,button):
        self.tableMenu.caller = button
        self.tableMenu.open()

    def open_directories(self, touch):
        if len(self.models_table.get_row_checks())>0:
            for selected_rows in self.models_table.get_row_checks():
                os.startfile(self.main_window_controller.models[int(selected_rows[4])].directory)
        else:
            Popup(title='Error', content=Label(text='Please select models first'),size_hint=(None, None), size=(400, 400)).open()


    def delete_models_dialog(self, touch):
        if len(self.models_table.get_row_checks())>0 and not self.confirm_delete_dialog:
            self.confirm_delete_dialog = MDDialog(
                text="Remove models?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,
                        on_press = self.close_confirm_delete_dialog
                    ),
                    MDFlatButton(
                        text="CONFIRM", text_color=self.theme_cls.primary_color,
                        on_press = self.delete_models
                    ),
                ],
            )
            self.confirm_delete_dialog.open()
        else:
            Popup(title='Error', content=Label(text='Please select models first'),size_hint=(None, None), size=(400, 400)).open()

    def delete_models(self, touch):
        self.main_window_controller.delete_models(self.models_table.get_row_checks())
        self.refresh_models()
        self.confirm_delete_dialog.dismiss(force=True)
        self.confirm_delete_dialog = None

    def close_confirm_delete_dialog(self,touch):
        self.confirm_delete_dialog.dismiss(force=True)
        self.confirm_delete_dialog = None

    def open_details(self):
        if self.main_window_controller.current_model.directory != '':
            self.root.ids.tools_browser.current = "details_tool"
        else:
            Popup(title='Error', content=Label(text='Please select file first'),size_hint=(None, None), size=(400, 400)).open()


    def reset_carousel(self):
        self.root.ids.preview_image.clear_widgets()
        self.root.ids.carousel_buttons.opacity=0
        self.root.ids.carousel_previous.disabled = True
        self.root.ids.carousel_next.disabled = True


