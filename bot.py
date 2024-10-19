import logging
import json
import aiosqlite

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums.content_type import ContentType
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode

logging.basicConfig(level=logging.INFO)

bot = Bot("8116965156:AAGb9sdlIRqV2WbTJEETIyOSRPgYFAwM8HY")
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    photo_url = "https://www.upload.ee/image/17277134/photo1.jpg"
    
    # Добавляем пользователя в базу данных
    await add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    
    # Отправка приветственного сообщения с фото без кнопки
    await message.answer_photo(
        photo=photo_url,
        caption="Привет! 👋 Добро пожаловать в нашего бота, созданного для обучения в онлайн! Здесь вы сможете:\n\n"
                "1. Начать обучение 📚 — Откройте для себя увлекательные курсы и уроки по различным темам.\n"
                "2. Задать вопрос ❓ — Если у вас возникли вопросы по курсам или обучению, не стесняйтесь спрашивать!\n"
                "3. Посмотреть прогресс 📈 — Узнайте, как продвигается ваше обучение и какие задания еще предстоит выполнить.\n\n"
                "Нажмите на кнопку ниже, чтобы начать свое обучение!"
    )

async def add_user(user_id, username, first_name, last_name):
    try:
        async with aiosqlite.connect('bot_database.db') as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            await db.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")

@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def parse_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    await message.answer(f'<b>{data["title"]}</b>\n\n<code>{data["desc"]}</code>\n\n{data["text"]}', parse_mode=ParseMode.HTML)

async def setup_db():
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')
        await db.commit()

async def main():
    await setup_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
