from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_do_task = KeyboardButton(text="🆕 Vazifa Qo'shish")
see_all_tasks = KeyboardButton(text="📜 Vazifalarni Qo'rish")
back_button = KeyboardButton(text="⬅️ Orqaga")
back_main_button = KeyboardButton(text="🏠 Bosh Menyu")

main_page_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
main_page_buttons.add(add_do_task, see_all_tasks)


add_task = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🟥 Hard")],
    [KeyboardButton(text="🟨 Middle")],
    [KeyboardButton(text="🟩 Low")],
], resize_keyboard=True)

yes_or_no = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='✅ Ha')],
    [KeyboardButton(text="❌ Yo'q")]
], resize_keyboard=True)