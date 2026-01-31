import smtplib
import sqlite3
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib as smtp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from sqlite import DataBase


class ProfileScreen(Screen):
    def __init__(self):
        super().__init__()
        self.theory_box = ProfileBox()
        self.add_widget(self.theory_box)


class ProfileBox(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Подключение к бд
        self.con = sqlite3.connect("db.db")
        self.cur = self.con.cursor()
        self.cur.execute(f'''
                          CREATE TABLE IF NOT EXISTS profile (
                              email TEXT,
                              first_name TEXT,
                              name TEXT
                          )
                ''')
        self.con.commit()

        self.cols = 2
        self.rows = 6
        # Данные
        database = DataBase()
        self.email = database.select_email()
        self.first_name = database.select_first_name()
        self.name = database.select_first_name()
        # Почта
        self.name_label = Label(
            text="Почта",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.email_input = TextInput(hint_text="Введите email", multiline=False, size_hint=(1, .8), text=self.email)
        self.add_widget(self.name_label)
        self.add_widget(self.email_input)
        # Пароль
        self.name_label = Label(
            text="Фамилия",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.first_name_input = TextInput(hint_text="Введите фамилию", multiline=False, size_hint=(1, .8),
                                          text=self.first_name)
        self.add_widget(self.name_label)
        self.add_widget(self.first_name_input)
        # Имя
        self.name_label = Label(
            text="Имя",
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle'
        )
        self.name_input = TextInput(hint_text="Введите имя", multiline=False, size_hint=(1, .8), text=self.name)
        self.add_widget(self.name_label)
        self.add_widget(self.name_input)
        # Сохранение
        self.button_save = Button(text="Сохранить")
        self.button_cancel = Button(text="Отмена")
        self.add_widget(self.button_cancel)
        self.add_widget(self.button_save)
        self.button_save.bind(on_press=self.save)
        self.button_cancel.bind(on_press=self.cancel)

    def save(self, instance):
        self.cur.execute(f"INSERT INTO profile (email, first_name, name) VALUES (?, ?, ?)",
                         (self.email_input.text, self.first_name_input.text, self.name_input.text))
        self.con.commit()
        self.email, self.first_name, self.name = self.email_input.text, self.first_name_input.text, self.name_input.text

        if self.email_input.text != '':
            recipient = self.email_input.text
            topic = 'Смена почты'
            sender = 'notebasic@yandex.ru'
            sender_password = 'kvqgsnmafyrjuvus'
            mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
            mail_lib.login(sender, sender_password)
            msg = EmailMessage()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = topic
            file_name = 'templates/changing_email.txt'
            with open(file_name, "r", encoding='utf-8') as file:
                msg.set_content(file.read())
            mail_lib.send_message(msg)
            mail_lib.quit()
            self.show_notification("Данные обновлены")

    def show_notification(self, text):
        popup = Popup(title='Уведомление', content=Label(text=text), size_hint=(None, None), size=(400, 400))
        popup.open()

    def cancel(self, instance):
        self.email_input._set_text(self.email)
        self.first_name_input._set_text(self.first_name)
        self.name_input._set_text(self.name)
