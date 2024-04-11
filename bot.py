
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from stt import STT
from config import TOKEN, STIKER_TOKEN
from questions import  base_questions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
stt = STT()




@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    # Create message text
    message_text = f"Привет, {user_name}! Я бот Олег. Напишу биографию любого человека, тебе достаточно ответить на пару вопросов!"

    # Create inline buttons
    reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = KeyboardButton(text="📝 Написать биографию")
    button_2 = KeyboardButton(text="🔎 Помощь")
    reply_kb.add(button_1, button_2)

    await bot.send_sticker(message.chat.id, STIKER_TOKEN)  # This line should be awaited
    await message.answer(message_text, reply_markup=reply_kb)

@dp.message_handler(lambda message: message.text == "📝 Написать биографию")
async def process_bio_request(message: types.Message):

    await message.answer("Давайте ответим на несколько простых вопросов")
    for question in base_questions:
        await message.answer(question)  # Предполагается, что base_questions - это список вопросов













"""Здесь идет работа с распознаванием голосовых"""
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.DOCUMENT
])
async def voice_message_handler(message: types.Message):
    """
    types.ContentType.AUDIO,
    Handler for receiving voice, audio, and document messages.
    """
    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")

    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено")

    text = stt.audio_to_text(file_on_disk)
    os.remove(f"{file_id}.tmp")
    await message.answer(text)

if __name__ == "__main__":
    # Start the bot
    print("Starting the bot")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
