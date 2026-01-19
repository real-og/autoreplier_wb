from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import buttons

to_send_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Отправить ✉️', callback_data='sent')
to_send_kb.row(button_1)

done_kb = InlineKeyboardMarkup()
button_1 = InlineKeyboardButton(text='Готово ✅', callback_data='done')
done_kb.row(button_1)




cancel_kb = ReplyKeyboardMarkup([[buttons.cancel]],
                                     resize_keyboard=True,
                                     one_time_keyboard=True)