
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
from BD import DB_bio
from MemoryAPI import upload_bio

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
stt = STT()

DB = DB_bio("biography.db")


"""Сделано на скорую руку, не судите!"""
global preprompt
global Biography
global gen
global doublepromt
doublepromt = ""
gen = []


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):

    user_name = message.from_user.first_name
    message_text = f"Привет, {user_name}! Я бот *Олег*. Сгенерирую биографию и эпитафию любого человека, тебе достаточно ответить на пару вопросов!"
    await bot.send_sticker(message.chat.id, STIKER1_TOKEN)
    await message.answer(message_text, reply_markup=kb.reply_kb, parse_mode="Markdown")


@dp.message_handler(lambda message: message.text == "📝 Генерация")
async def cmd_start(message: types.Message):
    await message.answer("Выберите (на клавиатуре)", reply_markup=kb.choose_epitaphy_kb)



"""Тут идет обработка сообщений"""
class BioForm(StatesGroup):
    answering_questions = State()
    editing_biography = State()
    answering_questions_epit = State()
    saving_biography = State()

@dp.message_handler(lambda message: message.text == "Биография")
async def process_bio_request(message: types.Message, state: FSMContext):
    await message.answer("*Давайте ответим на несколько простых базовых вопросов📃*", reply_markup=kb.home_kb, parse_mode="Markdown")
    await BioForm.answering_questions.set()
    # Отправляем первый вопрос сразу после установки состояния
    if base_questions:  # Проверяем, что список вопросов не пуст
        await message.answer(base_questions[0], parse_mode="Markdown")


"""
Здесь происходит сохранения ответов для дальнейшей обработки
"""
async def get_answers(state: FSMContext):
    user_data = await state.get_data()
    return user_data.get("answers", [])


@dp.message_handler(state=BioForm.answering_questions)
async def answer_question(message: types.Message, state: FSMContext):
    if message.text == "В главное меню":
        await state.finish()
        await message.answer("Возврат в главное меню", reply_markup=kb.reply_kb)
    else:
        answers = await get_answers(state)
        answers.append(message.text)
        gen.append(message.text)
        await state.update_data(answers=answers)

        if len(answers) < len(base_questions):
            await message.answer(base_questions[len(answers)], parse_mode="Markdown")
        else:
            global  preprompt
            await state.finish()
            PROMPT = "\n".join([f"{j}: {i}" for j, i in zip(base_questions, answers)])
            await message.answer("⚙️⚙️⚙️*Обрабатываю*⚙️⚙️⚙️", parse_mode="Markdown")
            preprompt = answer1(PROMPT)
            await bot.send_sticker(message.chat.id, STIKER2_TOKEN)
            await message.answer("*Отлично! Ваши ответы приняты.* Предлагаю вам в свободной форме (можно голосовым сообщением 🎙️) рассказать о данном человеке более подробно. Мне нужны подробности о его семье, образовании, карьере и достижениях, чтобы создать интересный и информативный текст. Если у вас есть эти данные, пожалуйста, предоставьте их мне для написания биографии.", parse_mode="Markdown")


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
            #doublepromt = "Здесь будет эпитафия"
            user = message.from_user.first_name


            await bot.send_sticker(message.chat.id, STIKER2_TOKEN)
            await message.answer(doublepromt, parse_mode="Markdown", reply_markup=kb.choose_bio_kb)





"""Кнопка назад"""
@dp.message_handler(lambda message: message.text == "В главное меню")
async def back_home(message: types.Message):
    await message.answer("Возврат в главное меню", reply_markup=kb.reply_kb)



"""Здесь идет работа с распознаванием голосовых"""
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.DOCUMENT,

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
        #Biography = "Родился выдающийся советский композитор Дмитрий Шостакович в Санкт-Петербурге в доме"
        await message.answer("*Итоговая биография*✔️ ️", parse_mode="Markdown")
        await message.answer(Biography, reply_markup=kb.correct_kb)

    """Регенерация биографии"""
    @dp.message_handler(lambda message: message.text == "Регенерировать")
    async def redactor(message: types.Message):
        await message.answer("⚙️⚙️⚙️*Регенерирую*⚙️⚙️⚙️", parse_mode="Markdown")
        regen_bio = answer3(Biography)
        await message.answer(regen_bio, reply_markup=kb.home_kb, parse_mode="Markdown")

    """Редактирование биографии"""
    @dp.message_handler(lambda message: message.text == "Редактировать⚙️")
    async def edit_biography(message: types.Message, state: FSMContext):
        await message.answer("Введите отредактированный текст биографии:", reply_markup=kb.home_kb)
        await BioForm.editing_biography.set()

    @dp.message_handler(state=BioForm.editing_biography)
    async def process_edited_biography(message: types.Message, state: FSMContext):
        # Сохраняем отредактированную биографию в контексте состояния
        await state.update_data(edited_biography=message.text)
        await message.answer("Биография успешно отредактирована!")
        await message.answer(message.text)
        await message.answer("Нажмите кнопку 'Отправить' для сохранения биографии", reply_markup=kb.save_kb)
        await BioForm.saving_biography.set()

    @dp.message_handler(state=BioForm.saving_biography, text="Отправить🌐")
    async def save(message: types.Message, state: FSMContext):
        # Извлекаем отредактированную биографию из контекста состояния
        user_data = await state.get_data()
        edited_biography = user_data.get('edited_biography')
        user = message.from_user.first_name

        if upload_bio(gen[0], gen[1], gen[2], gen[3], gen[4], gen[5], gen[6], gen[7], edited_biography, doublepromt, user):
            await message.answer("Биография успешно отправлена!", reply_markup=kb.home_kb)

        await state.finish()



if __name__ == "__main__":
    # Start the bot
    print("Starting the bot")
    try:
        executor.start_polling(dp, skip_updates=True)
    except (KeyboardInterrupt, SystemExit):
        pass
