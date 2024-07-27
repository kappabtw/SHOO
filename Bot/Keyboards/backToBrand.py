# -*- coding: windows-1251 -*-
from aiogram import types
from Bot import data

back_to_brand = types.InlineKeyboardButton(text = data.Message['back']['catalog'], callback_data=data.Callback['catalog'])

back_to_brand_sales = types.InlineKeyboardButton(text = data.Message['back']['brand']['sales'], callback_data=data.Callback['sales'])

back_to_brand_new = types.InlineKeyboardButton(text = data.Message['back']['brand']['new'], callback_data=data.Callback['new_items'])


