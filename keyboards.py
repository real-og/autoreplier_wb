from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

to_send_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Отправить ✉️', callback_data='sent')
to_send_kb.row(button_1)

done_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Готово ✅', callback_data='done')
done_kb.row(button_1)


