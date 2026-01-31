import sqlite3


class DataBase():
    def __init__(self):
        super().__init__()

        self.con = sqlite3.connect("db.db")  # Подключаем базу данных
        self.cur = self.con.cursor()

        self.con.commit()  # Применяем изменения

    def create(self, name):
        self.cur.execute(f'''
                  CREATE TABLE IF NOT EXISTS {name} (
                      ind INTEGER,
                      pos REAL,
                      duration TEXT,
                      signature INTEGER
                  )
        ''')
        self.con.commit()

    def update(self, name, new_list):
        self.cur.execute(f"INSERT INTO {name} (ind, pos, duration, signature) VALUES (?, ?, ?, ?)", new_list)
        self.con.commit()

    def update_sign(self, name, signature, pos):
        self.cur.execute(f"UPDATE {name} SET signature = ? WHERE pos = ?", (signature, pos))
        self.con.commit()

    def select(self, name):
        result = list(self.cur.execute(f"SELECT * FROM {name}").fetchall())
        return result

    def delete(self, name, ind, pos):
        self.cur.execute(f"DELETE FROM {name} WHERE ind=? AND pos=?", (ind, pos))
        self.con.commit()

    def select_id_database(self):
        return self.cur.execute(f"SELECT id FROM saved_database WHERE now_open = 1").fetchone()[0]

    def select_author(self, k=0):
        if k == 0:
            try:
                return ' '.join(list(self.cur.execute(f"SELECT first_name, name FROM profile").fetchall()[-1]))
            except Exception as e:
                return ''
        else:
            return self.cur.execute(f"SELECT author FROM saved_database WHERE now_open = 1").fetchone()[0]

    def select_email(self):
        try:
            return self.cur.execute(f"SELECT email FROM profile").fetchall()[-1][0]
        except Exception as e:
            return ''

    def select_name(self):
        try:
            return self.cur.execute(f"SELECT name FROM profile").fetchall()[-1][0]
        except Exception as e:
            return ''

    def select_first_name(self):
        try:
            return self.cur.execute(f"SELECT first_name FROM profile").fetchall()[-1][0]
        except Exception as e:
            return ''

    def select_title(self):
        return self.cur.execute(f"SELECT name FROM saved_database WHERE now_open = 1").fetchone()[0]

