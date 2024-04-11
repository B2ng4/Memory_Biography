
import os
from pathlib import Path
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from stt import STT
from config import TOKEN, STIKER_TOKEN
from questions import  base_questions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import kb
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
stt = STT()



@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):

    user_name = message.from_user.first_name
    message_text = f"Привет, {user_name}! Я бот Олег. Напишу биографию любого человека, тебе достаточно ответить на пару вопросов!"
    await bot.send_sticker(message.chat.id, STIKER_TOKEN)
    await message.answer(message_text, reply_markup=kb.reply_kb)


@dp.message_handler(lambda message: message.text == "📝 Генерация")
async def cmd_start(message: types.Message):
    await message.answer("Выберите (на клавиатуре)", reply_markup=kb.choose_kb)




"""Тут идет обработка сообщений"""
class BioForm(StatesGroup):
    answering_questions = State()

@dp.message_handler(lambda message: message.text == "Биография")
async def process_bio_request(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("Давайте ответим на несколько простых вопросов", reply_markup=kb.home_kb)
    await BioForm.answering_questions.set()

@dp.message_handler(state=BioForm.answering_questions)
async def answer_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if "answers" not in data:
            data["answers"] = []

        data["answers"].append(message.text)

        if len(data["answers"]) < len(base_questions):
            await message.answer(base_questions[len(data["answers"]) - 1]) 
        else:
            await message.answer("Ваша биография:\n" + "\n".join(data["answers"][1:])) ##############################Это можно удалить (делал для проверки) !!только эта строка
            await state.finish()
        PROMPT = "" #########################Это переменная принимает в себя ответы на вопрсы
        if len(data["answers"]) == len(base_questions):
            PROMPT = " ".join(data["answers"])












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
