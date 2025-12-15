from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class ProfileScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = ProfileBox()
        self.add_widget(self.theory_box)

class ProfileBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 6
        # Логин
        self.name_label = Label(
            text="Логин",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        text_input = TextInput(hint_text='Введите логин', multiline=False, size_hint=(1, .8))
        self.add_widget(self.name_label)
        self.add_widget(text_input)
        # Почта
        self.name_label = Label(
            text="Почта",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        text_input = TextInput(hint_text='Введите Email', multiline=False, size_hint=(1, .8))
        self.add_widget(self.name_label)
        self.add_widget(text_input)
        #Пароль
        self.name_label = Label(
            text="Пароль",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        text_input = TextInput(hint_text='Введите пароль', multiline=False, size_hint=(1, .8), password=True)
        self.add_widget(self.name_label)
        self.add_widget(text_input)
        #Имя
        self.name_label = Label(
            text="Имя",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        text_input = TextInput(hint_text='Введите имя', multiline=False, size_hint=(1, .8))
        self.add_widget(self.name_label)
        self.add_widget(text_input)
        #Сохранение
        self.button_save = Button(text="Сохранить")
        self.button_cancel = Button(text="Отмена")
        self.add_widget(self.button_cancel)
        self.add_widget(self.button_save)