import webbrowser

import pyperclip as pyperclip
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)

    def instruction_pressed(self):
        with open('templates/instruction.txt', encoding='utf-8') as file:
            text = file.read()
            popup = Popup(title='Инструкция', content=Label(text=text), size_hint=(None, None), size=(self.width / 3 * 2, 400))
            popup.open()

    def email_clicked(self):
        pyperclip.copy("notebasic@yandex.ru")
        popup = Popup(title='Скопировано', content=Label(text="Адрес добавлен в буфер обмены"), size_hint=(None, None),
                      size=(400, 400))
        popup.open()


