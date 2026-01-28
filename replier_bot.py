from aiogram import types
from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
import traceback
import logging

from states import State
import keyboards as kb
from config import BOT_TOKEN, GROUP_ID, WB_TOKEN_IP, WB_TOKEN_OOO, PROXY, GPT_KEY
import wb_api
import redis_db
import settings
import texts
import buttons
import gpt_generator
import diagnostics
import datetime


logging.basicConfig(level=logging.WARNING)


storage = MemoryStorage()


bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(texts.back_to_menu)
    print(message)


@dp.message_handler(commands=['diagnostics'], state="*")
async def send_welcome(message: types.Message):
    await message.answer(texts.diagnos_wait)
    proxy_check = diagnostics.check_proxy(PROXY)
    openai_check = diagnostics.check_openai_via_proxy(PROXY, GPT_KEY)
    wb_ooo_check = diagnostics.check_wb(WB_TOKEN_OOO)
    wb_ip_check = diagnostics.check_wb(WB_TOKEN_IP)
    await message.answer(texts.diagnos_result(proxy_check, openai_check, [wb_ooo_check, wb_ip_check]))

    


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
    try:
        answer = gpt_generator.get_reply(feedback_to_test)
    except Exception as e:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('EXCEPTION /test from the bot')
            print(ts)
            print(traceback.format_exc())
            await message.answer(texts.error_alert)
    await message.answer(answer)


@dp.message_handler(commands=['set_automod'], state="*")
async def send_welcome(message: types.Message):
    selected_rates = redis_db.get_selected_rates()
    await message.answer(texts.automod_changing, reply_markup=kb.get_automod_kb(selected_rates))
    await State.choosing_automod.set()


@dp.callback_query_handler(state=State.choosing_automod)
async def send_series(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'menu':
        await callback.message.answer(texts.back_to_menu, reply_markup=ReplyKeyboardRemove())
        await state.reset_state(with_data=False)
        return

    tapped_num = int(callback.data)
    selected_numbers = redis_db.get_selected_rates()

    if tapped_num in selected_numbers:
        selected_numbers.remove(tapped_num)
    else:
        selected_numbers.append(tapped_num)

    try:
        await bot.edit_message_reply_markup(callback.message.chat.id,
                            callback.message.message_id,
                            reply_markup=kb.get_automod_kb(selected_numbers))
    except:
        print('Фейл во время попытки изменить клавиатуру с кодом')
    redis_db.set_selected_rates(selected_numbers)
    await bot.answer_callback_query(callback.id)
    

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


    if tapped == 'sent':

        # not found in redis
        if item_to_ans is None:
            try:
                await bot.edit_message_reply_markup(GROUP_ID, message_id, reply_markup=kb.error_kb)
            except Exception as e:
                print('Ошибка при изменении кнопки')
            await bot.answer_callback_query(callback.id, text='Ошибка при поиске отзыва')
            return
        

        if item_to_ans['account'] == 'OOO':
            auth = WB_TOKEN_OOO
        elif item_to_ans['account'] == 'IP':
            auth = WB_TOKEN_IP

        # already answered
        wb_feedback = wb_api.get_feedback_by_id(auth, item_to_ans['feedback_id'])
        if wb_feedback.json()['data']['answer'] is not None:
            try:
                await bot.edit_message_reply_markup(GROUP_ID, message_id, reply_markup=kb.done_by_hand)
            except Exception as e:
                print('уже отвечено')
            await bot.answer_callback_query(callback.id, text='уже отвечено')
            return
        

        wb_api.answer_feedback_mock(auth, item_to_ans['feedback_id'], callback.message.text)
        try:
            await bot.edit_message_reply_markup(GROUP_ID, message_id, reply_markup=kb.done_kb)
        except Exception as e:
            print('Ошибка при изменении кнопки')
    else:
        await bot.answer_callback_query(callback.id, text='Ошибка при поиске отзыва')


    if tapped == 'regenerate':
        print(item_to_ans)

    
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