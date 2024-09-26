from asyncio import new_event_loop
from aiogram import Bot, Dispatcher, executor

Bot_token = 'your_token_of_bot'

loop = new_event_loop()
bot = Bot(token=Bot_token, parse_mode='HTML')
dp = Dispatcher(bot=bot, loop=loop)

if __name__ == '__main__':
    from headers import dp
    executor.start_polling(dp)
