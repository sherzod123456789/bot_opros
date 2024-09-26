from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

callback = CallbackData('mark', 'action')

key1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Пройти опрос👇', callback_data='mark:reg')
        ],
        [
            InlineKeyboardButton(text='Создать свой опрос 📋', callback_data='mark:create_poll')
        ]
    ]
)

key2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Найти свой опрос по Номеру 🔍', callback_data='mark:find_poll')
        ]
    ]
)
