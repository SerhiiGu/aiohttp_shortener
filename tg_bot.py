import asyncio
import string
import sys
import random
from db_utils import insert_data, get_user_links
import logging
from aiogram import Bot, Dispatcher, executor, types
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
API_TOKEN = config['DEFAULT']['API_TOKEN']

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\n A'm links shortener!")


@dp.message_handler(commands=['my_links', 'get_my_links'])
async def my_links(message: types.Message):
    links = await get_user_links(message.from_user.id)
    await message.reply('\n'.join(links))


@dp.message_handler()
async def echo(message: types.Message):
    link = message.text
    if link.startswith('http') or link.startswith('https'):
        characters = string.ascii_letters + string.digits
        new_link = ''.join(random.choice(characters) for i in range(6))
        await insert_data(link, new_link, message.from_user.id)
        await message.answer(f"http://127.0.0.1:8080/{new_link}")
    else:
        await message.answer("Wrong link!")


if __name__ == '__main__':
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    executor.start_polling(dp, skip_updates=True)
