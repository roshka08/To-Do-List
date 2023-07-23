from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

uncompleted_button = InlineKeyboardButton(text="❌ Bajarilmadi", callback_data="completed")
completed_button = InlineKeyboardButton(text="✅ Bajarildi", callback_data="completed")

delete_button = InlineKeyboardButton(text="🗑 O'chirish", callback_data="delete")

task_buttons_for_true = InlineKeyboardMarkup(row_width=2)
task_buttons_for_true.add(uncompleted_button, delete_button)

task_buttons_for_false = InlineKeyboardMarkup(row_width=2)
task_buttons_for_false.add(completed_button, delete_button)

yes_or_no = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text='✅ Ha', callback_data="yes")],
    [InlineKeyboardButton(text="❌ Yo'q", callback_data="no")]
])