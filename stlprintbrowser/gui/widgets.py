from kivymd.uix.boxlayout import MDBoxLayout

class CarouselItem(MDBoxLayout):
    def __init__(self,source = 'no_image_available.png',text = ''):
        self.image_source = source
        super().__init__(orientation = 'vertical')
        self.ids.image.source = source
        self.ids.text.text = text
