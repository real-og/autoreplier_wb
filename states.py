from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    changing_instructions = State()
    choosing_automod = State()