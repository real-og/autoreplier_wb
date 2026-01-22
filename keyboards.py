from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
import buttons


def get_automod_kb(selected: List[int]):
    kb = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton(text='1️⃣✅' if 1 in selected else '1️⃣⛔️', callback_data='1')
    button_2 = InlineKeyboardButton(text='2️⃣✅' if 2 in selected else '2️⃣⛔️', callback_data='2')
    button_3 = InlineKeyboardButton(text='3️⃣✅' if 3 in selected else '3️⃣⛔️', callback_data='3')
    button_4 = InlineKeyboardButton(text='4️⃣✅' if 4 in selected else '4️⃣⛔️', callback_data='4')
    button_5 = InlineKeyboardButton(text='5️⃣✅' if 5 in selected else '5️⃣⛔️', callback_data='5')
    button_6 = InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')

    kb.row(button_1, button_2, button_3, button_4, button_5)
    kb.row(button_6)
    return kb

to_send_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Отправить ✉️', callback_data='sent')
button_2 = InlineKeyboardButton(text='🔁', callback_data='regenerate')
to_send_kb.row(button_1, button_2)

done_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Готово ✅', callback_data='done')
done_kb.row(button_1)

done_auto_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Готово ✅🤖', callback_data='done')
done_auto_kb.row(button_1)




cancel_kb = ReplyKeyboardMarkup([[buttons.cancel]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True)