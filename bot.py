
import os
from pathlib import Path
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from stt import STT
from config import TOKEN, STIKER1_TOKEN,  STIKER2_TOKEN
from questions import  base_questions, epit_questions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import kb
from gigachat_answers import answer1,answer2,answer3, answer4

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
stt = STT()


global preprompt
global Biography
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    user_name = message.from_user.first_name
    message_text = f"Привет, {user_name}! Я бот *Олег*. Сгенерирую биографию любого человека, тебе достаточно ответить на пару вопросов!"
    await bot.send_sticker(message.chat.id, STIKER1_TOKEN)
    await message.answer(message_text, reply_markup=kb.reply_kb, parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == "📝 Генерация")
async def cmd_start(message: types.Message):
    await message.answer("Выберите (на клавиатуре)", reply_markup=kb.choose_kb)



"""Тут идет обработка сообщений"""
class BioForm(StatesGroup):
    answering_questions = State()
    editing_biography = State()
    answering_questions_epit = State()

@dp.message_handler(lambda message: message.text == "Биография")
async def process_bio_request(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("*Давайте ответим на несколько простых базовых вопросов📃*", reply_markup=kb.home_kb, parse_mode="Markdown")
    await BioForm.answering_questions.set()
    # Отправляем первый вопрос сразу после установки состояния
    if base_questions:  # Проверяем, что список вопросов не пуст
        await message.answer(base_questions[0], parse_mode="Markdown")

@dp.message_handler(state=BioForm.answering_questions)
async def answer_question(message: types.Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.finish()
        await message.answer("Возврат в главное меню", reply_markup=kb.reply_kb)
    else:
        global preprompt
        async with state.proxy() as data:
            if "answers" not in data:
                data["answers"] = []

            data["answers"].append(message.text)

            if len(data["answers"]) < len(base_questions):
                await message.answer(base_questions[len(data["answers"])], parse_mode="Markdown")
            else:
                await state.finish()
                PROMPT = "\n".join([f"{j}: {i}" for j, i in zip(base_questions, data["answers"])])
                await message.answer("⚙️⚙️⚙️*Обрабатываю*⚙️⚙️⚙️", parse_mode="Markdown")
                preprompt = answer1(PROMPT) #генерация предварительного промпта
                await bot.send_sticker(message.chat.id, STIKER2_TOKEN)
                await message.answer("*Отлично! Ваши ответы приняты.* Предлагаю вам в свободной форме (можно голосовым сообщением 🎙️) рассказать о данном человеке более подробно. Мне нужны подробности о его семье, образовании, карьере и достижениях, чтобы создать интересный и информативный текст. Если у вас есть эти данные, пожалуйста, предоставьте их мне для написания биографии." , parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == "Эпитафия")
async def process_epitaph_request(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("*Давайте ответим на несколько простых вопросов для эпитафии💬*", reply_markup=kb.home_kb, parse_mode="Markdown")
    await BioForm.answering_questions_epit.set()
    # Отправляем первый вопрос сразу после установки состояния
    if epit_questions:  # Проверяем, что список вопросов не пуст
        await message.answer(epit_questions[0], parse_mode="Markdown")

@dp.message_handler(state=BioForm.answering_questions_epit)
async def answer_epit_question(message: types.Message, state: FSMContext):
    global doublepromt
    async with state.proxy() as data:
        if "epit_answers" not in data:
            data["epit_answers"] = []

        data["epit_answers"].append(message.text)

        if len(data["epit_answers"]) < len(epit_questions):
            await message.answer(epit_questions[len(data["epit_answers"])], parse_mode="Markdown")
        else:
            await state.finish()
            PROMPT = "\n".join([f"{j}: {i}" for j, i in zip(epit_questions, data["epit_answers"])])
            await message.answer("⚙️⚙️⚙️*Обрабатываю*⚙️⚙️⚙️", parse_mode="Markdown")
            doublepromt = answer4(PROMPT) 
            await bot.send_sticker(message.chat.id, STIKER2_TOKEN)
            await message.answer( doublepromt, parse_mode="Markdown")


"""Кнопка назад"""
@dp.message_handler(lambda message: message.text == "В главное меню")
async def back_home(message: types.Message):
    await message.answer("Возврат в главное меню", reply_markup=kb.reply_kb)



"""Редактирование биографии"""


@dp.message_handler(lambda message: message.text == "Редактировать⚙️")
async def edit_biography(message: types.Message):
    await message.answer("Введите отредактированный текст биографии:", reply_markup=kb.home_kb)
    await BioForm.editing_biography.set()

# @dp.message_handler(state=BioForm.editing_biography)
# async def process_edited_biography(message: types.Message, state: FSMContext):
#     global Biography
#     edited_biography = message.text
#     Biography = edited_biography
#     async with state.proxy() as data:
#         biography_message_id = data["biography_message_id"]
#     await bot.edit_message_text(chat_id=message.chat.id, message_id=biography_message_id, text=edited_biography, reply_markup=kb.correct_kb)
#     await message.answer("Биография успешно отредактирована!")
#     await state.finish()



"""Регенерация биографии"""
@dp.message_handler(lambda message: message.text == "Регенерировать♻️")
async def redactor(message: types.Message):
    global Biography
    regen_bio = answer3(Biography)
    await message.answer("⚙️⚙️⚙️*Регенерирую*⚙️⚙️⚙️", parse_mode="Markdown")

    await message.answer(regen_bio, reply_markup=kb.home_kb, parse_mode="Markdown")


"""Здесь идет работа с распознаванием голосовых"""
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.DOCUMENT
])
async def voice_message_handler(message: types.Message):

    if message.content_type == types.ContentType.VOICE:
        file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")

    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено ✔️")
    await message.answer("⚙️⚙️⚙️*Генерирую*⚙️⚙️⚙️", parse_mode="Markdown")
    text = stt.audio_to_text(file_on_disk)
    os.remove(f"{file_id}.tmp")
    Biography = answer2(preprompt,text)
    await message.answer("*Итоговая биография*✔️ ️", parse_mode="Markdown")
    await message.answer(Biography, reply_markup=kb.correct_kb)









if __name__ == "__main__":
    # Start the bot
    print("Starting the bot")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
