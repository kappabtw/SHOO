# -*- coding: windows-1251 -*-
from aiogram import types

catalog = types.InlineKeyboardButton(text = "�������", callback_data="catalog")
manager = types.InlineKeyboardButton(text = "��������", callback_data="manager", url = "https://t.me/sinokda")
reviews = types.InlineKeyboardButton(text = "������", callback_data = "reviews")
info = types.InlineKeyboardButton(text = "����������", callback_data="info")

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[catalog, info], [reviews, manager]])

