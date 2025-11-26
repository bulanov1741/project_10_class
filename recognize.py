import time

import numpy as np
import pyaudio
import wave

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from const import Const


class RecognizeBox(BoxLayout):
    def __init__(self):
        super().__init__()
        button_recognition = Button(
            text=">",
            pos_hint={"center_x": 0.25, "center_y": 0.5},
        )
        button_tuning = Button(
            text="+",
            pos_hint={"center_x": 0.75, "center_y": 0.5},
        )

        button_recognition.bind(on_press=self.recognition)
        button_tuning.bind(on_press=self.tuning)

        self.add_widget(button_recognition)
        self.add_widget(button_tuning)


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

    # Распознание нот
    def recognition(self, instance):
        # имя файла для записи
        filename = "recorded.wav"
        # установить размер блока в 1024 сэмпла
        chunk = 1024
        # образец формата
        FORMAT = pyaudio.paInt16
        channels = 1
        # 44100 сэмплов в секунду
        sample_rate = 44100
        record_seconds = 20
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
        print("Recording...")
        for i in range(int(44100 / chunk * record_seconds)):
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
                print(freq)
                print(freq)
                if abs(freq - 130.8) < 3:
                    print("До")
                elif abs(freq) - 138.6 < 3:
                    print("До#")
                elif abs(freq - 146.8) < 3:
                    print("Ре")
                elif abs(freq - 155.6) < 3:
                    print("Ре#")
                elif abs(freq - 164.8) < 3:
                    print("Ми")
                elif abs(freq - 174.6) < 3:
                    print("Фа")
                elif abs(freq - 185.0) < 3:
                    print("Фа#")
                elif abs(freq - 196.0) < 3:
                    print("Соль")
                elif abs(freq - 207.7) < 3:
                    print("Соль#")
                elif abs(freq - 220.0) < 3:
                    print("Ля")
                elif abs(freq - 233.1) < 3:
                    print("Ля#")
                elif abs(freq - 246.9) < 3:
                    print("Си")

            # если вы хотите слышать свой голос во время записи
            # stream.write(data)
            frames.append(data)
        print("Finished recording.")
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
        wf.close()

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



class RecognizeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.recognize_box = RecognizeBox()
        self.add_widget(self.recognize_box)




