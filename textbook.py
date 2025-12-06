from functools import partial
from tkinter import filedialog

import tkinter as tk
from tkinter import filedialog

from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

from const import Const
from sqlite import DataBase


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
        self.orientation = 'vertical'

        self.instruments = InstrumentsBox()
        self.add_widget(self.instruments)

        self.note_page = NotePage(size_hint=(None, None), size=(self.width, self.width * 2 ** 0.5))
        self.scroll_page = ScrollView()
        self.scroll_page.size_hint_y = 0.8
        self.scroll_page.add_widget(self.note_page)
        self.add_widget(self.scroll_page)
        self.keyboard = ImagePaste('templates/img.png', self.width, self.height, (self.width, self.height / 5), (0, 0))
        self.add_widget(self.keyboard)

        self.draw_mode = False

        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        self.clear_widgets()

        # ИНСТРУМЕНТЫ
        self.instruments = InstrumentsBox()
        self.instruments.size_hint_y = 0.6
        self.add_widget(self.instruments)
        # Обработчики нажатий
        self.instruments.save_file.bind(on_press=self.save_file)
        self.instruments.delete_note.bind(on_press=self.delete_last_note)
        # self.instruments.choice_of_tonality.bind(on_press=self.changing_screens_on_theory)
        # self.instruments.choice_of_time_signature.bind(on_press=self.changing_screens_on_theory)
        #
        self.instruments.flat.bind(on_press=partial(self.adding_signature, value=-1))
        self.instruments.sharp.bind(on_press=partial(self.adding_signature, value=1))
        self.instruments.natural.bind(on_press=partial(self.adding_signature, value=0))

        self.instruments.whole.bind(on_press=partial(self.changing_duration, duration='1/1'))
        self.instruments.half.bind(on_press=partial(self.changing_duration, duration='1/2'))
        self.instruments.quarter.bind(on_press=partial(self.changing_duration, duration='1/4'))
        self.instruments.eighth.bind(on_press=partial(self.changing_duration, duration='1/8'))
        self.instruments.sixteenth.bind(on_press=partial(self.changing_duration, duration='1/16'))
        self.instruments.thirty_second.bind(on_press=partial(self.changing_duration, duration='1/32'))

        self.instruments.whole_pause.bind(
            on_press=partial(self.changing_pause, duration='1/1', image='templates/whole.png'))
        self.instruments.half_pause.bind(
            on_press=partial(self.changing_pause, duration='1/2', image='templates/half.png'))
        self.instruments.quarter_pause.bind(
            on_press=partial(self.changing_pause, duration='1/4', image='templates/quarter_pause.png'))
        self.instruments.eighth_pause.bind(
            on_press=partial(self.changing_pause, duration='1/8', image='templates/eighth_pause.png'))
        self.instruments.sixteenth_pause.bind(
            on_press=partial(self.changing_pause, duration='1/16', image='templates/sixteenth_pause.png'))
        self.instruments.thirty_second_pause.bind(
            on_press=partial(self.changing_pause, duration='1/32', image='templates/thirty_second_pause.png'))
        # self.instruments.dot.bind(on_press=partial(self.changing_pause, duration='1/1', image='whole.png'))
        # self.instruments.tie.bind(on_press=partial(self.changing_pause, duration='1/1', image='whole.png'))

        self.scroll_page = ScrollView()
        self.note_page = NotePage(size_hint=(None, None), size=(self.width, self.width * 2 ** 0.5))
        self.scroll_page.add_widget(self.note_page)
        self.add_widget(self.scroll_page)
        self.scroll_page.size_hint_y = 5

        self.keyboard = ImagePaste('templates/img.png', self.width, self.height, (self.width, self.height / 5), (0, 0))
        self.keyboard.pos_hint_y = 0.1
        self.add_widget(self.keyboard)

        self.keyboard.size = (self.width, self.height / 5)
        self.note_page.size = (self.width, self.width * 2 ** 0.5)

    # Обработка нажатий или движений

    def on_touch_down(self, touch):
        super(TextbookBox, self).on_touch_down(touch)
        if not self.collide_point(*touch.pos):
            return False
        else:
            if self.note_page.current_clef == 1:
                current_string = self.note_page.current_string_1
            else:
                current_string = self.note_page.current_string_2
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
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 5,
                                       0)
                        print("До")
                    elif touch.pos[0] <= self.width / 7 * 2:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 4.5,
                                       1)
                        print("Ре")
                    elif touch.pos[0] <= self.width / 7 * 3:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 4,
                                       2)
                        print("Ми")
                    elif touch.pos[0] <= self.width / 7 * 4:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 3.5,
                                       3)
                        print("Фа")
                    elif touch.pos[0] <= self.width / 7 * 5:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 3,
                                       4)
                        print("Соль")
                    elif touch.pos[0] <= self.width / 7 * 6:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 2.5,
                                       5)
                        print("Ля")
                    elif touch.pos[0] <= self.width:
                        self.draw_note(self.note_page.height / 10 * 9 - current_string * (
                                self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * 2,
                                       6)
                        print("Си")
            return True

    # Сохранение файла
    def save_file(self, instance):
        file = self.select_save_location()
        if file:
            self.note_page.export_to_png(file)

    # Выбор место сохранения
    def select_save_location(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            title="Выберите место для сохранения файла",
            initialdir="/",  # Начальная директория
            filetypes=(("PNG files", "*.png"), ("All Files", "*.*")),  # Типы файлов
            defaultextension=".png"  # Расширение по умолчанию
        )

        if file_path:
            return file_path

    def on_off_drawing_mode(self, instance):
        self.draw_mode = not self.draw_mode

    def draw_note(self, y, ind):
        if self.note_page.current_clef == 1:
            with self.note_page.canvas:
                Color(0, 0, 0, 1)
                if int(self.note_page.current_duration.split('/')[1]) < 4:
                    Line(ellipse=(
                        int(self.note_page.current_pos_1) - self.note_page.k_size_note,
                        y - self.note_page.k_size_note // 2,
                        self.note_page.k_size_note * 2, self.note_page.k_size_note))
                else:
                    Ellipse(pos=(
                        int(self.note_page.current_pos_1) - self.note_page.k_size_note,
                        y - self.note_page.k_size_note // 2),
                        size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                if int(self.note_page.current_duration.split('/')[1]) > 1:
                    Line(points=(
                        int(self.note_page.current_pos_1) + self.note_page.k_size_note,
                        y + self.note_page.k_size_note // 2,
                        int(self.note_page.current_pos_1) + self.note_page.k_size_note,
                        y + self.note_page.k_size_note * 4),
                        width=1.5)
                    if ind % 2 == 0 and (ind > 12 or ind < 2):
                        Line(points=(
                            int(self.note_page.current_pos_1) - self.note_page.k_size_note * 2, y,
                            int(self.note_page.current_pos_1) + self.note_page.k_size_note * 2, y), width=1.5)
                self.note_page.list_of_notes_treble.append(
                    (16 - ind, self.note_page.current_pos_1, self.note_page.current_string_1,
                     self.note_page.current_duration, 0, float(self.width)))
                self.note_page.database.update('notepage_treble_1',
                                               (16 - ind, self.note_page.current_pos_1, self.note_page.current_string_1,
                                                self.note_page.current_duration, 0, float(self.note_page.width)))
                self.note_page.current_pos_1 += self.note_page.each_note * (
                        int(self.note_page.time_signature.split('/')[1]) /
                        int(self.note_page.current_duration.split('/')[
                                1]))
        else:
            with self.note_page.canvas:
                Color(0, 0, 0, 1)
                if int(self.note_page.current_duration.split('/')[1]) < 4:
                    Line(ellipse=(
                        int(self.note_page.current_pos_2) - self.note_page.k_size_note,
                        y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2,
                        self.note_page.k_size_note * 2, self.note_page.k_size_note))
                else:
                    Ellipse(pos=(int(self.note_page.current_pos_2) - self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2),
                            size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                if int(self.note_page.current_duration.split('/')[1]) > 1:
                    Line(points=(int(self.note_page.current_pos_2) + self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note // 2,
                                 int(self.note_page.current_pos_2) + self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note * 4),
                         width=1.5)
                    if ind % 2 == 1 and (ind > 6 or ind < -3):
                        Line(points=(
                            int(self.note_page.current_pos_2) - self.note_page.k_size_note * 2,
                            y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12,
                            int(self.note_page.current_pos_2) + self.note_page.k_size_note * 2,
                            y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12), width=1.5)

                self.note_page.list_of_notes_bass.append(
                    (11 - ind, self.note_page.current_pos_2, self.note_page.current_string_2,
                     self.note_page.current_duration, 0, float(self.width)))
                self.note_page.database.update('notepage_bass_1',
                                               (11 - ind, self.note_page.current_pos_2, self.note_page.current_string_2,
                                                self.note_page.current_duration, 0, float(self.note_page.width)))

                self.note_page.current_pos_2 += self.note_page.each_note * (
                        int(self.note_page.time_signature.split('/')[1]) /
                        int(self.note_page.current_duration.split('/')[
                                1]))
        self.note_page.make_beat()

    # Обработчики нажатий инструментов

    def changing_duration(self, instance, duration):
        self.note_page.current_duration = duration

    def changing_pause(self, instance, duration, image):
        self.note_page.changing_pause(duration, image, self.note_page.current_clef)
        if self.note_page.current_clef == 1:
            self.note_page.list_of_notes_bass.append(
                (8, self.note_page.current_pos_1, self.note_page.current_string_1, duration, 0, float(self.width)))

            self.note_page.database.update('notepage_treble_1',
                                           (
                                               0, self.note_page.current_pos_1, self.note_page.current_string_1,
                                               self.note_page.current_duration, 3,
                                               float(self.width)))

            self.note_page.current_pos_1 += self.note_page.each_note * (
                    int(self.note_page.time_signature.split('/')[1]) /
                    int(duration.split('/')[1]))


        else:
            self.note_page.list_of_notes_bass.append(
                (8, self.note_page.current_pos_2, self.note_page.current_string_2, duration, 0, float(self.width)))

            self.note_page.database.update('notepage_treble_1',
                                           (
                                               0, self.note_page.current_pos_1, self.note_page.current_string_1,
                                               self.note_page.current_duration, 3,
                                               float(self.width)))

            self.note_page.current_pos_2 += self.note_page.each_note * (
                    int(self.note_page.time_signature.split('/')[1]) /
                    int(duration.split('/')[1]))

    def delete_last_note(self, instance):
        name = 'notepage_' + 'treble' * (self.note_page.current_clef == 1) + 'bass' * (
                self.note_page.current_clef == 2) + '_1'
        try:
            if self.note_page.current_clef == 1:
                ind = self.note_page.list_of_notes_treble[-1][0]
                pos = self.note_page.list_of_notes_treble[-1][1]
                number_string = self.note_page.list_of_notes_treble[-1][2]
            else:
                ind = self.note_page.list_of_notes_bass[-1][0]
                pos = self.note_page.list_of_notes_bass[-1][1]
                number_string = self.note_page.list_of_notes_bass[-1][2]
            self.note_page.database.delete(name, ind, pos, number_string)
            if self.note_page.current_clef == 1:
                self.note_page.list_of_notes_treble.pop(-1)
                print([i for i in self.note_page.list_of_notes_treble])
                self.note_page.current_pos_1 = self.width / 9 + sum([
                    self.note_page.each_note * (
                            int(self.note_page.time_signature.split('/')[1]) /
                            int(i[3].split('/')[1])) for i in self.note_page.list_of_notes_treble])
            else:
                self.note_page.list_of_notes_bass.pop(-1)
                self.note_page.current_pos_2 = self.width / 9 + sum([
                    self.note_page.each_note * (
                            int(self.note_page.time_signature.split('/')[1]) /
                            int(i[3].split('/')[1])) for i in self.note_page.list_of_notes_bass])
            self.note_page.update_size(instance, 1)
        except Exception as e:
            print(e)
            return None

    def adding_signature(self, instance, value):
        pos_x, pos_y = -1000, -1000
        if self.note_page.current_clef == 1 and len(self.note_page.list_of_notes_treble) > 0:
            pos_x = self.note_page.list_of_notes_treble[-1][1]
            pos_y = self.note_page.height / 10 * 9 - self.note_page.current_string_1 * (
                    self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * \
                    self.note_page.list_of_notes_treble[-1][0]
        elif self.note_page.current_clef == 2 and len(self.note_page.list_of_notes_bass) > 0:
            pos_x = self.note_page.list_of_notes_bass[-1][1]
            pos_y = self.note_page.height / 10 * 9 - self.note_page.current_string_2 * (
                    self.note_page.height / 6 + self.note_page.height // 100 * 8) - self.note_page.height // 100 * \
                    self.note_page.list_of_notes_bass[-1][
                        0] + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2
        size_x = self.note_page.k_size_note * 3
        size_y = self.note_page.k_size_note * 6
        if value == -1:
            with self.note_page.canvas:
                sign = Image(source='templates/flat.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y + size_y)
                sign.size = (size_x, size_y)
        elif value == 1:
            with self.note_page.canvas:
                sign = Image(source='templates/sharp.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y + size_y)
                sign.size = (size_x, size_y)
        if self.note_page.current_clef == 1 and len(self.note_page.list_of_notes_treble) > 0:
            x = self.note_page.list_of_notes_treble[-1]
            self.note_page.list_of_notes_treble[-1] = ([(x[i] if i != 4 else value) for i in range(len(x))])
            self.note_page.database.delete('notepage_treble_1', self.note_page.list_of_notes_treble[-1][0],
                                           self.note_page.list_of_notes_treble[-1][1],
                                           self.note_page.list_of_notes_treble[-1][2])
            self.note_page.database.update('notepage_treble_1', self.note_page.list_of_notes_treble[-1])
        elif self.note_page.current_clef == 2 and len(self.note_page.list_of_notes_bass) > 0:
            x = self.note_page.list_of_notes_bass[-1]
            self.note_page.list_of_notes_bass[-1] = ([(x[i] if i != 4 else value) for i in range(len(x))])
            self.note_page.database.delete('notepage_bass_1', self.note_page.list_of_notes_bass[-1][0],
                                           self.note_page.list_of_notes_bass[-1][1],
                                           self.note_page.list_of_notes_bass[-1][2])
            self.note_page.database.update('notepage_bass_1', self.note_page.list_of_notes_treble[-1])


class NotePage(Widget):
    def __init__(self, **kwargs):
        super(NotePage, self).__init__(**kwargs)

        # Подключение к бд
        self.database = DataBase()

        self.list_of_notes_treble = self.connecting_db('notepage_treble_1')  # Все ноты скрипичного ключа
        self.list_of_notes_bass = self.connecting_db('notepage_bass_1')  # Все ноты басового ключа
        self.time_signature = '4/4'  # Размер произведения
        self.current_string_1 = 0  # Текущая строка в Скр. ключе
        self.current_string_2 = 0  # Текущая строка в Бас. ключе
        self.current_duration = '1/4'  # По умолчанию длительность
        self.each_note = self.width * 8 / 9 / 4 / int(self.time_signature.split('/')[0])  # На каждую мин долю
        self.current_pos_1 = self.width / 9  # Текущая позиция Скр. ключ
        self.current_pos_2 = self.width / 9  # Текущая позиция Бас.ключ
        self.y_pos = [self.height // 200 * i for i in range(-6, 19)]  # Позиция по вертикали (все возможные)
        self.current_clef = 1  # Текущий знак (для работы с клавиатурой)
        self.k_size_note = self.height // 150  # Коэфф размера ноты

        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        self.clear_widgets()
        with self.canvas:
            Color(rgba=(1, 1, 1, 1))
            self.rect = Rectangle(size=self.size, pos=self.pos)

            self.filling_canvas()

            interval = self.height / 10
            for string in range(10):
                for i in range(5):
                    Color(0, 0, 0, 1)  # RGBA
                    Line(points=(0, self.height - interval - i * self.height / 100, self.width,
                                 self.height - interval - i * self.height / 100), width=1.5)
                if string % 2 == 0:
                    clef = Image(source='templates/treble_clef.png', allow_stretch=True, keep_ratio=False)
                    clef.height = self.height // 20
                    clef.width = self.width / 9
                else:
                    clef = Image(source='templates/bass_clef.png', allow_stretch=False, keep_ratio=True)
                    clef.height = self.height // 20
                    clef.width = self.width / 9
                clef.pos = (0, self.height - interval - 4 * self.height // 100)
                self.add_widget(clef)
                # self.time_signature_img = Image(source='bass_clef.png', allow_stretch=False, keep_ratio=True)
                interval += self.height / 12

    def on_touch_down(self, touch):
        with self.canvas:
            if touch.button == 'left':
                if self.current_clef == 1:
                    current_string = self.current_string_1
                else:
                    current_string = self.current_string_2
                interval = self.height / 10 * 9 - current_string * (self.height / 6 + self.height // 100 * 8)
                Color(rgba=(0, 0, 0, 1))
                if ((self.height / 10 * 9 - self.current_string_1 * (
                        self.height / 12 + self.height // 100 * 8)) + self.height // 48 >= touch.pos[1] >= (
                        (self.height / 10 * 9 - self.current_string_1 * (
                                self.height / 12 + self.height // 100 * 8)) - (
                                self.height / 48 + self.height // 100 * 4))):
                    interval = self.height / 10 * 9 - self.current_string_1 * (
                            self.height / 12 + self.height // 100 * 8)
                    index = [abs(touch.pos[1] - interval + j) for j in self.y_pos].index(
                        min([abs(touch.pos[1] - interval + i) for i in self.y_pos]))
                    y = [interval - j for j in self.y_pos][index]

                    if int(self.current_duration.split('/')[1]) < 4:
                        Line(ellipse=(int(self.current_pos_1) - self.k_size_note, y - self.k_size_note // 2,
                                      self.k_size_note * 2, self.k_size_note))
                    else:
                        Ellipse(pos=(int(self.current_pos_1) - self.k_size_note, y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                    if int(self.current_duration.split('/')[1]) > 1:
                        Line(points=(
                            int(self.current_pos_1) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note // 2 - (index < 11) * self.k_size_note,
                            int(self.current_pos_1) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note * 4 - 8 * (index < 11) * self.k_size_note), width=1.5)
                        self.changing_duration(index, y)
                    # Дополнительные линии
                    if index % 2 == 0 and (index < 6 or index > 14):
                        Line(points=(
                            int(self.current_pos_1) - self.k_size_note * 2, y,
                            int(self.current_pos_1) + self.k_size_note * 2, y), width=1.5)
                        if index < 4:
                            Line(points=(
                                int(self.current_pos_1) - self.k_size_note * 2, interval - self.y_pos[index - 2],
                                int(self.current_pos_1) + self.k_size_note * 2, interval - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 0:
                                Line(points=(
                                    int(self.current_pos_1) - self.k_size_note * 2,
                                    interval - self.y_pos[index - 3],
                                    int(self.current_pos_1) + self.k_size_note * 2,
                                    interval - self.y_pos[index - 3]), width=1.5)
                        if index > 14:
                            Line(points=(
                                int(self.current_pos_1) - self.k_size_note * 2, interval - self.y_pos[index - 2],
                                int(self.current_pos_1) + self.k_size_note * 2, interval - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 18:
                                Line(points=(
                                    int(self.current_pos_1) - self.k_size_note * 2,
                                    interval - self.y_pos[index - 3],
                                    int(self.current_pos_1) + self.k_size_note * 2,
                                    interval - self.y_pos[index - 3]), width=1.5)

                    elif index == 17:
                        Line(points=(
                            int(self.current_pos_1) - self.k_size_note * 2, interval - self.y_pos[index - 1],
                            int(self.current_pos_1) + self.k_size_note * 2, interval - self.y_pos[index - 1]),
                            width=1.5)
                    elif index == 1 or index == 3:
                        Line(points=(
                            int(self.current_pos_1) - self.k_size_note * 2, interval - self.y_pos[index + 1],
                            int(self.current_pos_1) + self.k_size_note * 2, interval - self.y_pos[index + 1]),
                            width=1.5)
                        if index == 1:
                            Line(points=(
                                int(self.current_pos_1) - self.k_size_note * 2, interval - self.y_pos[index + 3],
                                int(self.current_pos_1) + self.k_size_note * 2, interval - self.y_pos[index + 3]),
                                width=1.5)

                    self.list_of_notes_treble.append(
                        (index, self.current_pos_1, self.current_string_1, self.current_duration, 0, float(self.width)))
                    self.database.update('notepage_treble_1',
                                         (
                                             index, self.current_pos_1, self.current_string_1,
                                             self.current_duration, 0,
                                             float(self.width)))
                    self.current_pos_1 += self.each_note * (int(self.time_signature.split('/')[1]) /
                                                            int(self.current_duration.split('/')[1]))
                    self.current_clef = 1
                elif (
                        ((self.height / 10 * 9 - self.current_string_2 * (
                                self.height / 12 + self.height // 100 * 8)) - (
                                 self.height / 48 + self.height // 100 * 4))) >= touch.pos[1] >= (
                        self.height / 10 * 9 - self.current_string_2 * (self.height / 12 + self.height // 100 * 8)) - (
                        self.height / 24 + self.height // 100 * 11):
                    interval = (self.height / 10 * 9 - self.current_string_2 * (
                            self.height / 12 + self.height // 100 * 8))
                    index = [abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + j) for j in
                             self.y_pos].index(
                        min([abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + i) for i in
                             self.y_pos]))
                    y = [interval - (self.height / 24 + self.height // 100 * 4) - j for j in self.y_pos][index]

                    if int(self.current_duration.split('/')[1]) < 4:
                        Line(ellipse=(int(self.current_pos_2) - self.k_size_note, y - self.k_size_note // 2,
                                      self.k_size_note * 2, self.k_size_note))
                    else:
                        Ellipse(pos=(int(self.current_pos_2) - self.k_size_note, y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                    if int(self.current_duration.split('/')[1]) > 1:
                        Line(points=(
                            int(self.current_pos_2) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note // 2 - (index < 11) * self.k_size_note,
                            int(self.current_pos_2) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note * 4 - 8 * (index < 11) * self.k_size_note), width=1.5)
                    if index % 2 == 0 and (index < 6 or index > 16):
                        Line(points=(
                            int(self.current_pos_2) - self.k_size_note * 2, y,
                            int(self.current_pos_2) + self.k_size_note * 2, y), width=1.5)

                        if index < 4:
                            Line(points=(
                                int(self.current_pos_2) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2],
                                int(self.current_pos_2) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 0:
                                Line(points=(
                                    int(self.current_pos_2) - self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3],
                                    int(self.current_pos_2) + self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3]), width=1.5)
                        if index > 14:
                            Line(points=(
                                int(self.current_pos_2) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2],
                                int(self.current_pos_2) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 18:
                                Line(points=(
                                    int(self.current_pos_2) - self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3],
                                    int(self.current_pos_2) + self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3]), width=1.5)

                    elif index == 17:
                        Line(points=(
                            int(self.current_pos_2) - self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1],
                            int(self.current_pos_2) + self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1]),
                            width=1.5)
                    elif index == 1 or index == 3:
                        Line(points=(
                            int(self.current_pos_2) - self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1],
                            int(self.current_pos_2) + self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1]),
                            width=1.5)
                        if index == 1:
                            Line(points=(
                                int(self.current_pos_2) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 3],
                                int(self.current_pos_2) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 3]),
                                width=1.5)

                    self.list_of_notes_bass.append(
                        (index, self.current_pos_2, self.current_string_2, self.current_duration, 0, self.width))
                    self.database.update('notepage_bass_1', (
                        index, self.current_pos_2, self.current_string_2, self.current_duration, 0,
                        float(self.width)))

                    self.current_pos_2 += self.each_note * (int(self.time_signature.split('/')[1]) /
                                                            int(self.current_duration.split('/')[1]))
                    self.current_clef = 2
            self.make_beat()

    # Такты
    def make_beat(self):
        count_strings = int(
            max(sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_treble]),
                sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in
                     self.list_of_notes_bass])) / int(
                self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) // 4
        for num_string in range(count_strings + 1):
            if num_string == count_strings:
                count_beats = int(
                    max(sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_treble]),
                        sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in
                             self.list_of_notes_bass])) / int(
                        self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) % 4
            else:
                count_beats = 4
            for i in range(count_beats):
                with self.canvas:
                    Color(0, 0, 0, 1)
                    Line(points=(self.width / 9 * 8 / 4 * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (self.height / 12 + self.height / 100 * 8),
                                 self.width / 9 * 8 / 4 * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 12 + self.height / 100 * 8) - self.height / 100 * 4), width=1.5)
                    Line(points=(self.width / 9 * 8 / 4 * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 12 + self.height / 100 * 8) - (
                                         self.height / 24 + self.height / 100 * 4),
                                 self.width / 9 * 8 / 4 * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 12 + self.height / 100 * 8) - (
                                         self.height / 24 + self.height / 100 * 8)), width=1.5)
        if self.current_string_1 < int(
                sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_treble]) / int(
                    self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) // 4:
            self.current_pos_1 = self.width / 9
        if self.current_string_2 < int(
                sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_bass]) / int(
                    self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) // 4:
            self.current_pos_2 = self.width / 9
        self.current_string_1 = int(
            sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_treble]) / int(
                self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) // 4
        self.current_string_2 = int(
            sum([int(x[3].split('/')[0]) / int(x[3].split('/')[1]) for x in self.list_of_notes_bass]) / int(
                self.time_signature.split('/')[0]) * int(self.time_signature.split('/')[1])) // 4

    def changing_pause(self, duration, image, clef):
        if clef == 1:
            current_string = self.current_string_1
        else:
            current_string = self.current_string_2
        y = self.height / 10 * 9 - current_string * (
                self.height // 12 + self.height // 100 * 8) - self.height // 100 * 5.5
        if clef == 1:
            with self.canvas:
                pause = Image(source=image, allow_stretch=False, keep_ratio=True)
                pause.pos = (self.current_pos_1 - self.each_note / 2, y)
                self.add_widget(pause)


        else:
            with self.canvas:
                pause = Image(source=image, allow_stretch=False, keep_ratio=True)
                pause.pos = (
                    self.current_pos_2 - self.each_note / 2, y - self.height / 12)
                self.add_widget(pause)

        self.make_beat()

    def changing_duration(self, index, y):
        with self.canvas:
            if int(self.current_duration.split('/')[1]) > 4:
                if index > 10:
                    start_x, start_y = int(self.current_pos_1) + self.k_size_note - 2 * (
                            index < 11) * self.k_size_note, y + self.k_size_note * 4 - 8 * (
                                               index < 11) * self.k_size_note
                    size_x, size_y = self.k_size_note * 2, self.k_size_note * 4
                    Line(ellipse=(start_x, start_y - size_y / 2, size_x, size_y, 180, 270), width=1.5)
                else:
                    start_x, start_y = int(self.current_pos_1) + self.k_size_note - 2 * (
                            index < 11) * self.k_size_note, y + self.k_size_note * 4 - 8 * (
                                               index < 11) * self.k_size_note
                    size_x, size_y = self.k_size_note * 4, self.k_size_note * 4
                    Line(ellipse=(start_x - size_x / 2, start_y, size_x, size_y, 90, 180), width=1.5)

    def connecting_db(self, name_db):
        self.database.create(name_db)
        return list(self.database.select(name_db))

    def filling_canvas(self):
        for i in self.list_of_notes_treble:
            if i[4] == 3:
                if i[3] == '1/1':
                    self.changing_pause(i[3], 'templates/whole.png', 1)
                elif i[3] == '1/2':
                    self.changing_pause(i[3], 'templates/half.png', 1)
                elif i[3] == '1/4':
                    self.changing_pause(i[3], 'templates/quarter_pause.png', 1)
                elif i[3] == '1/8':
                    self.changing_pause(i[3], 'templates/eighth_pause.png', 1)
                elif i[3] == '1/16':
                    self.changing_pause(i[3], 'templates/sixteenth_pause.png', 1)
                elif i[3] == '1/32':
                    self.changing_pause(i[3], 'templates/thirty_second_pause.png', 1)
                self.current_pos_1 += self.each_note * (
                        int(self.time_signature.split('/')[1]) /
                        int(i[3].split('/')[1]))
                continue
            self.draw_note_filling_canvas(self.height / 10 * 9 - i[2] * (
                    self.height / 12 + self.height // 100 * 8), i[0], i[1] / i[5] * self.width, i[3], 1)
        for i in self.list_of_notes_bass:
            if i[4] == 3:
                if i[3] == '1/1':
                    self.changing_pause(i[3], 'templates/whole.png', 2)
                elif i[3] == '1/2':
                    self.changing_pause(i[3], 'templates/half.png', 2)
                elif i[3] == '1/4':
                    self.changing_pause(i[3], 'templates/quarter_pause.png', 2)
                elif i[3] == '1/8':
                    self.changing_pause(i[3], 'templates/eighth_pause.png', 2)
                elif i[3] == '1/16':
                    self.changing_pause(i[3], 'templates/sixteenth_pause.png', 2)
                elif i[3] == '1/32':
                    self.changing_pause(i[3], 'templates/thirty_second_pause.png', 2)
                self.current_pos_2 += self.each_note * (
                        int(self.time_signature.split('/')[1]) /
                        int(i[3].split('/')[1]))
                continue
            self.draw_note_filling_canvas(self.height / 10 * 9 - i[2] * (
                    self.height / 12 + self.height // 100 * 8), i[0], i[1], i[3], 2)

    def draw_note_filling_canvas(self, y, ind, pos, duration, clef):
        y -= (ind - 6) * self.height // 200
        if clef == 1:
            with self.canvas:
                Color(0, 0, 0, 1)
                if int(duration.split('/')[1]) < 4:
                    Line(ellipse=(int(pos) - self.k_size_note, y - self.k_size_note // 2,
                                  self.k_size_note * 2, self.k_size_note))
                else:
                    Ellipse(pos=(
                        int(pos) - self.k_size_note,
                        y - self.k_size_note // 2),
                        size=(self.k_size_note * 2, self.k_size_note))
                if int(duration.split('/')[1]) > 1:
                    Line(points=(int(pos) - (ind < 11) * self.k_size_note + (ind >= 11) * self.k_size_note,
                                 y + self.k_size_note // 2 - (ind < 11) * self.k_size_note,
                                 int(pos) - (ind < 11) * self.k_size_note + (ind >= 11) * self.k_size_note,
                                 y + self.k_size_note * 4 - 8 * (ind < 11) * self.k_size_note),
                         width=1.5)
                if ind % 2 == 0 and (ind < 6 or ind > 14):
                    Line(points=(
                        int(pos) - self.k_size_note * 2, y,
                        int(pos) + self.k_size_note * 2, y), width=1.5)

                self.current_pos_1 += self.each_note * (
                        int(self.time_signature.split('/')[1]) /
                        int(duration.split('/')[
                                1]))
        else:
            with self.canvas:
                Color(0, 0, 0, 1)
                if int(duration.split('/')[1]) < 4:
                    Line(ellipse=(int(pos) - self.k_size_note,
                                  y - self.height / 12 - self.k_size_note // 2,
                                  self.k_size_note * 2, self.k_size_note))
                else:
                    Ellipse(pos=(int(pos) - self.k_size_note,
                                 y - self.height / 12 - self.k_size_note // 2),
                            size=(self.k_size_note * 2, self.k_size_note))
                if int(duration.split('/')[1]) > 1:
                    Line(points=(int(pos) - (ind < 11) * self.k_size_note + (ind >= 11) * self.k_size_note,
                                 y - self.height / 12 + self.k_size_note // 2 - (ind < 11) * self.k_size_note,
                                 int(pos) - (ind < 11) * self.k_size_note + (ind >= 11) * self.k_size_note,
                                 y - self.height / 12 + self.k_size_note * 4 - 8 * (ind < 11) * self.k_size_note),
                         width=1.5)
                if ind % 2 == 0 and (ind < 6 or ind > 14):
                    Line(points=(
                        int(pos) - self.k_size_note * 2,
                        y - self.height / 12,
                        pos + self.k_size_note * 2,
                        y - self.height / 12), width=1.5)

                self.current_pos_2 += self.each_note * (
                        int(self.time_signature.split('/')[1]) /
                        int(duration.split('/')[
                                1]))
        self.make_beat()


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


class InstrumentsBox(StackLayout):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.hint_y = 1

        self.save_file = Button(width=50, size_hint=(None, self.hint_y),
                                background_normal='templates/save_file.png')  # text="Сохранить файл",
        self.new_file = Button(width=50, size_hint=(None, self.hint_y),
                               background_normal="templates/add_file.png")  # text="Новый файл",
        self.delete_note = Button(width=self.width, size_hint=(None, self.hint_y),
                                  background_normal='templates/delete_note.png')  # text="Режим рисования",

        self.choice_of_tonality = Button(width=50, size_hint=(None, self.hint_y))  # text="Выбор тональности",
        self.choice_of_time_signature = Button(width=50, size_hint=(None, self.hint_y))  # text="Выбор размера",

        self.flat = Button(width=self.width, size_hint=(None, self.hint_y),
                           background_normal='templates/flat.png')  # text="Бемоль",
        self.sharp = Button(width=self.width, size_hint=(None, self.hint_y),
                            background_normal='templates/sharp.png')  # text="Диез",
        self.natural = Button(width=self.width, size_hint=(None, self.hint_y),
                              background_normal='templates/natural.png')  # text="Бекар",

        self.whole = Button(width=self.width, size_hint=(None, self.hint_y),
                            background_normal='templates/whole.png')  # text="Целая",
        self.half = Button(width=self.width, size_hint=(None, self.hint_y),
                           background_normal='templates/half.png')  # text="Половинка",
        self.quarter = Button(width=self.width, size_hint=(None, self.hint_y),
                              background_normal='templates/quarter.png')  # text="Четверь",
        self.eighth = Button(width=self.width, size_hint=(None, self.hint_y),
                             background_normal='templates/eighth.png')  # text="Восьмая",
        self.sixteenth = Button(width=self.width, size_hint=(None, self.hint_y),
                                background_normal='templates/sixteenth.png')  # text="Шестнадцая",
        self.thirty_second = Button(width=self.width, size_hint=(None, self.hint_y),
                                    background_normal='templates/thirty_second.png')  # text="Тридцать вторая",

        self.whole_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                  background_normal='templates/whole.png')  # text="Целая пауза",
        self.half_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                 background_normal='templates/half.png')  # text="Половинка пауза",
        self.quarter_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                    background_normal='templates/quarter_pause.png')  # text="Четверь пауза",
        self.eighth_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                   background_normal='templates/eighth_pause.png')  # text="Восьмая пауза",
        self.sixteenth_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                      background_normal='templates/sixteenth_pause.png')  # text="Шестнадцая пауза",
        self.thirty_second_pause = Button(width=self.width, size_hint=(None, self.hint_y),
                                          background_normal='templates/thirty_second_pause.png')  # text="Тридцать вторая пауза",

        self.list_instruments = [self.save_file, self.new_file, self.delete_note,
                                 self.flat, self.sharp, self.natural, self.whole, self.half, self.quarter, self.eighth,
                                 self.sixteenth, self.thirty_second,
                                 self.whole_pause, self.half_pause, self.quarter_pause, self.eighth_pause,
                                 self.sixteenth_pause, self.thirty_second_pause]

        for i in self.list_instruments:
            self.add_widget(i)


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
