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
        self.width = 60
        self.hint_y = 0.1

        self.save_file = Button(width=50, size_hint=(None, self.hint_y), background_normal='save_file.png') # text="Сохранить файл",
        self.new_file = Button(width=50, size_hint=(None, self.hint_y), background_normal='add_file.png') #text="Новый файл",
        self.draw = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='drawing.png') # text="Режим рисования",

        self.choice_of_tonality = Button(width=50, size_hint=(None, self.hint_y)) #text="Выбор тональности",
        self.choice_of_time_signature = Button(width=50, size_hint=(None, self.hint_y)) #text="Выбор размера",

        self.flat = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='flat.png') # text="Бемоль",
        self.sharp = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='sharp.png') # text="Диез",
        self.natural = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='natural.png') #text="Бекар",

        self.whole = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='whole.png') # text="Целая",
        self.half = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='half.png') # text="Половинка",
        self.quarter = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='quarter.png') # text="Четверь",
        self.eighth = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='eighth.png') #text="Восьмая",
        self.sixteenth = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='sixteenth.png') # text="Шестнадцая",
        self.thirty_second = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='thirty_second.png') # text="Тридцать вторая",

        self.whole_pause = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='whole.png') # text="Целая пауза",
        self.half_pause = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='half.png') # text="Половинка пауза",
        self.quarter_pause = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='quarter_pause.png') # text="Четверь пауза",
        self.eighth_pause = Button(width=self.width, size_hint=(None, self.hint_y),background_normal='eighth_pause.png') # text="Восьмая пауза",
        self.sixteenth_pause = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='sixteenth_pause.png') # text="Шестнадцая пауза",
        self.thirty_second_pause = Button(width=self.width, size_hint=(None, self.hint_y), background_normal='thirty_second_pause.png') # text="Тридцать вторая пауза",

        self.dot = Button(text="Точка", width=self.width, size_hint=(None, self.hint_y))
        self.tie = Button(text="Лига", width=self.width, size_hint=(None, self.hint_y))


        self.list_instruments = [self.flat, self.sharp, self.natural, self.whole, self.half, self.quarter, self.eighth,
                                 self.sixteenth, self.thirty_second,
                                 self.whole_pause, self.half_pause, self.quarter_pause, self.eighth_pause,
                                 self.sixteenth_pause, self.thirty_second_pause]

        for i in self.list_instruments:
            self.add_widget(i)
