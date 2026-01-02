from aiogram import types
from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import keyboards as kb
from config import BOT_TOKEN, GROUP_ID, WB_TOKEN_IP, WB_TOKEN_OOO
import wb_api
import redis_db



logging.basicConfig(level=logging.WARNING)


storage = MemoryStorage()


bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer('pong')


@dp.callback_query_handler(state='*')
async def send_series(callback: types.CallbackQuery):
    tapped = callback.data
    message_id = callback.message.message_id
    print(tapped)
    print(message_id)


    all = redis_db.get_all_redis()
    item_to_ans = None
    for item in all:
        if item['reply_message_id'] == message_id:
            item_to_ans = item
            break
    
    if item_to_ans:
        if item_to_ans['account'] == 'OOO':
            auth = WB_TOKEN_OOO
        elif item_to_ans['account'] == 'IP':
            auth = WB_TOKEN_IP
        wb_api.answer_feedback_mock(auth, item_to_ans['feedback_id'], callback.message.text)
        try:
            await bot.edit_message_reply_markup(GROUP_ID, message_id, reply_markup=kb.done_kb)
        except Exception as e:
            print('Ошибка при изменении кнопки')
    else:
        await bot.answer_callback_query(callback.id, text='Ошибка при поиске отзыва')

    
    await bot.answer_callback_query(callback.id)



if __name__ == '__main__':
    print("Starting autoreplier tg bot")
    executor.start_polling(dp, skip_updates=True)