from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class TheoryScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = TheoryScrollView()
        self.add_widget(self.theory_box)

class TheoryScrollView(ScrollView):
    def __init__(self):
        super().__init__()
        # button_title = Button(
        #     text="Теория",
        #     pos_hint={"center_x": 0.25, "center_y": 0.5},
        # )
        # self.add_widget(button_title)

        layout = GridLayout(cols=1, size_hint_y=None)
        # Устанавливаем высоту GridLayout динамически
        layout.bind(minimum_height=layout.setter('height'))

        label = Label(text=f'Теория', size_hint_y=None, height=100)
        layout.add_widget(label)
        for i in range(100):
            label = Label(text=f'Label {i}', size_hint_y=None, height=40)
            layout.add_widget(label)

        self.size_hint =(1, 1)
        self.add_widget(layout)