from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import DatabaseHandler
import datetime
from sqlite3worker import Sqlite3Worker

TOKEN = '6434219032:AAEoJhhMFHctZkoJbLiV2KEdd8WHDmqF7kc'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

worker = Sqlite3Worker('database.db')
db = DatabaseHandler(worker)

events = db.setup()
events = db.get_appointments()


# Стартовая клавиатура
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Записаться'),
    KeyboardButton('Посмотреть списки на сегодняшнюю запись')
)

# Клавиатура для записи на определенное время
events = [f"Записаться с {i[2]} до {i[3]} в {i[1]}" for i in events]
events_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*events)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    username = message.from_user.username
    await message.reply("Привет, " + username + "! Я бот для записи на прием к врачу. Чтобы начать, нажмите на кнопку 'Записаться'.", reply_markup=start_keyboard)


@dp.message_handler(lambda message: message.text == "Записаться")
async def choose_time(message: types.Message):
    await message.answer("Выберите время:", reply_markup=events_keyboard)


@dp.message_handler(lambda message: message.text in events)
async def choose_time(message: types.Message):
    await message.answer("Введите ваше имя и фамилию: (например, Умаров Абдулазиз)))")


@dp.message_handler(state='*')
async def process_name(message: types.Message):
    name = message.text  # Здесь вы получаете текст сообщения пользователя
    print(name)
    db.add_student(current_time_slot, name, message.from_user.id, len(events[current_time_slot]) + 1)
    await message.answer(f"Спасибо, {name}, ваше имя и фамилия получены.")
    

# @dp.message_handler(lambda message: message.text == "Посмотреть списки на сегодняшнюю запись")
# async def show_lists(message: types.Message):
#     lists_message = ""
#     for time_slot, queue in events.items():
#         lists_message += f"{time_slot}: {len(queue)} человек(а) в очереди\n"
#     await message.reply(lists_message, reply_markup=start_keyboard)

@dp.message_handler(lambda message: message.text.startswith("Записаться с"))
async def ask_for_name(message: types.Message):
    time_slot = message.text.split("Записаться с ")[1]
    if time_slot in events:
        await message.answer("Введите ваше имя и фамилию:")
        global current_time_slot
        current_time_slot = time_slot

@dp.message_handler(lambda message: current_time_slot in message.text)
async def queue_up(message: types.Message):
    name = message.text.strip()
    queue_number = len(events[current_time_slot]) + 1
    events[current_time_slot].append(name)
    await message.reply(f"Вы успешно записались! Ваша очередь {queue_number}.", reply_markup=start_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
