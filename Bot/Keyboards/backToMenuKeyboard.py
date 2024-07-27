# -*- coding: windows-1251 -*-
from aiogram import types
from Bot import data

back_to_menu = types.InlineKeyboardButton(text = data.Message['back']['menu'], callback_data = data.Callback['menu'])

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[back_to_menu]])

