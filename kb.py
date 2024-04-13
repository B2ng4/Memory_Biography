    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Клава главного меню"""
reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text="📝 Генерация")
button_2 = KeyboardButton(text="🔎 Помощь")
reply_kb.add(button_1, button_2)


"""Клава выбора генерации"""
choose_kb = ReplyKeyboardMarkup(resize_keyboard=True)
biography_bt = KeyboardButton(text="Биография")
epitaph_bt = KeyboardButton(text="Эпитафия")
choose_kb.add(epitaph_bt, biography_bt)

"""Клава домой"""
home_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_bt = KeyboardButton(text="В главное меню")
home_kb.add(back_bt)


"""Клава исправления"""

correct_kb = ReplyKeyboardMarkup(resize_keyboard=True)
replace_bt = KeyboardButton(text="Редактировать⚙️")
redactor_bt = KeyboardButton(text="Регенерировать")
correct_kb.add(replace_bt, redactor_bt)

"""Клавиатура сохранения"""


save_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_bt = KeyboardButton(text="В главное меню")
save_bt = KeyboardButton(text="Сохранить")

save_kb.add(save_bt)
save_kb.add(back_bt)