from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_select_sport = InlineKeyboardButton('Выбрать вид спорта', callback_data='select_sport')
inline_button_help = InlineKeyboardButton('Список доступных команд', callback_data='help')


inline_kb = InlineKeyboardMarkup()
inline_kb.add(inline_button_select_sport)
inline_kb.add(inline_button_help)
