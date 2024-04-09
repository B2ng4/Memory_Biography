import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from stt import STT
from config import TOKEN

bot = Bot(token=TOKEN)  # Bot object
dp = Dispatcher(bot)  # Dispatcher for the bot
stt = STT()

# Handler for /start and /help commands
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    # Create message text
    message_text = f"Привет, {user_name}! Я напишу биографию любого человека, тебе достаточно ответить на пару вопросов!"

    # Create inline buttons
    inline_kb = InlineKeyboardMarkup(row_width=1)
    button_1 = InlineKeyboardButton(text="📝 Написать биографию", callback_data="create")
    button_2 = InlineKeyboardButton(text="🔎 Помощь", callback_data="help")
    inline_kb.add(button_1, button_2)

    # Send message with buttons
    await message.reply(message_text, reply_markup=inline_kb)

# Handler for receiving voice, audio, and document messages
@dp.message_handler(content_types=[
    types.ContentType.VOICE,
    types.ContentType.AUDIO,
    types.ContentType.DOCUMENT
])
async def voice_message_handler(message: types.Message):
    """
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
