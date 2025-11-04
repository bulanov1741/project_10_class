from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class ProfileScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = ProfileBox()
        self.add_widget(self.theory_box)

class ProfileBox(BoxLayout):
    def __init__(self):
        super().__init__()
        button_title = Button(
            text="Профиль",
            pos_hint={"center_x": 0.25, "center_y": 0.5},
        )
        self.add_widget(button_title)