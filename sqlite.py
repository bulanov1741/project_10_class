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
                      number_string INTEGER,
                      duration TEXT,
                      signature INTEGER,
                      width_monitor REAL
                  )
        ''')
        self.con.commit()
    def update(self, name, new_list):
        self.cur.execute(f"INSERT INTO {name} (ind, pos, number_string, duration, signature, width_monitor) VALUES (?, ?, ?, ?, ?, ?)", new_list)
        self.con.commit()

    def select(self, name):
        result = list(self.cur.execute(f"SELECT * FROM {name}").fetchall())
        return result

    def delete(self, name, ind, pos, number_string):
        self.cur.execute(f"DELETE FROM {name} WHERE ind=? AND pos=? AND number_string=?", (ind, pos, number_string))
        self.con.commit()
