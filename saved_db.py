import sqlite3

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView


class SavedDatabaseScreen(Screen):
    def __init__(self):
        super().__init__()
        self.saved_db_box = SavedDatabaseView()
        self.add_widget(self.saved_db_box)

class SavedDatabaseView(ScrollView):
    def __init__(self):
        super().__init__()
        layout = GridLayout(cols=2, size_hint_y=None)
        # Устанавливаем высоту GridLayout динамически
        layout.bind(minimum_height=layout.setter('height'))

        self.con = sqlite3.connect("db.db")
        self.cur = self.con.cursor()
        self.cur.execute(f'''
                                  CREATE TABLE IF NOT EXISTS saved_database (
                                      id INTEGER PRIMARY KEY,
                                      name TEXT,
                                      time_created TEXT,
                                      time_changed TEXT
                                  )
                        ''')
        self.con.commit()
        self.saved_db_list = list(self.cur.execute(f"SELECT * FROM saved_database").fetchall())

        for i in self.saved_db_list:
            name_database = Label(
            text=i[1],
            color=(0, 0, 0, 1),  # синий цвет
            halign='center',
            valign='middle'
            )
            b_r = Button(text=f'Урок {i+1}', size_hint_y=None, height=40)
            layout.add_widget(name_database)
            layout.add_widget(b_r)

        self.size_hint = (1, 1)
        self.add_widget(layout)
