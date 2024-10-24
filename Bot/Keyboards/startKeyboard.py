# -*- coding: windows-1251 -*-
from aiogram import types
from Bot import data

catalog_callback_data:str = "catalog"
manager_callback_data:str = "manager"
reviews_callback_data:str = "reviews"
info_callback_data:str = "info"

manager_url = data.manager_url
channel = data.review_channel



catalog = types.InlineKeyboardButton(text = data.Message['catalog'], callback_data=data.Callback['catalog'])
manager = types.InlineKeyboardButton(text = data.Message['manager'], callback_data=data.Callback['manager'], url = manager_url)
reviews = types.InlineKeyboardButton(text = data.Message['reviews'], callback_data = data.Callback['reviews'], url = channel)
info = types.InlineKeyboardButton(text = data.Message['info'], callback_data=data.Callback['info'])

keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[catalog, info], [reviews, manager]])

