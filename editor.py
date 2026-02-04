import smtplib
from email.message import EmailMessage
from functools import partial
from tkinter import filedialog

import tkinter as tk
from tkinter import filedialog

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from const import Const
from sqlite import DataBase


class EditorScreen(Screen):
    def __init__(self):
        super().__init__()
        self.editor_box = EditorBox()
        self.add_widget(self.editor_box)

        # Обновление размеров элементов при изменении размера виджета
        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        pass


class EditorBox(BoxLayout):
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

        Window.bind(on_key_down=self.on_keydown)

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
        self.instruments.choice_of_tonality.bind(text=self.select_tonality)
        self.instruments.choice_of_time_signature.bind(text=self.select_time_signature)

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
            on_press=partial(self.changing_pause, duration='1/1', image='templates/whole_pause.png'))
        self.instruments.half_pause.bind(
            on_press=partial(self.changing_pause, duration='1/2', image='templates/half_pause.png'))
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
        super(EditorBox, self).on_touch_down(touch)
        if not self.collide_point(*touch.pos):
            return False
        else:
            if self.note_page.current_clef == 1:
                x_pos = self.note_page.x_pos_1
            else:
                x_pos = self.note_page.x_pos_2
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
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 5,
                                       0)
                        print("До")
                    elif touch.pos[0] <= self.width / 7 * 2:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 4.5,
                                       1)
                        print("Ре")
                    elif touch.pos[0] <= self.width / 7 * 3:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 4,
                                       2)
                        print("Ми")
                    elif touch.pos[0] <= self.width / 7 * 4:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 3.5,
                                       3)
                        print("Фа")
                    elif touch.pos[0] <= self.width / 7 * 5:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 3,
                                       4)
                        print("Соль")
                    elif touch.pos[0] <= self.width / 7 * 6:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 2.5,
                                       5)
                        print("Ля")
                    elif touch.pos[0] <= self.width:
                        self.draw_note(self.note_page.height / 10 * 9 - (x_pos // (
                                int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                                               self.note_page.height / 6) - self.note_page.height // 100 * 2,
                                       6)
                        print("Си")
            return True

    # Сохранение файла
    def save_file(self, instance):
        file = self.select_save_location()
        if file:
            self.note_page.export_to_png(file)
            self.sending_by_mail(file)

    # Отправка файла
    def sending_by_mail(self, file_name):
        recipient = self.note_page.database.select_email()
        if recipient != '':
            topic = self.note_page.database.select_title()
            sender = 'notebasic@yandex.ru'
            sender_password = 'kvqgsnmafyrjuvus'
            mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
            mail_lib.login(sender, sender_password)
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = topic
            with open(file_name, "rb") as file:
                img_data = file.read()
            msg.add_attachment(img_data, maintype='image', subtype='png')
            mail_lib.send_message(msg)
            mail_lib.quit()
            self.show_notification("Файл успешно отправлен")
        else:
            self.show_notification("Укажите адрес почтового ящика в разделе Профиль")

    # Показ уведомлений
    def show_notification(self, text):
        popup = Popup(title='Уведомление', content=Label(text=text), size_hint=(None, None), size=(400, 400))
        popup.open()

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
                        int(self.note_page.current_pos_1()) - self.note_page.k_size_note,
                        y - self.note_page.k_size_note // 2,
                        self.note_page.k_size_note * 2, self.note_page.k_size_note), width=1.5)
                else:
                    Ellipse(pos=(
                        int(self.note_page.current_pos_1()) - self.note_page.k_size_note,
                        y - self.note_page.k_size_note // 2),
                        size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                if int(self.note_page.current_duration.split('/')[1]) > 1:
                    Line(points=(
                        int(self.note_page.current_pos_1()) + self.note_page.k_size_note,
                        y + self.note_page.k_size_note // 2,
                        int(self.note_page.current_pos_1()) + self.note_page.k_size_note,
                        y + self.note_page.k_size_note * 4),
                        width=1.5)
                    if ind % 2 == 0 and (ind > 12 or ind < 2):
                        Line(points=(
                            int(self.note_page.current_pos_1()) - self.note_page.k_size_note * 2, y,
                            int(self.note_page.current_pos_1()) + self.note_page.k_size_note * 2, y), width=1.5)

                self.note_page.list_of_notes_treble_coords.append((self.note_page.current_pos_1(), y))
                self.note_page.list_of_notes_treble.append(
                    (16 - ind, self.note_page.x_pos_1,
                     self.note_page.current_duration, 0,))
                self.note_page.database.update(f'notepage_treble_{self.note_page.id_database}',
                                               (16 - ind, self.note_page.x_pos_1,
                                                self.note_page.current_duration, 0))
                self.note_page.x_pos_1 += int(self.note_page.time_signature.split('/')[1]) / int(
                    self.note_page.current_duration.split('/')[1])
        else:
            with self.note_page.canvas:
                Color(0, 0, 0, 1)
                if int(self.note_page.current_duration.split('/')[1]) < 4:
                    Line(ellipse=(
                        int(self.note_page.current_pos_2()) - self.note_page.k_size_note,
                        y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2,
                        self.note_page.k_size_note * 2, self.note_page.k_size_note), width=1.5)
                else:
                    Ellipse(pos=(int(self.note_page.current_pos_2()) - self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 - self.note_page.k_size_note // 2),
                            size=(self.note_page.k_size_note * 2, self.note_page.k_size_note))
                if int(self.note_page.current_duration.split('/')[1]) > 1:
                    Line(points=(int(self.note_page.current_pos_2()) + self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note // 2,
                                 int(self.note_page.current_pos_2()) + self.note_page.k_size_note,
                                 y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12 + self.note_page.k_size_note * 4),
                         width=1.5)
                    if ind % 2 == 1 and (ind > 6 or ind < -3):
                        Line(points=(
                            int(self.note_page.current_pos_2()) - self.note_page.k_size_note * 2,
                            y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12,
                            int(self.note_page.current_pos_2()) + self.note_page.k_size_note * 2,
                            y + self.note_page.height // 100 * 2.5 - self.note_page.height / 12), width=1.5)

                self.note_page.list_of_notes_bass_coords.append((self.note_page.current_pos_2(), y))
                self.note_page.list_of_notes_bass.append(
                    (11 - ind, self.note_page.x_pos_2,
                     self.note_page.current_duration, 0))
                self.note_page.database.update(f'notepage_bass_{self.note_page.id_database}',
                                               (11 - ind, self.note_page.x_pos_2,
                                                self.note_page.current_duration, 0))

                self.note_page.x_pos_2 += int(self.note_page.time_signature.split('/')[1]) / int(
                    self.note_page.current_duration.split('/')[1])
        self.note_page.make_beat()

    # Обработчики нажатий инструментов

    def changing_duration(self, instance, duration):
        self.note_page.current_duration = duration

    def changing_pause(self, instance, duration, image):
        self.note_page.changing_pause(duration, image, self.note_page.current_clef)
        if self.note_page.current_clef == 1:
            self.note_page.list_of_notes_bass.append(
                (8, self.note_page.x_pos_2, duration, 0))

            self.note_page.database.update(f'notepage_treble_{self.note_page.id_database}',
                                           (
                                               0, self.note_page.x_pos_2,
                                               self.note_page.current_duration, 3,
                                           ))

            self.note_page.x_pos_1 += int(self.note_page.time_signature.split('/')[1]) / int(
                self.note_page.current_duration.split('/')[1])


        else:
            self.note_page.list_of_notes_bass.append(
                (8, self.note_page.x_pos_2, duration, 0))

            self.note_page.database.update(f'notepage_bass_{self.note_page.id_database}',
                                           (
                                               0, self.note_page.x_pos_2,
                                               self.note_page.current_duration, 3,
                                           ))

            self.note_page.x_pos_2 += int(self.note_page.time_signature.split('/')[1]) / int(
                self.note_page.current_duration.split('/')[1])

    def delete_last_note(self, instance):
        name = 'notepage_' + 'treble' * (self.note_page.current_clef == 1) + 'bass' * (
                self.note_page.current_clef == 2) + '_' + str(self.note_page.id_database)
        if self.note_page.current_clef == 1:
            if len(self.note_page.list_of_notes_treble) > 0:
                ind = self.note_page.list_of_notes_treble[-1][0]
                pos = self.note_page.list_of_notes_treble[-1][1]
                self.note_page.database.delete(name, ind, pos)
                self.note_page.x_pos_1 -= int(self.note_page.time_signature.split('/')[1]) / int(
                    self.note_page.list_of_notes_treble[-1][2].split('/')[1])
                self.note_page.list_of_notes_treble.pop(-1)
        else:
            if len(self.note_page.list_of_notes_bass) > 0:
                ind = self.note_page.list_of_notes_bass[-1][0]
                pos = self.note_page.list_of_notes_bass[-1][1]
                self.note_page.database.delete(name, ind, pos)
                self.note_page.x_pos_2 -= int(self.note_page.time_signature.split('/')[1]) / int(
                    self.note_page.list_of_notes_bass[-1][2].split('/')[1])
                self.note_page.list_of_notes_bass.pop(-1)
        self.note_page.update_size(instance, 1)

    def adding_signature(self, instance, value):
        if self.note_page.current_clef == 1:
            pos_x = self.note_page.current_pos_1()
            pos_y = self.note_page.height / 10 * 9 - (
                    (self.note_page.x_pos_1 - int(self.note_page.time_signature.split('/')[1]) / int(
                        self.note_page.current_duration.split('/')[1])) // (
                            int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                            self.note_page.height / 12 + self.note_page.height // 100 * 8) - self.note_page.height // 25
            self.note_page.database.update_sign(f'notepage_treble_{self.note_page.id_database}', value,
                                                self.note_page.x_pos_1 - int(
                                                    self.note_page.time_signature.split('/')[1]) / int(
                                                    self.note_page.current_duration.split('/')[1]))
        else:
            pos_x = self.note_page.current_pos_2()
            pos_y = (self.note_page.height / 10 * 9 - (
                    (self.note_page.x_pos_2 - int(self.note_page.time_signature.split('/')[1]) / int(
                        self.note_page.current_duration.split('/')[1])) // (
                            int(self.note_page.time_signature.split('/')[0]) * self.note_page.scale)) * (
                             self.note_page.height / 12 + self.note_page.height // 100 * 8)) - self.note_page.height // 25 - self.note_page.height // 12
            self.note_page.database.update_sign(f'notepage_bass_{self.note_page.id_database}', value,
                                                self.note_page.x_pos_2 - int(
                                                    self.note_page.time_signature.split('/')[1]) / int(
                                                    self.note_page.current_duration.split('/')[1]))
        pos_x -= int(self.note_page.time_signature.split('/')[1]) / int(
            self.note_page.current_duration.split('/')[1]) * self.note_page.each_note
        size_x = self.note_page.k_size_note * 3
        size_y = self.note_page.k_size_note * 6
        if value == -1:
            with self.note_page.canvas:
                sign = Image(source='templates/flat.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y)
                sign.size = (size_x, size_y)
        elif value == 1:
            with self.note_page.canvas:
                sign = Image(source='templates/sharp.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y)
                sign.size = (size_x, size_y)

    def select_tonality(self, instance, value):
        self.note_page.tonality = value

    def select_time_signature(self, instance, value):
        self.note_page.time_signature = value
        self.note_page.update_size(1, 1)

    # Обработчик нажатий на клавиатуру
    def on_keydown(self, instance, keyboard, keycode, text, modifiers):
        if 'ctrl' in modifiers:
            # Уменьшение масштаба
            if keycode == 45:
                self.note_page.scale += 1
                self.note_page.each_note = self.note_page.width * 8 / 9 / self.note_page.scale / int(
                    self.note_page.time_signature.split('/')[0])
                self.note_page.update_size(instance, 1)
            # Увеличение масштаба
            elif keycode == 46 and self.note_page.scale > 1:
                self.note_page.scale -= 1
                self.note_page.each_note = self.note_page.width * 8 / 9 / self.note_page.scale / int(
                    self.note_page.time_signature.split('/')[0])
                self.note_page.update_size(instance, 1)
            # Копирование куска произведения
            elif text == 'c':
                try:
                    x, y = self.note_page.rect_highlight.pos
                    w, h = self.note_page.rect_highlight.size
                    self.note_page.clipboard = [x, y, x + w, y + h]
                except:
                    pass
            # Вставка
            elif text == 'v':
                x, y, x1, y1 = self.note_page.clipboard
                if x > x1:
                    x1, x = x, x1
                if y > y1:
                    y1, y = y, y1
                for i in range(len(self.note_page.list_of_notes_treble_coords)):
                    if x <= self.note_page.list_of_notes_treble_coords[i][0] <= x1 and y <= self.note_page.list_of_notes_treble_coords[i][1] <= y1:
                        elem = self.note_page.list_of_notes_treble[i]
                        self.note_page.list_of_notes_treble.append(
                            (elem[0], self.note_page.x_pos_1, elem[2], elem[3]))
                        self.note_page.database.update(f'notepage_treble_{self.note_page.id_database}',
                                             (
                                                 elem[0], self.note_page.x_pos_1,
                                                 elem[2], elem[3]))
                        self.note_page.x_pos_1 += int(self.note_page.time_signature.split('/')[1]) / int(
                            elem[2].split('/')[1])
                for i in range(len(self.note_page.list_of_notes_bass_coords)):
                    if x <= self.note_page.list_of_notes_bass_coords[i][0] <= x1 and y <= self.note_page.list_of_notes_bass_coords[i][1] <= y1:
                        elem = self.note_page.list_of_notes_bass[i]
                        self.note_page.list_of_notes_bass.append(
                            (elem[0], self.note_page.x_pos_2, elem[2], elem[3]))
                        self.note_page.database.update(f'notepage_bass_{self.note_page.id_database}',
                                             (
                                                 elem[0], self.note_page.x_pos_2,
                                                 elem[2], elem[3]))
                        self.note_page.x_pos_2 += int(self.note_page.time_signature.split('/')[1]) / int(
                            elem[2].split('/')[1])
                self.note_page.update_size(instance, 1)



class NotePage(Widget):
    def __init__(self, **kwargs):
        super(NotePage, self).__init__(**kwargs)

        # Подключение к бд
        self.database = DataBase()
        self.id_database = self.database.select_id_database()
        self.title = self.database.select_title()
        self.author = self.database.select_author(k=1)

        self.list_of_notes_treble_coords = []  # Координаты нот скрипичного ключа
        self.list_of_notes_bass_coords = []  # Координаты нот басового ключа
        self.list_of_notes_treble = self.connecting_db(
            f'notepage_treble_{self.id_database}')  # Все ноты скрипичного ключа
        self.list_of_notes_bass = self.connecting_db(f'notepage_bass_{self.id_database}')  # Все ноты басового ключа

        self.time_signature = '4/4'  # Размер произведения
        self.tonality = 'C-dur'  # Тональность
        self.current_duration = '1/4'  # По умолчанию длительность
        self.x_pos_1 = 0  # Текущая позиция Скр. ключ
        self.x_pos_2 = 0  # Текущая позиция Бас.ключ
        self.y_pos = [self.height // 200 * i for i in range(-6, 19)]  # Позиция по вертикали (все возможные)
        self.current_clef = 1  # Текущий знак (для работы с клавиатурой)
        self.k_size_note = self.height // 150  # Коэфф размера ноты

        self.scale = 4  # Количество тактов на строке
        self.each_note = self.width * 8 / 9 / self.scale / int(self.time_signature.split('/')[0])  # На каждую мин долю
        self.selected_note = -1
        self.clipboard = [0, 0, 0, 0]  # Буфер обмена

        self.bind(size=self.update_size, pos=self.update_size)

        self.title_label = Label(
            text=self.title,
            font_size=30,
            color=(0, 0, 0, 1),
            width=self.width / 2,
            halign='center',
            valign='middle'
        )

        self.author_label = Label(
            text=self.author,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )

    def update_size(self, instance, value):
        self.clear_widgets()
        with self.canvas:
            Color(rgba=(1, 1, 1, 1))
            self.rect = Rectangle(size=self.size, pos=self.pos)

            self.filling_canvas()

            self.title_label.pos = [self.width / 4, self.height * 0.93]
            self.author_label.pos = [self.width / 4 * 3, self.height * 0.9]
            self.add_widget(self.title_label)
            self.add_widget(self.author_label)

            interval = self.height / 10
            for string in range(10):
                for i in range(5):
                    Color(0, 0, 0, 1)  # RGBA
                    Line(points=(0, self.height - interval - i * self.height / 100, self.width,
                                 self.height - interval - i * self.height / 100), width=1.5)
                if string % 2 == 0:
                    clef = Image(source='templates/treble_clef.png', allow_stretch=True, keep_ratio=False)
                    clef.height = self.height // 20
                    clef.width = self.width / 20
                else:
                    clef = Image(source='templates/bass_clef.png', allow_stretch=False, keep_ratio=True)
                    clef.height = self.height // 20
                    clef.width = self.width / 20
                clef.pos = (0, self.height - interval - 4 * self.height // 100)
                self.add_widget(clef)
                if string < 2:
                    time_signature_label_1 = Label(text=self.time_signature.split('/')[0],
                                                   font_name="D:/PycharmProjects/10_class/ZenDotsKir.ttf",
                                                   color=(0, 0, 0, 1), font_size=self.height / 50,
                                                   pos=(
                                                       self.width / 45,
                                                       self.height - interval - 4 * self.height // 100))
                    time_signature_label_2 = Label(text=self.time_signature.split('/')[1],
                                                   font_name="D:/PycharmProjects/10_class/ZenDotsKir.ttf",
                                                   color=(0, 0, 0, 1), font_size=self.height / 50,
                                                   pos=(
                                                       self.width / 45,
                                                       self.height - interval - 7 * self.height // 100))

                    self.add_widget(time_signature_label_1)
                    self.add_widget(time_signature_label_2)
                interval += self.height / 12

    def on_touch_down(self, touch):
        with self.canvas:
            if touch.button == 'left':
                if self.current_clef == 1:
                    x_pos = self.x_pos_1
                else:
                    x_pos = self.x_pos_2
                interval = self.height / 10 * 9 - (x_pos // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                        self.height / 6 + self.height // 100 * 8)
                Color(rgba=(0, 0, 0, 1))
                if ((self.height / 10 * 9 - (self.x_pos_1 // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                        self.height / 12 + self.height // 100 * 8)) + self.height // 48 >= touch.pos[1] >= (
                        (self.height / 10 * 9 - (
                                self.x_pos_1 // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                                 self.height / 12 + self.height // 100 * 8)) - (
                                self.height / 48 + self.height // 100 * 4))):
                    interval = self.height / 10 * 9 - (
                        (self.x_pos_1 // (int(self.time_signature.split('/')[0]) * self.scale))) * (
                                       self.height / 12 + self.height // 100 * 8)
                    index = [abs(touch.pos[1] - interval + j) for j in self.y_pos].index(
                        min([abs(touch.pos[1] - interval + i) for i in self.y_pos]))
                    y = [interval - j for j in self.y_pos][index]

                    if int(self.current_duration.split('/')[1]) < 4:
                        Line(ellipse=(int(self.width / 9 + self.x_pos_1 % (self.scale * int(
                            self.time_signature.split('/')[0])) * self.each_note) - self.k_size_note,
                                      y - self.k_size_note // 2,
                                      self.k_size_note * 2, self.k_size_note), width=1.5)
                    else:
                        Ellipse(pos=(int(self.current_pos_1()) - self.k_size_note, y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                    if int(self.current_duration.split('/')[1]) > 1:
                        Line(points=(
                            int(self.current_pos_1()) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note // 2 - (index < 11) * self.k_size_note,
                            int(self.current_pos_1()) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note * 4 - 8 * (index < 11) * self.k_size_note), width=1.5)
                        self.changing_duration(index, y, self.current_pos_1(), self.current_duration)
                    # Дополнительные линии
                    if index % 2 == 0 and (index < 8 or index > 16):
                        Line(points=(
                            int(self.current_pos_1()) - self.k_size_note * 2, y,
                            int(self.current_pos_1()) + self.k_size_note * 2, y), width=1.5)
                        if index < 6:
                            Line(points=(
                                int(self.current_pos_1()) - self.k_size_note * 2, interval - self.y_pos[index - 2],
                                int(self.current_pos_1()) + self.k_size_note * 2, interval - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 2:
                                Line(points=(
                                    int(self.current_pos_1()) - self.k_size_note * 2,
                                    interval - self.y_pos[index - 3],
                                    int(self.current_pos_1()) + self.k_size_note * 2,
                                    interval - self.y_pos[index - 3]), width=1.5)
                        if index > 18:
                            Line(points=(
                                int(self.current_pos_1()) - self.k_size_note * 2, interval - self.y_pos[index - 2],
                                int(self.current_pos_1()) + self.k_size_note * 2, interval - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 20:
                                Line(points=(
                                    int(self.current_pos_1()) - self.k_size_note * 2,
                                    interval - self.y_pos[index - 3],
                                    int(self.current_pos_1()) + self.k_size_note * 2,
                                    interval - self.y_pos[index - 3]), width=1.5)

                    elif index == 21:
                        Line(points=(
                            int(self.current_pos_1()) - self.k_size_note * 2, interval + self.y_pos[index - 1],
                            int(self.current_pos_1()) + self.k_size_note * 2, interval + self.y_pos[index - 1]),
                            width=1.5)
                    elif index == 3 or index == 5:
                        Line(points=(
                            int(self.current_pos_1()) - self.k_size_note * 2, interval - self.y_pos[index + 1],
                            int(self.current_pos_1()) + self.k_size_note * 2, interval - self.y_pos[index + 1]),
                            width=1.5)
                        if index == 3:
                            Line(points=(
                                int(self.current_pos_1()) - self.k_size_note * 2, interval - self.y_pos[index + 3],
                                int(self.current_pos_1()) + self.k_size_note * 2, interval - self.y_pos[index + 3]),
                                width=1.5)

                    self.list_of_notes_treble_coords.append((self.current_pos_1(), y))
                    self.list_of_notes_treble.append(
                        (index, self.x_pos_1, self.current_duration, 0))
                    self.database.update(f'notepage_treble_{self.id_database}',
                                         (
                                             index, self.x_pos_1,
                                             self.current_duration, 0))
                    print(self.time_signature)
                    self.x_pos_1 += int(self.time_signature.split('/')[1]) / int(
                        self.current_duration.split('/')[1])
                    self.current_clef = 1
                elif (
                        ((self.height / 10 * 9 - (
                                self.x_pos_2 // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                                  self.height / 12 + self.height // 100 * 8)) - (
                                 self.height / 48 + self.height // 100 * 4))) >= touch.pos[1] >= (
                        self.height / 10 * 9 - (
                        self.x_pos_2 // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                                self.height / 12 + self.height // 100 * 8)) - (
                        self.height / 24 + self.height // 100 * 11):
                    interval = (self.height / 10 * 9 - (
                            self.x_pos_2 // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                                        self.height / 12 + self.height // 100 * 8))
                    index = [abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + j) for j in
                             self.y_pos].index(
                        min([abs(touch.pos[1] - interval + (self.height / 24 + self.height // 100 * 4) + i) for i in
                             self.y_pos]))
                    y = [interval - (self.height / 24 + self.height // 100 * 4) - j for j in self.y_pos][index]

                    if int(self.current_duration.split('/')[1]) < 4:
                        Line(ellipse=(int(self.current_pos_2()) - self.k_size_note, y - self.k_size_note // 2,
                                      self.k_size_note * 2, self.k_size_note), width=1.5)
                    else:
                        Ellipse(pos=(int(self.width / 9 + self.x_pos_2 % (self.scale * int(
                            self.time_signature.split('/')[0])) * self.each_note) - self.k_size_note,
                                     y - self.k_size_note // 2),
                                size=(self.k_size_note * 2, self.k_size_note))
                    if int(self.current_duration.split('/')[1]) > 1:
                        Line(points=(
                            int(self.current_pos_2()) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note // 2 - (index < 11) * self.k_size_note,
                            int(self.current_pos_2()) + self.k_size_note - 2 * (index < 11) * self.k_size_note,
                            y + self.k_size_note * 4 - 8 * (index < 11) * self.k_size_note), width=1.5)
                    self.changing_duration(index, y, self.current_pos_2(), self.current_duration)
                    if index % 2 == 0 and (index < 8 or index > 18):
                        Line(points=(
                            int(self.current_pos_2()) - self.k_size_note * 2, y,
                            int(self.current_pos_2()) + self.k_size_note * 2, y), width=1.5)

                        if index < 6:
                            Line(points=(
                                int(self.current_pos_2()) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2],
                                int(self.current_pos_2()) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 2:
                                Line(points=(
                                    int(self.current_pos_2()) - self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3],
                                    int(self.current_pos_2()) + self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3]), width=1.5)
                        if index > 16:
                            Line(points=(
                                int(self.current_pos_2()) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2],
                                int(self.current_pos_2()) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 2]),
                                width=1.5)
                            if index == 20:
                                Line(points=(
                                    int(self.current_pos_2()) - self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3],
                                    int(self.current_pos_2()) + self.k_size_note * 2,
                                    interval - self.height // 12 - self.y_pos[index - 3]), width=1.5)

                    elif index == 19:
                        Line(points=(
                            int(self.current_pos_2()) - self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1],
                            int(self.current_pos_2()) + self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1]),
                            width=1.5)
                    elif index == 3 or index == 5:
                        Line(points=(
                            int(self.current_pos_2()) - self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1],
                            int(self.current_pos_2()) + self.k_size_note * 2,
                            interval - self.height // 12 - self.y_pos[index - 1]),
                            width=1.5)
                        if index == 3:
                            Line(points=(
                                int(self.current_pos_2()) - self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 3],
                                int(self.current_pos_2()) + self.k_size_note * 2,
                                interval - self.height // 12 - self.y_pos[index - 3]),
                                width=1.5)

                    self.list_of_notes_bass_coords.append((self.current_pos_2(), y))
                    self.list_of_notes_bass.append(
                        (index, self.x_pos_2, self.current_duration, 0))
                    self.database.update(f'notepage_bass_{self.id_database}', (
                        index, self.x_pos_2, self.current_duration, 0
                    ))

                    self.x_pos_2 += int(self.time_signature.split('/')[1]) / int(
                        self.current_duration.split('/')[1])
                    self.current_clef = 2
            elif touch.button == 'right':
                Color(0, 0, 0, 0.5)
                self.rect_highlight = Rectangle(pos=touch.pos, size=(1, 1))
            self.make_beat()

    def on_touch_move(self, touch):
        if touch.button == 'right':
            x, y = self.rect_highlight.pos
            self.rect_highlight.size = (touch.pos[0] - x, touch.pos[1] - y)

    def on_touch_up(self, touch):
        if touch.button == 'right':
            self.canvas.remove(self.rect_highlight)

    # Такты
    def make_beat(self):
        count_strings = int(max(self.x_pos_1, self.x_pos_2) // (self.scale * int(self.time_signature.split('/')[0])))
        for num_string in range(count_strings + 1):
            if num_string == count_strings:
                count_beats = int((max(self.x_pos_1, self.x_pos_2) % (
                        self.scale * int(self.time_signature.split('/')[0]))) // self.scale)
            else:
                count_beats = self.scale
            for i in range(count_beats):
                with self.canvas:
                    Color(0, 0, 0, 1)
                    Line(points=(self.width / 9 * 8 / self.scale * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (self.height / 6),
                                 self.width / 9 * 8 / self.scale * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 6) - self.height / 100 * 4), width=1.5)
                    Line(points=(self.width / 9 * 8 / self.scale * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 6) - (
                                         self.height / 12),
                                 self.width / 9 * 8 / self.scale * (i + 1) + self.width / 9 - self.each_note / 3,
                                 self.height / 10 * 9 - num_string * (
                                         self.height / 6) - (
                                         self.height / 12 + self.height / 100 * 4)), width=1.5)

    def changing_pause(self, duration, image, clef):
        if clef == 1:
            x_pos = self.x_pos_1
        else:
            x_pos = self.x_pos_2
        y = self.height / 10 * 9 - (x_pos // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                self.height // 12 + self.height // 100 * 8) - self.height // 100 * 5.5
        if clef == 1:
            with self.canvas:
                pause = Image(source=image, allow_stretch=False, keep_ratio=True)
                pause.pos = ((self.width / 9 + self.x_pos_1 % (
                        self.scale * int(self.time_signature.split('/')[0])) * self.each_note) - self.each_note / 2,
                             y)
                self.add_widget(pause)
                self.list_of_notes_treble_coords.append((self.current_pos_1(), y))


        else:
            with self.canvas:
                pause = Image(source=image, allow_stretch=False, keep_ratio=True)
                pause.pos = (
                    (self.width / 9 + self.x_pos_2 % (self.scale * int(
                        self.time_signature.split('/')[0])) * self.each_note) - self.each_note / 2,
                    y - self.height / 12)
                self.add_widget(pause)
                self.list_of_notes_bass_coords.append((self.current_pos_2(), y))

        self.make_beat()

    def changing_duration(self, index, y, current_pos, duration):
        with self.canvas:
            if int(duration.split('/')[1]) > 4:
                if index > 10:
                    start_x, start_y = int(current_pos) + self.k_size_note - 2 * (
                            index < 11) * self.k_size_note, y + self.k_size_note * 4 - 8 * (
                                               index < 11) * self.k_size_note
                    size_x, size_y = self.k_size_note * 2, self.k_size_note * 4
                    Line(ellipse=(start_x, start_y - size_y / 2, size_x, size_y, 180, 270), width=1.5)
                else:
                    start_x, start_y = int(current_pos) + self.k_size_note - 2 * (
                            index < 11) * self.k_size_note, y + self.k_size_note * 4 - 8 * (
                                               index < 11) * self.k_size_note
                    size_x, size_y = self.k_size_note * 4, self.k_size_note * 4
                    Line(ellipse=(start_x - size_x / 2, start_y, size_x, size_y, 90, 180), width=1.5)

    def connecting_db(self, name_db):
        self.database.create(name_db)
        return list(self.database.select(name_db))

    def filling_canvas(self):
        self.list_of_notes_treble_coords, self.list_of_notes_bass_coords = [], []
        self.x_pos_1, self.x_pos_2 = 0, 0
        for i in self.list_of_notes_treble:
            if i[3] == 3:
                if i[2] == '1/1':
                    self.changing_pause(i[2], 'templates/whole_pause.png', 1)
                elif i[2] == '1/2':
                    self.changing_pause(i[2], 'templates/half_pause.png', 1)
                elif i[2] == '1/4':
                    self.changing_pause(i[2], 'templates/quarter_pause.png', 1)
                elif i[2] == '1/8':
                    self.changing_pause(i[2], 'templates/eighth_pause.png', 1)
                elif i[2] == '1/16':
                    self.changing_pause(i[2], 'templates/sixteenth_pause.png', 1)
                elif i[2] == '1/32':
                    self.changing_pause(i[2], 'templates/thirty_second_pause.png', 1)
                self.x_pos_1 += int(self.time_signature.split('/')[1]) / int(
                    self.current_duration.split('/')[1])
                continue
            self.draw_note_filling_canvas(
                self.height / 10 * 9 - (i[1] // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                        self.height / 6), i[0],
                self.width / 9 + i[1] % (self.scale * int(self.time_signature.split('/')[0])) * self.each_note, i[2],
                i[3], 1)
        for i in self.list_of_notes_bass:
            if i[3] == 3:
                if i[2] == '1/1':
                    self.changing_pause(i[2], 'templates/whole_pause.png', 2)
                elif i[2] == '1/2':
                    self.changing_pause(i[2], 'templates/half_pause.png', 2)
                elif i[2] == '1/4':
                    self.changing_pause(i[2], 'templates/quarter_pause.png', 2)
                elif i[2] == '1/8':
                    self.changing_pause(i[2], 'templates/eighth_pause.png', 2)
                elif i[2] == '1/16':
                    self.changing_pause(i[2], 'templates/sixteenth_pause.png', 2)
                elif i[2] == '1/32':
                    self.changing_pause(i[2], 'templates/thirty_second_pause.png', 2)
                self.x_pos_2 += int(self.time_signature.split('/')[1]) / int(
                    self.current_duration.split('/')[1])
                continue
            self.draw_note_filling_canvas(
                self.height / 10 * 9 - (i[1] // (int(self.time_signature.split('/')[0]) * self.scale)) * (
                        self.height / 6), i[0],
                self.width / 9 + i[1] % (self.scale * int(self.time_signature.split('/')[0])) * self.each_note, i[2],
                i[3], 2)

    def draw_note_filling_canvas(self, y, ind, pos, duration, sign, clef):
        y -= (ind - 6) * self.height // 200
        if clef == 1:
            with self.canvas:
                Color(0, 0, 0, 1)
                if int(duration.split('/')[1]) < 4:
                    Line(ellipse=(int(pos) - self.k_size_note, y - self.k_size_note // 2,
                                  self.k_size_note * 2, self.k_size_note), width=1.5)
                else:
                    Ellipse(pos=(
                        int(pos) - self.k_size_note,
                        y - self.k_size_note // 2),
                        size=(self.k_size_note * 2, self.k_size_note))
                    self.changing_duration(ind, y, pos, duration)
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

                self.adding_signature(sign, self.current_pos_1(), y)

                self.list_of_notes_treble_coords.append((int(pos), y))

                self.x_pos_1 += int(self.time_signature.split('/')[1]) / int(
                    self.current_duration.split('/')[1])
        else:
            with self.canvas:
                Color(0, 0, 0, 1)
                if int(duration.split('/')[1]) < 4:
                    Line(ellipse=(int(pos) - self.k_size_note,
                                  y - self.height / 12 - self.k_size_note // 2,
                                  self.k_size_note * 2, self.k_size_note), width=1.5)
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
                self.changing_duration(ind, y - self.height / 12, pos, duration)
                if ind % 2 == 0 and (ind < 6 or ind > 14):
                    Line(points=(
                        int(pos) - self.k_size_note * 2,
                        y - self.height / 12,
                        pos + self.k_size_note * 2,
                        y - self.height / 12), width=1.5)

                self.list_of_notes_bass_coords.append((int(pos), y))

                self.adding_signature(sign, self.current_pos_2(), y - self.height / 12)

                self.x_pos_2 += int(self.time_signature.split('/')[1]) / int(
                    self.current_duration.split('/')[1])
        self.make_beat()

    def adding_signature(self, value, pos_x, pos_y):
        size_x = self.k_size_note * 3
        size_y = self.k_size_note * 6
        if value == -1:
            with self.canvas:
                sign = Image(source='templates/flat.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y - size_y // 2)
                sign.size = (size_x, size_y)
                self.add_widget(sign)
        elif value == 1:
            with self.canvas:
                sign = Image(source='templates/sharp.png', allow_stretch=True, keep_ratio=False)
                sign.pos = (pos_x - 1.5 * size_x, pos_y - size_y // 2)
                sign.size = (size_x, size_y)
                self.add_widget(sign)

    def current_pos_1(self):
        return (self.width / 9 + self.x_pos_1 % (self.scale * int(self.time_signature.split('/')[0])) * self.each_note)

    def current_pos_2(self):
        return (self.width / 9 + self.x_pos_2 % (self.scale * int(self.time_signature.split('/')[0])) * self.each_note)


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
        self.const = Const()
        self.hint_y = 1

        self.save_file = Button(size_hint=(1 / 18, self.hint_y),
                                background_normal='templates/save_file.png')  # text="Сохранить файл",

        self.box_choice = BoxLayout()
        self.box_choice.orientation = 'vertical'
        self.box_choice.size_hint_x = 1 / 18
        self.choice_of_time_signature = Spinner(values=['4/4', '3/4', '2/4', '7/8', '6/8', '3/8', '2/2', '3/16', '5/8'],
                                                text='4/4')  # "Выбор тональности",
        self.choice_of_tonality = Spinner(values=self.const.all_tonalties, text='C-dur')  # "Выбор размера",
        self.box_choice.add_widget(self.choice_of_tonality)
        self.box_choice.add_widget(self.choice_of_time_signature)

        self.delete_note = Button(size_hint=(1 / 18, self.hint_y),
                                  background_normal='templates/delete_note.png')  # text="Режим рисования",

        self.flat = Button(size_hint=(1 / 18, self.hint_y),
                           background_normal='templates/flat.png')  # text="Бемоль",
        self.sharp = Button(size_hint=(1 / 18, self.hint_y),
                            background_normal='templates/sharp.png')  # text="Диез",
        self.natural = Button(size_hint=(1 / 18, self.hint_y),
                              background_normal='templates/natural.png')  # text="Бекар",

        self.whole = Button(size_hint=(1 / 18, self.hint_y),
                            background_normal='templates/whole.png')  # text="Целая",
        self.half = Button(size_hint=(1 / 18, self.hint_y),
                           background_normal='templates/half.png')  # text="Половинка",
        self.quarter = Button(size_hint=(1 / 18, self.hint_y),
                              background_normal='templates/quarter.png')  # text="Четверь",
        self.eighth = Button(size_hint=(1 / 18, self.hint_y),
                             background_normal='templates/eighth.png')  # text="Восьмая",
        self.sixteenth = Button(size_hint=(1 / 18, self.hint_y),
                                background_normal='templates/sixteenth.png')  # text="Шестнадцая",
        self.thirty_second = Button(size_hint=(1 / 18, self.hint_y),
                                    background_normal='templates/thirty_second.png')  # text="Тридцать вторая",

        self.whole_pause = Button(size_hint=(1 / 18, self.hint_y),
                                  background_normal='templates/whole_pause.png')  # text="Целая пауза",
        self.half_pause = Button(size_hint=(1 / 18, self.hint_y),
                                 background_normal='templates/half_pause.png')  # text="Половинка пауза",
        self.quarter_pause = Button(size_hint=(1 / 18, self.hint_y),
                                    background_normal='templates/quarter_pause.png')  # text="Четверь пауза",
        self.eighth_pause = Button(size_hint=(1 / 18, self.hint_y),
                                   background_normal='templates/eighth_pause.png')  # text="Восьмая пауза",
        self.sixteenth_pause = Button(size_hint=(1 / 18, self.hint_y),
                                      background_normal='templates/sixteenth_pause.png')  # text="Шестнадцая пауза",
        self.thirty_second_pause = Button(size_hint=(1 / 18, self.hint_y),
                                          background_normal='templates/thirty_second_pause.png')  # text="Тридцать вторая пауза",

        self.list_instruments = [self.save_file, self.box_choice, self.delete_note,
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
 
 
x_pos
 1. Прибавление доли
 2. x = Отступ + self.(x_pos % масштаб) * self.each_note
'''
