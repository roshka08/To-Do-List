from loader import db, dp
from aiogram import types
from states.add_tasks import AddTasks
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from keyboards.default.main import add_task, yes_or_no, main_page_buttons
from datetime import date

@dp.message_handler(text="🆕 Vazifa Qo'shish")
async def add_new_task(message: types.Message, state: FSMContext):
    await message.answer('Vazifani Nomini Kiriting: ', reply_markup=ReplyKeyboardRemove())
    await AddTasks.next()

@dp.message_handler(state=AddTasks.task_title)
async def get_task_title(message: types.Message, state: FSMContext):
    await state.update_data(data={'task_title': message.text})
    await message.answer('Vazifani Zarurligini Tanlang: ', reply_markup=add_task)
    await AddTasks.next()

@dp.message_handler(state=AddTasks.priority)
async def get_task_priority(message: types.Message, state: FSMContext):
    if message.text == "🟥 Hard":
        await state.update_data(data={'task_priority': '🟥 Hard'})
    elif message.text == "🟨 Middle":
        await state.update_data(data={'task_priority': '🟨 Middle'})
    else:
        await state.update_data(data={'task_priority': '🟩 Low'})
    await message.answer('Vazifa Tugalanganmi?', reply_markup=yes_or_no)
    await AddTasks.next()

@dp.message_handler(state=AddTasks.completed)
async def get_task_completed(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_title = data['task_title']
    task_priority = data['task_priority']
    if message.text == "❌ Yo'q":
        task_completed = False
    else:
        task_completed = True
    await state.update_data(data={'task_completed': task_completed})
    await message.answer(f"Vazifani Nomi: {task_title}\nVazifani Zarurligi: {task_priority}\nVazifani Tugalganligi: {message.text}\n\n{'*' * 30}\n\nSiz Hohlagan Vazifami?", reply_markup=yes_or_no)
    await AddTasks.next()

@dp.message_handler(state=AddTasks.check)   
async def get_task_check(message: types.Message, state: FSMContext):
    if message.text == '✅ Ha':
        await message.answer("Sizning Vazifangiz Qo'shildi!", reply_markup=main_page_buttons)
        data = await state.get_data()
        task_title = data['task_title']
        task_priority = data['task_priority']
        task_completed = data['task_completed']
        await db.add_task(task_title=task_title, priority=task_priority, completed=task_completed, time=str(date.today()))
        await state.finish()
    else:
        await message.answer("Siz Vazifangizni Rad Qildingiz!", reply_markup=main_page_buttons)
        await state.finish()
        