from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, PollAnswer
from main import dp, bot
from keyboards import key1, key2, callback
import sqlite3


# Функция для создания таблиц
def create_tables():
    with sqlite3.connect('oprosnik.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL UNIQUE,
                interests TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS polls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                FOREIGN KEY(owner_id) REFERENCES users(user_id)
            )
        ''')
        connect.commit()


# Создайте таблицы при запуске скрипта
create_tables()


@dp.message_handler(Command('start'))
async def start(message: Message):
    with sqlite3.connect('oprosnik.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (name, user_id) VALUES (?, ?)
        ''', [message.chat.first_name, message.chat.id])
        connect.commit()
    await bot.send_message(chat_id=message.chat.id, text='Привет', reply_markup=key1)


@dp.callback_query_handler(callback.filter(action='reg'))
async def Registration(call: CallbackQuery):
    await call.answer(cache_time=10)
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question='Какие темы вам интересны?',
        options=[
            'Программирование 💻',
            'Путешествие 🚢',
            'Новости и СМИ 🆕',
            'Маркетинг и реклама 🛒',
            'Технологии 📱',
            'Юмор и развлечения 🤣',
            'Блоги 🎥',
            'Бизнес и стартапы 👨‍💼',
            'Крипто 📈',
            'Экономика и финансы 💲',
        ],
        is_anonymous=True,
        allows_multiple_answers=True
    )


@dp.poll_answer_handler()
async def handle_poll_answer(poll: PollAnswer):
    interests = str(poll.option_ids)
    user_id = poll.user.id
    with sqlite3.connect('oprosnik.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''
            UPDATE users SET interests = ? WHERE user_id = ?
        ''', [interests, user_id])
        connect.commit()
    await bot.send_message(user_id, 'DONE!!!', reply_markup=key2)


@dp.message_handler(Command('update'))
async def update(message: Message):
    with sqlite3.connect('oprosnik.db') as connect:
        cursor = connect.cursor()
        cursor.execute('''
            SELECT interests FROM users WHERE user_id = ?
        ''', [message.chat.id])
        database = cursor.fetchone()
        interests = database[0] if database else ''

    choosed = {
        '0': 'Программирование 💻',
        '1': 'Путешествие 🚢',
        '2': 'Новости и СМИ 🆕',
        '3': 'Маркетинг и реклама 🛒',
        '4': 'Технологии 📱',
        '5': 'Юмор и развлечения 🤣',
        '6': 'Блоги 🎥',
        '7': 'Бизнес и стартапы 👨‍💼',
        '8': 'Крипто 📈',
        '9': 'Экономика и финансы 💲',
    }

    # Преобразование строки интересов в список
    interests_list = interests.split(',') if interests else  []
    selected_interests = [choosed[i] for i in interests_list if i in choosed]
    interests_text = ', '.join(selected_interests) if selected_interests else 'Нет выбранных интересов'

    # Отправка сообщения с текущими выбранными интересами
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Твои текущие интересы:\n{interests_text}\n\nОбнови свои интересы, выбрав новые темы:'
    )

    # Отправка опроса с текущими выбранными интересами
    await bot.send_poll(
        chat_id=message.chat.id,
        question='Какие темы вам интересны?',
        options=[
            'Программирование 💻',
            'Путешествие 🚢',
            'Новости и СМИ 🆕',
            'Маркетинг и реклама 🛒',
            'Технологии 📱',
            'Юмор и развлечения 🤣',
            'Блоги 🎥',
            'Бизнес и стартапы 👨‍💼',
            'Крипто 📈',
            'Экономика и финансы 💲',
        ],
        is_anonymous=True,
        allows_multiple_answers=True
    )


# @dp.message_handler(Command('create_poll'))
# async def create_poll(message: Message):
#     # Проверка, что команда содержит правильное количество аргументов
#     try:
#         _, question, *options = message.text.split('\n')
#         if len(options) < 2:
#             await bot.send_message(message.chat.id, 'Укажите хотя бы два варианта ответа.')
#             return
#     except ValueError:
#         await bot.send_message(message.chat.id,
#                                'Некорректный формат команды. Используйте /create_poll <вопрос>\n<вариант1>\n<вариант2>\n...')
#         return
#
#     # Сохранение опроса в базу данных
#     with sqlite3.connect('oprosnik.db') as connect:
#         cursor = connect.cursor()
#         cursor.execute('''
#             INSERT INTO polls (owner_id, question, options) VALUES (?, ?, ?)
#         ''', [message.chat.id, question, '\n'.join(options)])
#         connect.commit()
#         poll_id = cursor.lastrowid
#
#     await bot.send_message(message.chat.id, f'Опрос создан. ID опроса: {poll_id}')
#
#
# @dp.message_handler(Command('get_poll'))
# async def get_poll(message: Message):
#     try:
#         _, poll_id = message.text.split()
#         poll_id = int(poll_id)
#     except ValueError:
#         await bot.send_message(message.chat.id, 'Укажите корректный ID опроса.')
#         return
#
#     with sqlite3.connect('oprosnik.db') as connect:
#         cursor = connect.cursor()
#         cursor.execute('''
#             SELECT question, options FROM polls WHERE id = ?
#         ''', [poll_id])
#         poll = cursor.fetchone()
#
#     if poll:
#         question, options = poll
#         options_list = options.split('\n')
#         await bot.send_poll(
#             chat_id=message.chat.id,
#             question=question,
#             options=options_list,
#             is_anonymous=False
#         )
#     else:
#         await bot.send_message(message.chat.id, 'Опрос не найден.')
