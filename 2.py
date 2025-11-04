import pyaudio
import numpy as np
from scipy.io import wavfile

from const import Const

for i in range(100):
    CHUNK = 1024  # Размер буферов аудиоданных
    FORMAT = pyaudio.paInt16  # Формат звукового потока
    CHANNELS = 1  # Количество каналов
    RATE = 44100  # Частота выборки
    RECORD_SECONDS = 1  # Длительность записи в секундах

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Запись началась...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Запись закончена.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Преобразование массива байтов в массив чисел
    audio_data = b''.join(frames)
    samples = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)

    # Нормализация уровня громкости
    normalized_samples = samples / np.max(np.abs(samples))

    # Быстрое преобразование Фурье
    fft_data = np.fft.rfft(normalized_samples)
    frequencies = np.fft.rfftfreq(len(normalized_samples), d=1. / RATE)
    magnitudes = np.abs(fft_data)

    # Определение основной частоты (самая высокая амплитуда)
    peak_frequency_idx = np.argmax(magnitudes)
    frequency = frequencies[peak_frequency_idx]

    const = Const()
    for i in range(len(const.okt_3)):
        if abs(abs(const.okt_3[i]) - abs(frequency)) < 3:
            print(const.notes[i])
    print(f'Основная частота сигнала: {frequency:.2f} Гц')
