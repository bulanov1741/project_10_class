import smtplib
import sqlite3
from datetime import time, datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput

from const import Const
from sqlite import DataBase


class SavedDatabaseScreen(Screen):
    def __init__(self):
        super().__init__()
        self.layout = SavedDatabaseLayout()
        self.add_widget(self.layout)

class SavedDatabaseLayout(FloatLayout):
    def __init__(self):
        super().__init__()
        self.add_note_page = Button(text='Добавить', pos_hint={'x': 0, 'top': 1}, size_hint=(0.25, 0.1))
        self.add_note_page.bind(on_press=self.adding_note_page)
        self.spinner = Spinner(values=["По порядку", "По названию", "По автору"], text="Сортировка")
        self.spinner.size_hint = (0.75, 0.1)
        self.spinner.pos_hint = {'x': 0.25, 'top': 1}
        self.spinner.bind(text=self.on_spinner_select)
        self.saved_db_box = SavedDatabaseView()
        self.saved_db_box.pos_hint = {'x': 0, 'top': 0.9}
        self.saved_db_box.size_hint = (1, 0.9)
        self.add_widget(self.add_note_page)
        self.add_widget(self.spinner)
        self.add_widget(self.saved_db_box)

        self.bind(size=self.update_size, pos=self.update_size)

    def update_size(self, instance, value):
        self.saved_db_box.layout.height = self.height / 10 * len(self.saved_db_box.saved_db_list)



    def adding_note_page(self, instance):
        self.saved_db_box.adding_note_page()

    def on_spinner_select(self, instance, value):
        self.saved_db_box.sorting_num = ["По порядку", "По названию", "По автору"].index(value)
        self.saved_db_box.sorting()


class SavedDatabaseView(ScrollView):
    def __init__(self):
        super().__init__()
        self.layout = GridLayout(cols=6, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        self.con = sqlite3.connect("db.db")
        self.cur = self.con.cursor()
        self.cur.execute(f'''
                                  CREATE TABLE IF NOT EXISTS saved_database (
                                      id INTEGER PRIMARY KEY,
                                      name TEXT,
                                      author TEXT,
                                      time_created TEXT,
                                      now_open INTEGER
                                  )
                        ''')

        self.database = DataBase()
        self.author = self.database.select_author()

        if list(self.cur.execute(f'SELECT COUNT(*) FROM saved_database').fetchall()) == [(0,)]:
            self.cur.execute(
                f"INSERT INTO saved_database (id, name, author, time_created, now_open) VALUES (?, ?, ?, ?, ?)",
                [1, "Новый лист", self.author, datetime.now().strftime("%H:%M:%S|%d.%m.%Y"), 1])
        self.con.commit()
        self.saved_db_list = list(self.cur.execute(f"SELECT * FROM saved_database").fetchall())

        self.sorting_num = 0

        for i in self.saved_db_list:
            name_database = TextInput(
            text=i[1],
            halign='center'
            )
            author = Label(
            text=i[2]
            )
            time_created = Label(
            text=i[3]
            )
            save = Button(text="Сохранить")
            delete = Button(text="Удалить")
            choose = Button(text="Выбрать")
            self.layout.add_widget(name_database)
            self.layout.add_widget(author)
            self.layout.add_widget(time_created)
            self.layout.add_widget(save)
            self.layout.add_widget(delete)
            self.layout.add_widget(choose)

            name_database.bind(on_text_validate=partial(self.saving_new_title, id_database=i[0], name=name_database))
            save.bind(on_press=partial(self.saving_new_title, id_database=i[0], name=name_database))
            delete.bind(on_press=partial(self.deleting_sheet_music, id_database=i[0]))
            choose.bind(on_press=partial(self.changing_sheet_music, id_database=i[0]))

        self.size_hint = (1, 1)
        self.add_widget(self.layout)


    def saving_new_title(self, instance, id_database, name):
        self.cur.execute(f'''UPDATE saved_database
            SET name = ?
            WHERE id = ?''', (name.text, id_database))
        self.con.commit()

    def deleting_sheet_music(self, instance, id_database):
        if self.cur.execute(f"SELECT now_open FROM saved_database WHERE id = ?",  (id_database,)).fetchone()[0] == 0:
            self.cur.execute(f"DELETE FROM saved_database WHERE id = ?", (id_database,))
            self.cur.execute(f"DROP TABLE IF EXISTS notepage_treble_{id_database}")
            self.cur.execute(f"DROP TABLE IF EXISTS notepage_bass_{id_database}")
            self.con.commit()
            self.saved_db_list = list(self.cur.execute(f"SELECT * FROM saved_database").fetchall())
            self.layout.height = self.height / 10 * len(self.saved_db_list)
            self.sorting()


    def changing_sheet_music(self, instance, id_database):
        self.cur.execute(f'''UPDATE saved_database
    SET now_open = ?
    WHERE now_open = ?''', (0, 1))
        self.con.commit()
        self.cur.execute(f'''UPDATE saved_database
            SET now_open = ?
            WHERE id =?''', (1, id_database))
        self.con.commit()


    def adding_note_page(self):
        name_id = len([i[0] for i in list(self.cur.execute('SELECT ID FROM saved_database WHERE name LIKE "Новый лист%"').fetchall())])
        max_id = max([i[0] for i in list(self.cur.execute('SELECT ID FROM saved_database').fetchall())])
        self.cur.execute(
            f"INSERT INTO saved_database (id, name, author, time_created, now_open) VALUES (?, ?, ?, ?, ?)",
            [max_id + 1, f"Новый лист({name_id})",
             self.author,
             datetime.now().strftime("%H:%M:%S|%d.%m.%Y"), 0])
        self.con.commit()
        self.saved_db_list = list(self.cur.execute(f"SELECT * FROM saved_database").fetchall())
        self.layout.height = self.height / 10 * len(self.saved_db_list)
        self.sorting()

    def sorting(self):
        self.layout.clear_widgets()
        self.saved_db_list = list(self.cur.execute(f"SELECT * FROM saved_database").fetchall())
        for i in sorted(self.saved_db_list, key=lambda x: x[self.sorting_num]):
            name_database = TextInput(
                text=i[1],
                halign='center'
            )
            author = Label(
                text=i[2]
            )
            time_created = Label(
                text=i[3]
            )
            save = Button(text="Сохранить")
            delete = Button(text="Удалить")
            choose = Button(text="Выбрать")
            self.layout.add_widget(name_database)
            self.layout.add_widget(author)
            self.layout.add_widget(time_created)
            self.layout.add_widget(save)
            self.layout.add_widget(delete)
            self.layout.add_widget(choose)

            name_database.bind(on_text_validate=partial(self.saving_new_title, id_database=i[0], name=name_database))
            save.bind(on_press=partial(self.saving_new_title, id_database=i[0], name=name_database))
            delete.bind(on_press=partial(self.deleting_sheet_music, id_database=i[0]))
            choose.bind(on_press=partial(self.changing_sheet_music, id_database=i[0]))


    def show_notification(self, text):
        popup = Popup(title='Уведомление', content=Label(text=text), size_hint=(None, None), size=(400, 400))
        popup.open()


