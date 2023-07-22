from aiogram.dispatcher.filters.state import State, StatesGroup

class AddTasks(StatesGroup):
    task_title = State()
    priority = State()
    completed = State()
    check = State()