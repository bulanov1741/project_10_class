import sqlite3
import threading
import time
from datetime import datetime

import numpy as np
import pyaudio
import wave

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from const import Const
from sqlite import DataBase


class RecognizeBox(BoxLayout):
    def __init__(self):
        super().__init__()
        self.orientation = 'vertical'
        self.button_recognition = Button(
            #text="Начать запись",
            background_normal='templates/play_black.png',
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        self.thread = None
        self.stop_event = threading.Event()

        self.button_recognition.bind(on_press=self.button_recognition_method)

        self.add_widget(self.button_recognition)


    def mi(self, *args):
        frequency = args[-1]
        p = pyaudio.PyAudio()

        volume = 1  # range [0.0, 1.0]
        fs = 44100  # sampling rate, Hz, must be integer
        duration = 0.3  # in seconds, may be float

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

        # per @yahweh comment explicitly convert to bytes sequence
        output_bytes = (volume * samples).tobytes()

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=fs,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        start_time = time.time()
        stream.write(output_bytes)
        print("Played sound for {:.2f} seconds".format(time.time() - start_time))

        stream.stop_stream()
        stream.close()

        p.terminate()

    def button_recognition_method(self, instance):
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.recognition)
            self.thread.start()
            #instance.text = 'Идет запись'
            instance.background_normal = 'templates/stop_black.png'
        else:
            # Остановка текущего потока
            self.stop_event.set()
            #instance.text = 'Начать запись'
            instance.background_normal = 'templates/play_black.png'
            self.show_notification('Запись завершена. Результат сохранен')

    # Распознание нот
    def recognition(self):
        # Лист для записи расшифрованного
        self.note_database = DataBase()
        self.con = sqlite3.connect("db.db")
        self.cur = self.con.cursor()
        self.name = f'notepage_treble_{self.adding_note_page_recognize()}'
        self.note_database.create(self.name)
        self.pos_x = 0

        # Частоты нот
        self.const = Const()


        # имя файла для записи
        filename = "recorded.wav"
        # установить размер блока в 1024 сэмпла
        chunk = 10000
        # образец формата
        FORMAT = pyaudio.paInt16
        channels = 1
        # 44100 сэмплов в секунду
        sample_rate = 44100
        # initialize PyAudio object
        p = pyaudio.PyAudio()
        # открыть объект потока как ввод и вывод
        stream = p.open(format=FORMAT,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        output=True,
                        frames_per_buffer=chunk)
        frames = []
        start = time.time()
        note = ''
        while True:
            data = stream.read(chunk)
            # преобразование байтовых данных в массив numpy
            data = np.frombuffer(data, dtype=np.int16)
            # выполнение преобразования Фурье для получения частотного спектра
            spectrum = np.fft.fft(data)
            # вычисление частотных значений
            freqs = np.fft.fftfreq(len(data), 1.0 / sample_rate)
            # поиск индекса нужной частоты (например, 1000 Гц)
            index = np.argmax(np.abs(spectrum))
            if np.abs(spectrum)[index] > 300000:
                freq = abs(freqs[index])
                mini, min_ind = 10000, 0
                for j in range(len(self.const.all_freq)):
                    if mini > abs(freq - self.const.all_freq[j]):
                        mini = abs(freq - self.const.all_freq[j])
                        min_ind = j % 12

                if min_ind == 0:
                    print("До")
                    self.note_database.update(self.name,
                                                   [16, self.pos_x,
                                                    '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 1:
                    self.note_database.update(self.name,
                                              [16, self.pos_x,
                                               '1/4', 1])
                    self.pos_x += 1
                    print("До#")
                elif min_ind == 2:
                    print("Ре")
                    self.note_database.update(self.name,
                                              [15, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 3:
                    print("Ре#")
                    self.note_database.update(self.name,
                                              [15, self.pos_x,
                                               '1/4', 1])
                    self.pos_x += 1
                elif min_ind == 4:
                    print("Ми")
                    self.note_database.update(self.name,
                                              [14, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 5:
                    print("Фа")
                    self.note_database.update(self.name,
                                              [13, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 6:
                    print("Фа#")
                    self.note_database.update(self.name,
                                              [13, self.pos_x,
                                               '1/4', 1])
                    self.pos_x += 1
                    self.con.commit()
                elif min_ind == 7:
                    print("Соль")
                    self.note_database.update(self.name,
                                              [12, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 8:
                    print("Соль#")
                    self.note_database.update(self.name,
                                              [12, self.pos_x,
                                               '1/4', 1])
                    self.pos_x += 1
                elif min_ind == 9:
                    print("Ля")
                    self.note_database.update(self.name,
                                              [11, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                elif min_ind == 10:
                    print("Ля#")
                    self.note_database.update(self.name,
                                              [11, self.pos_x,
                                               '1/4', 1])
                    self.pos_x += 1
                elif min_ind == 11:
                    print("Си")
                    self.note_database.update(self.name,
                                              [10, self.pos_x,
                                               '1/4', 0])
                    self.pos_x += 1
                print(time.time() - start)
                start = time.time()

            # если вы хотите слышать свой голос во время записи
            # stream.write(data)
            frames.append(data)
            if self.stop_event.is_set():
                # остановить и закрыть поток
                stream.stop_stream()
                stream.close()
                # завершить работу объекта pyaudio
                p.terminate()
                # сохранить аудиофайл
                # открываем файл в режиме 'запись байтов'
                wf = wave.open(filename, "wb")
                # установить каналы
                wf.setnchannels(channels)
                # установить формат образца
                wf.setsampwidth(p.get_sample_size(FORMAT))
                # установить частоту дискретизации
                wf.setframerate(sample_rate)
                # записываем кадры как байты
                wf.writeframes(b"".join(frames))
                # закрыть файл
                self.con.close()
                wf.close()
                break


    def adding_note_page_recognize(self):
        name_id = len([i[0] for i in list(self.cur.execute('SELECT ID FROM saved_database WHERE name LIKE "Распознанный лист%"').fetchall())]) + 1
        max_id = max([i[0] for i in list(self.cur.execute('SELECT ID FROM saved_database').fetchall())])
        self.cur.execute(
            f"INSERT INTO saved_database (id, name, author, time_created, now_open) VALUES (?, ?, ?, ?, ?)",
            [max_id + 1, f"Распознанный лист({name_id})",
             self.note_database.select_author(),
             datetime.now().strftime("%H:%M:%S|%d.%m.%Y"), 0])
        self.con.commit()
        return max_id + 1




    def tuning(self, instance):
        const = Const()
        for note in const.notes:
            print(f'Нажмите и удерживайте ноту {note}')

            a = []

            chunk = 1024
            FORMAT = pyaudio.paInt16
            channels = 1
            sample_rate = 44100
            record_seconds = 3
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                            channels=channels,
                            rate=sample_rate,
                            input=True,
                            output=True,
                            frames_per_buffer=chunk)
            frames = []
            for i in range(int(44100 / chunk * record_seconds)):
                data = stream.read(chunk)
                data = np.frombuffer(data, dtype=np.int16)
                spectrum = np.fft.fft(data)
                freqs = np.fft.fftfreq(len(data), 1.0 / sample_rate)
                index = np.argmax(np.abs(spectrum))
                if np.abs(spectrum)[index] > 300000:
                    freq = freqs[index]
                    a.append(abs(freq))

            print(f'{note} - {list(sorted(a))[len(a) // 2]}')

    def show_notification(self, text):
        popup = Popup(title='Уведомление', content=Label(text=text), size_hint=(None, None), size=(400, 400))
        popup.open()



class RecognizeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.recognize_box = RecognizeBox()
        self.add_widget(self.recognize_box)




