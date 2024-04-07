

import kivy

import cv2

import pytesseract

import os

import PIL

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput

from os.path import exists
from os import remove

__version__ = '0.0.1'

Window.size = (380, 620)
Builder.load_file('design.kv')

class GeneralWindow(Widget):
    #ГАЛЕРЕЯ
    def openGallery(self):


        self.grid.clear_widgets()    
        self.myImg = Image(source='',
                           size_hint = (1, 2))
        self.grid.add_widget(self.myImg)
        self.file_chooser = FileChooserIconView(path='/Users/nikita/Pictures',
                                                size_hint = (1.1, 4))
                                                
        self.grid.add_widget(self.file_chooser)
        self.bind(on_touch_down=self.select_file)

    def select_file(self, instance, touch):
        if self.collide_point(*touch.pos):
            for file in self.file_chooser.selection:
                self.myImg.export_to_png('./gallery.png')
                self.myImg.source = file
                break

    #нажатие кнопки КАМЕРА
    def photoTake(self, *args):
        if  self.grid.children:        
            self.myCamera.export_to_png('./picture.png')
            print("ФОТОЧКУ СДЕЛАЛь")
            self.myCamera.play = False
            self.grid.clear_widgets()
            self.grid.clear_widgets()
            if exists("./picture.png"):
                self.photoImg = Image(source = ("./picture.png"))
                self.grid.add_widget(self.photoImg)
                print("rabotaet")
                self.photoImg.reload()
            else:
                pass
    
    def onCamera(self):
        self.grid.clear_widgets()
        self.myCamera = Camera(resolution = (1920, 2000),
                                play = True)
                                
        self.grid.add_widget(self.myCamera)
        print("включил")
        self.btn = Button(text = 'фото',
                        pos_hint={'center_x': 0.5,
                                  'center_y': 1},
                        size_hint = (.4, .2),
                        background_normal = '',
                        background_color = (0, 144, 255, 1),
                        color = (1, 1, 0, 1),
                        bold = True,
                        outline_width = 3,
                        on_press = self.photoTake
                        )
        self.grid.add_widget(self.btn)




        #СКАН ТЕКСТА
    def read_text_from_image(self):
        if exists("./picture.png") and exists('./gallery.png'):
            time1 = os.path.getmtime('./picture.png')
            time2 = os.path.getmtime('./gallery.png')
            if time1 > time2:
                image = cv2.imread('./picture.png')
            else:
                image = cv2.imread('./gallery.png')
            # Извлечение текста с помощью Tesseract
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)

            textImg = pytesseract.image_to_string(img_thresh, lang='eng+rus')
            print('работает', textImg)
            self.labelText = TextInput(text = textImg)
            self.grid.clear_widgets()
            self.grid.add_widget(self.labelText)
            
             
        else:
            self.lb = Label(text = 'Ой((')
            self.grid.clear_widgets()
            self.grid.add_widget(self.lb)
    



     


class MyApp(App):
    def build(self):   
        Window.clearcolor = (50/255, 199/255, 168/255, 1)  #Вот тут все понятно, Без заморочек красит мне все окно
        print('КИВИ',kivy.__version__)
        return GeneralWindow()


if __name__ == '__main__':
    MyApp().run()

