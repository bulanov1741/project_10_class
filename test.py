from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView


class TestScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = TestScrollView()
        self.add_widget(self.theory_box)

class TestScrollView(ScrollView):
    def __init__(self):
        super().__init__()
        layout = GridLayout(cols=2, size_hint_y=None)
        # Устанавливаем высоту GridLayout динамически
        layout.bind(minimum_height=layout.setter('height'))

        for i in range(1, 51, 2):
            b_l = Button(text=f'Урок {i}', size_hint_y=None, height=40)
            b_r = Button(text=f'Урок {i+1}', size_hint_y=None, height=40)
            layout.add_widget(b_l)
            layout.add_widget(b_r)

        self.size_hint = (1, 1)
        self.add_widget(layout)