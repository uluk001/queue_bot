import datetime
from sqlite3worker import Sqlite3Worker
from db import DatabaseHandler


worker = Sqlite3Worker('database.db')
db = DatabaseHandler(worker)

events = db.setup()
events = db.get_appointments()


# Стартовая клавиатура

# Клавиатура для записи на определенное время
events = [f"Записаться с {i[2]} до {i[3]} в {i[1]}" for i in events]

print(events)