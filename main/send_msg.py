from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions

bot = Bot(token="6075679825:AAGrgD6b9hybk9EoNue44k1ZPW8paFJCs5M")
dp = Dispatcher(bot)
async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)