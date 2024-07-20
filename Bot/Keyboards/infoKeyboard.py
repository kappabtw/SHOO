# -*- coding: windows-1251 -*-
from aiogram import types


back_from_info = types.InlineKeyboardButton(text = "Назад в меню", callback_data="back_from_info")

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[back_from_info]])

