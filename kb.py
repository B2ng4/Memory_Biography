    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

"""Клава главного меню"""
reply_kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text="📝 Генерация")
button_2 = KeyboardButton(text="🔎 Помощь")
reply_kb.add(button_1, button_2)


"""Клава выбора Эпитафии"""
choose_epitaphy_kb = ReplyKeyboardMarkup(resize_keyboard=True)
#biography_bt = KeyboardButton(text="Биография")
epitaph_bt = KeyboardButton(text="Начать")
choose_epitaphy_kb.add(epitaph_bt)


"""Клава выбора Биографии"""
choose_bio_kb = ReplyKeyboardMarkup(resize_keyboard=True)
#biography_bt = KeyboardButton(text="Биография")
bio_bt = KeyboardButton(text="Биография")
choose_bio_kb.add(bio_bt)




"""Клава домой"""
home_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_bt = KeyboardButton(text="В главное меню")
home_kb.add(back_bt)


"""Клава исправления"""

correct_kb = ReplyKeyboardMarkup(resize_keyboard=True)
save_bt = KeyboardButton(text="Отправить🌐")
replace_bt = KeyboardButton(text="Редактировать⚙️")
redactor_bt = KeyboardButton(text="Регенерировать")
correct_kb.add(save_bt)
correct_kb.add(replace_bt)
correct_kb.add(redactor_bt)

"""Клавиатура сохранения"""


save_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_bt = KeyboardButton(text="В главное меню")
save_bt = KeyboardButton(text="Отправить🌐")

save_kb.add(save_bt)
save_kb.add(back_bt)


"""Кнопка для ссылки"""
url_bt = InlineKeyboardButton( text="Страница", url="https://mc.dev.rand.agency/page/79051330")
url_kb = InlineKeyboardMarkup().add(url_bt)