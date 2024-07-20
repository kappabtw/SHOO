# -*- coding: windows-1251 -*-
from aiogram import types


back_to_menu = types.InlineKeyboardButton(text = "Назад в меню", callback_data="back_to_menu")

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[back_to_menu]])

