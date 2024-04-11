from aiogram.fsm.state import State, StatesGroup


class GenerationState(StatesGroup):
    TEXT = State()
    IMAGE = State()
    FILE = State()
    IN_PROCESS = State()
