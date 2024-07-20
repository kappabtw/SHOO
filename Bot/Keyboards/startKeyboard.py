# -*- coding: windows-1251 -*-
from aiogram import types

catalog = types.InlineKeyboardButton(text = "Каталог", callback_data="catalog")
manager = types.InlineKeyboardButton(text = "Менеджер", callback_data="manager", url = "https://t.me/sinokda")
reviews = types.InlineKeyboardButton(text = "Отзывы", callback_data = "reviews")
info = types.InlineKeyboardButton(text = "Информация", callback_data="info")

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[catalog, info], [reviews, manager]])

