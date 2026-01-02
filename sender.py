import asyncio
from aiogram import Bot
from config import BOT_TOKEN, GROUP_ID
import keyboards as kb


bot = Bot(BOT_TOKEN, parse_mode='HTML')


async def async_send_message(text, keyboard=None):
    try:
        mes = await bot.send_message(GROUP_ID, text, reply_markup=keyboard)
        print(mes)
        s = await bot.get_session()
        await s.close()
        return mes.message_id
    except Exception as e:
        print(e)



def send_text_message(text, keyboard=None):
    message_id = asyncio.run(async_send_message(text, keyboard))
    return message_id