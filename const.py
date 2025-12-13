from kivy.core.window import Window


class Const():
    def __init__(self):
        # Размеры экрана
        self.width = Window.width
        self.height = Window.height

        # Ноты
        self.lat = 'C	C#	D	D#	E	F	F#	G	G#	A	A#	B'.split()
        self.notes = 'До До# Ре	Ре#	Ми	Фа	Фа#	Соль Соль#	Ля	Ля#	Си'.split()
        # Их частоты
        self.okt_0 = '16.35	17.32	18.35	19.45	20.60	21.83	23.12	24.50	25.96	27.50	29.14	30.87'.split()
        self.okt_1 = '32.70	34.65	36.71	38.89	41.20	43.65	46.25	49.00	51.91	55.00	58.27	61.74'.split()
        self.okt_2 = '65.41	69.30	73.42	77.78	82.41	87.31	92.50	98.00	103.8	110.0	116.5	123.5'.split()
        self.okt_3 = '130.8	138.6	146.8	155.6	164.8	174.6	185.0	196.0	207.7	220.0	233.1	246.9'.split()
        self.okt_4 = '261.6	277.2	293.7	311.1	329.6	349.2	370.0	392.0	415.3	440.0	466.2	493.9'.split()
        self.okt_5 = '523.3	554.4	587.3	622.3	659.3	698.5	740.0	784.0	830.6	880.0	932.3	987.8'.split()
        self.okt_6 = '1047	1109	1175	1245	1319	1397	1480	1568	1661	1760	1865	1976'.split()
        self.okt_7 = '2093	2217	2349	2489	2637	2794	2960	3136	3322	3520	3729	3951'.split()
        self.okt_8 = '4186	4435	4699	4978	5274	5588	5920	6272	6645	7040	7459	7902'.split()

        self.okt_1 = [float(i) for i in self.okt_1]
        self.okt_2 = [float(i) for i in self.okt_2]
        self.okt_3 = [float(i) for i in self.okt_3]
        self.okt_4 = [float(i) for i in self.okt_4]
        self.okt_5 = [float(i) for i in self.okt_5]
        self.okt_6 = [float(i) for i in self.okt_6]
        self.okt_7 = [float(i) for i in self.okt_7]
        self.okt_8 = [float(i) for i in self.okt_8]

        self.all_tonalties = ['C-dur', 'G-dur', 'D-dur', 'A-dur', 'E-dur', 'H-dur', 'Fis-dur', 'Cis-dur', 'Gis-dur',
                              'Dis-dur', 'Ais-dur', 'Es-dur', 'B-dur', 'F-dur', 'Des-dur', 'As-dur', 'Es-dur', 'B-dur',
                              'F-dur', 'C-dur', 'a-moll', 'e-moll', 'h-moll', 'fis-moll', 'cis-moll', 'gis-moll',
                              'dis-moll', 'ais-moll', 'es-moll', 'b-moll', 'f-moll', 'des-moll', 'as-moll', 'es-moll',
                              'b-moll', 'f-moll', 'c-moll', 'g-moll', 'd-moll', 'a-moll']

        # for i in range(len(notes)):
        #     print(f'''{"el" * (i != 0)}if abs(freq - {okt_3[i]}) < 5:
        #     print("{notes[i]}")''')


all_tonalties = '''C-dur
G-dur
D-dur
A-dur
E-dur
H-dur
Fis-dur
Cis-dur
Gis-dur
Dis-dur
Ais-dur
Es-dur
B-dur
F-dur
Des-dur
As-dur
Es-dur
B-dur
F-dur
C-dur
a-moll
e-moll
h-moll
fis-moll
cis-moll
gis-moll
dis-moll
ais-moll
es-moll
b-moll
f-moll
des-moll
as-moll
es-moll
b-moll
f-moll
c-moll
g-moll
d-moll
a-moll
'''.split()
print(all_tonalties)
