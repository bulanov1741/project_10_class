import numpy as np
import pyaudio
import time
from scipy.signal import find_peaks


class VolumeFilteredNoteDetector:
    def __init__(self):
        self.CHUNK = 4096
        self.RATE = 44100
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1

        # Пороги громкости (в dBFS)
        self.MIN_VOLUME_DB = -30  # Минимальная громкость для анализа
        self.MAX_VOLUME_DB = -3  # Максимальная громкость (чтобы избежать клиппинга)

        # Ноты
        self.notes = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }

        self.p = pyaudio.PyAudio()

    def calculate_rms(self, audio_data):
        """Вычисление RMS (среднеквадратичное значение) громкости"""
        return np.sqrt(np.mean(audio_data ** 2))

    def calculate_db(self, audio_data):
        """Преобразование RMS в децибелы (dBFS)"""
        rms = self.calculate_rms(audio_data)
        if rms < 1e-10:  # Защита от деления на ноль
            return -100
        return 20 * np.log10(rms)

    def get_note_name(self, frequency):
        """Определение названия ноты по частоте"""
        if frequency < 20:
            return None

        note_name = min(self.notes.items(),
                        key=lambda x: abs(x[1] - frequency))[0]
        octave = 4 + int(np.log2(frequency / self.notes[note_name]))

        return f"{note_name}{octave}"

    def start_detection_with_volume_filter(self):
        """Распознавание нот с фильтрацией по громкости"""
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

        print("🎤 Слушаю... Нажмите Ctrl+C для остановки")
        print(f"Пороги громкости: {self.MIN_VOLUME_DB} dB до {self.MAX_VOLUME_DB} dB")
        print("-" * 60)

        # Статистика для адаптивных порогов
        volume_history = []
        is_silence = True

        try:
            while True:
                sounds = []
                # Читаем аудиоданные
                data = np.frombuffer(stream.read(self.CHUNK), dtype=np.float32)

                # Вычисляем громкость
                volume_db = self.calculate_db(data)
                volume_history.append(volume_db)
                if len(volume_history) > 100:
                    volume_history.pop(0)

                # Определяем, есть ли звук
                if volume_db > self.MIN_VOLUME_DB and volume_db < self.MAX_VOLUME_DB:
                    if is_silence:
                        print("\n🎶 Начало звука...")
                        is_silence = False

                    # Анализируем только если громкость в допустимом диапазоне
                    sounds.append(self.analyze_audio(data, volume_db))
                else:
                    if not is_silence and volume_db < self.MIN_VOLUME_DB:
                        print(max(sounds, key=lambda x:x[2]))
                        is_silence = True

                # Выводим индикатор громкости
                # self.display_volume_meter(volume_db)

        except KeyboardInterrupt:
            print("\n\nОстановлено.")
        finally:
            stream.stop_stream()
            stream.close()
            self.p.terminate()

    def analyze_audio(self, audio_data, volume_db):
        """Анализ аудио при достаточной громкости"""
        # Применяем оконную функцию
        windowed = audio_data * np.hanning(len(audio_data))

        # Вычисляем БПФ
        fft = np.abs(np.fft.rfft(windowed))



        freqs = np.fft.rfftfreq(len(windowed), 1.0 / self.RATE)

        # Находим пики
        noise_floor = np.percentile(fft, 50)  # Медиана как уровень шума
        min_peak_height = noise_floor * 10  # Пики должны быть в 10 раз выше шума

        peaks, properties = find_peaks(fft,
                                       height=min_peak_height,
                                       distance=50,
                                       prominence=noise_floor * 5)

        if len(peaks) > 0:
            # Основная частота - самый высокий пик
            main_peak = peaks[np.argmax(properties['peak_heights'])]
            freq = freqs[main_peak]

            # Фильтр частот
            if 80 < freq < 1200:
                note = self.get_note_name(freq)
                if note:
                    confidence = properties['peak_heights'][np.argmax(properties['peak_heights'])] / noise_floor
                    return (f"{note:4s}", float(f"{freq:6.1f}"),
                          float(f"{volume_db:5.1f}"), float(f"{confidence:5.1f}"))


    # def display_volume_meter(self, volume_db):
    #     """Отображение индикатора громкости"""
    #     # Нормализуем громкость для отображения
    #     min_db = -60
    #     max_db = 0
    #
    #     normalized = max(0, min(1, (volume_db - min_db) / (max_db - min_db)))
    #     bar_length = 30
    #     filled = int(normalized * bar_length)
    #
    #     bar = '█' * filled + '░' * (bar_length - filled)
    #
    #     # Цветовая индикация
    #     if volume_db < self.MIN_VOLUME_DB:
    #         color = "\033[90m"  # Серый - тихо
    #     elif self.MIN_VOLUME_DB <= volume_db < -20:
    #         color = "\033[92m"  # Зеленый - нормально
    #     elif -20 <= volume_db < -10:
    #         color = "\033[93m"  # Желтый - громко
    #     else:
    #         color = "\033[91m"  # Красный - очень громко
    #
    #     reset = "\033[0m"
    #     print(f"\r{color}Громкость: {bar} {volume_db:5.1f} dB{reset}", end='')

a = VolumeFilteredNoteDetector()
a.start_detection_with_volume_filter()