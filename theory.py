from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout


class TheoryScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = InstrumentsBox()
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

        self.size_hint = (1, 1)
        self.add_widget(layout)


class InstrumentsBox(StackLayout):
    def __init__(self):
        super().__init__()
        self.save_file = Button(text="Сохранить файл", width=50, size_hint=(None, 0.15), )
        self.new_file = Button(text="Новый файл", width=50, size_hint=(None, 0.15))

        self.choice_of_tonality = Button(text="Выбор тональности", width=50, size_hint=(None, 0.15))
        self.choice_of_time_signature = Button(text="Выбор размера", width=50, size_hint=(None, 0.15))

        self.flat = Button(text="Бемоль", width=100, size_hint=(None, 0.15))
        self.sharp = Button(text="Диез", width=100, size_hint=(None, 0.15))
        self.whole = Button(text="Целая", width=100, size_hint=(None, 0.15), background_normal='whole.png')
        self.half = Button(text="Половинка", width=100, size_hint=(None, 0.15), background_normal='half.png')
        self.quarter = Button(text="Четверь", width=100, size_hint=(None, 0.15), background_normal='quarter.png')
        self.eighth = Button(text="Восьмая", width=100, size_hint=(None, 0.15), background_normal='eighth.png')
        self.sixteenth = Button(text="Шестнадцая", width=100, size_hint=(None, 0.15), background_normal='sixteenth.png')
        self.thirty_second = Button(text="Тридцать вторая", width=100, size_hint=(None, 0.15), background_normal='whole.png')

        self.whole_pause = Button(text="Целая пауза", width=100, size_hint=(None, 0.15), background_normal='whole.png')
        self.half_pause = Button(text="Половинка пауза", width=100, size_hint=(None, 0.15), background_normal='whole.png')
        self.quarter_pause = Button(text="Четверь пауза", width=100, size_hint=(None, 0.15), background_normal='whole.png')
        self.eighth_pause = Button(text="Восьмая пауза", width=100, size_hint=(None, 0.15),background_normal='whole.png')
        self.sixteenth_pause = Button(text="Шестнадцая пауза", width=100, size_hint=(None, 0.15), background_normal='whole.png')
        self.thirty_second_pause = Button(text="Тридцать вторая пауза", width=100, size_hint=(None, 0.15), background_normal='whole.png')

        self.dot = Button(text="Точка", width=100, size_hint=(None, 0.15))
        self.tie = Button(text="Лига", width=100, size_hint=(None, 0.15))


        self.list_instruments = [self.flat, self.sharp, self.whole, self.half, self.quarter, self.eighth,
                                 self.sixteenth, self.thirty_second,
                                 self.whole_pause, self.half_pause, self.quarter_pause, self.eighth_pause,
                                 self.sixteenth_pause, self.thirty_second_pause]

        for i in self.list_instruments:
            self.add_widget(i)
