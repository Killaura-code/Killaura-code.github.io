import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums.content_type import ContentType
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode

logging.basicConfig(level=logging.INFO)

bot = Bot("TOKEN")
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    webAppInfo = types.WebAppInfo(url="URL VASH")
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text='Отправить данные', web_app=webAppInfo))
    
    await message.answer(text="Привет! 👋 Добро пожаловать в нашего бота, созданного для обучения в онлайн! Здесь вы сможете:\n\n"
                           "1. Начать обучение 📚 — Откройте для себя увлекательные курсы и уроки по различным темам.\n"
                           "2. Задать вопрос ❓ — Если у вас возникли вопросы по курсам или обучению, не стесняйтесь спрашивать!\n"
                           "3. Посмотреть прогресс 📈 — Узнайте, как продвигается ваше обучение и какие задания еще предстоит выполнить.\n\n"
                           "Нажмите на кнопку ниже, чтобы начать свое обучение!", 
                           reply_markup=builder.as_markup())

@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def parse_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    await message.answer(f'<b>{data["title"]}</b>\n\n<code>{data["desc"]}</code>\n\n{data["text"]}', parse_mode=ParseMode.HTML)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
