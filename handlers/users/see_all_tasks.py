from loader import db, dp
from aiogram import types
from keyboards.inline.main import task_buttons_for_false, task_buttons_for_true,  yes_or_no
from keyboards.default.main import main_page_buttons
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="📜 Vazifalarni Ko'rish", state="*")
async def see_all_tasks(message: types.Message, state: FSMContext):
    tasks = await db.select_all_tasks(from_who=message.from_user.first_name)

    if len(tasks) >= 1:
        for task in tasks:
            task_id = task.get('id')
            task_completed = task.get('completed')
            await state.update_data(data={"task_completed": task_completed})
            await state.update_data(data={"task_id": task_id})
            
            if task.get('completed') == True:
                await message.answer(f"Vazifani Nomi: {task.get('task_title')}\nVazifani Zarurligi: {task.get('priority')}\nTugalganligi: ✅ Ha\n\nSana: {task.get('time')}", reply_markup=task_buttons_for_true)
            else:
                await message.answer(f"Vazifani Nomi: {task.get('task_title')}\nVazifani Zarurligi: {task.get('priority')}\nTugalganligi: ❌ Yo'q\n\nSana: {task.get('time')}", reply_markup=task_buttons_for_false)
    else:
        await message.answer("Sizda Vazifa Yo'q!", reply_markup=main_page_buttons)

@dp.callback_query_handler(text="completed")
async def complete_task(call: types.CallbackQuery, state: FSMContext):
    task = await state.get_data()
    task_completed = task.get('task_completed')
    task_id = task.get('task_id')
    if task_completed == True:
        await call.message.delete()
        await db.update_task_complete(task_completed=False, id=task_id)
        await call.message.answer('Vazifa O\'zgartilindi!', reply_markup=main_page_buttons)
    else:
        await call.message.delete()
        await db.update_task_complete(task_completed=True, id=task_id)
        await call.message.answer('Vazifa O\'zgartilindi!', reply_markup=main_page_buttons)

@dp.callback_query_handler(text="delete")
async def delete_task(call: types.CallbackQuery):
    await call.message.edit_text("O'chirib Tashlamoqchimisiz?", reply_markup=yes_or_no)

@dp.callback_query_handler(text='yes')
async def really_delete_task(call: types.CallbackQuery, state: FSMContext):
    task = await state.get_data()
    task_id = task.get('task_id')
    await call.message.delete()
    await db.delete_task(task_id=task_id)
    await call.message.answer("Sizning Vazifangiz O'chirildi!!!", reply_markup=main_page_buttons)

@dp.callback_query_handler(text='no')
async def dont_delete_task(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Sizning Vazifangiz O'chirilmadi!")