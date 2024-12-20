from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    username = State()
    phone = State()
    trauma = State()


class TrainingState(StatesGroup):
    result = State()
    confirm = State()
