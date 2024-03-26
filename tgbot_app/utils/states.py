from aiogram.fsm.state import StatesGroup, State


class GenerationState(StatesGroup):
    TEXT = State()
    IMAGE = State()
    FILE = State()
    IN_PROCESS = State()
