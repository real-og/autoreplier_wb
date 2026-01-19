from aiogram import types
from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import logging
from states import State
import keyboards as kb
from config import BOT_TOKEN, GROUP_ID, WB_TOKEN_IP, WB_TOKEN_OOO
import wb_api
import redis_db
import settings
import texts
import buttons
import gpt_generator


logging.basicConfig(level=logging.WARNING)


storage = MemoryStorage()


bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer('pong')
    print(message)


@dp.message_handler(commands=['get_settings'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(settings.INSTRUCTIONS)


@dp.message_handler(commands=['set_settings'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(settings.INSTRUCTIONS)
    await message.answer(texts.change_instructions, reply_markup=kb.cancel_kb)
    await State.changing_instructions.set()

@dp.message_handler(state=State.changing_instructions)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text.lower().strip() == buttons.cancel.lower().strip():
        await message.answer(texts.back_to_menu, reply_markup=ReplyKeyboardRemove())
    elif message.text:
        settings.INSTRUCTIONS = message.text
        await message.answer(texts.success_instruction_change)
        await message.answer(texts.back_to_menu, reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)

    
@dp.message_handler(commands=['test'], state="*")
async def send_welcome(message: types.Message):
    feedback_to_test = message.get_args()
    answer = gpt_generator.get_reply(feedback_to_test)
    await message.answer(answer)
    

@dp.message_handler(commands=['logs'], state="*")
async def send_welcome(message: types.Message):
    await message.answer_document(types.InputFile("log.txt"))

@dp.message_handler(commands=['help'], state="*")
async def send_welcome(message: types.Message):
    await message.answer('Инструкция скоро')
    


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
        wb_api.answer_feedback___(auth, item_to_ans['feedback_id'], callback.message.text)
        try:
            await bot.edit_message_reply_markup(GROUP_ID, message_id, reply_markup=kb.done_kb)
        except Exception as e:
            print('Ошибка при изменении кнопки')
    else:
        await bot.answer_callback_query(callback.id, text='Ошибка при поиске отзыва')

    
    await bot.answer_callback_query(callback.id)

async def on_startup(_):
    await bot.set_my_commands([
        types.BotCommand("start", "Запуск"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("logs", "Логи"),
        types.BotCommand("get_settings", "Посмотреть настройки"),
        types.BotCommand("set_settings", "Установить настройки"),
    ])

if __name__ == '__main__':
    print("Starting autoreplier tg bot")
    executor.start_polling(dp, skip_updates=True)