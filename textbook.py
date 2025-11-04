from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from const import Const


class TextbookScreen(Screen):
    def __init__(self):
        super().__init__()
        self.textbook_box = TextbookBox()
        self.add_widget(self.textbook_box)

        # Обновление размеров элементов при изменении размера виджета
        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        pass


class TextbookBox(BoxLayout):
    def __init__(self):
        super().__init__()
        self.note_page = NotePage(size_hint=(None, None), size=(self.width, self.width * 2 ** 0.5))
        self.scroll_page = ScrollView()
        self.scroll_page.add_widget(self.note_page)
        self.scroll_page.size_hint_x = 100
        self.scroll_page.size_hint_y = 5
        self.add_widget(self.scroll_page)
        self.keyboard = ImagePaste('img.png', self.width, self.height, (self.width, self.height / 5), (0, 0))
        self.add_widget(self.keyboard)

        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        self.clear_widgets()
        self.note_page = NotePage(size_hint=(None, None), size=(self.width, self.width * 2 ** 0.5))
        self.scroll_page = ScrollView()
        self.scroll_page.size_hint_x = 100
        self.scroll_page.add_widget(self.note_page)
        self.add_widget(self.scroll_page)
        self.keyboard = ImagePaste('img.png', self.width, self.height, (self.width, self.height / 5), (0, 0))
        self.add_widget(self.keyboard)

    # Обработка нажатий или движений
    def on_touch_down(self, touch):
        super(TextbookBox, self).on_touch_down(touch)
        if not self.collide_point(*touch.pos):
            return False
        else:
            if touch.pos[1] <= self.height / 5:
                if touch.button == 'left':
                    if touch.pos[1] >= self.height / 10 and (
                            self.width / 28 * 3 <= touch.pos[0] <= self.width / 28 * 5):
                        print("До# / Реb")
                    elif touch.pos[1] >= self.height / 10 and (
                            self.width / 28 * 7 <= touch.pos[0] <= self.width / 28 * 9):
                        print("Ре# / Миb")
                    elif touch.pos[1] >= self.height / 10 and (
                            self.width / 28 * 15 <= touch.pos[0] <= self.width / 28 * 17):
                        print("Фа# / Сольb")
                    elif touch.pos[1] >= self.height / 10 and (
                            self.width / 28 * 19 <= touch.pos[0] <= self.width / 28 * 21):
                        print("Соль# / Ляb")
                    elif touch.pos[1] >= self.height / 10 and (
                            self.width / 28 * 23 <= touch.pos[0] <= self.width / 28 * 25):
                        print("Ля# / Сиb")
                    elif touch.pos[0] <= self.width / 7:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 5,
                                       0)
                        print("До")
                    elif touch.pos[0] <= self.width / 7 * 2:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 4.5,
                                       1)
                        print("Ре")
                    elif touch.pos[0] <= self.width / 7 * 3:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 4,
                                       2)
                        print("Ми")
                    elif touch.pos[0] <= self.width / 7 * 4:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 3.5,
                                       3)
                        print("Фа")
                    elif touch.pos[0] <= self.width / 7 * 5:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 3,
                                       4)
                        print("Соль")
                    elif touch.pos[0] <= self.width / 7 * 6:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 2.5,
                                       5)
                        print("Ля")
                    elif touch.pos[0] <= self.width:
                        self.draw_note(self.note_page.height / 10 * 9 - self.note_page.current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 2,
                                       6)
                        print("Си")
        return True

    def draw_note(self, y, ind):
        if self.note_page.current_clef == 1:
            with self.note_page.canvas:
                Color(0, 0, 0, 1)
                Ellipse(pos=(
                    int(self.note_page.current_pos_1) - self.note_page.k_size_note,
                    y - self.note_page.k_size_note // 2),
                    size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                Line(points=(
                    int(self.note_page.current_pos_1) + self.note_page.k_size_note, y + self.note_page.k_size_note // 2,
                    int(self.note_page.current_pos_1) + self.note_page.k_size_note, y + self.note_page.k_size_note * 4))
                if ind % 2 == 0:
                    Line(points=(
                        int(self.note_page.current_pos_1) - self.note_page.k_size_note * 2, y,
                        int(self.note_page.current_pos_1) + self.note_page.k_size_note * 2, y))
                self.note_page.list_of_notes_treble.append(
                    (16 - ind, self.note_page.current_pos_1, self.note_page.current_duration, 0))
                self.note_page.current_pos_1 += self.note_page.each_note / int(
                    self.note_page.current_duration.split('/')[0]) * int(
                    self.note_page.current_duration.split('/')[1])
        else:
            with self.note_page.canvas:
                Color(0, 0, 0, 1)
                Ellipse(pos=(int(self.note_page.current_pos_2) - self.note_page.k_size_note,
                             y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2),
                        size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                Line(points=(int(self.note_page.current_pos_2) + self.note_page.k_size_note,
                             y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note // 2,
                             int(self.note_page.current_pos_2) + self.note_page.k_size_note,
                             y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note * 4))
                if ind % 2 == 1:
                    Line(points=(
                        int(self.note_page.current_pos_2) - self.note_page.k_size_note * 2,
                        y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12,
                        int(self.note_page.current_pos_2) + self.note_page.k_size_note * 2,
                        y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12))

                self.note_page.list_of_notes_bass.append(
                    (11 - ind, self.note_page.current_pos_2, self.note_page.current_duration, 0))

                self.note_page.current_pos_2 += self.note_page.each_note / int(
                    self.note_page.current_duration.split('/')[0]) * int(
                    self.note_page.current_duration.split('/')[1])
        self.make_beat()


class NotePage(Widget):
    def __init__(self, **kwargs):
        super(NotePage, self).__init__(**kwargs)

        self.list_of_notes_treble = []  # Все ноты скрипичного ключа
        self.list_of_notes_bass = []  # Все ноты басового ключа
        self.time_signature = '4/4'  # Размер произведения
        self.current_string = 0  # Текущая строка
        self.current_duration = '1/4'  # По умолчанию длительность
        self.each_note = self.width * 8 / 9 / 4 / (
                int(self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1]))  # На каждую четверть
        self.current_pos_1 = self.width / 9 + len(
            self.list_of_notes_treble) * self.each_note  # Текущая позиция Скр. ключ
        self.current_pos_2 = self.width / 9 + len(self.list_of_notes_bass) * self.each_note  # Текущая позиция Бас.ключ
        self.y_pos = [self.height // 200 * i for i in range(-6, 14)]  # Позиция по вертикали (все возможные)
        self.current_clef = 1  # Текущий знак (для работы с клавиатурой)
        self.k_size_note = self.height // 100  # Коэфф размера ноты
        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        print(self.list_of_notes_treble, self.list_of_notes_bass, sep='\n')
        self.clear_widgets()
        with self.canvas:
            Color(rgba=(1, 1, 1, 1))
            self.rect = Rectangle(size=self.size, pos=self.pos)
            interval = self.height / 10
            for string in range(6):
                for i in range(5):
                    Color(0, 0, 0, 1)  # RGBA
                    Line(points=(0, self.height - interval - i * self.height // 100, self.width,
                                 self.height - interval - i * self.height // 100))
                if string % 2 == 0:
                    self.clef = Image(source='treble_clef.png', allow_stretch=True, keep_ratio=False)
                    self.clef.height = self.height // 20
                    self.clef.width = self.width / 9
                else:
                    self.clef = Image(source='bass_clef.png', allow_stretch=False, keep_ratio=True)
                    self.clef.height = self.height // 20
                    self.clef.width = self.width / 9
                self.clef.pos = (0, self.height - interval - 4 * self.height // 100)
                interval += self.height / 12

    def on_touch_down(self, touch):
        with self.canvas:
            if touch.button == 'left':
                interval = self.height / 10 * 9 - self.current_string * (self.height / 6 + self.height // 100 * 8)
                if interval + self.height // 100 * 3 >= touch.pos[1] >= interval - (
                        self.height / 12 + self.height // 100 * 11):
                    Color(rgba=(0, 0, 0, 1))
                    if touch.pos[1] >= (interval - (self.height / 48 + self.height // 100 * 4)):
                        index = [abs(touch.pos[1] - interval + j) for j in self.y_pos].index(
                            min([abs(touch.pos[1] - interval + i) for i in self.y_pos]))
                        y = [interval - j for j in self.y_pos][index]
                        Ellipse(pos=(int(self.current_pos_1) - self.k_size_note, y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                        Line(points=(int(self.current_pos_1) + self.k_size_note, y + self.k_size_note // 2,
                                     int(self.current_pos_1) + self.k_size_note, y + self.k_size_note * 4))
                        if index % 2 == 0:
                            Line(points=(
                                int(self.current_pos_1) - self.k_size_note * 2, touch.pos[1],
                                int(self.current_pos_1) + self.k_size_note * 2, touch.pos[1]))
                        self.list_of_notes_treble.append((index, self.current_pos_1, self.current_duration, 0))
                        self.current_pos_1 += self.each_note / int(self.current_duration.split('/')[0]) * int(
                            self.current_duration.split('/')[1])
                        self.current_clef = 1
                    else:
                        index = [abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + j) for j in
                                 self.y_pos].index(
                            min([abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + i) for i in
                                 self.y_pos]))
                        y = [interval - (self.height / 24 + self.height // 100 * 4) - j for j in self.y_pos][index]
                        Ellipse(pos=(int(self.current_pos_2) - self.k_size_note, y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                        Line(points=(int(self.current_pos_2) + self.k_size_note, y + self.k_size_note // 2,
                                     int(self.current_pos_2) + self.k_size_note, y + self.k_size_note * 4))
                        if index % 2 == 0:
                            Line(points=(
                                int(self.current_pos_2) - self.k_size_note * 2, y,
                                int(self.current_pos_2) + self.k_size_note * 2, y))
                            self.list_of_notes_bass.append((index, self.current_pos_2, self.current_duration, 0))
                        self.current_pos_2 += self.each_note / int(self.current_duration.split('/')[0]) * int(
                            self.current_duration.split('/')[1])
                        self.current_clef = 2
                    self.make_beat()

    # Такты
    def make_beat(self):
        for i in range(int(max(sum([int(x[2].split('/')[0]) / int(x[2].split('/')[1]) for x in self.list_of_notes_treble]),
                           sum([int(x[2].split('/')[0]) / int(x[2].split('/')[1]) for x in self.list_of_notes_bass])) / int(
            self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1]))):
            with self.canvas:
                Color(0, 0, 0, 1)
                Line(points=(self.width / 4 * (i + 1),
                             self.height / 10 * 9 - self.current_string * (self.height / 6 + self.height // 100 * 8),
                             self.width / 4 * (i + 1),
                             self.height / 10 * 9 - self.current_string * (self.height / 6 + self.height // 100 * 8) - self.height // 100 * 4))
                Line(points=(self.width / 4 * (i + 1),
                             self.height / 10 * 9 - self.current_string * (self.height / 6 + self.height // 100 * 8) - (
                                         self.height / 24 + self.height // 100 * 4),
                             self.width / 4 * (i + 1),
                             self.height / 10 * 9 - self.current_string * (self.height / 6 + self.height // 100 * 8) - (
                                         self.height / 24 + self.height // 100 * 8)))


class ImagePaste(Widget):
    def __init__(self, source, width_w, height_w, size, pos):
        self.source = source
        self.width_w, self.height_w = width_w, height_w
        self.size_, self.pos_ = size, pos
        super(ImagePaste, self).__init__()

        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        with self.canvas:
            self.image = Image(source=self.source, allow_stretch=True, keep_ratio=False)
            self.image.size = self.size_
            self.image.pos = self.pos_


'''
1. Сохранение файла
2. Создать новый файл
2. Выбор тональности
3.Выбор знаков
4. Выбор длительности
5. Выбор паузы
6. Добавление диеза или бемоля
 self.list_of_notes_bass.append((index, self.current_pos, self.current_duration, signature))
'''
